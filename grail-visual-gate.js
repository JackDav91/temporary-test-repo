/* GENGRAIL GRAIL HUB v1.12 — structured eBay identity + visual verification gate
   Identity hierarchy:
   1) eBay structured product metadata / ePID when present
   2) Gengrail visual recognition
   3) seller title only as fallback context

   Fail closed: contradictory or unresolved collision-prone printings do not enter
   peer pricing, ROI, ranking or Grail Plan economics.
*/
(function(){
'use strict';
if(window.__gengrailVisualGateInstalled)return;
window.__gengrailVisualGateInstalled=true;

const nativeFetch=window.fetch.bind(window);
const AI_BACKEND='https://gengrail-card-ai.gengrailtcg.workers.dev';
const EBAY_SEARCH_PATH='/api/ebay/opportunities/search';
const CACHE_KEY='gengrail_grail_identity_gate_v112';
const CACHE_TTL=24*60*60*1000;
const CONCURRENCY=3;
const MAX_IMAGE_BYTES=5_500_000;
const CONTRACT=Object.freeze({scope:'pokemon_raw_single',recognitionVersion:4,requestedFields:['cardName','cardNumber','language','setName','setCode','rarity','illustrator'],requireFieldConfidence:true,requireCanonicalIdentity:true,requirePrintingIdentity:true});
const CANONICAL=Object.freeze({'2/102':'blastoise','4/102':'charizard','15/102':'venusaur','58/102':'pikachu','9/111':'lugia','13/75':'umbreon'});
const COLLISION=new Set(['2/102','4/102','15/102']);

/* Confirmed eBay catalogue identities. These are authoritative overrides when the
   Browse search result exposes an ePID. Extend this map only from verified eBay
   Product Details, never from seller title text. */
const EPID_IDENTITY=Object.freeze({
 '26052763408':{cardName:'Venusaur',cardNumber:'15/102',family:'CELEBRATIONS',setName:'Celebrations: Classic Collection',year:2021}
});

const clean=v=>String(v||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[’']/g,'').replace(/[^a-z0-9/]+/g,' ').replace(/\s+/g,' ').trim();
const cardNumber=v=>{const m=String(v||'').match(/\b(\d{1,4})\s*\/\s*(\d{1,4})\b/);return m?`${Number(m[1])}/${Number(m[2])}`:''};
const titleNumber=t=>cardNumber(t);
const imageUrl=item=>String(item?.image?.imageUrl||item?.thumbnailImages?.[0]?.imageUrl||'');
const itemKey=item=>String(item?.itemId||item?.itemWebUrl||imageUrl(item)||item?.title||'');

function obviousAccessory(title){
 const t=clean(title);
 return /\b(keychain|key chain|keyring|key ring|key fob|fob|pendant|necklace|charm|novelty|magnet|magnetic|sticker|poster|print|art print|frame|framed|display frame|holder|stand|acrylic|case only|empty case|card not included|no card included|without card|replica|reproduction|proxy|custom|fan art|metal card|gold card|bundle|job lot|lot of|multi buy|multibuy)\b/.test(t)||/\bbuy\s*\d+\s*get\s*\d+\s*free\b/.test(t);
}
function expectedFamily(title,n){
 const t=clean(title);
 if(/\b(celebrations|celebration|25th|25 th|25th anniversary|classic collection|pokemon 25|2021)\b/.test(t)&&COLLISION.has(n))return 'CELEBRATIONS';
 if(/\b(evolutions|xy evolutions)\b/.test(t))return 'EVOLUTIONS';
 if(/\b(base set 2|base set ii)\b/.test(t))return 'BASE_SET_2';
 if(/\bneo genesis\b/.test(t))return 'NEO_GENESIS';
 if(/\bneo discovery\b/.test(t))return 'NEO_DISCOVERY';
 if(/\bshadowless\b/.test(t))return 'BASE_SET_SHADOWLESS';
 if(/\b(base set|wotc|wizards of the coast|1999|1998|unlimited|1st edition|first edition)\b/.test(t))return 'BASE_SET';
 return 'UNKNOWN';
}
function familyFromText(v){
 const s=clean(v);
 if(/\bcelebrations\b|classic collection|25th anniversary|pokemon 25/.test(s))return 'CELEBRATIONS';
 if(/\bevolutions\b|xy evolutions/.test(s))return 'EVOLUTIONS';
 if(/base set 2|base set ii/.test(s))return 'BASE_SET_2';
 if(/neo genesis/.test(s))return 'NEO_GENESIS';
 if(/neo discovery/.test(s))return 'NEO_DISCOVERY';
 if(/shadowless/.test(s))return 'BASE_SET_SHADOWLESS';
 if(/\bbase set\b/.test(s))return 'BASE_SET';
 return 'UNKNOWN';
}
function recognisedFamily(card){return familyFromText(`${card?.setName||''} ${card?.setCode||''}`)}
function nameMatches(expected,actual){
 const a=clean(expected),b=clean(actual);
 if(!a||!b)return false;
 if(a===b||a.includes(b)||b.includes(a))return true;
 const A=new Set(a.split(' ')),B=new Set(b.split(' '));let hit=0;for(const x of A)if(B.has(x))hit++;
 return hit/Math.max(A.size,B.size)>=.65;
}

function getEpid(item){
 const direct=[item?.epid,item?.ePID,item?.productId,item?.product?.epid,item?.product?.ePID,item?.product?.productId];
 for(const v of direct){const s=String(v||'').trim();if(/^\d{6,}$/.test(s))return s}
 return '';
}
function aspectPairs(item){
 const out=[];
 const push=(name,value)=>{const n=String(name||'').trim();if(!n)return;for(const v of (Array.isArray(value)?value:[value])){const s=String(v?.value??v?.localizedValue??v||'').trim();if(s)out.push([n,s])}};
 const arrays=[item?.localizedAspects,item?.aspects,item?.itemSpecifics,item?.product?.localizedAspects,item?.product?.aspects,item?.productDetails?.localizedAspects,item?.productDetails?.aspects];
 for(const src of arrays){
  if(Array.isArray(src)){for(const a of src){push(a?.name??a?.localizedAspectName??a?.aspectName,a?.value??a?.localizedValue??a?.values)}}
  else if(src&&typeof src==='object'){for(const [k,v] of Object.entries(src))push(k,v)}
 }
 return out;
}
function structuredIdentity(item){
 const epid=getEpid(item),known=EPID_IDENTITY[epid];
 if(known)return {...known,epid,source:'EPID_VERIFIED',confidence:1};
 const pairs=aspectPairs(item),get=(...names)=>{
  const wanted=names.map(clean);
  const row=pairs.find(([k])=>wanted.includes(clean(k)));
  return row?row[1]:'';
 };
 const setName=get('Set','Card Set','Series','Expansion'),number=cardNumber(get('Card Number','Collector Number','Card No','Number')),cardName=get('Card Name','Character','Pokemon','Pokémon'),language=get('Language'),rarity=get('Rarity'),year=Number((get('Year Manufactured','Year','Release Year').match(/\b(19|20)\d{2}\b/)||[])[0]||0),family=familyFromText(setName);
 const productType=get('Type','Product Type','Card Type','Item Type');
 const evidence=Boolean(setName||number||cardName||language||rarity||year||productType);
 return {source:evidence?'EBAY_ASPECTS':'NONE',epid,setName,cardNumber:number,cardName,language,rarity,year,productType,family,evidence,pairs};
}
function structuredReject(item){
 const meta=structuredIdentity(item),title=String(item?.title||''),n=titleNumber(title),expectedName=CANONICAL[n]||'';
 if(meta.source==='NONE')return {pass:null,meta,reason:'structured_unavailable'};
 const pt=clean(meta.productType);
 if(/keychain|key ring|keyring|charm|pendant|necklace|accessory|sticker|magnet|frame|holder|stand|case/.test(pt))return {pass:false,meta,reason:'structured_non_card_product'};
 if(meta.cardNumber&&n&&meta.cardNumber!==n)return {pass:false,meta,reason:'structured_collector_number_conflict'};
 if(meta.cardName&&expectedName&&!nameMatches(expectedName,meta.cardName))return {pass:false,meta,reason:'structured_card_name_conflict'};
 if(COLLISION.has(n)){
  if(meta.family==='CELEBRATIONS')return {pass:false,meta,reason:'structured_celebrations_collision'};
  if(meta.family==='EVOLUTIONS'||meta.family==='BASE_SET_2')return {pass:false,meta,reason:'structured_printing_conflict'};
  if(meta.year>=2002&&meta.family!=='BASE_SET'&&meta.family!=='BASE_SET_SHADOWLESS')return {pass:false,meta,reason:'structured_modern_printing_conflict'};
 }
 return {pass:true,meta,reason:'structured_checked'};
}

function readCache(){try{return JSON.parse(localStorage.getItem(CACHE_KEY)||'{}')||{}}catch{return {}}}
function writeCache(cache){try{localStorage.setItem(CACHE_KEY,JSON.stringify(cache))}catch{}}
function cached(cache,key,img){const row=cache[key];if(!row||row.image!==img||Date.now()-Number(row.at||0)>CACHE_TTL)return null;return row}
function blobToDataUrl(blob){return new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(String(r.result||''));r.onerror=()=>reject(new Error('image_read_failed'));r.readAsDataURL(blob)})}
async function imageToDataUrl(url){
 if(!url)throw new Error('image_missing');
 const res=await nativeFetch(url,{method:'GET',mode:'cors',credentials:'omit',cache:'force-cache'});
 if(!res.ok)throw new Error(`image_http_${res.status}`);
 const blob=await res.blob();
 if(!/^image\//i.test(blob.type||''))throw new Error('image_type_invalid');
 if(blob.size>MAX_IMAGE_BYTES)throw new Error('image_too_large');
 return blobToDataUrl(blob);
}
async function recognise(dataUrl){
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),22000);
 try{
  const res=await nativeFetch(AI_BACKEND+'/api/recognise-card',{method:'POST',mode:'cors',credentials:'omit',cache:'no-store',signal:controller.signal,headers:{'content-type':'text/plain;charset=UTF-8','accept':'application/json'},body:JSON.stringify({...CONTRACT,image:dataUrl})});
  const data=await res.json().catch(()=>null);
  if(!res.ok||!data?.ok)return {ok:false,reason:data?.error||`ai_http_${res.status}`};
  return {ok:true,data};
 }catch(e){return {ok:false,reason:e?.name==='AbortError'?'ai_timeout':String(e?.message||e)}}finally{clearTimeout(timer)}
}
function evaluate(item,recognition,structured){
 const title=String(item?.title||''),n=titleNumber(title),expectedName=CANONICAL[n]||'',titleFamily=expectedFamily(title,n),card=recognition?.data?.card||{},meta=structured?.meta||structuredIdentity(item);
 if(structured?.pass===false)return {pass:false,reason:structured.reason,structured:meta};
 if(!recognition?.ok)return {pass:false,reason:recognition?.reason||'visual_unverified',structured:meta};
 if(!recognition.data?.identified||recognition.data?.supported===false||!card?.cardName)return {pass:false,reason:'visual_not_single_card',structured:meta};
 const seenNumber=cardNumber(card?.cardNumber);
 if(n&&seenNumber!==n)return {pass:false,reason:'visual_collector_number_conflict',seenNumber,structured:meta};
 if(expectedName&&!nameMatches(expectedName,card?.cardName))return {pass:false,reason:'visual_card_name_conflict',seenName:String(card?.cardName||''),structured:meta};
 const seenFamily=recognisedFamily(card),authoritativeFamily=meta?.family&&meta.family!=='UNKNOWN'?meta.family:'UNKNOWN';
 if(COLLISION.has(n)){
  if(authoritativeFamily==='CELEBRATIONS')return {pass:false,reason:'structured_celebrations_collision',seenFamily,structured:meta};
  if(authoritativeFamily==='EVOLUTIONS'||authoritativeFamily==='BASE_SET_2')return {pass:false,reason:'structured_printing_conflict',seenFamily,structured:meta};
  if(titleFamily==='BASE_SET'&&seenFamily!=='BASE_SET'&&seenFamily!=='BASE_SET_SHADOWLESS')return {pass:false,reason:seenFamily==='CELEBRATIONS'?'visual_celebrations_collision':'visual_printing_conflict',seenFamily,structured:meta};
 }
 if(titleFamily==='NEO_GENESIS'&&seenFamily!=='NEO_GENESIS')return {pass:false,reason:'visual_printing_conflict',seenFamily,structured:meta};
 if(titleFamily==='NEO_DISCOVERY'&&seenFamily!=='NEO_DISCOVERY')return {pass:false,reason:'visual_printing_conflict',seenFamily,structured:meta};
 if(titleFamily==='BASE_SET_SHADOWLESS'&&seenFamily!=='BASE_SET_SHADOWLESS'&&seenFamily!=='BASE_SET')return {pass:false,reason:'visual_printing_conflict',seenFamily,structured:meta};
 return {pass:true,reason:meta?.source&&meta.source!=='NONE'?'structured_visual_verified':'visual_verified',seenNumber,seenName:String(card?.cardName||''),seenSet:String(card?.setName||''),confidence:Number(card?.confidence||recognition.data?.confidence||0),structured:meta};
}
async function verifyOne(item,cache){
 const title=String(item?.title||''),img=imageUrl(item),key=itemKey(item),structured=structuredReject(item);
 if(obviousAccessory(title))return {item,pass:false,reason:'accessory_title',structured:structured.meta};
 if(structured.pass===false)return {item,pass:false,reason:structured.reason,structured:structured.meta};
 if(/\b(psa|bgs|beckett|cgc|ace|sgc)\s*(?:grade\s*)?(10|[1-9](?:\.5)?)\b/i.test(title))return {item,pass:true,reason:'graded_title_deferred',structured:structured.meta};
 const cacheId=`${key}|${getEpid(item)}|${structured.meta?.setName||''}|${structured.meta?.cardNumber||''}`;
 const old=cached(cache,cacheId,img);if(old)return {item,...old};
 let verdict;
 try{const dataUrl=await imageToDataUrl(img);verdict=evaluate(item,await recognise(dataUrl),structured)}
 catch(e){verdict={pass:false,reason:String(e?.message||e||'visual_unverified'),structured:structured.meta}}
 cache[cacheId]={...verdict,image:img,at:Date.now()};
 return {item,...verdict};
}
async function mapLimit(items,limit,fn){
 const out=new Array(items.length);let next=0;
 async function worker(){while(true){const i=next++;if(i>=items.length)return;out[i]=await fn(items[i],i)}}
 await Promise.all(Array.from({length:Math.min(limit,items.length)},worker));return out;
}
async function verifyItems(items){
 const list=Array.isArray(items)?items:[],cache=readCache();
 const results=await mapLimit(list,CONCURRENCY,item=>verifyOne(item,cache));writeCache(cache);
 const passed=results.filter(x=>x?.pass).map(x=>{if(x.structured?.source&&x.structured.source!=='NONE')x.item.__gengrailStructuredIdentity=x.structured;return x.item});
 const rejected=results.filter(x=>x&&!x.pass);
 window.__gengrailVisualGateLast={at:new Date().toISOString(),version:'1.12',input:list.length,passed:passed.length,rejected:rejected.length,reasons:rejected.reduce((a,x)=>(a[x.reason]=(a[x.reason]||0)+1,a),{}),structuredHits:results.filter(x=>x?.structured?.source&&x.structured.source!=='NONE').length};
 console.info('[Gengrail Grail Hub] identity gate',window.__gengrailVisualGateLast);
 return passed;
}

window.fetch=async function(input,init){
 const url=typeof input==='string'?input:String(input?.url||'');
 const response=await nativeFetch(input,init);
 if(!url.includes(EBAY_SEARCH_PATH)||!response.ok)return response;
 try{
  const data=await response.clone().json();
  if(!data?.ok||!Array.isArray(data.itemSummaries))return response;
  const verified=await verifyItems(data.itemSummaries);
  const body=JSON.stringify({...data,itemSummaries:verified,identityGate:{version:'1.12',input:data.itemSummaries.length,passed:verified.length,rejected:data.itemSummaries.length-verified.length,diagnostic:window.__gengrailVisualGateLast}});
  const headers=new Headers(response.headers);headers.set('content-type','application/json;charset=UTF-8');headers.set('cache-control','no-store');
  return new Response(body,{status:response.status,statusText:response.statusText,headers});
 }catch(e){
  console.warn('[Gengrail Grail Hub] identity gate failed closed',e);
  try{
   const data=await response.clone().json();
   if(data?.ok&&Array.isArray(data.itemSummaries)){
    const headers=new Headers(response.headers);headers.set('content-type','application/json;charset=UTF-8');headers.set('cache-control','no-store');
    return new Response(JSON.stringify({...data,itemSummaries:[],identityGate:{version:'1.12',input:data.itemSummaries.length,passed:0,rejected:data.itemSummaries.length,error:String(e?.message||e)}}),{status:response.status,statusText:response.statusText,headers});
   }
  }catch{}
  return response;
 }
};

window.GengrailVisualGate={version:'1.12',verifyItems,structuredIdentity,clearCache(){try{localStorage.removeItem(CACHE_KEY);localStorage.removeItem('gengrail_grail_visual_gate_v111')}catch{}},last:()=>window.__gengrailVisualGateLast||null};
})();
