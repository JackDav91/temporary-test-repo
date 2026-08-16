/* GENGRAIL PROFIT ENGINE DIAGNOSTIC v1.0
   Temporary test-only visibility for schema-4 financial state.
   Reads the public Profit Engine interfaces; does not mutate business data.
*/
(function(){
'use strict';
const money=v=>new Intl.NumberFormat('en-GB',{style:'currency',currency:'GBP'}).format(Number(v)||0);
const pct=v=>`${Number(v||0).toFixed(1)}%`;
const esc=v=>String(v??'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]||c));

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
 #profitEngineDiagnostic .ped-pot{background:#080b09;border:1px solid #28362c;border-radius:8px;padding:9px}
 #profitEngineDiagnostic .ped-pot small{display:block;color:#888;font-size:9px;font-weight:900}
 #profitEngineDiagnostic .ped-pot b{display:block;margin-top:3px;font-size:16px}
 #profitEngineDiagnostic .ped-note{margin-top:10px;border-left:3px solid #8a6c25;padding:8px 10px;background:#171107;color:#d7c48f;font-size:10px;line-height:1.45}
 @media(min-width:700px){#profitEngineDiagnostic .ped-grid{grid-template-columns:repeat(5,1fr)}#profitEngineDiagnostic .ped-hero{grid-template-columns:repeat(4,1fr)}}`;
 document.head.appendChild(s);
}
function stageLabel(g){return g?.profitStage?.label||`Stage ${g?.currentProfitStage||1}`}
function render(){
 const host=document.getElementById('profitEngineDiagnostic');if(!host)return;
 const getG=window.getGrailPlanState,getF=window.getProfitFinanceSnapshot;
 if(typeof getG!=='function'||typeof getF!=='function'){
   host.innerHTML='<div class="ped-title">PROFIT ENGINE</div><div class="ped-note">Profit Engine state is not available yet.</div>';return;
 }
 let g,f;try{g=getG();f=getF()}catch(err){host.innerHTML=`<div class="ped-title">PROFIT ENGINE</div><div class="ped-note">Diagnostic read failed: ${esc(err?.message||err)}</div>`;return}
 if(!g||!f){host.innerHTML='<div class="ped-title">PROFIT ENGINE</div><div class="ped-note">No schema-4 state returned.</div>';return}
 const pots=f.potBalances||{},tr=g.trends||{},owner=g.ownerReadiness||{};
 host.innerHTML=`
  <div class="ped-head"><div><div class="ped-title">PROFIT ENGINE</div><div class="ped-sub">Schema 4 financial diagnostic · temporary test panel</div></div><span class="ped-badge">TEST DIAGNOSTIC</span></div>
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
  <div class="ped-note">Diagnostic only. Existing Dashboard accounting remains unchanged. Profit Split uses realised trading profit; bootstrap proceeds are tracked separately and do not drive stage performance.</div>`;
}
function mount(){
 ensureStyles();
 const dash=document.getElementById('dash');if(!dash)return;
 let host=document.getElementById('profitEngineDiagnostic');
 if(!host){host=document.createElement('div');host.id='profitEngineDiagnostic';const panel=dash.querySelector('.panel');if(panel)panel.insertAdjacentElement('afterend',host);else dash.appendChild(host)}
 render();
 const rev=document.getElementById('rev');if(rev&&!rev.dataset.profitDiagnosticObserved){rev.dataset.profitDiagnosticObserved='1';new MutationObserver(render).observe(rev,{subtree:true,childList:true,characterData:true})}
}
window.addEventListener('gengrail:main-updated',()=>setTimeout(render,0));
window.addEventListener('storage',()=>setTimeout(render,0));
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(mount,0));else setTimeout(mount,0);
})();
