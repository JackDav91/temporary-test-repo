from pathlib import Path
import re

# Gengrail patch v3: restore preferred Home presentation, fix viewport fill,
# loosen discovery economics without weakening the core business Profit Engine,
# and make Daily Discovery queries specific enough to form defensible peer groups.

# 1) Grail Hub discovery economics + targeted lanes.
p=Path('grail-hub.js')
s=p.read_text()
if 'GENGRAIL GRAIL HUB v1.6' not in s:
    raise SystemExit('Safety stop: expected Grail Hub v1.6')

old="""const DISCOVERY_CONFIG=Object.freeze({
  version:1,
  refreshHours:24,
  lanes:['Pokemon TCG Charizard','Pokemon TCG Pikachu','Pokemon TCG Umbreon','Pokemon TCG Lugia','Pokemon TCG Eevee','Pokemon TCG PSA']
});"""
new="""const DISCOVERY_CONFIG=Object.freeze({
  version:2,
  refreshHours:24,
  // Discovery works best when each lane creates a genuine peer-priced set rather than a broad character soup.
  lanes:['Pokemon Charizard 4/102','Pokemon Pikachu 58/102','Pokemon Blastoise 2/102','Pokemon Venusaur 15/102','Pokemon Lugia 9/111','Pokemon Umbreon 13/75'],
  floorRoi:10,
  preferredRoi:20,
  floorMargin:10
});"""
if old not in s:
    raise SystemExit('Discovery config anchor not found')
s=s.replace(old,new,1)

old="minRoi:num(g.minimumROI),minProfit:1,url:String(r.item.itemWebUrl||'')"
new="minRoi:DISCOVERY_CONFIG.floorRoi,minProfit:1,url:String(r.item.itemWebUrl||'')"
if old not in s:
    raise SystemExit('Discovery economics minRoi anchor not found')
s=s.replace(old,new,1)

old="""e.qualityPass=conditionKnown&&e.profit>0&&e.roi>=num(g.minimumROI)&&e.margin>=num(g.minimumNetMargin)&&confidence>=num(g.minimumConfidence);
    e.liquidityPass=e.landed<=num(g.availableGrailPlanLiquidity);
    e.safe=e.qualityPass&&e.liquidityPass;"""
new="""e.discoveryPass=conditionKnown&&e.profit>0&&e.roi>=DISCOVERY_CONFIG.floorRoi&&e.margin>=DISCOVERY_CONFIG.floorMargin&&confidence>=num(g.minimumConfidence);
    e.preferredPass=e.discoveryPass&&e.roi>=DISCOVERY_CONFIG.preferredRoi;
    // Grail Plan may use viable 10%+ candidates, but ranking explicitly favours 20%+ opportunities.
    e.qualityPass=e.discoveryPass;
    e.liquidityPass=e.landed<=num(g.availableGrailPlanLiquidity);
    e.safe=e.qualityPass&&e.liquidityPass;
    if(e.preferredPass)e.rankScore=Math.min(100,(e.rankScore||0)+8);"""
if old not in s:
    raise SystemExit('Discovery quality gate anchor not found')
s=s.replace(old,new,1)

# Preserve all genuinely positive ranked rows for review; guardrails decide whether they enter Grail Plan.
old="const ranked=rankListings(all,g),rows=ranked.filter(x=>x.profit>0&&x.roi>0&&x.margin>0),plan=buildBasket(rows,g),now=Date.now(),sheet="
new="const ranked=rankListings(all,g),rows=ranked.filter(x=>x.profit>0&&x.roi>0&&x.margin>0),plan=buildBasket(rows,g),now=Date.now(),sheet="
if old not in s:
    raise SystemExit('Daily Sheet positive-economics anchor not found')

# 2) Restore Home Compact v1 styling, then fix viewport fill without redesigning it.
p=Path('home-compact.css')
s=p.read_text()
if 'GENGRAIL HOME COMPACT v2' not in s:
    raise SystemExit('Safety stop: expected Home Compact v2')
s=s.replace('GENGRAIL HOME COMPACT v2 — responsive full-height command centre','GENGRAIL HOME COMPACT v1.1 — restored command centre with viewport fill',1)
s=s.replace("  height:calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 10px);\n  min-height:0;\n  overflow:hidden;","  min-height:calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 10px);\n  height:auto;\n  overflow:visible;",1)
s=s.replace('  height:100% !important;\n  padding:10px 30px 10px 9px !important;','  height:auto !important;\n  padding:8px 30px 8px 9px !important;',1)
# Remove the later forced tall-phone min-heights that changed the preferred UI proportions.
s=re.sub(r'\n/\* Tall-phone tile height correction v2\.1 \*/.*?\n\}\n@media \(max-width:520px\) and \(min-height:900px\)\{.*?\n\}\n?','\n',s,flags=re.S)
# Use the available vertical space naturally while keeping the original tile appearance.
marker="""
/* Viewport-fill correction: preserve v1 card proportions; distribute spare height instead of redesigning tiles. */
@media (max-width:520px) and (min-height:821px){
  body.home-page .home-screen{min-height:calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 160px) !important}
  body.home-page .home-menu{align-content:stretch !important}
  body.home-page .home-menu button{min-height:96px !important}
}
@media (max-width:520px) and (min-height:900px){
  body.home-page .home-menu button{min-height:104px !important}
}
"""
if 'Viewport-fill correction' not in s:
    s += marker
p.write_text(s)

# 3) Cache bust the touched assets.
p=Path('index.html')
s=p.read_text()
for asset in ('grail-hub.js','home-compact.css'):
    pattern=r'('+re.escape(asset)+r')(?:\?v=[^"\']+)?'
    s,n=re.subn(pattern,lambda m:m.group(1)+'?v=23.1.0',s)
    if n<1:
        raise SystemExit(f'Cache reference not found for {asset}')
p.write_text(s)

p=Path('sw.js')
s=p.read_text()
s,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v23.1.0-discovery-home';",s,count=1)
if n!=1:
    raise SystemExit('Service worker cache anchor not found')
p.write_text(s)

# Safety gates: do not touch recognition, eBay integration, stock, sales, finance or raw/graded contracts.
checks={
    'grail-hub.js':['floorRoi:10','preferredRoi:20','floorMargin:10','e.discoveryPass','e.preferredPass','function buildDailySheet','function scanStream'],
    'home-compact.css':['GENGRAIL HOME COMPACT v1.1','Viewport-fill correction','height:auto !important'],
    'index.html':['recognise-card','graded-integration.js','gengrail-ebay.js','grail-hub.js?v=23.1.0','home-compact.css?v=23.1.0'],
    'sw.js':['gengrail-log-v23.1.0-discovery-home']
}
for file,needles in checks.items():
    text=Path(file).read_text()
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'Safety stop: {needle!r} missing from {file}')
