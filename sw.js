const C='gengrail-log-v24.11.2-selectable-observer';
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
      .replace("const PATCH_VERSION='selectable-stream-v1.0.0'","const PATCH_VERSION='selectable-stream-v1.1.2'")
      .replace('unique.slice(0,18)','unique.slice(0,12)');

    const forceSelectable=`\n(function(){\n'use strict';\nfunction shouldTakeOver(){\n const root=document.getElementById('grailHubOverlay');\n const shell=root&&root.querySelector('.grail-hub-shell');\n if(!root||!shell||!window.GengrailSelectableStream)return false;\n if(shell.querySelector('.gsel-wrap'))return false;\n const txt=(shell.textContent||'').toUpperCase();\n return txt.includes('OPPORTUNITY STREAM')||txt.includes('DAILY SHEET')||!!shell.querySelector('#grailOpportunityAction');\n}\nfunction takeover(){try{if(shouldTakeOver())window.GengrailSelectableStream.render()}catch(e){console.warn('Selectable stream takeover failed',e)}}\nconst mo=new MutationObserver(()=>setTimeout(takeover,0));\nfunction start(){const root=document.getElementById('grailHubOverlay')||document.body;mo.observe(root,{subtree:true,childList:true,attributes:true});takeover()}\nif(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();\ndocument.addEventListener('click',e=>{const t=e.target&&e.target.closest&&e.target.closest('#grailOpportunityAction');if(t)setTimeout(takeover,0)},true);\n})();`;

    const body=(await safety.text())+'\n\n'+(await gate.text())+'\n\n'+(await hub.text())+'\n\n'+selectableBody+'\n\n'+forceSelectable;
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
