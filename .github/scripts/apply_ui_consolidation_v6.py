from pathlib import Path
import re

CSS = r'''/* GENGRAIL UI CONSOLIDATION v24.0.0 — presentation only */
:root{--ui-gold:#e0ad16;--ui-gold2:#f2c84b;--ui-green:#82dda0;--ui-amber:#ffd36f;--ui-red:#ff8c8c;--ui-border:#343434;--ui-panel:#101010;--gengrail-visible-height:100dvh}

/* Home: use the actual visible iOS viewport supplied by ui-consolidation.js. */
body.home-page .app{height:calc(var(--gengrail-visible-height) - 8px)!important;min-height:0!important;overflow:hidden!important}
body.home-page .home-screen{min-height:0!important;flex:1 1 auto!important}
body.home-page .home-menu{min-height:0!important;grid-template-rows:repeat(3,minmax(0,1fr))!important}
body.home-page .home-menu button{min-height:0!important;height:100%!important}
body.home-page .gengrail-performance-ticker{overflow:hidden!important;margin-bottom:0!important}
body.home-page .gengrail-ticker-track{padding-left:10px!important}

/* Global hierarchy: consistent radii and meaning. */
.ui-consolidated .panel{border-radius:16px}
.ui-consolidated .btn,.ui-consolidated button{border-radius:11px}
.ui-consolidated .ui-primary-action{background:var(--ui-gold)!important;color:#080808!important;border-color:var(--ui-gold2)!important}
.ui-consolidated .ui-status-only{pointer-events:none!important;cursor:default!important;background:#171107!important;color:var(--ui-amber)!important;border:1px solid #8a6c25!important;box-shadow:none!important}
.ui-consolidated .ui-secondary-copy{font-size:11px;color:#888;line-height:1.4;margin-top:7px}

/* Stock: camera first, then compact secondary actions. */
#stock .product-intake-grid{display:grid!important;grid-template-columns:1fr 1fr!important;gap:10px!important}
#stock #startCameraIntake{grid-column:1/-1!important;min-height:132px!important}
#stock .product-intake-grid [data-graded-import="stock"],#stock #startPhotoIntake,#stock #startManualIntake{min-height:112px!important;padding:14px 10px!important}
#stock .product-intake-grid [data-graded-import="stock"] b,#stock #startPhotoIntake b,#stock #startManualIntake b{font-size:18px!important}
#stock .product-intake-grid [data-graded-import="stock"] small,#stock #startPhotoIntake small,#stock #startManualIntake small{font-size:10px!important}
#stock .product-intake-grid [data-graded-import="stock"] .graded-intake-icon,#stock #startPhotoIntake .intake-icon,#stock #startManualIntake .intake-icon{font-size:24px!important;margin-bottom:3px!important}
#stock .compact-intake-note{margin-bottom:14px!important}
@media(max-width:390px){#stock .product-intake-grid{grid-template-columns:1fr!important}#stock #startCameraIntake{grid-column:auto!important}.product-intake-grid [data-graded-import="stock"],#stock #startPhotoIntake,#stock #startManualIntake{min-height:96px!important}}

/* Recognition result: statuses should look like statuses, not actions. */
#stockEntryPanel .ui-market-status{border:1px solid #8a6c25!important;background:#171107!important;color:var(--ui-amber)!important}
#stockEntryPanel .ui-market-status button{pointer-events:none!important}

/* Pricing Calculator: one compact sequence instead of stacked feature history. */
#pricing.ui-pricing-clean .pricing-purpose{margin-bottom:10px!important}
#pricing.ui-pricing-clean .pricing-ai-tools{margin-bottom:10px!important}
#pricing.ui-pricing-clean .pricing-tabs{margin-bottom:10px!important}
#pricing.ui-pricing-clean .pricing-core-grid{gap:10px!important}
#pricing.ui-pricing-clean #pricePostageSummary{margin:8px 0 2px!important;padding:10px 12px!important;min-height:0!important;border-radius:11px!important}
#pricing.ui-pricing-clean #pricePostageSummary>*{margin:0!important}
#pricing.ui-pricing-clean #pricePostageSummary br{display:none!important}
#pricing.ui-pricing-clean .pricing-recalc{width:100%!important;margin-top:12px!important;min-height:52px!important}
#pricing.ui-pricing-clean .pricing-result{margin-top:12px!important}
#pricing.ui-pricing-clean .pricing-hero{padding:13px!important;border-color:#d88418!important}
#pricing.ui-pricing-clean .pricing-stats-4{grid-template-columns:1fr 1fr!important;gap:8px!important}
#pricing.ui-pricing-clean .pricing-stat{padding:10px 8px!important}
#pricing.ui-pricing-clean .compact-details{margin-top:10px!important}
#pricing.ui-pricing-clean .ui-pricing-profile-note{border-left:3px solid var(--ui-gold);padding-left:10px;color:#cfc2a1}

/* Settings: config is compact, maintenance remains visually separate. */
#settings.ui-settings-clean .panel{padding:14px!important}
#settings.ui-settings-clean .settings-status-row{padding:11px 12px!important}
#settings.ui-settings-clean .postage-settings-grid{display:grid!important;gap:8px!important}
#settings.ui-settings-clean .postage-setting{padding:0!important;border:1px solid #303030!important;border-radius:11px!important;background:#0b0b0b!important}
#settings.ui-settings-clean .postage-setting summary{padding:11px 12px!important}
#settings.ui-settings-clean .postage-setting .pf-edit{padding:0 12px 12px!important;margin-top:0!important}
#settings.ui-settings-clean #resetPostageProfiles{width:100%!important}
#settings.ui-settings-clean .ui-backup-actions{display:grid!important;grid-template-columns:1fr 1fr!important;gap:8px!important}
#settings.ui-settings-clean .ui-backup-actions #json{grid-column:1/-1!important;order:-1!important;background:var(--ui-gold)!important;color:#080808!important;border-color:var(--ui-gold2)!important}
#settings.ui-settings-clean .danger-zone{margin-top:12px!important}

/* Dashboard: top-level decision information prominent, detail quieter and tighter. */
#dash.ui-dashboard-clean .panel{margin-top:10px!important}
#dash.ui-dashboard-clean .kpi{padding:10px!important}
#dash.ui-dashboard-clean .ui-dashboard-detail{opacity:.96}
#dash.ui-dashboard-clean .ui-dashboard-detail .kpi{min-height:0!important}
#dash.ui-dashboard-clean .ui-owner-readiness{display:none!important}

/* Grail Hub: reduce explanation before action. */
.grail-plan-hero{padding:16px!important}
.grail-plan-question{font-size:30px!important;line-height:.98!important;margin-top:10px!important}
.grail-plan-copy{font-size:13px!important;line-height:1.4!important;margin-top:8px!important}
.grail-plan-target{margin-top:12px!important}
.grail-guardrails{margin-top:9px!important}
.grail-action-grid{grid-template-columns:repeat(3,1fr)!important}
.grail-action-card{min-height:142px!important;padding:14px!important}
.grail-action-card>span:last-child{font-size:11px!important;line-height:1.3!important}
#grailRefreshAction{display:none!important}
.grail-ui-refresh{margin-left:auto;background:#222;color:#eee;border:1px solid #444;border-radius:999px;padding:8px 11px;font-weight:900}
.grail-state-strip{grid-template-columns:repeat(2,1fr)!important}
.grail-hub-section-title{margin-bottom:9px!important}
@media(max-width:620px){.grail-action-grid{grid-template-columns:1fr 1fr!important}.grail-action-card.primary{grid-column:1/-1!important;min-height:118px!important}.grail-action-card{min-height:126px!important}.grail-plan-question{font-size:26px!important}}

/* Opportunity Stream: plan and results dominate, diagnostics compress. */
.grail-stream-toolbar{padding:12px!important}
.grail-stream-toolbar label{font-size:9px!important}
.grail-stream-search{gap:7px!important}
.grail-discovery-row{margin-top:8px!important}
.grail-stream-hint{font-size:10px!important;line-height:1.35!important;margin-top:7px!important;color:#777!important}
.grail-stream-summary{display:flex!important;gap:8px!important;overflow:auto!important;padding:0 1px!important;margin:10px 0!important}
.grail-stream-summary>div{min-width:max-content!important;flex:1!important;padding:9px 11px!important}
.grail-stream-summary small{font-size:8px!important}.grail-stream-summary b{font-size:16px!important}
.grail-stream-state{padding:10px 12px!important;margin-bottom:10px!important;font-size:12px!important}
.grail-plan-preview{padding:15px!important;margin:10px 0!important}
.grail-plan-preview h3{font-size:28px!important;line-height:1!important;margin:8px 0!important}
.grail-opportunity{padding:12px!important}
.grail-opportunity-grid{gap:7px!important}
.grail-opportunity-reason{font-size:10px!important;line-height:1.35!important}

/* Graded recognition: product language, not implementation vocabulary. */
.gsc-assumed,.graded-stock-assumed{font-size:11px!important;line-height:1.4!important}
[data-ggrader]+[data-gconfirm]{width:100%!important}
'''

