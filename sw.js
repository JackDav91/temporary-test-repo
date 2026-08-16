const C='gengrail-log-v21.3.0-graded-bridge';
const A=['./','./index.html','./manifest.json','./gengrail-theme.css','./gengrail-ebay.js','./graded-integration.js','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(A)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
async function pageWithGradedBridge(request){
 const r=await fetch(request);if(!r.ok)return r;
 const type=r.headers.get('content-type')||'';if(!type.includes('text/html'))return r;
 let html=await r.text();
 if(!html.includes('graded-integration.js'))html=html.replace(/<\/body>/i,'<script src="./graded-integration.js?v=21.3.0"></script></body>');
 const h=new Headers(r.headers);h.delete('content-length');h.set('cache-control','no-store');
 return new Response(html,{status:r.status,statusText:r.statusText,headers:h});
}
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 const u=new URL(e.request.url),isPage=e.request.mode==='navigate'||u.pathname.endsWith('/index.html')||u.pathname.endsWith('/');
 if(isPage){e.respondWith(pageWithGradedBridge(e.request).catch(()=>caches.match(e.request)));return}
 e.respondWith(fetch(e.request).then(r=>{const copy=r.clone();caches.open(C).then(c=>c.put(e.request,copy)).catch(()=>{});return r}).catch(()=>caches.match(e.request)));
});
