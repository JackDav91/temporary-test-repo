/* GENGRAIL TEST — LISTING POLICY v1.1
   Isolated catalogue/listing pricing experiment for temporary-test-repo only.
   SEED: velocity first, protect 10% projected net margin.
   BUILD: protect 15%, prefer 20%, still price competitively.
   SCALE: protect 15%, prefer 20%, tighter market undercut.
   Current eBay context: UK private seller, £0 seller transaction fee; buyer postage treated as pass-through.
*/
(function(){
'use strict';
if(window.__gengrailSeedListingPolicyV11)return;
window.__gengrailSeedListingPolicyV11=true;

const STAGES={
 SEED:{minMargin:.10,preferred:.15,undercut:.03,label:'SEED · VELOCITY FIRST'},
 BUILD:{minMargin:.15,preferred:.20,undercut:.02,label:'BUILD · VELOCITY + MARGIN'},
 SCALE:{minMargin:.15,preferred:.20,undercut:.01,label:'SCALE · CAPITAL EFFICIENCY'}
};
const $=id=>document.getElementById(id);
const num=v=>Number.isFinite(Number(v))?Number(v):0;
const gbp=v=>new Intl.NumberFormat('en-GB',{style:'currency',currency:'GBP'}).format(num(v));
const r2=v=>Math.round((num(v)+Number.EPSILON)*100)/100;
function price99(v){const n=num(v);if(!(n>0))return 0;const whole=Math.floor(n),p=whole+.99;return Number((p+1e-9>=n?p:whole+1.99).toFixed(2))}
function stageKey(){
 try{const g=typeof getGrailPlanState==='function'?getGrailPlanState():null;const k=String(g?.mode||'').toUpperCase();if(STAGES[k])return k}catch{}
 return 'SEED';
}
function recognition(){try{return typeof currentRecognition!=='undefined'?currentRecognition:null}catch{return null}}
function validatedMarket(r){
 const mp=r?.marketPricing;if(!mp)return 0;
 // Prefer the visible validated recent-market cluster over any upstream pre-baked suggestion.
 const vals=[mp?.gbp?.trend,mp?.gbp?.avg7,mp?.gbp?.avg30].map(num).filter(v=>v>0).sort((a,b)=>a-b);
 if(vals.length){const i=Math.floor(vals.length/2);return vals.length%2?vals[i]:(vals[i-1]+vals[i])/2}
 return num(mp.activeMedian||mp.median||mp.marketValue||mp.conservativeMarket||mp.suggestedGbp||mp.suggestedMarketValue);
}
function quote(r){
 const market=validatedMarket(r);if(!(market>0))return null;
 const qty=Math.max(1,num($('pq')?.value)||1),cost=num($('pp')?.value)/qty,st=STAGES[stageKey()];
 const pack=.30;
 const floor=cost>0?(cost+pack)/(1-st.minMargin):0;
 const preferred=cost>0?(cost+pack)/(1-st.preferred):0;
 const velocity=market*(1-st.undercut);
 const recommended=price99(Math.max(floor,velocity));
 const projectedProfit=recommended-cost-pack;
 const margin=recommended>0?projectedProfit/recommended:0;
 return {stage:stageKey(),st,market,cost,pack,floor:r2(floor),preferredFloor:r2(preferred),velocity:r2(velocity),recommended,profit:r2(projectedProfit),margin,constrained:cost>0&&floor>market+.01};
}

const originalMarketSuggested=typeof marketSuggestedPrice==='function'?marketSuggestedPrice:null;
if(originalMarketSuggested){
 marketSuggestedPrice=function(r){const q=quote(r);return q?.recommended||(originalMarketSuggested?originalMarketSuggested(r):0)};
}

function findPricingCard(){
 const direct=document.querySelector('#stockEntryPanel .market-price-card.on,.market-price-card.on,#stockEntryPanel .market-pricing-card,.market-pricing-card');
 if(direct)return direct;
 const nodes=[...document.querySelectorAll('#stockEntryPanel section,#stockEntryPanel article,#stockEntryPanel div,section,article')];
 return nodes.find(el=>{const t=(el.textContent||'').toUpperCase();return t.includes('MARKET PRICING')&&t.includes('VALIDATED EXACT CARD')&&t.includes('SUGGESTED')})||null;
}
function findSuggestedNode(card){
 const direct=card?.querySelector('.market-price-main,.market-pricing-main,[data-market-suggested]');if(direct)return direct;
 if(!card)return null;
 const all=[...card.querySelectorAll('div,b,strong,h1,h2,h3,p,span')];
 return all.find(el=>/^\s*£[\d,.]+\s*SUGGESTED\s*$/i.test((el.textContent||'').trim()))
   ||all.find(el=>/£[\d,.]+[\s\S]*suggested/i.test(el.textContent||''))
   ||null;
}
function policyLine(card){
 let el=card?.querySelector('.gengrail-test-listing-policy');
 if(!el&&card){el=document.createElement('div');el.className='gengrail-test-listing-policy';el.style.cssText='margin-top:12px;padding:11px 12px;border:1px solid #31543b;border-left:4px solid #82dda0;border-radius:8px;background:#07110a;color:#b8c7bc;font-size:11px;line-height:1.5';card.appendChild(el)}
 return el;
}
function relabelOutlier(card,r){
 const vals=[r?.marketPricing?.gbp?.trend,r?.marketPricing?.gbp?.avg7,r?.marketPricing?.gbp?.avg30].map(num).filter(v=>v>0).sort((a,b)=>a-b);
 const low=num(r?.marketPricing?.gbp?.low);if(!card||!vals.length||!(low>0))return;
 const med=vals[Math.floor(vals.length/2)];if(low>=med*.6)return;
 const all=[...card.querySelectorAll('*')];
 const label=all.find(el=>/MARKET LOW/i.test((el.textContent||'').trim())&&el.children.length===0);
 if(label)label.textContent='RAW MARKET LOW · EXCLUDED';
}
function update(){
 const r=recognition();if(!r)return;const q=quote(r);if(!q)return;
 const card=findPricingCard();if(!card)return;
 const main=findSuggestedNode(card);
 if(main)main.textContent=`${gbp(q.recommended)} suggested`;
 const line=policyLine(card);
 if(line)line.innerHTML=`<b style="color:#82dda0">${q.st.label}</b><br>Validated market anchor ${gbp(q.market)} · velocity target ${gbp(q.velocity)} · protected ${(q.st.minMargin*100).toFixed(0)}% floor ${q.cost>0?gbp(q.floor):'awaiting buy cost'}${q.cost>0?` · projected ${gbp(q.profit)} / ${(q.margin*100).toFixed(1)}%`:''}${q.constrained?' · <b style="color:#ffd36f">MARKET CONSTRAINED</b>':''}<br><span style="color:#7e8f82">Private eBay seller transaction fee £0 · packaging assumption £0.30 · purchase cost is a floor guardrail, not the market anchor.</span>`;
 relabelOutlier(card,r);
 // Keep the button/action path aligned with the live recommendation where possible.
 card.dataset.gengrailSuggested=String(q.recommended);
 window.__gengrailLiveSuggestedPrice=q.recommended;
}
let timer=0;const schedule=()=>{clearTimeout(timer);timer=setTimeout(update,40)};
function bind(){
 ['pp','pq','pc','pcondition','plist'].forEach(id=>{const el=$(id);if(!el||el.dataset.seedPolicyBoundV11)return;el.dataset.seedPolicyBoundV11='1';el.addEventListener('input',schedule,{passive:true});el.addEventListener('change',schedule,{passive:true});el.addEventListener('keyup',schedule,{passive:true})});
 schedule();
}
// Capture input at document level as a fallback for fields replaced/re-rendered by the catalogue UI.
document.addEventListener('input',e=>{if(['pp','pq','pc','pcondition','plist'].includes(e.target?.id))schedule()},true);
document.addEventListener('change',e=>{if(['pp','pq','pc','pcondition','plist'].includes(e.target?.id))schedule()},true);
const mo=new MutationObserver(bind);
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>{bind();mo.observe(document.body,{childList:true,subtree:true})});else{bind();mo.observe(document.body,{childList:true,subtree:true})}
// Lightweight signature watcher catches iOS/Safari value changes even if the page suppresses normal input handlers.
let lastSig='';setInterval(()=>{const sig=[num($('pp')?.value),num($('pq')?.value),$('pc')?.value||'',stageKey(),!!recognition()].join('|');if(sig!==lastSig){lastSig=sig;schedule()}},300);
window.addEventListener('gengrail:main-updated',schedule);
window.GengrailTestListingPolicy={version:'1.1',quote:()=>quote(recognition()),recalculate:update,stages:STAGES};
})();