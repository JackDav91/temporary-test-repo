const C='gengrail-log-v24.11.0-selectable-bootstrap';
const A=['./','./index.html','./manifest.json','./gengrail-theme.css','./gengrail-ebay.js','./gengrail-profit-engine.js','./profit-engine-diagnostic.js','./home-compact.css','./grail-hub.css','./grail-pre2002-safety.js','./grail-visual-gate.js','./grail-hub.js','./grail-selectable-stream-v1.js','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(A)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});

function isAppShell(path){return path.endsWith('/temporary-test-repo/')||path.endsWith('/temporary-test-repo/index.html')||path.endsWith('/index.html')}

self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 const url=new URL(e.request.url),path=url.pathname;

 // Make the test build load the selectable stream directly from the app shell.
 // This avoids relying on the legacy Grail Hub bundle order to activate it.
 if(isAppShell(path)){
  e.respondWith((async()=>{
   try{
    const network=await fetch(new Request(e.request,{cache:'reload'}));
    if(!network.ok)throw new Error('app_shell_fetch_failed');
    let html=await network.text();
    const marker='data-gengrail-selectable-bootstrap="1"';
    if(!html.includes(marker)){
     const tag='<script src="./grail-selectable-stream-v1.js?v=24.11.0" '+marker+'></script>';
     html=html.includes('</body>')?html.replace('</body>',tag+'\n</body>'):html+'\n'+tag;
    }
    const response=new Response(html,{status:network.status,statusText:network.statusText,headers:{'content-type':'text/html;charset=UTF-8','cache-control':'no-store'}});
    const copy=response.clone();caches.open(C).then(c=>c.put(e.request,copy)).catch(()=>{});
    return response;
   }catch(err){return caches.match(e.request).then(r=>r||fetch(e.request))}
  })());
  return;
 }

 // Serve the selectable stream as an explicit v1.1 runtime patch and reduce
 // expensive targeted-comp enrichment from 18 candidates to 12.
 if(path.endsWith('/grail-selectable-stream-v1.js')){
  e.respondWith((async()=>{
   try{
    const r=await fetch(new Request(e.request,{cache:'reload'}));
    if(!r.ok)throw new Error('selectable_stream_fetch_failed');
    let body=await r.text();
    body=body
      .replace("const PATCH_VERSION='selectable-stream-v1.0.0'","const PATCH_VERSION='selectable-stream-v1.1.0'")
      .replace('unique.slice(0,18)','unique.slice(0,12)');
    return new Response(body,{status:200,headers:{'content-type':'application/javascript;charset=UTF-8','cache-control':'no-store'}});
   }catch(err){return caches.match(e.request).then(r=>r||fetch(e.request))}
  })());
  return;
 }

 // Keep vintage safety and visual validation ahead of the legacy hub code,
 // but do not append the selectable stream here anymore; it now boots directly.
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

 const forceReload=path.endsWith('/grail-pre2002-safety.js')||path.endsWith('/grail-visual-gate.js')||path.endsWith('/grail-hub.css')||path.endsWith('/profit-engine-diagnostic.js')||path.endsWith('/gengrail-theme.css');
 const req=forceReload?new Request(e.request,{cache:'reload'}):e.request;
 e.respondWith(fetch(req).then(r=>{const copy=r.clone();caches.open(C).then(c=>c.put(e.request,copy)).catch(()=>{});return r}).catch(()=>caches.match(e.request)));
});
