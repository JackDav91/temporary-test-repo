from pathlib import Path
import re

# Gengrail v4: harden actual-card identity, keep unknown raw condition review-only,
# and use the remaining iPhone viewport without redesigning the restored Home UI.

p=Path('grail-hub.js')
s=p.read_text()
if 'GENGRAIL GRAIL HUB v1.6' not in s:
    raise SystemExit('Safety stop: expected Grail Hub v1.6')

old="function obviousReject(t){return /\\b(proxy|custom|fan art|digital|code card|empty slab|slab only|case only|repack|mystery|orica|lot|bundle|collection|job lot|break|metal card|gold card)\\b/.test(t)}"
new="function obviousReject(t){return /\\b(proxy|replica|reproduction|custom|fan art|fanart|digital|code card|empty slab|slab only|case only|repack|mystery|orica|lot|bundle|collection|job lot|break|metal card|gold card|keychain|key chain|keyring|key ring|novelty|magnetic case|extended artwork|display case|display frame|card holder|card stand|protective case|acrylic case|card not included|card is not included|no card included|without card|empty case|case for|frame for|holder for)\\b/.test(t)}"
if old not in s:
    raise SystemExit('obviousReject anchor not found')
s=s.replace(old,new,1)

old="""  const cardNumber=`${Number(n[1])}/${Number(n[2])}`;
  const grader=graderFrom(t),grade=gradeFrom(t,grader);"""
new="""  const cardNumber=`${Number(n[1])}/${Number(n[2])}`;
  // Collector number is necessary but not sufficient: require positive evidence that the listing is the card itself.
  const actualCardSignal=/\\b(card|tcg|holo|holofoil|rare|unlimited|1st edition|first edition|shadowless|wotc|pokemon)\\b/.test(t);
  const accessoryNoun=/\\b(case|keychain|key ring|keyring|frame|holder|stand|display|novelty|magnet|magnetic|acrylic|artwork)\\b/.test(t);
  if(!actualCardSignal||accessoryNoun)return null;
  const grader=graderFrom(t),grade=gradeFrom(t,grader);"""
if old not in s:
    raise SystemExit('parseListing identity anchor not found')
s=s.replace(old,new,1)

old="const conditionKnown=e.type!=='RAW'||e.condition!=='UNKNOWN';"
new="const conditionKnown=e.type!=='RAW'||e.condition!=='UNKNOWN'; // UNKNOWN raw condition remains REVIEW-only and cannot enter Grail Plan."
if old not in s:
    raise SystemExit('condition gate anchor not found')
s=s.replace(old,new,1)
p.write_text(s)

p=Path('home-compact.css')
s=p.read_text()
if 'GENGRAIL HOME COMPACT v1.1' not in s:
    raise SystemExit('Safety stop: expected restored Home Compact v1.1')
pattern=r'/\* Viewport-fill correction: preserve v1 card proportions; distribute spare height instead of redesigning tiles\. \*/.*?@media \(max-width:520px\) and \(min-height:900px\)\{.*?\n\}'
replacement="""/* Viewport-fill correction v1.2: preserve the restored design and consume spare phone height. */
@media (max-width:520px) and (min-height:821px){
  body.home-page .app{min-height:calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 10px) !important}
  body.home-page .home-screen{flex:1 1 auto !important;min-height:0 !important}
  body.home-page .home-menu{flex:1 1 auto !important;grid-template-rows:repeat(3,minmax(108px,1fr)) !important;align-content:stretch !important}
  body.home-page .home-menu button{min-height:108px !important}
  body.home-page .gengrail-performance-ticker{margin-top:8px !important}
}
@media (max-width:520px) and (min-height:900px){
  body.home-page .home-menu{grid-template-rows:repeat(3,minmax(118px,1fr)) !important}
  body.home-page .home-menu button{min-height:118px !important}
}"""
s,n=re.subn(pattern,replacement,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('Viewport correction anchor not found')
p.write_text(s)

p=Path('index.html')
s=p.read_text()
for asset,ver in (('grail-hub.js','23.2.0'),('home-compact.css','23.2.0')):
    pattern="("+re.escape(asset)+r")(?:\?v=[^\"']+)?"
    s,n=re.subn(pattern,lambda m:m.group(1)+'?v='+ver,s)
    if n<1:
        raise SystemExit(f'Cache reference not found for {asset}')
p.write_text(s)

p=Path('sw.js')
s=p.read_text()
s,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v23.2.0-identity-home';",s,count=1)
if n!=1:
    raise SystemExit('Service worker cache anchor not found')
p.write_text(s)

checks={
  'grail-hub.js':['keychain','card not included','actualCardSignal','accessoryNoun','UNKNOWN raw condition remains REVIEW-only','floorRoi:10','preferredRoi:20'],
  'home-compact.css':['Viewport-fill correction v1.2','minmax(108px,1fr)','minmax(118px,1fr)'],
  'index.html':['grail-hub.js?v=23.2.0','home-compact.css?v=23.2.0','graded-integration.js','gengrail-ebay.js'],
  'sw.js':['gengrail-log-v23.2.0-identity-home']
}
for file,needles in checks.items():
    text=Path(file).read_text()
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'Safety stop: {needle!r} missing from {file}')
