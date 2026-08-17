const C='gengrail-log-v24.11.6-comp-window-5';
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
      .replace("const PATCH_VERSION='selectable-stream-v1.0.0'","const PATCH_VERSION='selectable-stream-v1.1.6'")
      .replace('unique.slice(0,18)','unique.slice(0,12)')
      .replace(
        "function economics(c,compItems){const comps=compItems.filter(x=>compMatches(c,x)&&String(x?.itemId||'')!==c.id);const prices=comps.map(price).filter(x=>x>0);if(prices.length<3)return null;const med=median(prices),low=percentile(prices,.35),market=(med+low)/2,landed=c.ask+c.ship,outbound=num(localStorage.getItem('gengrailOpp_oppOutbound'))||4.10,pack=num(localStorage.getItem('gengrailOpp_oppPack'))||.30,feeRate=.135,fees=market*feeRate,profit=market-fees-outbound-pack-landed,roi=landed>0?profit/landed*100:0,margin=market>0?profit/market*100:0,confidence=Math.min(.94,.68+Math.min(.18,prices.length*.015));return {...c,peerCount:prices.length,marketMedian:med,lowerBand:low,market,landed,outbound,pack,fees,profit,roi,margin,confidence,pass:profit>0&&roi>=10&&margin>=10,preferred:profit>0&&roi>=15&&margin>=15};}",
        "function economics(c,compItems){const comps=compItems.filter(x=>compMatches(c,x)&&String(x?.itemId||'')!==c.id);const rawPrices=comps.map(price).filter(x=>x>0);if(rawPrices.length<2)return null;const anchor=median(rawPrices),prices=rawPrices.filter(p=>Math.abs(p-anchor)<=5);if(prices.length<2)return null;const med=median(prices),low=percentile(prices,.35),market=(med+low)/2,landed=c.ask+c.ship,outbound=num(localStorage.getItem('gengrailOpp_oppOutbound'))||4.10,pack=num(localStorage.getItem('gengrailOpp_oppPack'))||.30,feeRate=.135,fees=market*feeRate,profit=market-fees-outbound-pack-landed,roi=landed>0?profit/landed*100:0,margin=market>0?profit/market*100:0,confidence=Math.min(.94,.68+Math.min(.18,prices.length*.015));return {...c,peerCount:prices.length,rawPeerCount:rawPrices.length,compWindow:5,marketMedian:med,lowerBand:low,market,landed,outbound,pack,fees,profit,roi,margin,confidence,pass:profit>0&&roi>=10&&margin>=10,preferred:profit>0&&roi>=15&&margin>=15};}"
      )
      .replace('if(prices.length<3)return null;','if(prices.length<2)return null;')
      .replace('none produced 3+ targeted comps with positive economics.','none produced 2+ targeted comps inside the ±£5 market window with positive economics.')
      .replace('No defensible targeted opportunities produced 3+ comparable listings.','No defensible targeted opportunities produced 2+ comparable listings inside the ±£5 market window.');

    const routePatch=`\n(function(){\n'use strict';\nif(window.__gengrailSelectableRouteV116)return;\nwindow.__gengrailSelectableRouteV116=true;\ndocument.addEventListener('click',function(e){\n const btn=e.target&&e.target.closest&&e.target.closest('#grailOpportunityAction');\n if(!btn)return;\n if(!(window.GengrailSelectableStream&&typeof window.GengrailSelectableStream.render==='function'))return;\n e.preventDefault();\n e.stopPropagation();\n e.stopImmediatePropagation();\n setTimeout(function(){window.GengrailSelectableStream.render();},0);\n},true);\n})();`;

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
