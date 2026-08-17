from pathlib import Path
import re

# Buying / Grail Hub UI cleanup only. No ranking, pricing, retrieval or persistence logic changes.

p=Path('grail-hub.js')
s=p.read_text()
if 'GENGRAIL GRAIL HUB v1.6' not in s:
    raise SystemExit('Safety stop: expected Grail Hub v1.6')

# Shorter hero copy.
s=s.replace("What is the smallest sensible combination of purchases that can move Gengrail toward today's profit target?","Build today’s smallest sensible route to projected profit.")

# Replace stale generic minimum ROI presentation with the actual discovery/preference language.
old="<div class=\"grail-guardrails\"><div class=\"grail-guardrail\"><small>MIN ROI</small><b>${Number(g.minimumROI||0).toFixed(0)}%</b></div><div class=\"grail-guardrail\"><small>MIN NET MARGIN</small><b>${Number(g.minimumNetMargin||0).toFixed(0)}%</b></div><div class=\"grail-guardrail\"><small>MIN CONFIDENCE</small><b>${pct(g.minimumConfidence)}</b></div></div>"
new="<div class=\"grail-guardrails\"><div class=\"grail-guardrail\"><small>DISCOVERY FLOOR</small><b>${DISCOVERY_CONFIG.floorRoi}% ROI</b></div><div class=\"grail-guardrail\"><small>PREFERRED BUY</small><b>${DISCOVERY_CONFIG.preferredRoi}%+ ROI</b></div><div class=\"grail-guardrail\"><small>MIN CONFIDENCE</small><b>${pct(g.minimumConfidence)}</b></div></div>"
if old in s:
    s=s.replace(old,new,1)
elif 'DISCOVERY FLOOR' not in s:
    raise SystemExit('Safety stop: guardrail markup not found')

# Compress permanent diagnostic prose.
s=s.replace("Manual search remains the diagnostic route. Daily Sheet v1 scans a configured discovery universe, deduplicates live listings, applies the same hardened identity/condition/economics rules, and saves the resulting snapshot locally for 24 hours.","Daily Sheet scans the configured market universe and refreshes every 24 hours. Manual search remains available for targeted checks.")

# Explain review reason directly on cards.
s=s.replace("${a.safe?'PLAN CANDIDATE':'REVIEW'}","${a.safe?'PLAN CANDIDATE':(a.type==='RAW'&&a.condition==='UNKNOWN'?'REVIEW · CONDITION UNKNOWN':'REVIEW')}")
p.write_text(s)

p=Path('grail-hub.css')
s=p.read_text()
if 'GENGRAIL GRAIL HUB v1.4' not in s:
    raise SystemExit('Safety stop: expected Grail Hub CSS baseline')

marker=r'''

/* BUYING UI REVIEW v1.7 — compact decision-first hierarchy. Presentation only. */
.grail-plan-hero{padding:12px!important}
.grail-plan-question{font-size:21px!important;line-height:1!important;margin-top:7px!important}
.grail-plan-copy{font-size:10px!important;line-height:1.32!important;margin-top:6px!important}
.grail-plan-target{margin-top:9px!important}
.grail-guardrails{margin-top:7px!important}
.grail-hub-section{margin-top:10px!important}
.grail-hub-section-title{margin-bottom:6px!important}

/* Three real destinations; refresh is a utility, not a fourth destination. */
.grail-action-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:7px!important}
.grail-hub-overlay .grail-action-card{min-height:102px!important;padding:10px 28px 9px 10px!important}
.grail-hub-overlay .grail-action-card b{font-size:16px!important}
.grail-hub-overlay .grail-action-card span{font-size:8.5px!important;line-height:1.22!important}
.grail-action-icon{margin-bottom:5px!important}
#grailRefreshAction{display:none!important}
.grail-hub-head .grail-refresh-mini{margin-left:auto!important;width:38px!important;height:38px!important;border-radius:999px!important;border:1px solid #3b3b3b!important;background:#171717!important;color:#ddd!important;font-size:20px!important;font-weight:900!important;padding:0!important}

/* Opportunity Stream: compact controls, then plan/results. */
.grail-stream-toolbar{padding:10px!important}
.grail-stream-toolbar label{margin-bottom:4px!important;font-size:8px!important}
.grail-stream-search input{padding:9px!important;font-size:15px!important}
.grail-stream-search button{padding:0 12px!important}
.grail-discovery-row{margin-top:6px!important}
.grail-stream-hint{font-size:8.5px!important;line-height:1.3!important;margin-top:5px!important}
.grail-stream-summary{display:flex!important;gap:6px!important;overflow-x:auto!important;margin-top:8px!important;padding-bottom:1px!important}
.grail-stream-summary>div{flex:1 0 auto!important;min-width:104px!important;padding:7px 9px!important}
.grail-stream-summary small{font-size:6.5px!important}.grail-stream-summary b{font-size:12px!important}
.grail-stream-state{margin-top:8px!important;padding:8px 10px!important;font-size:9.5px!important}
.grail-plan-preview{margin-top:9px!important;padding:10px!important}
.grail-plan-preview h3{font-size:19px!important;margin:5px 0 3px!important}
.grail-plan-preview p{font-size:9px!important}
.grail-stream-results{margin-top:8px!important}
.grail-opportunity{padding:10px!important}
.grail-opportunity-reason{font-size:8px!important}

@media(max-width:620px){
  .grail-action-grid{grid-template-columns:1fr 1fr!important}
  .grail-action-card.primary{grid-column:1/-1!important}
  .grail-plan-question{font-size:20px!important}
}
'''
if 'BUYING UI REVIEW v1.7' not in s:
    s+=marker
