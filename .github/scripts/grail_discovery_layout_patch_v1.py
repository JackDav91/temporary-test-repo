from pathlib import Path

p=Path('grail-hub.js')
s=p.read_text()
if 'GENGRAIL GRAIL HUB v1.5' not in s:
    raise SystemExit('Safety stop: expected Grail Hub v1.5 source')

s=s.replace('GENGRAIL GRAIL HUB v1.5 — Opportunity Stream v1.2 condition gate','GENGRAIL GRAIL HUB v1.6 — daily discovery foundation + layout restore',1)

old="let streamState={query:'Pokemon TCG card',rows:[],safe:[],lastPlan:null,loading:false,error:''};"
new="""const DAILY_SHEET_KEY='gengrail_grail_daily_sheet_v1';
const DISCOVERY_CONFIG=Object.freeze({
  version:1,
  refreshHours:24,
  lanes:['Pokemon TCG Charizard','Pokemon TCG Pikachu','Pokemon TCG Umbreon','Pokemon TCG Lugia','Pokemon TCG Eevee','Pokemon TCG PSA']
});
let streamState={query:'Pokemon TCG card',rows:[],safe:[],lastPlan:null,loading:false,error:'',discoveryLoading:false,dailySheet:null};
let layoutLock=null;"""
if old not in s: raise SystemExit('streamState anchor not found')
s=s.replace(old,new,1)

anchor="function state(){try{return typeof window.getGrailPlanState==='function'?window.getGrailPlanState():null}catch{return null}}"
insert=anchor+"""
function loadDailySheet(){try{return JSON.parse(localStorage.getItem(DAILY_SHEET_KEY)||'null')}catch{return null}}
function saveDailySheet(sheet){try{localStorage.setItem(DAILY_SHEET_KEY,JSON.stringify(sheet))}catch{}streamState.dailySheet=sheet;return sheet}
function sheetAgeText(sheet){if(!sheet?.generatedAt)return 'No daily sheet built yet.';const generated=new Date(sheet.generatedAt),due=new Date(sheet.refreshDue);return `Built ${generated.toLocaleString('en-GB',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'})} · refresh due ${due.toLocaleString('en-GB',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'})}`}
function restoreLayout(){
  const y=layoutLock?.scrollY??window.scrollY;
  document.documentElement.classList.remove('grail-hub-open');document.body.classList.remove('grail-hub-open');
  document.documentElement.style.overflow=layoutLock?.htmlOverflow||'';document.documentElement.style.overflowX=layoutLock?.htmlOverflowX||'';
  document.body.style.overflow=layoutLock?.bodyOverflow||'';document.body.style.overflowX=layoutLock?.bodyOverflowX||'';document.body.style.width=layoutLock?.bodyWidth||'';document.body.style.position=layoutLock?.bodyPosition||'';
  document.documentElement.scrollLeft=0;document.body.scrollLeft=0;const root=document.getElementById('grailHubOverlay');if(root)root.scrollLeft=0;
  layoutLock=null;requestAnimationFrame(()=>window.scrollTo(0,y));
}
function lockLayout(){
  if(layoutLock)return;
  layoutLock={scrollY:window.scrollY,htmlOverflow:document.documentElement.style.overflow,htmlOverflowX:document.documentElement.style.overflowX,bodyOverflow:document.body.style.overflow,bodyOverflowX:document.body.style.overflowX,bodyWidth:document.body.style.width,bodyPosition:document.body.style.position};
  document.documentElement.classList.add('grail-hub-open');document.body.classList.add('grail-hub-open');
  document.documentElement.style.overflow='hidden';document.documentElement.style.overflowX='hidden';document.body.style.overflow='hidden';document.body.style.overflowX='hidden';document.body.style.width='100%';
}
"""
if anchor not in s: raise SystemExit('state anchor not found')
s=s.replace(anchor,insert,1)

old="""  root.querySelector('.grail-hub-shell').innerHTML=`<div class=\"grail-hub-head\"><button class=\"grail-hub-back\" type=\"button\" id=\"grailStreamBack\">←</button><div><div class=\"grail-hub-title\">OPPORTUNITY STREAM</div><div class=\"grail-hub-sub\">Live eBay candidates ranked for ${esc(g.mode)} mode</div></div></div><div class=\"grail-stream-toolbar\"><label for=\"grailStreamQuery\">CURRENT EBAY SEARCH</label><div class=\"grail-stream-search\"><input id=\"grailStreamQuery\" value=\"${esc(streamState.query)}\" placeholder=\"e.g. Pokemon Charizard 4/102\"><button id=\"grailStreamScan\" type=\"button\">${streamState.loading?'SCANNING…':'SCAN LIVE'}</button></div><div class=\"grail-stream-hint\">Use a specific Pokémon, collector number or slab search for the strongest peer matching. Ambiguous listings are rejected automatically.</div></div>"""
new="""  const sheet=streamState.dailySheet||loadDailySheet();streamState.dailySheet=sheet;
  root.querySelector('.grail-hub-shell').innerHTML=`<div class=\"grail-hub-head\"><button class=\"grail-hub-back\" type=\"button\" id=\"grailStreamBack\">←</button><div><div class=\"grail-hub-title\">OPPORTUNITY STREAM</div><div class=\"grail-hub-sub\">Live eBay candidates ranked for ${esc(g.mode)} mode</div></div></div><div class=\"grail-stream-toolbar\"><label for=\"grailStreamQuery\">CURRENT EBAY SEARCH</label><div class=\"grail-stream-search\"><input id=\"grailStreamQuery\" value=\"${esc(streamState.query)}\" placeholder=\"e.g. Pokemon Charizard 4/102\"><button id=\"grailStreamScan\" type=\"button\">${streamState.loading?'SCANNING…':'SCAN LIVE'}</button></div><div class=\"grail-discovery-row\"><button id=\"grailDailyBuild\" type=\"button\">${streamState.discoveryLoading?'BUILDING DAILY SHEET…':'BUILD DAILY SHEET'}</button><span>${esc(sheetAgeText(sheet))}</span></div><div class=\"grail-stream-hint\">Manual search remains the diagnostic route. Daily Sheet v1 scans a configured discovery universe, deduplicates live listings, applies the same hardened identity/condition/economics rules, and saves the resulting snapshot locally for 24 hours.</div></div>"""
