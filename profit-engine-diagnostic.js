/* GENGRAIL PROFIT ENGINE DASHBOARD v1.1
   Temporary test-repo consolidation layer.
   Read-only: promotes Profit Engine as Dashboard, mirrors legacy accounting KPIs,
   and surfaces recorded Profit Split redirects. Does not mutate business data.
*/
(function(){
'use strict';
const money=v=>new Intl.NumberFormat('en-GB',{style:'currency',currency:'GBP'}).format(Number(v)||0);
const pct=v=>`${Number(v||0).toFixed(1)}%`;
const esc=v=>String(v??'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]||c));
const text=id=>document.getElementById(id)?.textContent?.trim()||'—';
const dbRead=()=>{try{return JSON.parse(localStorage.getItem('gengrailBizV1')||'null')}catch{return null}};
const potLabel={STOCK_LIQUIDITY:'Stock / Liquidity',TAX_RESERVE:'Tax Reserve',BUSINESS_RESERVE:'Business Reserve',GROWTH_FUND:'Growth Fund',OWNER_POT:'Owner Pot'};

function ensureStyles(){
 if(document.getElementById('profitEngineDiagnosticStyles'))return;
 const s=document.createElement('style');s.id='profitEngineDiagnosticStyles';
 s.textContent=`
 #profitEngineDiagnostic{border:1px solid #31543b;border-left:5px solid #58c77a;background:linear-gradient(180deg,#0b160e,#0a0d0b);border-radius:13px;padding:14px;margin-top:12px;box-shadow:6px 6px #000}
 #profitEngineDiagnostic .ped-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:12px}
 #profitEngineDiagnostic .ped-title{font:24px Impact,sans-serif;letter-spacing:.04em}
 #profitEngineDiagnostic .ped-badge{border:1px solid #8a6c25;color:#ffd36f;background:#171107;border-radius:999px;padding:5px 8px;font-size:9px;font-weight:900;white-space:nowrap}
 #profitEngineDiagnostic .ped-sub{color:#8fa596;font-size:11px;line-height:1.45;margin-top:3px}
 #profitEngineDiagnostic .ped-hero{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px}
 #profitEngineDiagnostic .ped-box{background:#07110a;border:1px solid #294d34;border-radius:9px;padding:10px;min-width:0}
 #profitEngineDiagnostic .ped-box small{display:block;color:#8fa596;font-size:9px;font-weight:900;letter-spacing:.04em}
 #profitEngineDiagnostic .ped-box b{display:block;margin-top:3px;font-size:18px;color:#eef6f0;word-break:break-word}
 #profitEngineDiagnostic .ped-box.accent b{color:#78e39a;font-size:22px}
 #profitEngineDiagnostic .ped-section{margin-top:12px;padding-top:12px;border-top:1px solid #25332a}
 #profitEngineDiagnostic .ped-section-title{color:#70e09a;font-size:10px;font-weight:950;letter-spacing:.14em;margin-bottom:8px}
 #profitEngineDiagnostic .ped-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:7px}
 #profitEngineDiagnostic .ped-pot{background:#080b09;border:1px solid #28362c;border-radius:8px;padding:9px;min-width:0}
 #profitEngineDiagnostic .ped-pot small{display:block;color:#888;font-size:9px;font-weight:900}
 #profitEngineDiagnostic .ped-pot b{display:block;margin-top:3px;font-size:16px;word-break:break-word}
 #profitEngineDiagnostic .ped-note{margin-top:10px;border-left:3px solid #8a6c25;padding:8px 10px;background:#171107;color:#d7c48f;font-size:10px;line-height:1.45}
 #profitEngineDiagnostic .ped-protection{border:1px solid #8a6c25;background:#171107;border-radius:10px;padding:11px;margin-top:10px}
 #profitEngineDiagnostic .ped-protection strong{color:#ffd36f;display:block;font-size:12px;margin-bottom:6px}
 #profitEngineDiagnostic .ped-redirect{display:flex;justify-content:space-between;gap:10px;border-top:1px solid #4b3b1c;padding-top:7px;margin-top:7px;font-size:11px}
 #profitEngineDiagnostic .ped-redirect span:last-child{color:#ffd36f;font-weight:900;text-align:right}
 #profitEngineDiagnostic .ped-split{display:grid;grid-template-columns:1.2fr .8fr .8fr;gap:6px;font-size:10px;margin-top:5px}
 #profitEngineDiagnostic .ped-split.head{color:#8f8f8f;font-weight:900}
 #profitEngineDiagnostic .ped-split:not(.head){padding:5px 0;border-top:1px solid #302b1d}
 #profitEngineDiagnostic .ped-financials{border-color:#4a4026}
 #profitEngineDiagnostic .ped-financials b{color:#f2f0e8}
 @media(min-width:700px){#profitEngineDiagnostic .ped-grid{grid-template-columns:repeat(5,1fr)}#profitEngineDiagnostic .ped-hero{grid-template-columns:repeat(4,1fr)}}`;
 document.head.appendChild(s);
}
function stageLabel(g){return g?.profitStage?.label||`Stage ${g?.currentProfitStage||1}`}
function latestAllocation(){
 const db=dbRead(),rows=Array.isArray(db?.profitEngine?.allocations)?db.profitEngine.allocations:[];
 return [...rows].reverse().find(a=>a?.status==='ACTIVE'&&a?.classification==='TRADING')||null;
}
function protectionHtml(a){
 if(!a)return '';
 const nominal=a.nominalAmounts||{},actual=a.actualAmounts||{},redirects=Array.isArray(a.redirects)?a.redirects:[];
 const rows=['STOCK_LIQUIDITY','TAX_RESERVE','BUSINESS_RESERVE','GROWTH_FUND','OWNER_POT'].map(k=>`<div class="ped-split"><span>${esc(potLabel[k])}</span><span>${money(nominal[k])}</span><span>${money(actual[k])}</span></div>`).join('');
 const target=a.protectionTargets?.taxReserve;
 const current=dbRead()?.profitEngine?.ledger?.filter(x=>x?.pot==='TAX_RESERVE').reduce((s,x)=>s+(Number(x.amount)||0),0)||0;
 const redirectHtml=redirects.length?redirects.map(r=>`<div class="ped-redirect"><span>${esc(potLabel[r.from]||r.from)} → ${esc(potLabel[r.to]||r.to)}<br><small>${esc(String(r.reason||'').replaceAll('_',' '))}</small></span><span>${money(r.amount)}</span></div>`).join(''):'<div class="ped-note">No allocation redirects on the latest trading sale.</div>';
 return `<div class="ped-section"><div class="ped-section-title">LATEST PROFIT SPLIT</div><div class="ped-protection"><strong>${redirects.length?'ALLOCATION PROTECTION ACTIVE':'NOMINAL ALLOCATION APPLIED'}</strong><div class="ped-split head"><span>POT</span><span>NOMINAL</span><span>ACTUAL</span></div>${rows}${redirectHtml}${Number.isFinite(Number(target))?`<div class="ped-note">Protected Tax target at allocation: ${money(target)} · Current Tax pot: ${money(current)} · Remaining gap: ${money(Math.max(0,Number(target)-current))}</div>`:''}</div></div>`;
}
function financialsHtml(){return `<div class="ped-section"><div class="ped-section-title">BUSINESS FINANCIALS</div><div class="ped-grid">
 <div class="ped-pot ped-financials"><small>SALES REVENUE</small><b>${esc(text('rev'))}</b></div>
 <div class="ped-pot ped-financials"><small>COGS</small><b>${esc(text('cogskpi'))}</b></div>
 <div class="ped-pot ped-financials"><small>GROSS PROFIT</small><b>${esc(text('grossprofit'))}</b></div>
 <div class="ped-pot ped-financials"><small>SELLING FEES</small><b>${esc(text('sellfees'))}</b></div>
 <div class="ped-pot ped-financials"><small>DIRECT COSTS</small><b>${esc(text('directcosts'))}</b></div>
 <div class="ped-pot ped-financials"><small>OPERATING EXPENSES</small><b>${esc(text('opex'))}</b></div>
 <div class="ped-pot ped-financials"><small>REALISED PRE-TAX PROFIT</small><b>${esc(text('profit'))}</b></div>
 <div class="ped-pot ped-financials"><small>CORP TAX REQUIREMENT</small><b>${esc(text('ctax'))}</b></div>
 <div class="ped-pot ped-financials"><small>RETAINED AFTER-TAX</small><b>${esc(text('retained'))}</b></div>
 </div></div>`}
function render(){
 const host=document.getElementById('profitEngineDiagnostic');if(!host)return;
 const getG=window.getGrailPlanState,getF=window.getProfitFinanceSnapshot;
 if(typeof getG!=='function'||typeof getF!=='function'){host.innerHTML='<div class="ped-title">PROFIT ENGINE</div><div class="ped-note">Profit Engine state is not available yet.</div>';return}
 let g,f;try{g=getG();f=getF()}catch(err){host.innerHTML=`<div class="ped-title">PROFIT ENGINE</div><div class="ped-note">Dashboard read failed: ${esc(err?.message||err)}</div>`;return}
 if(!g||!f){host.innerHTML='<div class="ped-title">PROFIT ENGINE</div><div class="ped-note">No schema-4 state returned.</div>';return}
 const pots=f.potBalances||{},tr=g.trends||{},owner=g.ownerReadiness||{};
 host.innerHTML=`
  <div class="ped-head"><div><div class="ped-title">PROFIT ENGINE</div><div class="ped-sub">Business performance, protected liquidity and Grail Plan readiness</div></div><span class="ped-badge">TEST BUILD</span></div>
  <div class="ped-hero">
   <div class="ped-box accent"><small>TODAY'S REALISED TRADING PROFIT</small><b>${money(f.realisedNetTradingProfitToday)}</b></div>
   <div class="ped-box"><small>PROFIT SPLIT STAGE</small><b>${esc(`Stage ${g.currentProfitStage} · ${stageLabel(g)}`)}</b></div>
   <div class="ped-box accent"><small>DEPLOYABLE LIQUIDITY</small><b>${money(g.availableGrailPlanLiquidity)}</b></div>
   <div class="ped-box"><small>GRAIL PLAN</small><b>${esc(g.mode)} · ${money(g.targetRange?.min)}–${money(g.targetRange?.max)}</b></div>
  </div>
  <div class="ped-section"><div class="ped-section-title">PROFIT SPLIT POTS</div><div class="ped-grid">
   <div class="ped-pot"><small>STOCK / LIQUIDITY</small><b>${money(pots.STOCK_LIQUIDITY)}</b></div>
   <div class="ped-pot"><small>TAX RESERVE</small><b>${money(pots.TAX_RESERVE)}</b></div>
   <div class="ped-pot"><small>BUSINESS RESERVE</small><b>${money(pots.BUSINESS_RESERVE)}</b></div>
   <div class="ped-pot"><small>GROWTH FUND</small><b>${money(pots.GROWTH_FUND)}</b></div>
   <div class="ped-pot"><small>OWNER POT</small><b>${money(pots.OWNER_POT)}</b></div>
  </div></div>
  ${protectionHtml(latestAllocation())}
  <div class="ped-section"><div class="ped-section-title">TRADING PERFORMANCE</div><div class="ped-grid">
   <div class="ped-pot"><small>7-DAY AVG / DAY</small><b>${money(tr.avg7)}</b></div>
   <div class="ped-pot"><small>30-DAY AVG / DAY</small><b>${money(tr.avg30)}</b></div>
   <div class="ped-pot"><small>90-DAY AVG / DAY</small><b>${money(tr.avg90)}</b></div>
   <div class="ped-pot"><small>180-DAY AVG / DAY</small><b>${money(tr.avg180)}</b></div>
   <div class="ped-pot"><small>OWNER READINESS</small><b>${esc(owner.status||'NOT READY')}</b></div>
  </div></div>
  <div class="ped-section"><div class="ped-section-title">CAPITAL ORIGIN</div><div class="ped-grid">
   <div class="ped-pot"><small>OWNER CASH CONTRIBUTIONS</small><b>${money(g.ownerCashContributions)}</b></div>
   <div class="ped-pot"><small>BOOTSTRAP CAPITAL</small><b>${money(g.bootstrapCapital)}</b></div>
   <div class="ped-pot"><small>RETAINED TRADING PROFIT</small><b>${money(g.retainedTradingProfit)}</b></div>
   <div class="ped-pot"><small>CAPITAL IN INVENTORY</small><b>${money(g.capitalCommittedToInventory)}</b></div>
   <div class="ped-pot"><small>SELF-FUNDED</small><b>${pct(g.selfFundedPercentage)}</b></div>
  </div></div>
  ${financialsHtml()}
  <div class="ped-note">Profit Engine is now the test Dashboard. Accounting KPIs remain calculated by the existing accounting functions; Grail Plan uses protected deployable liquidity and realised trading profit.</div>`;
}
function mount(){
 ensureStyles();const dash=document.getElementById('dash');if(!dash)return;
 const legacy=dash.querySelector('.panel');if(legacy){legacy.style.display='none';legacy.dataset.profitEngineLegacy='hidden'}
 let host=document.getElementById('profitEngineDiagnostic');
 if(!host){host=document.createElement('div');host.id='profitEngineDiagnostic';if(legacy)legacy.insertAdjacentElement('afterend',host);else dash.prepend(host)}
 render();
 ['rev','cogskpi','grossprofit','sellfees','directcosts','opex','profit','ctax','retained'].forEach(id=>{const el=document.getElementById(id);if(el&&!el.dataset.profitDiagnosticObserved){el.dataset.profitDiagnosticObserved='1';new MutationObserver(render).observe(el,{subtree:true,childList:true,characterData:true})}})
}
window.addEventListener('gengrail:main-updated',()=>setTimeout(render,0));
window.addEventListener('storage',()=>setTimeout(render,0));
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(mount,0));else setTimeout(mount,0);
})();
