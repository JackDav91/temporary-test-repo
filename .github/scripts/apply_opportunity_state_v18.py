from pathlib import Path
import re

p=Path('grail-hub.js')
s=p.read_text()
if 'GENGRAIL GRAIL HUB v1.6' not in s or 'BUYING UI REVIEW v1.7' not in Path('grail-hub.css').read_text():
    raise SystemExit('Safety stop: expected Buying UI v1.7 baseline')

# Add explicit stream view state. Daily Sheet is the default dataset; manual scans are temporary targeted views.
old="let streamState={query:'Pokemon TCG card',rows:[],safe:[],lastPlan:null,loading:false,error:'',discoveryLoading:false,dailySheet:null};"
new="let streamState={query:'',rows:[],safe:[],lastPlan:null,loading:false,error:'',discoveryLoading:false,dailySheet:null,view:'daily'};"
if old in s:
    s=s.replace(old,new,1)
elif "view:'daily'" not in s:
    raise SystemExit('Safety stop: streamState anchor missing')

# Render from Daily Sheet by default; targeted scans only replace the visible dataset temporarily.
old="""function renderStream(){
  const root=document.getElementById('grailHubOverlay'),g=state();if(!root||!g)return;
  const rows=streamState.rows,safe=rows.filter(x=>x.safe),quality=rows.filter(x=>x.qualityPass),plan=streamState.lastPlan||buildBasket(rows,g);streamState.lastPlan=plan;
  const sheet=streamState.dailySheet||loadDailySheet();streamState.dailySheet=sheet;
"""
new="""function renderStream(){
  const root=document.getElementById('grailHubOverlay'),g=state();if(!root||!g)return;
  const sheet=streamState.dailySheet||loadDailySheet();streamState.dailySheet=sheet;
  const usingDaily=streamState.view!=='targeted'&&!!sheet;
  const rows=usingDaily?(Array.isArray(sheet.rows)?sheet.rows:[]):streamState.rows;
  const safe=rows.filter(x=>x.safe),quality=rows.filter(x=>x.qualityPass),plan=usingDaily?buildBasket(rows,g):(streamState.lastPlan||buildBasket(rows,g));if(!usingDaily)streamState.lastPlan=plan;
"""
if old not in s:
    raise SystemExit('Safety stop: renderStream header anchor missing')
s=s.replace(old,new,1)

# Replace render markup with explicit dataset mode and return-to-daily action.
old_fragment="""<div class=\"grail-stream-toolbar\"><label for=\"grailStreamQuery\">CURRENT EBAY SEARCH</label><div class=\"grail-stream-search\"><input id=\"grailStreamQuery\" value=\"${esc(streamState.query)}\" placeholder=\"e.g. Pokemon Charizard 4/102\"><button id=\"grailStreamScan\" type=\"button\">${streamState.loading?'SCANNING…':'SCAN LIVE'}</button></div><div class=\"grail-discovery-row\"><button id=\"grailDailyBuild\" type=\"button\">${streamState.discoveryLoading?'BUILDING DAILY SHEET…':'BUILD DAILY SHEET'}</button><span>${esc(sheetAgeText(sheet))}</span></div><div class=\"grail-stream-hint\">Daily Sheet scans the configured market universe and refreshes every 24 hours. Manual search remains available for targeted checks.</div></div><div class=\"grail-stream-summary\">"""
new_fragment="""<div class=\"grail-stream-toolbar\"><div class=\"grail-stream-mode ${usingDaily?'daily':'targeted'}\"><b>${usingDaily?'DAILY SHEET':'TARGETED SEARCH RESULTS'}</b>${!usingDaily&&sheet?'<button id=\"grailReturnDaily\" type=\"button\">RETURN TO DAILY SHEET</button>':''}</div><label for=\"grailStreamQuery\">TARGETED EBAY SEARCH</label><div class=\"grail-stream-search\"><input id=\"grailStreamQuery\" value=\"${esc(usingDaily?'':streamState.query)}\" placeholder=\"e.g. Pokemon Charizard 4/102\"><button id=\"grailStreamScan\" type=\"button\">${streamState.loading?'SCANNING…':'SCAN LIVE'}</button></div><div class=\"grail-discovery-row\"><button id=\"grailDailyBuild\" type=\"button\">${streamState.discoveryLoading?'BUILDING DAILY SHEET…':'BUILD DAILY SHEET'}</button><span>${esc(sheetAgeText(sheet))}</span></div><div class=\"grail-stream-hint\">Daily Sheet is the default opportunity set and refreshes every 24 hours. Use targeted search for a temporary card-specific check.</div></div><div class=\"grail-stream-summary\">"""
if old_fragment not in s:
    raise SystemExit('Safety stop: stream toolbar markup anchor missing')
s=s.replace(old_fragment,new_fragment,1)