JS = r'''(()=>{
'use strict';
const qs=(s,r=document)=>r.querySelector(s),qsa=(s,r=document)=>[...r.querySelectorAll(s)];
function visibleHeight(){const vv=window.visualViewport;const h=Math.round(vv?.height||window.innerHeight||document.documentElement.clientHeight);document.documentElement.style.setProperty('--gengrail-visible-height',h+'px')}
function setText(el,text){if(el&&el.textContent.trim()!==text)el.textContent=text}
function addClassByTitle(root,title,cls){qsa('.panel',root).forEach(p=>{const t=qs('.title',p);if(t&&t.textContent.trim().toUpperCase()===title)p.classList.add(cls)})}
function cleanStock(){const root=qs('#stock');if(!root)return;root.classList.add('ui-stock-clean');const photo=qs('#startPhotoIntake b',root);setText(photo,'PHOTO LIBRARY');const ps=qs('#startPhotoIntake small',root);setText(ps,'Choose an existing card image');const slab=qs('[data-graded-import="stock"] b',root);if(slab)setText(slab,'GRADED SLAB');const man=qs('#startManualIntake b',root);if(man)setText(man,'MANUAL ENTRY');qsa('button',root).forEach(b=>{if(b.textContent.trim()==='NO MARKET PRICE'){b.textContent='MARKET PRICE UNAVAILABLE';b.classList.add('ui-status-only')}})}
function cleanPricing(){const root=qs('#pricing');if(!root)return;root.classList.add('ui-pricing-clean');qsa('*',root).forEach(el=>{if(el.children.length===0&&/MICRO VALUE BUYING PROFILE/i.test(el.textContent||'')){el.textContent=el.textContent.replace(/MICRO VALUE BUYING PROFILE/i,'CALCULATOR BUYING PROFILE');el.classList.add('ui-pricing-profile-note')}})}
function cleanSettings(){const root=qs('#settings');if(!root)return;root.classList.add('ui-settings-clean');const ai=qsa('.settings-status-row',root).find(x=>/AI Recognition/i.test(x.textContent));if(ai){const sm=qs('small',ai);setText(sm,'Raw + graded Pokémon recognition')}const actions=qsa('.panel',root).find(p=>/BACKUP & EXPORT/i.test(qs('.title',p)?.textContent||''))?.querySelector('.actions');if(actions)actions.classList.add('ui-backup-actions');const clean=qsa('button',root).find(b=>/CLEAN ORPHANED ORDERS/i.test(b.textContent));if(clean&&!clean.nextElementSibling?.classList?.contains('ui-secondary-copy')){const d=document.createElement('div');d.className='ui-secondary-copy';d.textContent='Removes order records that no longer have a matching sale or stock item.';clean.after(d)}}
function cleanDashboard(){const root=qs('#dash');if(!root)return;root.classList.add('ui-dashboard-clean');qsa('*',root).forEach(el=>{const t=(el.textContent||'').trim().toUpperCase();if(el.children.length===0&&['TRADING PERFORMANCE','CAPITAL ORIGIN','BUSINESS FINANCIALS','LATEST PROFIT SPLIT'].includes(t)){el.closest('.panel,section,div')?.classList.add('ui-dashboard-detail')}if(el.children.length===0&&t==='OWNER READINESS'){el.closest('.kpi,.grail-state-cell,div')?.classList.add('ui-owner-readiness')}})}
function cleanGrail(){const root=qs('#grailHubOverlay');if(!root||root.hidden)return;const head=qs('.grail-hub-head',root);if(head&&!qs('.grail-ui-refresh',head)&&qs('#grailRefreshAction',root)){const b=document.createElement('button');b.type='button';b.className='grail-ui-refresh';b.textContent='↻';b.setAttribute('aria-label','Refresh plan state');b.onclick=()=>qs('#grailRefreshAction',root)?.click();head.appendChild(b)}}
function cleanGradedCopy(){qsa('[data-ggrader]').forEach(sel=>{const small=sel.parentElement?.querySelector('small');if(small&&/USER_CONFIRMED/i.test(small.textContent))small.textContent='Your confirmation is saved as a manual grader check.'});qsa('.gsc-slabmeta span,.graded-stock-meta b').forEach(el=>{if(/ASSUMED/i.test(el.textContent))el.textContent=el.textContent.replace(/ASSUMED/i,'NEEDS CONFIRMATION')})}
function apply(){document.body.classList.add('ui-consolidated');visibleHeight();cleanStock();cleanPricing();cleanSettings();cleanDashboard();cleanGrail();cleanGradedCopy()}
let scheduled=false;const schedule=()=>{if(scheduled)return;scheduled=true;requestAnimationFrame(()=>{scheduled=false;apply()})};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply,{once:true});else apply();
window.addEventListener('resize',visibleHeight,{passive:true});window.visualViewport?.addEventListener('resize',visibleHeight,{passive:true});window.visualViewport?.addEventListener('scroll',visibleHeight,{passive:true});
new MutationObserver(schedule).observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['class','hidden']});
})();'''

