from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()
if 'pricing-ui-review-v21' not in s or 'pricing-ai-tools' not in s:
    raise SystemExit('Safety stop: expected Pricing UI v2.1 baseline')

style=r'''
<style id="pricing-ui-review-v22">
/* PRICING UI REVIEW v2.2 — restore camera scan + final spacing cleanup. */
#pricing .pricing-ai-tools{display:grid!important;grid-template-columns:1fr 1fr!important;gap:8px!important}
#pricing .pricing-scan-card{grid-column:1/-1!important;min-height:70px!important;margin:0!important;border:1px solid #8a6818!important;border-radius:12px!important;background:linear-gradient(180deg,#17140d,#111)!important;color:#f4f1ea!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;padding:10px!important;font:inherit!important}
#pricing .pricing-scan-card .pricing-scan-icon{color:#f2c84b!important;font-size:22px!important;line-height:1!important;margin-bottom:3px!important}
#pricing .pricing-scan-card b{font-family:Impact,sans-serif!important;font-size:20px!important;letter-spacing:.035em!important}
#pricing .pricing-scan-card small{color:#999!important;font-size:9px!important;margin-top:3px!important}
#pricing .pricing-ai-tools>label.btn,#pricing .pricing-ai-tools>[data-graded-import="pricing"]{min-height:58px!important}
#pricing #pricingAiClear{grid-column:1/-1!important}
#pricing #pricePostageSummary{display:grid!important;gap:7px!important}
#pricing #pricePostageSummary>div{display:grid!important;grid-template-columns:minmax(110px,.8fr) minmax(0,1.5fr)!important;align-items:center!important;column-gap:10px!important}
#pricing #pricePostageSummary small,#pricing #pricePostageSummary .label{display:block!important;margin:0!important;line-height:1.15!important}
#pricing #pricePostageSummary b,#pricing #pricePostageSummary .value{display:block!important;margin:0!important;line-height:1.2!important;min-width:0!important;overflow-wrap:anywhere!important}
#pricing .pricing-profile-context{margin-top:7px!important;padding-top:7px!important;border-top:1px solid #4a3b18!important;color:#a99d82!important;font-size:9px!important;line-height:1.4!important}
@media(max-width:520px){#pricing #pricePostageSummary>div{grid-template-columns:105px minmax(0,1fr)!important}}
</style>
'''

script=r'''
<script id="pricing-scan-card-v22">
(()=>{
'use strict';
function installPricingScan(){
  const root=document.getElementById('pricing');if(!root)return;
  const tools=root.querySelector('.pricing-ai-tools');if(!tools)return;
  const photoLabel=[...tools.querySelectorAll('label')].find(el=>/CARD PHOTO/i.test(el.textContent||''));
  const photoInput=photoLabel?.querySelector('input[type="file"]');
  const graded=tools.querySelector('[data-graded-import="pricing"]');
  const photoText=photoLabel?.querySelector('b');if(photoText)photoText.textContent='CARD PHOTO';
  const gradedText=graded?.querySelector('b');if(gradedText)gradedText.textContent='GRADED SLAB';
  if(photoInput&&!tools.querySelector('.pricing-scan-card')){
    const scan=document.createElement('button');scan.type='button';scan.className='pricing-scan-card';
    scan.innerHTML='<span class="pricing-scan-icon">⌁</span><b>SCAN CARD</b><small>Use the iPhone camera</small>';
    scan.addEventListener('click',()=>{
      photoInput.setAttribute('capture','environment');
      window.addEventListener('focus',()=>setTimeout(()=>photoInput.removeAttribute('capture'),250),{once:true});
      photoInput.click();
    });
    tools.insertBefore(scan,photoLabel||tools.firstChild);
  }
  const profileLeaf=[...root.querySelectorAll('*')].find(el=>el.children.length===0&&/MICRO VALUE BUYING PROFILE/i.test(el.textContent||''));
  if(profileLeaf){
    profileLeaf.textContent=profileLeaf.textContent.replace(/MICRO VALUE BUYING PROFILE/i,'STRICT MICRO-VALUE BUYING PROFILE');
    const box=profileLeaf.closest('.note,.callout')||profileLeaf.parentElement;
    if(box&&!box.querySelector('.pricing-profile-context')){
      const d=document.createElement('div');d.className='pricing-profile-context';
      d.textContent='Calculator-specific buy thresholds. Opportunity Stream discovery uses a 10% ROI floor and 20% preferred ROI.';
      box.appendChild(d);
    }
  }
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',installPricingScan,{once:true});else installPricingScan();
})();
</script>
'''

if 'pricing-ui-review-v22' not in s:s=s.replace('</head>',style+'\n</head>',1)
if 'pricing-scan-card-v22' not in s:s=s.replace('</body>',script+'\n</body>',1)
p.write_text(s)

p=Path('sw.js')
s=p.read_text();s,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v24.2.0-pricing-scan';",s,count=1)
if n!=1: raise SystemExit('Safety stop: service worker cache anchor missing')
p.write_text(s)

for f,needles in {
 'index.html':['pricing-ui-review-v22','pricing-scan-card-v22','SCAN CARD','STRICT MICRO-VALUE BUYING PROFILE','Opportunity Stream discovery uses a 10% ROI floor'],
 'sw.js':['gengrail-log-v24.2.0-pricing-scan']
}.items():
    text=Path(f).read_text()
    for needle in needles:
        if needle not in text: raise SystemExit(f'Safety stop: {needle!r} missing from {f}')
