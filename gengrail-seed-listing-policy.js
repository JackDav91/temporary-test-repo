/* GENGRAIL TEST — LISTING POLICY v1.0
   Isolated catalogue/listing pricing experiment for temporary-test-repo only.
   SEED: velocity first, protect 10% projected net margin.
   BUILD: protect 15%, prefer 20%, still price competitively.
   SCALE: protect 15%, prefer 20%, tighter market undercut.
   Current eBay context: UK private seller, £0 seller transaction fee; buyer postage treated as pass-through.
*/
(function(){
'use strict';
if(window.__gengrailSeedListingPolicyV1)return;
window.__gengrailSeedListingPolicyV1=true;

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
function rawMarket(r){
 const mp=r?.marketPricing;if(!mp)return 0;
 const direct=num(mp.suggestedGbp||mp.suggestedMarketValue||mp.activeMedian||mp.median||mp.marketValue||mp.conservativeMarket);
 if(direct>0)return direct;
 const vals=[mp?.gbp?.trend,mp?.gbp?.avg7,mp?.gbp?.avg30].map(num).filter(v=>v>0).sort((a,b)=>a-b);
 if(!vals.length)return 0;const i=Math.floor(vals.length/2);return vals.length%2?vals[i]:(vals[i-1]+vals[i])/2;
}
function quote(r){
 const market=rawMarket(r);if(!(market>0))return null;
 const qty=Math.max(1,num($('pq')?.value)||1),cost=num($('pp')?.value)/qty,st=STAGES[stageKey()];
 // Private eBay: seller transaction fee = £0. Buyer-paid postage offsets fulfilment postage.
 // Packaging remains a genuine per-order economic cost.
 const pack=.30;
 const floor=cost>0?(cost+pack)/(1-st.minMargin):0;
 const preferred=cost>0?(cost+pack)/(1-st.preferred):0;
 const velocity=market*(1-st.undercut);
 const recommended=price99(Math.max(floor,velocity));
 const projectedProfit=recommended-cost-pack;
 const margin=recommended>0?projectedProfit/recommended:0;
 return {stage:stageKey(),st,market,cost,pack,floor:r2(floor),preferredFloor:r2(preferred),velocity:r2(velocity),recommended,profit:r2(projectedProfit),margin,constrained:floor>market+.01};
}

const originalMarketSuggested=typeof marketSuggestedPrice==='function'?marketSuggestedPrice:null;
if(originalMarketSuggested){
 marketSuggestedPrice=function(r){const q=quote(r);return q?.recommended||(originalMarketSuggested?originalMarketSuggested(r):0)};
}

function policyLine(card){
 let el=card.querySelector('.gengrail-test-listing-policy');
 if(!el){el=document.createElement('div');el.className='gengrail-test-listing-policy';el.style.cssText='margin-top:10px;padding:10px 12px;border:1px solid #31543b;border-left:4px solid #82dda0;border-radius:8px;background:#07110a;color:#b8c7bc;font-size:11px;line-height:1.5';card.appendChild(el)}
 return el;
}
function update(){
 const r=recognition();if(!r)return;const q=quote(r);if(!q)return;
 const card=document.querySelector('#stockEntryPanel .market-price-card.on')||document.querySelector('.market-price-card.on');if(!card)return;
 const main=card.querySelector('.market-price-main');if(main)main.textContent=`${gbp(q.recommended)} suggested`;
 const line=policyLine(card);
 line.innerHTML=`<b style="color:#82dda0">${q.st.label}</b><br>Velocity target ${gbp(q.velocity)} · protected ${(q.st.minMargin*100).toFixed(0)}% floor ${q.cost>0?gbp(q.floor):'awaiting buy cost'}${q.cost>0?` · projected ${gbp(q.profit)} / ${(q.margin*100).toFixed(1)}%`:''}${q.constrained?' · <b style="color:#ffd36f">MARKET CONSTRAINED</b>':''}<br><span style="color:#7e8f82">Private eBay seller transaction fee: £0 · buyer postage treated as pass-through · packaging assumption £0.30.</span>`;
 // If the displayed raw market low is obviously outside the validated pricing cluster, label it honestly.
 const vals=[r?.marketPricing?.gbp?.trend,r?.marketPricing?.gbp?.avg7,r?.marketPricing?.gbp?.avg30].map(num).filter(v=>v>0).sort((a,b)=>a-b);
 const low=num(r?.marketPricing?.gbp?.low);if(vals.length&&low>0){const med=vals[Math.floor(vals.length/2)];if(low<med*.6){const boxes=[...card.querySelectorAll('.market-price-grid div')];const lowBox=boxes[3];if(lowBox){const small=lowBox.querySelector('small');if(small)small.textContent='RAW MARKET LOW · EXCLUDED'}}}
}
let timer=0;const schedule=()=>{clearTimeout(timer);timer=setTimeout(update,60)};
function bind(){['pp','pq','pc','pcondition','plist'].forEach(id=>{const el=$(id);if(!el||el.dataset.seedPolicyBound)return;el.dataset.seedPolicyBound='1';el.addEventListener('input',schedule);el.addEventListener('change',schedule)});schedule()}
const mo=new MutationObserver(bind);
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>{bind();mo.observe(document.body,{childList:true,subtree:true})});else{bind();mo.observe(document.body,{childList:true,subtree:true})}
window.addEventListener('gengrail:main-updated',schedule);
window.GengrailTestListingPolicy={version:'1.0',quote:()=>quote(recognition()),recalculate:update,stages:STAGES};
})();