# 1. Write UI layer.
Path('ui-consolidation.css').write_text(CSS)
Path('ui-consolidation.js').write_text(JS)

# 2. Grail Hub copy/hierarchy cleanup without changing business logic.
p=Path('grail-hub.js'); s=p.read_text()
if 'DISCOVERY_CONFIG=Object.freeze' not in s: raise SystemExit('Grail anchor missing')
s=s.replace("${a.safe?'PLAN CANDIDATE':'REVIEW'}","${a.safe?'PLAN CANDIDATE':(a.type==='RAW'&&a.condition==='UNKNOWN'?'REVIEW · CONDITION UNKNOWN':'REVIEW')}",1)
s=s.replace("What is the smallest sensible combination of purchases that can move Gengrail toward today's profit target?","Build today’s smallest sensible route to projected profit.",1)
old="<div class=\"grail-guardrails\"><div class=\"grail-guardrail\"><small>MIN ROI</small><b>${Number(g.minimumROI||0).toFixed(0)}%</b></div><div class=\"grail-guardrail\"><small>MIN NET MARGIN</small><b>${Number(g.minimumNetMargin||0).toFixed(0)}%</b></div><div class=\"grail-guardrail\"><small>MIN CONFIDENCE</small><b>${pct(g.minimumConfidence)}</b></div></div>"
new="<div class=\"grail-guardrails\"><div class=\"grail-guardrail\"><small>DISCOVERY FLOOR</small><b>${DISCOVERY_CONFIG.floorRoi}% ROI</b></div><div class=\"grail-guardrail\"><small>PREFERRED BUY</small><b>${DISCOVERY_CONFIG.preferredRoi}%+ ROI</b></div><div class=\"grail-guardrail\"><small>MIN CONFIDENCE</small><b>${pct(g.minimumConfidence)}</b></div></div>"
if old not in s: raise SystemExit('Grail guardrail markup missing')
s=s.replace(old,new,1)
s=s.replace("Manual search remains the diagnostic route. Daily Sheet v1 scans a configured discovery universe, deduplicates live listings, applies the same hardened identity/condition/economics rules, and saves the resulting snapshot locally for 24 hours.","Daily Sheet scans the configured market universe and refreshes every 24 hours. Manual search remains available for targeted checks.",1)
p.write_text(s)

