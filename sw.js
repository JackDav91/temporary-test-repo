const C='gengrail-log-v24.9.8-grail-pre2002-direct';
const A=['./','./index.html','./manifest.json','./gengrail-theme.css','./gengrail-ebay.js','./gengrail-profit-engine.js','./profit-engine-diagnostic.js','./home-compact.css','./grail-hub.css','./grail-pre2002-safety.js','./grail-visual-gate.js','./grail-hub.js','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(A)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 const url=new URL(e.request.url),path=url.pathname;
 if(path.endsWith('/grail-hub.js')){
  e.respondWith((async()=>{
   try{
    const [safety,gate,hub]=await Promise.all([
     fetch(new URL('./grail-pre2002-safety.js',self.location.href),{cache:'reload'}),
     fetch(new URL('./grail-visual-gate.js',self.location.href),{cache:'reload'}),
     fetch(new Request(e.request,{cache:'reload'}))
    ]);
    if(!safety.ok||!gate.ok||!hub.ok)throw new Error('grail_bundle_fetch_failed');
    const body=(await safety.text())+'\n\n'+(await gate.text())+'\n\n'+(await hub.text());
    const response=new Response(body,{status:200,headers:{'content-type':'application/javascript;charset=UTF-8','cache-control':'no-store'}});
    const copy=response.clone();caches.open(C).then(c=>c.put(e.request,copy)).catch(()=>{});
    return response;
   }catch(err){return caches.match(e.request).then(r=>r||fetch(e.request))}
  })());
  return;
 }
 const forceReload=path.endsWith('/grail-pre2002-safety.js')||path.endsWith('/grail-visual-gate.js')||path.endsWith('/grail-hub.css')||path.endsWith('/profit-engine-diagnostic.js')||path.endsWith('/gengrail-theme.css')||path.endsWith('/index.html')||path.endsWith('/temporary-test-repo/');
 const req=forceReload?new Request(e.request,{cache:'reload'}):e.request;
 e.respondWith(fetch(req).then(r=>{const copy=r.clone();caches.open(C).then(c=>c.put(e.request,copy)).catch(()=>{});return r}).catch(()=>caches.match(e.request)));
});
