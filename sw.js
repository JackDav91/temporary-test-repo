const C='gengrail-log-v24.11.11-opportunity-hotfix';
const A=['./','./index.html','./manifest.json','./gengrail-theme.css','./gengrail-ebay.js','./gengrail-profit-engine.js','./profit-engine-diagnostic.js','./home-compact.css','./grail-hub.css','./grail-pre2002-safety.js','./grail-visual-gate.js','./grail-hub.js','./grail-selectable-stream-v1.js','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(A)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 const url=new URL(e.request.url),path=url.pathname;
 if(path.endsWith('/temporary-test-repo/')||path.endsWith('/temporary-test-repo/index.html')||path.endsWith('/index.html')){
  const req=new Request(e.request,{cache:'reload'});
  e.respondWith(fetch(req).then(r=>{const copy=r.clone();caches.open(C).then(c=>c.put(e.request,copy)).catch(()=>{});return r}).catch(()=>caches.match(e.request)));
  return;
 }
 if(path.endsWith('/grail-hub.js')){
  e.respondWith((async()=>{
   try{
    const [safety,gate,hub,selectable]=await Promise.all([
     fetch(new URL('./grail-pre2002-safety.js',self.location.href),{cache:'reload'}),
     fetch(new URL('./grail-visual-gate.js',self.location.href),{cache:'reload'}),
     fetch(new Request(e.request,{cache:'reload'})),
     fetch(new URL('./grail-selectable-stream-v1.js',self.location.href),{cache:'reload'})
    ]);
    if(!safety.ok||!gate.ok||!hub.ok||!selectable.ok)throw new Error('grail_bundle_fetch_failed');
    let selectableBody=await selectable.text();
    selectableBody=selectableBody
      .replace("const PATCH_VERSION='selectable-stream-v1.0.0'","const PATCH_VERSION='selectable-stream-v1.2.1'")
      .replace('unique.slice(0,18)','unique.slice(0,24)')
      .replace("function economics(c,compItems){const comps=compItems.filter(x=>compMatches(c,x)&&String(x?.itemId||'')!==c.id);const prices=comps.map(price).filter(x=>x>0);if(prices.length<3)return null;const med=median(prices),low=percentile(prices,.35),market=(med+low)/2,landed=c.ask+c.ship,outbound=num(localStorage.getItem('gengrailOpp_oppOutbound'))||4.10,pack=num(localStorage.getItem('gengrailOpp_oppPack'))||.30,feeRate=.135,fees=market*feeRate,profit=market-fees-outbound-pack-landed,roi=landed>0?profit/landed*100:0,margin=market>0?profit/market*100:0,confidence=Math.min(.94,.68+Math.min(.18,prices.length*.015));return {...c,peerCount:prices.length,marketMedian:med,lowerBand:low,market,landed,outbound,pack,fees,profit,roi,margin,confidence,pass:profit>0&&roi>=10&&margin>=10,preferred:profit>0&&roi>=15&&margin>=15};}","function economics(c,compItems){const comps=compItems.filter(x=>compMatches(c,x)&&String(x?.itemId||'')!==c.id);const rawPrices=comps.map(price).filter(x=>x>0).sort((a,b)=>a-b);if(rawPrices.length<2)return null;let prices=[],bestSpread=Infinity,bestMid=Infinity;for(let i=0;i<rawPrices.length;i++){let j=i;while(j+1<rawPrices.length&&rawPrices[j+1]-rawPrices[i]<=10)j++;const cluster=rawPrices.slice(i,j+1),spread=cluster[cluster.length-1]-cluster[0],mid=median(cluster);if(cluster.length>prices.length||(cluster.length===prices.length&&(spread<bestSpread||(spread===bestSpread&&mid<bestMid)))){prices=cluster;bestSpread=spread;bestMid=mid}}if(prices.length<2)return null;const med=median(prices),low=percentile(prices,.35),market=(med+low)/2,landed=c.ask+c.ship,outbound=0,pack=num(localStorage.getItem('gengrailOpp_oppPack'))||.30,feeRate=.135,fees=market*feeRate,profit=market-fees-pack-landed,roi=landed>0?profit/landed*100:0,margin=market>0?profit/market*100:0,confidence=Math.min(.94,.68+Math.min(.18,prices.length*.015));const maxLandedRoi=(market*(1-feeRate)-pack)/1.10,maxLandedMargin=market*(1-feeRate-.10)-pack,maxLanded=Math.max(0,Math.min(maxLandedRoi,maxLandedMargin)),maxBuy=Math.max(0,maxLanded-c.ship),pass=profit>0&&roi>=10&&margin>=10,preferred=profit>0&&roi>=15&&margin>=15,negotiable=!pass&&maxBuy>0&&maxBuy<c.ask&&maxBuy>=c.ask*.60,watch=!pass&&!negotiable&&market>landed,velocityScore=(Math.min(prices.length,8)*10)+(confidence*25)+(preferred?28:pass?20:negotiable?12:0)-Math.min(18,landed/20);return {...c,peerCount:prices.length,rawPeerCount:rawPrices.length,compWindow:5,compSpread:bestSpread,marketMedian:med,lowerBand:low,market,landed,outbound,pack,fees,profit,roi,margin,confidence,maxBuy,pass,preferred,negotiable,watch,velocityScore};}")
      .replace("function cheapShortlist(items,lane,maxPrice){const rows=[],seen=new Set();for(const item of items){const c=identity(item,lane);if(!c||!c.id||c.ask<2||c.ask>maxPrice||seen.has(c.query))continue;seen.add(c.query);rows.push(c)}rows.sort((a,b)=>a.ask-b.ask);if(rows.length<=3)return rows;const picks=[rows[0],rows[Math.floor(rows.length*.25)],rows[Math.floor(rows.length*.5)],rows[Math.floor(rows.length*.75)]].filter(Boolean),out=[];const q=new Set();for(const x of picks){if(!q.has(x.query)){q.add(x.query);out.push(x)}}return out.slice(0,4)}","function cheapShortlist(items,lane,maxPrice){const rows=[],seen=new Set();for(const item of items){const c=identity(item,lane);if(!c||!c.id||c.ask<1.5||c.ask>maxPrice||seen.has(c.query))continue;seen.add(c.query);rows.push(c)}rows.sort((a,b)=>a.ask-b.ask);if(rows.length<=6)return rows;const picks=[rows[0],rows[Math.floor(rows.length*.12)],rows[Math.floor(rows.length*.28)],rows[Math.floor(rows.length*.48)],rows[Math.floor(rows.length*.68)],rows[Math.floor(rows.length*.86)]].filter(Boolean),out=[];const q=new Set();for(const x of picks){if(!q.has(x.query)){q.add(x.query);out.push(x)}}return out.slice(0,6)}")
      .replace("Find qualified buys first. You choose the basket.","SEED velocity: more defensible choices, faster capital turns.")
      .replace("Modern 2002+ rotating discovery → unique card shortlist → targeted comp search. Minimum selectable floor: 10% ROI and 10% net margin. 15%+ is preferred.","SEED velocity mode: broader unique-card sampling, then BUY / NEGOTIATE / WATCH classification. 10% ROI + 10% net margin remains the protected buy floor; 15%+ is preferred.")
      .replace("if(e&&e.profit>0&&e.margin>=5)rows.push(e)","if(e&&(e.pass||e.negotiable||e.watch))rows.push(e)")
      .replace("rows.sort((a,b)=>Number(b.pass)-Number(a.pass)||Number(b.preferred)-Number(a.preferred)||b.profit-a.profit||b.roi-a.roi)","rows.sort((a,b)=>Number(b.preferred)-Number(a.preferred)||Number(b.pass)-Number(a.pass)||Number(b.negotiable)-Number(a.negotiable)||(b.velocityScore||0)-(a.velocityScore||0)||b.profit-a.profit)")
      .replace("S.rows=rows.sort((a,b)=>Number(b.pass)-Number(a.pass)||b.profit-a.profit).slice(0,20)","S.rows=rows.sort((a,b)=>Number(b.preferred)-Number(a.preferred)||Number(b.pass)-Number(a.pass)||Number(b.negotiable)-Number(a.negotiable)||(b.velocityScore||0)-(a.velocityScore||0)||b.profit-a.profit).slice(0,20)")
      .replace('if(prices.length<3)return null;','if(prices.length<2)return null;')
      .replace('Discovery returned candidates but none produced 3+ targeted comps with positive economics.','Discovery returned candidates, but none formed a defensible 2+ comp cluster for BUY, NEGOTIATE or WATCH classification.')
      .replace('No defensible targeted opportunities produced 3+ comparable listings.','No defensible targeted opportunities produced a 2+ comp cluster for BUY, NEGOTIATE or WATCH classification.');
    const routePatch=`\n(function(){\n'use strict';\nif(window.__gengrailSelectableRouteV121)return;window.__gengrailSelectableRouteV121=true;\ndocument.addEventListener('click',function(e){const btn=e.target&&e.target.closest&&e.target.closest('#grailOpportunityAction');if(!btn)return;if(!(window.GengrailSelectableStream&&typeof window.GengrailSelectableStream.render==='function'))return;e.preventDefault();e.stopPropagation();setTimeout(function(){try{window.GengrailSelectableStream.render();}catch(err){console.error('Opportunity Stream render failed',err);}},0);},true);\n})();`;
    const body=(await safety.text())+'\n\n'+(await gate.text())+'\n\n'+(await hub.text())+'\n\n'+selectableBody+'\n\n'+routePatch;
    const response=new Response(body,{status:200,headers:{'content-type':'application/javascript;charset=UTF-8','cache-control':'no-store'}});
    const copy=response.clone();caches.open(C).then(c=>c.put(e.request,copy)).catch(()=>{});
    return response;
   }catch(err){return caches.match(e.request).then(r=>r||fetch(e.request))}
  })());
  return;
 }
 const forceReload=path.endsWith('/grail-pre2002-safety.js')||path.endsWith('/grail-visual-gate.js')||path.endsWith('/grail-selectable-stream-v1.js')||path.endsWith('/grail-hub.css')||path.endsWith('/profit-engine-diagnostic.js')||path.endsWith('/gengrail-theme.css');
 const req=forceReload?new Request(e.request,{cache:'reload'}):e.request;
 e.respondWith(fetch(req).then(r=>{const copy=r.clone();caches.open(C).then(c=>c.put(e.request,copy)).catch(()=>{});return r}).catch(()=>caches.match(e.request)));
});
