const C='gengrail-log-v21.3.1-graded-bridge-fix';
const A=['./','./index.html','./manifest.json','./gengrail-theme.css','./gengrail-ebay.js','./graded-integration.js','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(A)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
async function ebayScriptWithGradedBridge(request){
 const r=await fetch(request);if(!r.ok)return r;
