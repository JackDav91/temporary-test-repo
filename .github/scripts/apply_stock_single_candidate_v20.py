from pathlib import Path
import re

# Stock recognition follow-up: one active candidate at a time + simplified grader confirmation.
# Recognition algorithms, market calculations and stock persistence remain unchanged.

# 1) Main stock intake reset also clears any graded bridge so a new raw scan cannot stack below it.
p=Path('index.html')
s=p.read_text()
if 'function resetRecognitionForNewIntake(){' not in s or 'stock-ui-review-v19' not in s:
    raise SystemExit('Safety stop: expected Stock UI v1.9 baseline')
old="""function resetRecognitionForNewIntake(){
 recognitionSessionId++;
 recognitionBusy=false;
 currentRecognition=null;
 pendingRecognition=null;
 setAiRecognitionPanel('idle');"""
new="""function resetRecognitionForNewIntake(){
 recognitionSessionId++;
 recognitionBusy=false;
 currentRecognition=null;
 pendingRecognition=null;
 const gradedBridge=document.getElementById('gradedStockBridge');
 if(gradedBridge){gradedBridge.hidden=true;gradedBridge.innerHTML='';}
 setAiRecognitionPanel('idle');"""
if old in s:
    s=s.replace(old,new,1)
elif "const gradedBridge=document.getElementById('gradedStockBridge');" not in s:
    raise SystemExit('Safety stop: raw intake reset anchor missing')
pat=r'(graded-integration\.js)(?:\?v=[^"\']+)?'
s,n=re.subn(pat,lambda m:m.group(1)+'?v=24.0.0',s)
if n<1: raise SystemExit('Safety stop: graded integration asset reference missing')
p.write_text(s)

# 2) Graded bridge clears any active raw workspace before starting and simplifies provisional grader messaging.
p=Path('graded-integration.js')
s=p.read_text()
if 'function addGradedImport' not in s or 'STOCK RECOGNITION UI v1.9' not in s:
    raise SystemExit('Safety stop: expected graded Stock UI v1.9 baseline')

s=s.replace("${assumed?'ACE ASSUMED · CONFIRM':'VALIDATED EXACT SLAB'}","${assumed?'PROVISIONAL MARKET':'VALIDATED EXACT SLAB'}")
s=s.replace("${esc(assumed?'ACE · ASSUMED':r.grader)}","${esc(assumed?'ACE · CONFIRMATION REQUIRED':r.grader)}")
s=s.replace("${esc(assumed?'ACE · NEEDS CONFIRMATION':r.grader)}","${esc(assumed?'ACE · CONFIRMATION REQUIRED':r.grader)}")
s=s.replace("${assumed?'<div class=\"gsc-assumed\">Priced provisionally as ACE from exact ACE listings. Confirm the grader before saving.</div>':''}","${assumed?'':''}")
s=s.replace("btn.innerHTML='<span class=\"graded-intake-icon\">▣</span><b>IMPORT GRADED SLAB</b><small>Recognise PSA, BGS, ACE & more</small>'","btn.innerHTML='<span class=\"graded-intake-icon\">▣</span><b>GRADED SLAB</b><small>Recognise PSA, BGS, ACE & more</small>'")

old="btn.onclick=()=>input.click();input.onchange=async()=>{const file=input.files?.[0];if(!file)return;status.textContent='Reading slab label and card…';btn.disabled=true;"
new="btn.onclick=()=>{if(mode==='stock'){try{if(typeof window.resetRecognitionForNewIntake==='function')window.resetRecognitionForNewIntake();else document.querySelector('.stock-intake-reset')?.click()}catch{}const old=document.getElementById('gradedStockBridge');if(old){old.hidden=true;old.innerHTML=''}}input.click()};input.onchange=async()=>{const file=input.files?.[0];if(!file)return;status.textContent='Reading slab label and card…';btn.disabled=true;"
if old in s:
    s=s.replace(old,new,1)
elif "if(mode==='stock'){try{if(typeof window.resetRecognitionForNewIntake" not in s:
    raise SystemExit('Safety stop: graded import click anchor missing')

s=s.replace('Your selection is saved as a manual grader confirmation.','Confirming the grader will save your manual check with this card.')
p.write_text(s)

# 3) Cache version.
p=Path('sw.js')
s=p.read_text();s,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v24.0.0-stock-single-candidate';",s,count=1)
if n!=1: raise SystemExit('Safety stop: service worker cache anchor missing')
p.write_text(s)

checks={
 'index.html':["const gradedBridge=document.getElementById('gradedStockBridge');",'graded-integration.js?v=24.0.0'],
 'graded-integration.js':['GRADED SLAB','ACE · CONFIRMATION REQUIRED','PROVISIONAL MARKET','Confirming the grader will save your manual check',"mode==='stock'"],
 'sw.js':['gengrail-log-v24.0.0-stock-single-candidate']
}
for f,needles in checks.items():
    text=Path(f).read_text()
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'Safety stop: {needle!r} missing from {f}')
