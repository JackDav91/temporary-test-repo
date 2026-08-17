/* GENGRAIL GRAIL HUB v1.11 — visual listing identity gate
   Verifies live eBay listing thumbnails with the existing Gengrail card-recognition worker
   before Grail Hub is allowed to price/rank those listings.
   Fail closed: unverified raw-card images do not enter peer pricing or Grail Plan economics.
*/
(function(){
'use strict';
if(window.__gengrailVisualGateInstalled)return;
window.__gengrailVisualGateInstalled=true;

const nativeFetch=window.fetch.bind(window);
const AI_BACKEND='https://gengrail-card-ai.gengrailtcg.workers.dev';
const EBAY_SEARCH_PATH='/api/ebay/opportunities/search';
const CACHE_KEY='gengrail_grail_visual_gate_v111';
const CACHE_TTL=24*60*60*1000;
const CONCURRENCY=3;
const MAX_IMAGE_BYTES=5_500_000;
const CONTRACT=Object.freeze({scope:'pokemon_raw_single',recognitionVersion:4,requestedFields:['cardName','cardNumber','language','setName','setCode','rarity','illustrator'],requireFieldConfidence:true,requireCanonicalIdentity:true});
const CANONICAL=Object.freeze({'2/102':'blastoise','4/102':'charizard','15/102':'venusaur','58/102':'pikachu','9/111':'lugia','13/75':'umbreon'});
const COLLISION=new Set(['2/102','4/102','15/102']);

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
function recognisedFamily(card){
 const s=clean(`${card?.setName||''} ${card?.setCode||''}`);
 if(/\bcelebrations\b|classic collection|25th/.test(s))return 'CELEBRATIONS';
 if(/\bevolutions\b/.test(s))return 'EVOLUTIONS';
 if(/base set 2|base set ii/.test(s))return 'BASE_SET_2';
 if(/neo genesis/.test(s))return 'NEO_GENESIS';
 if(/neo discovery/.test(s))return 'NEO_DISCOVERY';
 if(/shadowless/.test(s))return 'BASE_SET_SHADOWLESS';
 if(/\bbase set\b/.test(s))return 'BASE_SET';
 return 'UNKNOWN';
}
function nameMatches(expected,actual){
 const a=clean(expected),b=clean(actual);
 if(!a||!b)return false;
 if(a===b||a.includes(b)||b.includes(a))return true;
 const A=new Set(a.split(' ')),B=new Set(b.split(' '));let hit=0;for(const x of A)if(B.has(x))hit++;
 return hit/Math.max(A.size,B.size)>=.65;
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
function evaluate(item,recognition){
 const title=String(item?.title||''),n=titleNumber(title),expectedName=CANONICAL[n]||'',expected=expectedFamily(title,n),card=recognition?.data?.card||{};
 if(!recognition?.ok)return {pass:false,reason:recognition?.reason||'visual_unverified'};
 if(!recognition.data?.identified||recognition.data?.supported===false||!card?.cardName)return {pass:false,reason:'visual_not_single_card'};
 const seenNumber=cardNumber(card?.cardNumber);
 if(n&&seenNumber!==n)return {pass:false,reason:'visual_collector_number_conflict',seenNumber};
 if(expectedName&&!nameMatches(expectedName,card?.cardName))return {pass:false,reason:'visual_card_name_conflict',seenName:String(card?.cardName||'')};
 const seenFamily=recognisedFamily(card);
 if(COLLISION.has(n)&&expected==='BASE_SET'&&seenFamily!=='BASE_SET'&&seenFamily!=='BASE_SET_SHADOWLESS')return {pass:false,reason:seenFamily==='CELEBRATIONS'?'visual_celebrations_collision':'visual_printing_conflict',seenFamily};
 if(expected==='NEO_GENESIS'&&seenFamily!=='NEO_GENESIS')return {pass:false,reason:'visual_printing_conflict',seenFamily};
 if(expected==='NEO_DISCOVERY'&&seenFamily!=='NEO_DISCOVERY')return {pass:false,reason:'visual_printing_conflict',seenFamily};
 if(expected==='BASE_SET_SHADOWLESS'&&seenFamily!=='BASE_SET_SHADOWLESS'&&seenFamily!=='BASE_SET')return {pass:false,reason:'visual_printing_conflict',seenFamily};
 return {pass:true,reason:'visual_verified',seenNumber,seenName:String(card?.cardName||''),seenSet:String(card?.setName||''),confidence:Number(card?.confidence||recognition.data?.confidence||0)};
}
async function verifyOne(item,cache){
 const title=String(item?.title||''),img=imageUrl(item),key=itemKey(item);
 if(obviousAccessory(title))return {item,pass:false,reason:'accessory_title'};
 if(/\b(psa|bgs|beckett|cgc|ace|sgc)\s*(?:grade\s*)?(10|[1-9](?:\.5)?)\b/i.test(title))return {item,pass:true,reason:'graded_title_deferred'};
 const old=cached(cache,key,img);if(old)return {item,...old};
 let verdict;
 try{const dataUrl=await imageToDataUrl(img);verdict=evaluate(item,await recognise(dataUrl))}
 catch(e){verdict={pass:false,reason:String(e?.message||e||'visual_unverified')}}
 cache[key]={...verdict,image:img,at:Date.now()};
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
 const passed=results.filter(x=>x?.pass).map(x=>x.item);
 const rejected=results.filter(x=>x&&!x.pass);
 window.__gengrailVisualGateLast={at:new Date().toISOString(),input:list.length,passed:passed.length,rejected:rejected.length,reasons:rejected.reduce((a,x)=>(a[x.reason]=(a[x.reason]||0)+1,a),{})};
 console.info('[Gengrail Grail Hub] visual gate',window.__gengrailVisualGateLast);
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
  const body=JSON.stringify({...data,itemSummaries:verified,visualGate:{version:'1.11',input:data.itemSummaries.length,passed:verified.length,rejected:data.itemSummaries.length-verified.length}});
  const headers=new Headers(response.headers);headers.set('content-type','application/json;charset=UTF-8');headers.set('cache-control','no-store');
  return new Response(body,{status:response.status,statusText:response.statusText,headers});
 }catch(e){
  console.warn('[Gengrail Grail Hub] visual gate failed closed',e);
  try{
   const data=await response.clone().json();
   if(data?.ok&&Array.isArray(data.itemSummaries)){
    const headers=new Headers(response.headers);headers.set('content-type','application/json;charset=UTF-8');headers.set('cache-control','no-store');
    return new Response(JSON.stringify({...data,itemSummaries:[],visualGate:{version:'1.11',input:data.itemSummaries.length,passed:0,rejected:data.itemSummaries.length,error:String(e?.message||e)}}),{status:response.status,statusText:response.statusText,headers});
   }
  }catch{}
  return response;
 }
};

window.GengrailVisualGate={version:'1.11',verifyItems,clearCache(){try{localStorage.removeItem(CACHE_KEY)}catch{}},last:()=>window.__gengrailVisualGateLast||null};
})();