# 3. Graded copy cleanup only.
p=Path('graded-integration.js'); s=p.read_text()
s=s.replace("Stored as USER_CONFIRMED, not machine verified.","Your selection is saved as a manual grader confirmation.")
s=s.replace("'ACE · ASSUMED'","'ACE · NEEDS CONFIRMATION'")
p.write_text(s)

# 4. Inject consolidation assets and cache-bust relevant UI assets.
p=Path('index.html'); s=p.read_text()
if 'ui-consolidation.css' not in s:
    s=s.replace('<link href="gengrail-theme.css" rel="stylesheet"/>','<link href="gengrail-theme.css" rel="stylesheet"/>\n<link href="ui-consolidation.css?v=24.0.0" rel="stylesheet" data-gengrail-ui-consolidation="1"/>',1)
if 'ui-consolidation.js' not in s:
    s=s.replace('</body></html>','<script src="ui-consolidation.js?v=24.0.0" data-gengrail-ui-consolidation="1"></script>\n</body></html>',1)
for asset in ('grail-hub.js','graded-integration.js'):
    pat=r'('+re.escape(asset)+r')(?:\?v=[^"\']+)?'
    s,n=re.subn(pat,lambda m:m.group(1)+'?v=24.0.0',s)
    if n<1: raise SystemExit('Asset ref missing: '+asset)
