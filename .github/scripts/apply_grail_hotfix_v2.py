from pathlib import Path
import re

# 1) Grail Hub JS: Daily Sheet should only retain candidates with positive economics.
p=Path('grail-hub.js')
s=p.read_text()
if 'GENGRAIL GRAIL HUB v1.6' not in s:
    raise SystemExit('Safety stop: expected Grail Hub v1.6')
old="const rows=rankListings(all,g),plan=buildBasket(rows,g),now=Date.now(),sheet="
new="const ranked=rankListings(all,g),rows=ranked.filter(x=>x.profit>0&&x.roi>0&&x.margin>0),plan=buildBasket(rows,g),now=Date.now(),sheet="
if old not in s:
    raise SystemExit('Daily Sheet ranking anchor not found')
s=s.replace(old,new,1)
p.write_text(s)

# 2) iOS Safari: prevent focus zoom/reflow on the live-search input.
p=Path('grail-hub.css')
s=p.read_text()
if 'GENGRAIL GRAIL HUB v1.4' not in s:
    raise SystemExit('Safety stop: expected Grail Hub CSS v1.4')
old=".grail-stream-search input{min-width:0;background:#070707!important;border:1px solid #3b3320!important;color:#fff!important;border-radius:9px!important;padding:11px!important;font-size:15px!important}"
new=".grail-stream-search input{width:100%!important;max-width:100%!important;min-width:0;background:#070707!important;border:1px solid #3b3320!important;color:#fff!important;border-radius:9px!important;padding:11px!important;font-size:16px!important}"
if old not in s:
    raise SystemExit('Search input CSS anchor not found')
s=s.replace(old,new,1)
p.write_text(s)

# 3) Home: visibly use more vertical space on modern/tall iPhones without allowing scroll.
p=Path('home-compact.css')
s=p.read_text()
if 'GENGRAIL HOME COMPACT v2' not in s:
    raise SystemExit('Safety stop: expected Home Compact v2')
marker='''\n/* Tall-phone tile height correction v2.1 */\n@media (max-width:520px) and (min-height:850px){\n  body.home-page .brand img{height:136px !important;max-height:136px !important}\n  body.home-page .home-menu button{min-height:100px !important}\n}\n@media (max-width:520px) and (min-height:900px){\n  body.home-page .brand img{height:142px !important;max-height:142px !important}\n  body.home-page .home-menu button{min-height:106px !important}\n}\n'''
if 'Tall-phone tile height correction v2.1' not in s:
    s += marker
p.write_text(s)

# 4) Cache-bust only the additive Hub/Home assets.
p=Path('index.html')
s=p.read_text()
for asset in ('grail-hub.css','grail-hub.js','home-compact.css'):
    pattern=r'('+re.escape(asset)+r')(?:\?v=[^"\']+)?'
    s,n=re.subn(pattern,lambda m:m.group(1)+'?v=23.0.1',s)
    if n<1:
        raise SystemExit(f'Cache reference not found for {asset}')
p.write_text(s)

# 5) Service worker cache bump.
p=Path('sw.js')
s=p.read_text()
old="const C='gengrail-log-v23.0.1-grail-discovery-layout';"
new="const C='gengrail-log-v23.0.2-grail-hotfix';"
if old not in s:
    raise SystemExit('Service worker cache anchor not found')
s=s.replace(old,new,1)
p.write_text(s)

# Safety gates. Keep raw/graded recognition and existing eBay integration present.
checks={
    'grail-hub.js':['ranked.filter(x=>x.profit>0&&x.roi>0&&x.margin>0)','function buildDailySheet','function scanStream'],
    'grail-hub.css':['font-size:16px!important','width:100%!important','overflow-x:hidden'],
    'home-compact.css':['Tall-phone tile height correction v2.1','min-height:100px !important'],
    'index.html':['recognise-card','graded-integration.js','gengrail-ebay.js','grail-hub.js?v=23.0.1','grail-hub.css?v=23.0.1','home-compact.css?v=23.0.1'],
    'sw.js':['gengrail-log-v23.0.2-grail-hotfix']
}
for file,needles in checks.items():
    text=Path(file).read_text()
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'Safety stop: {needle!r} missing from {file}')
