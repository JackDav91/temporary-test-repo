const C='gengrail-log-v21.3.2-graded-bridge-nav-reset';
const A=['./manifest.json','./gengrail-theme.css','./gengrail-ebay.js','./graded-integration.js','./icon-192.png','./icon-512.png'];

self.addEventListener('install',e=>{
  e.waitUntil(caches.open(C).then(c=>c.addAll(A)));
  self.skipWaiting();
});

self.addEventListener('activate',e=>{
  e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==C).map(k=>caches.delete(k)))));
  self.clients.claim();
});

async function ebayScriptWithGradedBridge(request){
  const r=await fetch(request,{cache:'no-store'});
  if(!r.ok)return r;
  const js=await r.text();
  const loader=`\n;(()=>{try{if(!document.querySelector('script[data-gengrail-graded-bridge]')){const s=document.createElement('script');s.src='./graded-integration.js?v=21.3.2';s.dataset.gengrailGradedBridge='1';document.head.appendChild(s)}}catch(e){console.warn('graded bridge loader',e)}})();\n`;
  const h=new Headers(r.headers);h.delete('content-length');h.set('cache-control','no-store');
  return new Response(js+loader,{status:r.status,statusText:r.statusText,headers:h});
}

self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  const u=new URL(e.request.url);
  const isNavigation=e.request.mode==='navigate'||u.pathname.endsWith('/index.html')||u.pathname.endsWith('/');

  // Never cache or serve cached HTML on this isolated test branch.
  if(isNavigation){
    e.respondWith(fetch(e.request,{cache:'no-store'}));
    return;
  }

  if(u.pathname.endsWith('/gengrail-ebay.js')){
    e.respondWith(ebayScriptWithGradedBridge(e.request));
    return;
  }

  e.respondWith(
    fetch(e.request).then(r=>{
      const copy=r.clone();
      caches.open(C).then(c=>c.put(e.request,copy)).catch(()=>{});
      return r;
    }).catch(()=>caches.match(e.request))
  );
});