# Make result heading + empty state reflect the active dataset.
old="""<section class=\"grail-hub-section\"><div class=\"grail-hub-section-title\">RANKED CURRENT LISTINGS</div><div class=\"grail-stream-results\">${rows.length?rows.slice(0,20).map(resultCard).join(''):'<div class=\"grail-stream-empty\">No ranked opportunities yet. Tap SCAN LIVE to search current eBay listings.</div>'}</div></section>`;"""
new="""<section class=\"grail-hub-section\"><div class=\"grail-hub-section-title\">${usingDaily?'DAILY SHEET RANKED LISTINGS':'TARGETED SEARCH RESULTS'}</div><div class=\"grail-stream-results\">${rows.length?rows.slice(0,20).map(resultCard).join(''):`<div class=\"grail-stream-empty\">${usingDaily?'No ranked Daily Sheet opportunities yet. Build the Daily Sheet to scan the configured market universe.':'No ranked opportunities in this targeted search. Try a specific Pokémon, set, or collector number.'}</div>`}</div></section>`;"""
if old not in s:
    raise SystemExit('Safety stop: results heading anchor missing')
s=s.replace(old,new,1)

# Wire return action.
old="""  root.querySelector('#grailStreamScan').onclick=scanStream;
  root.querySelector('#grailDailyBuild').onclick=buildDailySheet;
"""
new="""  root.querySelector('#grailStreamScan').onclick=scanStream;
  root.querySelector('#grailDailyBuild').onclick=buildDailySheet;
  const returnDaily=root.querySelector('#grailReturnDaily');if(returnDaily)returnDaily.onclick=()=>{streamState.view='daily';streamState.error='';streamState.loading=false;renderStream()};
"""
if old not in s: raise SystemExit('Safety stop: stream event anchor missing')
s=s.replace(old,new,1)

# Daily build returns to primary Daily Sheet view.
s=s.replace("saveDailySheet(sheet);streamState.rows=rows;streamState.safe=rows.filter(x=>x.safe);streamState.lastPlan=plan;streamState.query='DAILY DISCOVERY';","saveDailySheet(sheet);streamState.rows=rows;streamState.safe=rows.filter(x=>x.safe);streamState.lastPlan=plan;streamState.query='';streamState.view='daily';",1)

# Targeted scan explicitly switches to temporary targeted view.
s=s.replace("streamState.query=q;streamState.loading=true;streamState.error='';streamState.rows=[];streamState.lastPlan=null;renderStream();","streamState.query=q;streamState.view='targeted';streamState.loading=true;streamState.error='';streamState.rows=[];streamState.lastPlan=null;renderStream();",1)

p.write_text(s)

p=Path('grail-hub.css')
s=p.read_text()
marker=r'''

/* OPPORTUNITY STREAM STATE v1.8 — Daily Sheet first, mobile-contained counters. */
.grail-stream-mode{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px;padding:7px 9px;border-radius:8px;background:#09150d;border:1px solid #294c34;color:#8ce5a5;font-size:8px;letter-spacing:.09em}
.grail-stream-mode.targeted{background:#151107;border-color:#5d4919;color:#e1c96f}
.grail-stream-mode button{margin:0!important;padding:6px 8px!important;border-radius:7px!important;background:#202020!important;color:#eee!important;border:1px solid #444!important;font-size:7.5px!important;font-weight:950!important;white-space:nowrap}
.grail-stream-empty{padding:15px 12px!important;min-height:0!important}
@media(max-width:520px){
  .grail-stream-summary{display:grid!important;grid-template-columns:1fr 1fr!important;gap:7px!important;overflow:visible!important;width:100%!important}
  .grail-stream-summary>div{min-width:0!important;width:auto!important;padding:8px!important}
  .grail-stream-summary b{font-size:13px!important;overflow-wrap:anywhere!important}
  .grail-stream-mode{align-items:center!important}
}
'''
if 'OPPORTUNITY STREAM STATE v1.8' not in s:
    s+=marker
p.write_text(s)

# Cache bust Grail assets only.
p=Path('index.html');s=p.read_text()
for asset in ('grail-hub.css','grail-hub.js'):
    pat=r'('+re.escape(asset)+r')(?:\?v=[^"\']+)?'
    s,n=re.subn(pat,lambda m:m.group(1)+'?v=23.8.0',s)
    if n<1: raise SystemExit('Safety stop: cache ref missing '+asset)
p.write_text(s)

p=Path('sw.js');s=p.read_text();s,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v23.8.0-opportunity-state';",s,count=1)
if n!=1: raise SystemExit('Safety stop: SW cache anchor missing')
p.write_text(s)

checks={
 'grail-hub.js':["view:'daily'",'TARGETED SEARCH RESULTS','RETURN TO DAILY SHEET','DAILY SHEET RANKED LISTINGS',"streamState.view='targeted'"],
 'grail-hub.css':['OPPORTUNITY STREAM STATE v1.8','grid-template-columns:1fr 1fr!important','grail-stream-mode'],
 'index.html':['grail-hub.css?v=23.8.0','grail-hub.js?v=23.8.0'],
 'sw.js':['gengrail-log-v23.8.0-opportunity-state']
}
for f,needles in checks.items():
    text=Path(f).read_text()
    for n in needles:
        if n not in text: raise SystemExit(f'Safety stop: {n!r} missing from {f}')
