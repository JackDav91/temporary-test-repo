from pathlib import Path
import re

# Gengrail v5: invalidate stale Daily Sheets, defensively strip accessory rows
# after ranking as a second safety barrier, and finish Home viewport fill.

p=Path('grail-hub.js')
s=p.read_text()
if 'GENGRAIL GRAIL HUB v1.6' not in s:
    raise SystemExit('Safety stop: expected Grail Hub v1.6')

# Bump discovery config/version so old local snapshots cannot survive parser changes.
s=s.replace('version:2,','version:3,',1)
old="function loadDailySheet(){try{return JSON.parse(localStorage.getItem(DAILY_SHEET_KEY)||'null')}catch{return null}}"
new="function loadDailySheet(){try{const sheet=JSON.parse(localStorage.getItem(DAILY_SHEET_KEY)||'null');if(!sheet)return null;if(Number(sheet.configVersion)!==Number(DISCOVERY_CONFIG.version)){localStorage.removeItem(DAILY_SHEET_KEY);return null}return sheet}catch{try{localStorage.removeItem(DAILY_SHEET_KEY)}catch{}return null}}"
if old not in s: raise SystemExit('loadDailySheet anchor missing')
s=s.replace(old,new,1)

# A second, title-level safety barrier means accessories cannot appear even if parsing logic regresses.
anchor="function rankListings(items,g){"
if anchor not in s: raise SystemExit('rankListings anchor missing')
insert="""function accessoryTitleReject(title){const t=clean(title);return /\\b(keychain|key chain|keyring|key ring|novelty|extended artwork|extended art|magnetic case|case|display|frame|holder|stand|card not included|no card included|without card|replica|reproduction|proxy|custom)\\b/.test(t)}\n"""
s=s.replace(anchor,insert+anchor,1)
old="return [...uniq.values()].sort((a,b)=>Number(b.safe)-Number(a.safe)||b.rankScore-a.rankScore||b.profit-a.profit);"
new="return [...uniq.values()].filter(x=>!accessoryTitleReject(x.title)).sort((a,b)=>Number(b.safe)-Number(a.safe)||b.rankScore-a.rankScore||b.profit-a.profit);"
if old not in s: raise SystemExit('rank return anchor missing')
s=s.replace(old,new,1)

# Also sanitize persisted rows on save/build.
old="const ranked=rankListings(all,g),rows=ranked.filter(x=>x.profit>0&&x.roi>0&&x.margin>0),plan=buildBasket(rows,g),now=Date.now(),sheet="
new="const ranked=rankListings(all,g),rows=ranked.filter(x=>!accessoryTitleReject(x.title)&&x.profit>0&&x.roi>0&&x.margin>0),plan=buildBasket(rows,g),now=Date.now(),sheet="
if old not in s: raise SystemExit('daily rows anchor missing')
s=s.replace(old,new,1)
p.write_text(s)

# Home: stretch the composition itself, not just tile minimum heights.
p=Path('home-compact.css')
s=p.read_text()
if 'Viewport-fill correction v1.2' not in s: raise SystemExit('Home viewport v1.2 anchor missing')
marker="""
/* Final viewport fill v1.3: keep the restored visual design but move the ticker toward the browser chrome. */
@media (max-width:520px) and (min-height:821px){
  body.home-page{min-height:100dvh !important}
  body.home-page .app{height:calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 4px) !important;min-height:0 !important;display:flex !important;flex-direction:column !important}
  body.home-page .home-screen{display:flex !important;flex-direction:column !important;flex:1 1 auto !important}
  body.home-page .home-menu{flex:1 1 auto !important;grid-template-rows:repeat(3,1fr) !important}
  body.home-page .home-menu button{height:100% !important;min-height:112px !important}
  body.home-page .gengrail-performance-ticker{margin-top:6px !important;margin-bottom:0 !important}
}
@media (max-width:520px) and (min-height:900px){
  body.home-page .home-menu button{min-height:122px !important}
}
"""
if 'Final viewport fill v1.3' not in s: s += marker
p.write_text(s)

# Cache bust.
p=Path('index.html'); s=p.read_text()
for asset in ('grail-hub.js','home-compact.css'):
    pat=r'('+re.escape(asset)+r')(?:\?v=[^"\']+)?'
    s,n=re.subn(pat,lambda m:m.group(1)+'?v=23.3.0',s)
    if n<1: raise SystemExit('cache ref missing '+asset)
p.write_text(s)

p=Path('sw.js'); s=p.read_text(); s,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v23.3.0-snapshot-home';",s,count=1)
if n!=1: raise SystemExit('sw cache anchor missing')
p.write_text(s)

checks={
 'grail-hub.js':['version:3','accessoryTitleReject','localStorage.removeItem(DAILY_SHEET_KEY)','filter(x=>!accessoryTitleReject(x.title)'],
 'home-compact.css':['Final viewport fill v1.3','height:calc(100dvh','min-height:122px'],
 'index.html':['grail-hub.js?v=23.3.0','home-compact.css?v=23.3.0'],
 'sw.js':['gengrail-log-v23.3.0-snapshot-home']
}
for f,needles in checks.items():
    text=Path(f).read_text()
    for needle in needles:
        if needle not in text: raise SystemExit(f'Safety stop: {needle} missing from {f}')