p.write_text(s)

# 5. Service worker cache.
p=Path('sw.js'); s=p.read_text()
s,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v24.0.0-ui-consolidation';",s,count=1)
if n!=1: raise SystemExit('SW cache anchor missing')
if "'./ui-consolidation.css'" not in s:
    s=s.replace("'./grail-hub.js'","'./grail-hub.js','./ui-consolidation.css','./ui-consolidation.js'")
p.write_text(s)

checks={
 'ui-consolidation.css':['GENGRAIL UI CONSOLIDATION','--gengrail-visible-height','#stock #startCameraIntake','.grail-action-grid'],
 'ui-consolidation.js':['visualViewport','PHOTO LIBRARY','ui-settings-clean','REVIEW'],
 'grail-hub.js':['DISCOVERY FLOOR','PREFERRED BUY','REVIEW · CONDITION UNKNOWN','Daily Sheet scans the configured market universe'],
 'graded-integration.js':['manual grader confirmation','NEEDS CONFIRMATION'],
 'index.html':['ui-consolidation.css?v=24.0.0','ui-consolidation.js?v=24.0.0','grail-hub.js?v=24.0.0','graded-integration.js?v=24.0.0'],
 'sw.js':['gengrail-log-v24.0.0-ui-consolidation','ui-consolidation.js']
}
for f, needles in checks.items():
    text=Path(f).read_text()
    for needle in needles:
        if needle not in text: raise SystemExit(f'Safety stop: {needle!r} missing from {f}')
