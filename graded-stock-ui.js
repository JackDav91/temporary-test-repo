(()=>{
'use strict';
const $=id=>document.getElementById(id);
let active=false;
function addStyle(){if($('gradedStockUiStyle'))return;const s=document.createElement('style');s.id='gradedStockUiStyle';s.textContent=`
.product-intake-launcher.graded-stock-active .compact-intake-note,
.product-intake-launcher.graded-stock-active .product-intake-grid,
.product-intake-launcher.graded-stock-active>.recognition-ready,
.product-intake-launcher.graded-stock-active>[data-graded-import="stock"],
.product-intake-launcher.graded-stock-active>[data-graded-input="stock"],
.product-intake-launcher.graded-stock-active>[data-graded-status="stock"]{display:none!important}
.product-intake-launcher.graded-stock-active{padding-bottom:0}
#aiIntakeWorkspace.graded-stock-workspace{display:block!important;border-color:#6b5215;border-left-color:#e0ad16;background:linear-gradient(180deg,#151107 0%,#090909 100%)}
#aiIntakeWorkspace.graded-stock-workspace #gradedStockBridge{margin:0!important;border:0!important;border-bottom:1px solid rgba(224,173,22,.22)!important;border-radius:0!important;background:transparent!important;padding:16px!important}
#aiIntakeWorkspace.graded-stock-workspace #stockEntryPanel.ai-integrated{display:block!important}
.graded-stock-reset{display:block;width:100%;margin:12px 0 0;padding:12px 14px;border-radius:10px;border:1px solid #494949;background:#242424;color:#fff;font-weight:900}
`;document.head.appendChild(s)}
function launcher(){return document.querySelector('.product-intake-launcher')}
function reset(){active=false;const l=launcher(),w=$('aiIntakeWorkspace'),p=$('stockEntryPanel'),b=$('gradedStockBridge');l?.classList.remove('graded-stock-active');w?.classList.remove('graded-stock-workspace');document.querySelector('.graded-stock-reset')?.remove();if(p){p.classList.remove('ai-integrated');if(l&&p.parentNode===w)l.after(p)}if(b)b.hidden=true}
function consolidate(){const b=$('gradedStockBridge'),p=$('stockEntryPanel'),w=$('aiIntakeWorkspace'),l=launcher();if(!b||!p||!w||!l||b.hidden)return;active=true;addStyle();l.classList.add('graded-stock-active');w.hidden=false;w.classList.add('graded-stock-workspace');p.classList.add('ai-integrated');if($('stockEntryTitle'))$('stockEntryTitle').textContent='PURCHASE DETAILS';if(b.parentNode!==w)w.prepend(b);if(p.parentNode!==w)w.appendChild(p);p.hidden=false;if(!document.querySelector('.graded-stock-reset')){const r=document.createElement('button');r.type='button';r.className='graded-stock-reset';r.textContent='CHANGE / ADD ANOTHER CARD';r.onclick=()=>{reset();window.scrollTo({top:l.getBoundingClientRect().top+window.scrollY-20,behavior:'smooth'})};w.insertBefore(r,p)}setTimeout(()=>w.scrollIntoView({behavior:'smooth',block:'start'}),30)}
function watch(){const mo=new MutationObserver(()=>{const b=$('gradedStockBridge');if(b&&!b.hidden&&!active)consolidate()});mo.observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['hidden']});['startCameraIntake','startPhotoIntake','startManualIntake','cancelStockEntry'].forEach(id=>$(id)?.addEventListener('click',reset));document.addEventListener('click',e=>{if(e.target?.matches?.('[data-graded-import="stock"]'))reset()},true)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',watch,{once:true});else watch();
})();