if old not in s: raise SystemExit('stream toolbar anchor not found')
s=s.replace(old,new,1)

old="  root.querySelector('#grailStreamScan').onclick=scanStream;"
new="  root.querySelector('#grailStreamScan').onclick=scanStream;\n  root.querySelector('#grailDailyBuild').onclick=buildDailySheet;"
if old not in s: raise SystemExit('scan bind anchor not found')
s=s.replace(old,new,1)

anchor="""async function scanStream(){
  const g=state(),input=document.getElementById('grailStreamQuery');if(!g||!input)return;const q=input.value.trim();if(!q)return alert('Enter an eBay search first.');"""
if anchor not in s: raise SystemExit('scanStream anchor not found')
# insert build function before scanStream
build="""async function buildDailySheet(){
  const g=state();if(!g||streamState.discoveryLoading)return;
  streamState.discoveryLoading=true;streamState.error='';renderStream();
  try{
    const maxPrice=Math.max(1,num(g.availableGrailPlanLiquidity)),all=[],seen=new Set();
    for(const q of DISCOVERY_CONFIG.lanes){
      const u=new URL(EBAY_BACKEND+'/api/ebay/opportunities/search');u.searchParams.set('q',q);u.searchParams.set('limit','100');u.searchParams.set('max_price',String(maxPrice));
      const res=await fetch(u,{method:'GET',mode:'cors',credentials:'omit',cache:'no-store',headers:{accept:'application/json'}});const d=await res.json().catch(()=>null);
      if(!res.ok||!d?.ok)continue;
      for(const item of (Array.isArray(d.itemSummaries)?d.itemSummaries:[])){const id=String(item?.itemId||item?.itemWebUrl||'');if(!id||seen.has(id))continue;seen.add(id);all.push(item)}
    }
    const rows=rankListings(all,g),plan=buildBasket(rows,g),now=Date.now(),sheet={schema:1,configVersion:DISCOVERY_CONFIG.version,generatedAt:new Date(now).toISOString(),refreshDue:new Date(now+DISCOVERY_CONFIG.refreshHours*3600000).toISOString(),mode:g.mode,targetRange:g.targetRange,deployableLiquidity:num(g.availableGrailPlanLiquidity),lanes:[...DISCOVERY_CONFIG.lanes],listingCount:all.length,rankedCount:rows.length,qualityCount:rows.filter(x=>x.qualityPass).length,safeCount:rows.filter(x=>x.safe).length,plan:{status:plan.status,cost:plan.cost,profit:plan.profit,chosen:plan.chosen.map(x=>({id:x.id,title:x.title,url:x.url,landed:x.landed,profit:x.profit,roi:x.roi,margin:x.margin,confidence:x.confidence,type:x.type,cardNumber:x.cardNumber,grader:x.grader,grade:x.grade,condition:x.condition,printingFamily:x.printingFamily}))},rows:rows.slice(0,40)};
    saveDailySheet(sheet);streamState.rows=rows;streamState.safe=rows.filter(x=>x.safe);streamState.lastPlan=plan;streamState.query='DAILY DISCOVERY';
  }catch(e){streamState.error=String(e?.message||e||'Daily discovery failed.');}
  finally{streamState.discoveryLoading=false;renderStream()}
}
"""
s=s.replace(anchor,build+anchor,1)

old="function open(){let root=document.getElementById('grailHubOverlay');if(!root){root=document.createElement('div');root.id='grailHubOverlay';root.className='grail-hub-overlay';root.innerHTML='<div class=\"grail-hub-shell\"></div>';document.body.appendChild(root)}root.hidden=false;document.body.style.overflow='hidden';render()}\nfunction close(){const root=document.getElementById('grailHubOverlay');if(root)root.hidden=true;document.body.style.overflow=''}"
new="function open(){let root=document.getElementById('grailHubOverlay');if(!root){root=document.createElement('div');root.id='grailHubOverlay';root.className='grail-hub-overlay';root.innerHTML='<div class=\"grail-hub-shell\"></div>';document.body.appendChild(root)}lockLayout();root.hidden=false;root.scrollLeft=0;root.scrollTop=0;render()}\nfunction close(){const root=document.getElementById('grailHubOverlay');if(root){root.hidden=true;root.scrollLeft=0}restoreLayout()}"
if old not in s: raise SystemExit('open/close anchor not found')
s=s.replace(old,new,1)

old="window.GengrailGrailHub={open,close,render,renderStream,scanStream,getOpportunityState:()=>JSON.parse(JSON.stringify(streamState))};"
new="window.GengrailGrailHub={open,close,render,renderStream,scanStream,buildDailySheet,getOpportunityState:()=>JSON.parse(JSON.stringify(streamState)),getDailySheet:()=>loadDailySheet()};"
if old not in s: raise SystemExit('export anchor not found')
s=s.replace(old,new,1)

p.write_text(s)
