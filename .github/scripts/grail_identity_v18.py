from pathlib import Path
import re

p=Path('grail-hub.js')
s=p.read_text()

s=s.replace('GENGRAIL GRAIL HUB v1.7 — identity-hardened discovery','GENGRAIL GRAIL HUB v1.8 — language + era identity hardening')
s=s.replace('version:4,','version:5,',1)

replacement="""function languageFrom(t){
  if(/\b(japanese|japan|jp|jpn|giapponese)\b/.test(t))return 'JA';
  if(/\b(italian|italiano|italiana|italia)\b/.test(t))return 'IT';
  if(/\b(german|deutsch|deutsche|deutschland)\b/.test(t))return 'DE';
  if(/\b(french|francais|français|france)\b/.test(t))return 'FR';
  if(/\b(spanish|espanol|español|espana|españa)\b/.test(t))return 'ES';
  if(/\b(portuguese|portugues|português|portugal)\b/.test(t))return 'PT';
  if(/\b(korean|korea|kr)\b/.test(t))return 'KO';
  if(/\b(chinese|simplified chinese|traditional chinese|cn|zh)\b/.test(t))return 'ZH';
  if(/\b(english|eng|uk)\b/.test(t))return 'EN';
  return 'EN';
}
function eraStatus(t,cardNumber,family,language){
  if(family==='BASE_SET'&&/\b(2021|2020|2019|2018|2017|2016|celebrations|25th anniversary|classic collection)\b/.test(t))return 'CONFLICT';
  if(family==='CELEBRATIONS'&&/\b(1999|2000|wotc|wizards of the coast)\b/.test(t)&&!/\b(celebrations|25th anniversary|classic collection|2021)\b/.test(t))return 'CONFLICT';
  if(family==='EVOLUTIONS'&&/\b(1999|wotc|wizards of the coast)\b/.test(t)&&!/\b2016\b/.test(t))return 'CONFLICT';
  if(family==='BASE_SET'&&language==='EN'&&/\b1998\b/.test(t)&&!/\b1999\b/.test(t))return 'REVIEW';
  return 'OK';
}
function identityStatus(t,cardNumber,family,language){
  if(COLLISION_PRONE_NUMBERS.has(cardNumber)&&family==='UNKNOWN')return 'UNCERTAIN';
  const era=eraStatus(t,cardNumber,family,language);
  if(era==='CONFLICT')return 'CONFLICT';
  if(era==='REVIEW')return 'REVIEW';
  return 'CONFIRMED';
}
"""
start=s.find('function identityStatus(')
end=s.find('function rawCondition',start)
if start<0 or end<0: raise SystemExit(f'identity block anchors not found: {start=} {end=}')
s=s[:start]+replacement+s[end:]

parse_start=s.find("const type=grader?'GRADED':'RAW',family=printingFamily(t,cardNumber)")
if parse_start<0: raise SystemExit('parseListing type anchor not found')
parse_end=s.find("\n  return {item,title,t,cardNumber",parse_start)
if parse_end<0: raise SystemExit('parseListing return anchor not found')
new_line="const type=grader?'GRADED':'RAW',family=printingFamily(t,cardNumber),language=languageFrom(t),identity=identityStatus(t,cardNumber,family,language),condition=type==='RAW'?rawCondition(title,item?.condition||''):'GRADED';"
s=s[:parse_start]+new_line+s[parse_end:]
ret_start=s.find("return {item,title,t,cardNumber",parse_start)
ret_end=s.find(';',ret_start)+1
if ret_start<0 or ret_end<=0: raise SystemExit('parseListing return not found')
s=s[:ret_start]+"return {item,title,t,cardNumber,grader,grade,type,printingFamily:family,language,identityStatus:identity,condition,ask,inbound:shippingPrice(item),tokens:tokensFor(title)};"+s[ret_end:]

peer_start=s.find('if(x.printingFamily!==row.printingFamily')
if peer_start<0: raise SystemExit('peer language anchor not found')
peer_end=s.find(';',peer_start)+1
s=s[:peer_start]+"if(x.printingFamily!==row.printingFamily||x.language!==row.language)return false;"+s[peer_end:]

s=s.replace("${esc(r.type)} · ${esc(r.condition)} · ${esc(r.printingFamily.replaceAll('_',' '))}","${esc(r.type)} · ${esc(r.condition)} · ${esc(r.language)} · ${esc(r.printingFamily.replaceAll('_',' '))}")
p.write_text(s)

sw=Path('sw.js')
w=sw.read_text()
w,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v24.9.0-grail-identity-v18';",w,count=1)
if n!=1: raise SystemExit('service worker cache anchor not found')
sw.write_text(w)

out=p.read_text()
assert 'version:5' in out
assert 'function languageFrom' in out
assert 'function eraStatus' in out
assert 'x.language!==row.language' in out
assert "identityStatus!=='CONFIRMED'" in out
assert 'floorRoi:10' in out and 'preferredRoi:20' in out and 'floorMargin:10' in out
print('Grail Hub identity v1.8 validated')