p.write_text(s)

# Tiny utility button added safely by JS markup hook, no runtime-wide mutation observer.
p=Path('grail-hub.js')
s=p.read_text()
anchor="<div class=\"grail-hub-head\">"
if anchor in s and 'grail-refresh-mini' not in s:
    s=s.replace(anchor,anchor,1)  # preserve markup; button injected in open() below if anchor not directly suitable

# Inject a local helper and call only inside Grail Hub open lifecycle.
helper="""
function ensureMiniRefresh(root){
  const head=root?.querySelector('.grail-hub-head');
  if(!head||head.querySelector('.grail-refresh-mini'))return;
  const source=root.querySelector('#grailRefreshAction');
  if(!source)return;
  const b=document.createElement('button');b.type='button';b.className='grail-refresh-mini';b.textContent='↻';b.setAttribute('aria-label','Refresh plan state');b.addEventListener('click',()=>source.click());head.appendChild(b);
}
"""
if 'function ensureMiniRefresh' not in s:
    insert_at=s.find('function statusCopy')
    if insert_at<0: raise SystemExit('Safety stop: helper insertion anchor missing')
    s=s[:insert_at]+helper+s[insert_at:]

# Add call after render/open where overlay exists; use a conservative replacement on render calls.
if 'ensureMiniRefresh(root);' not in s:
    candidates=['root.innerHTML=','render(root']
    # safest: append after any function that obtains grailHubOverlay in open path using setTimeout fallback
    open_anchor="lockLayout();"
    if open_anchor not in s: raise SystemExit('Safety stop: open lifecycle anchor missing')
    s=s.replace(open_anchor,open_anchor+"setTimeout(()=>{const root=document.getElementById('grailHubOverlay');if(root)ensureMiniRefresh(root)},0);",1)
p.write_text(s)

# Cache bust only Grail assets.
p=Path('index.html')
s=p.read_text()
for asset in ('grail-hub.css','grail-hub.js'):
    pat=r'('+re.escape(asset)+r')(?:\?v=[^"\']+)?'
    s,n=re.subn(pat,lambda m:m.group(1)+'?v=23.7.0',s)
    if n<1: raise SystemExit('Safety stop: cache ref missing '+asset)
p.write_text(s)

p=Path('sw.js')
s=p.read_text()
s,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v23.7.0-buying-ui';",s,count=1)
if n!=1: raise SystemExit('Safety stop: SW cache anchor missing')
p.write_text(s)

checks={
 'grail-hub.js':['DISCOVERY FLOOR','PREFERRED BUY','REVIEW · CONDITION UNKNOWN','function ensureMiniRefresh','Daily Sheet scans the configured market universe'],
 'grail-hub.css':['BUYING UI REVIEW v1.7','#grailRefreshAction{display:none','grail-refresh-mini','grail-stream-summary{display:flex'],
 'index.html':['grail-hub.css?v=23.7.0','grail-hub.js?v=23.7.0'],
 'sw.js':['gengrail-log-v23.7.0-buying-ui']
}
for f,needles in checks.items():
    text=Path(f).read_text()
    for n in needles:
        if n not in text: raise SystemExit(f'Safety stop: {n!r} missing from {f}')
