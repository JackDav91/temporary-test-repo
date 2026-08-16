from pathlib import Path

p=Path('grail-hub.js')
s=p.read_text()
if 'GENGRAIL GRAIL HUB v1.4' not in s:
    raise SystemExit('Safety stop: expected Grail Hub v1.4 source')

old="""function rawCondition(title,itemCondition=''){
  const t=clean(`${title} ${itemCondition}`);
  if(/\\b(damaged|damage|dmg|creased|crease|water damage|torn)\\b/.test(t))return 'DMG';
  if(/\\b(heavily played|heavy play|hp condition|hp played)\\b/.test(t)||/\\(hp\\)/.test(t))return 'HP';
  if(/\\b(moderately played|moderate play|mp condition)\\b/.test(t)||/\\(mp\\)/.test(t))return 'MP';
  if(/\\b(lightly played|light play|lp condition)\\b/.test(t)||/\\(lp\\)/.test(t))return 'LP';
  if(/\\b(near mint|nm condition|mint condition|pack fresh)\\b/.test(t)||/\\(nm\\)/.test(t))return 'NM';
  return 'UNKNOWN';
}"""
new="""function rawCondition(title,itemCondition=''){
  const t=clean(`${title} ${itemCondition}`);
  if(/\\b(damaged|damage|dmg|creased|crease|water damage|torn)\\b/.test(t))return 'DMG';
  if(/\\b(heavily played|heavy play|hp condition|hp played|hp)\\b/.test(t))return 'HP';
  if(/\\b(moderately played|moderate play|mp condition|mp)\\b/.test(t))return 'MP';
  if(/\\b(lightly played|light play|lp condition|lp)\\b/.test(t))return 'LP';
  if(/\\b(near mint|nm condition|mint condition|pack fresh|nm)\\b/.test(t))return 'NM';
  return 'UNKNOWN';
}"""
if old not in s: raise SystemExit('rawCondition anchor not found')
s=s.replace(old,new,1)

old="""    e.qualityPass=e.profit>0&&e.roi>=num(g.minimumROI)&&e.margin>=num(g.minimumNetMargin)&&confidence>=num(g.minimumConfidence);"""
new="""    const conditionKnown=e.type!=='RAW'||e.condition!=='UNKNOWN';
    e.qualityPass=conditionKnown&&e.profit>0&&e.roi>=num(g.minimumROI)&&e.margin>=num(g.minimumNetMargin)&&confidence>=num(g.minimumConfidence);"""
if old not in s: raise SystemExit('qualityPass anchor not found')
s=s.replace(old,new,1)

s=s.replace('GENGRAIL GRAIL HUB v1.4 — Opportunity Stream v1.1 accuracy hardening','GENGRAIL GRAIL HUB v1.5 — Opportunity Stream v1.2 condition gate',1)
p.write_text(s)
