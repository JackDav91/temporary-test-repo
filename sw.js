const C='gengrail-log-v24.11.5-selectable-click-route';
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
      .replace("const PATCH_VERSION='selectable-stream-v1.0.0'","const PATCH_VERSION='selectable-stream-v1.1.5'")
      .replace('unique.slice(0,18)','unique.slice(0,12)')
      .replace('if(prices.length<3)return null;','if(prices.length<2)return null;')
      .replace('none produced 3+ targeted comps with positive economics.','none produced 2+ targeted comps with positive economics.')
      .replace('No defensible targeted opportunities produced 3+ comparable listings.','No defensible targeted opportunities produced 2+ comparable listings.');

    const routePatch=`\n(function(){\n'use strict';\nif(window.__gengrailSelectableRouteV115)return;\nwindow.__gengrailSelectableRouteV115=true;\ndocument.addEventListener('click',function(e){\n const btn=e.target&&e.target.closest&&e.target.closest('#grailOpportunityAction');\n if(!btn)return;\n if(!(window.GengrailSelectableStream&&typeof window.GengrailSelectableStream.render==='function'))return;\n e.preventDefault();\n e.stopPropagation();\n e.stopImmediatePropagation();\n setTimeout(function(){window.GengrailSelectableStream.render();},0);\n},true);\n})();`;

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
