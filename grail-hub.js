/* GENGRAIL GRAIL HUB v1 — Buying command centre
   Read-only consumer of the Profit Engine contract.
   No opportunity search logic is changed in this slice.
*/
(function(){
'use strict';
const money=v=>new Intl.NumberFormat('en-GB',{style:'currency',currency:'GBP'}).format(Number(v)||0);
const pct=v=>`${(Number(v||0)*100).toFixed(0)}%`;
const esc=v=>String(v??'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]||c));

function state(){
  try{return typeof window.getGrailPlanState==='function'?window.getGrailPlanState():null}catch{return null}
}
function statusCopy(g){
  if(!g)return 'Profit Engine state is not available yet.';
  if(g.liquidityConstrained)return `Opportunity capture constrained · additional liquidity required ${money(g.liquidityShortfall)}`;
  if(Number(g.availableGrailPlanLiquidity)<=0)return 'No deployable liquidity is currently available. Protected pots remain ring-fenced.';
  return `${g.mode} mode is active. Search objectives are subordinate to ROI, margin, confidence, sell-through and liquidity protection.`;
}
function openExisting(labelMatchers){
  const nodes=[...document.querySelectorAll('button,[role="button"],a')];
  const el=nodes.find(n=>labelMatchers.some(re=>re.test((n.textContent||'').trim())));
  if(el){close();setTimeout(()=>el.click(),0);return true}
  return false;
}
function render(){
  const root=document.getElementById('grailHubOverlay');if(!root)return;
  const g=state();
  if(!g){root.querySelector('.grail-hub-shell').innerHTML=`<div class="grail-hub-head"><button class="grail-hub-back" type="button" id="grailHubBack">←</button><div><div class="grail-hub-title">GRAIL HUB</div><div class="grail-hub-sub">Buying command centre</div></div></div><div class="grail-status">Profit Engine state is not available yet.</div>`;root.querySelector('#grailHubBack').onclick=close;return}
  const stage=g.profitStage||{};
  root.querySelector('.grail-hub-shell').innerHTML=`
    <div class="grail-hub-head">
      <button class="grail-hub-back" type="button" id="grailHubBack">←</button>
      <div><div class="grail-hub-title">GRAIL HUB</div><div class="grail-hub-sub">Today's route to projected profit</div></div>
    </div>
    <section class="grail-plan-hero">
      <div class="grail-plan-kicker"><span>GRAIL PLAN</span><span class="grail-plan-mode">${esc(g.mode)}</span></div>
      <div class="grail-plan-question">What is the smallest sensible combination of purchases that can move Gengrail toward today's profit target?</div>
      <div class="grail-plan-copy">The plan uses only deployable business liquidity. Protected Tax, Reserve, Growth and Owner funds stay outside the buying bankroll unless explicitly configured otherwise.</div>
      <div class="grail-plan-target">
        <div><small>AVAILABLE GRAIL PLAN LIQUIDITY</small><b>${money(g.availableGrailPlanLiquidity)}</b></div>
        <div class="secondary"><small>TODAY'S PROJECTED NET PROFIT OBJECTIVE</small><b>${money(g.targetRange?.min)}–${money(g.targetRange?.max)}</b></div>
      </div>
      <div class="grail-guardrails">
        <div class="grail-guardrail"><small>MIN ROI</small><b>${Number(g.minimumROI||0).toFixed(0)}%</b></div>
        <div class="grail-guardrail"><small>MIN NET MARGIN</small><b>${Number(g.minimumNetMargin||0).toFixed(0)}%</b></div>
        <div class="grail-guardrail"><small>MIN CONFIDENCE</small><b>${pct(g.minimumConfidence)}</b></div>
      </div>
      <div class="grail-status ${g.liquidityConstrained?'':'good'}">${esc(statusCopy(g))}</div>
    </section>

    <section class="grail-hub-section">
      <div class="grail-hub-section-title">BUYING WORKSPACE</div>
      <div class="grail-action-grid">
        <button class="grail-action-card primary" id="grailPlanAction" type="button"><span class="grail-action-icon">♛</span><b>Grail Plan</b><span>Build the best sensible purchase basket from live opportunities and today's bankroll.</span></button>
        <button class="grail-action-card" id="grailOpportunityAction" type="button"><span class="grail-action-icon">⌁</span><b>Opportunity Stream</b><span>Open the existing Opportunity Finder while the ranked live-stream layer is connected next.</span></button>
        <button class="grail-action-card" id="grailPricingAction" type="button"><span class="grail-action-icon">£</span><b>Pricing Calculator</b><span>Identify, value and test raw cards or graded slabs before committing capital.</span></button>
        <button class="grail-action-card" id="grailRefreshAction" type="button"><span class="grail-action-icon">↻</span><b>Refresh Plan State</b><span>Reload liquidity, stage, protection and target inputs from the Profit Engine.</span></button>
      </div>
    </section>

    <section class="grail-hub-section">
      <div class="grail-hub-section-title">PLAN INPUTS</div>
      <div class="grail-state-strip">
        <div class="grail-state-cell"><small>PROFIT STAGE</small><b>Stage ${Number(g.currentProfitStage||1)} · ${esc(stage.label||'Build Capital')}</b></div>
        <div class="grail-state-cell"><small>30-DAY AVG / DAY</small><b>${money(g.trends?.avg30)}</b></div>
        <div class="grail-state-cell"><small>CAPITAL IN INVENTORY</small><b>${money(g.capitalCommittedToInventory)}</b></div>
        <div class="grail-state-cell"><small>SELF-FUNDED</small><b>${Number(g.selfFundedPercentage||0).toFixed(1)}%</b></div>
      </div>
    </section>
    <div class="grail-hub-foot">Grail Hub consumes Profit Engine state. It does not recalculate accounting, Tax protection or business liquidity independently.</div>`;
  root.querySelector('#grailHubBack').onclick=close;
  root.querySelector('#grailRefreshAction').onclick=render;
  root.querySelector('#grailPricingAction').onclick=()=>{if(!openExisting([/PRICING CALCULATOR/i,/WORK OUT TRUE VALUE/i]))alert('Pricing Calculator navigation is not available from this build yet.')};
  root.querySelector('#grailOpportunityAction').onclick=()=>{if(!openExisting([/OPPORTUNITY FINDER/i,/OPPORTUNITIES/i]))alert('Opportunity Finder is not exposed as a standalone navigation action yet. The live Opportunity Stream is the next Grail Hub slice.')};
  root.querySelector('#grailPlanAction').onclick=()=>alert('Grail Plan basket generation is the next build slice. This v1 screen is already using the live financial constraints it will optimise against.');
}
function open(){
  let root=document.getElementById('grailHubOverlay');
  if(!root){root=document.createElement('div');root.id='grailHubOverlay';root.className='grail-hub-overlay';root.innerHTML='<div class="grail-hub-shell"></div>';document.body.appendChild(root)}
  root.hidden=false;document.body.style.overflow='hidden';render();
}
function close(){const root=document.getElementById('grailHubOverlay');if(root)root.hidden=true;document.body.style.overflow=''}
function bindBuying(){
  const buttons=[...document.querySelectorAll('button')];
  const buying=buttons.find(b=>/^BUYING$/i.test((b.querySelector('.home-label')?.textContent||b.textContent||'').trim()));
  if(!buying||buying.dataset.grailHubBound)return;
  buying.dataset.grailHubBound='1';
  buying.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation();open()},true);
}
window.GengrailGrailHub={open,close,render};
window.addEventListener('gengrail:main-updated',()=>{if(!document.getElementById('grailHubOverlay')?.hidden)render()});
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(bindBuying,0));else setTimeout(bindBuying,0);
})();
