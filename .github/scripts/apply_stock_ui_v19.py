from pathlib import Path
import re

# Stock + recognition UI cleanup only. Recognition logic and persistence remain untouched.

p=Path('index.html')
s=p.read_text()
if 'PRODUCT ENGINE FOUNDATION v1' not in s or 'id="startCameraIntake"' not in s:
    raise SystemExit('Safety stop: expected stock intake baseline')

# User-facing stock action labels only.
s=s.replace('<b>IMPORT PHOTO</b><small>Choose an existing card image</small>','<b>PHOTO LIBRARY</b><small>Choose an existing card image</small>',1)
s=s.replace('<b>ENTER MANUALLY</b><small>Open the full stock sheet</small>','<b>MANUAL ENTRY</b><small>Open the full stock sheet</small>',1)

# Add a scoped style block before </head>; no runtime script injection.
marker=r'''
<style id="stock-ui-review-v19">
/* STOCK UI REVIEW v1.9 — camera-first intake + cleaner recognition hierarchy. */
#stock .product-intake-launcher{padding:14px!important}
#stock .product-intake-launcher .compact-intake-note{margin-bottom:10px!important;padding:0!important;color:#9e9a94!important}
#stock .product-intake-grid{display:grid!important;grid-template-columns:1fr 1fr!important;gap:9px!important;margin-top:10px!important}
#stock #startCameraIntake{grid-column:1/-1!important;min-height:126px!important}
#stock #startCameraIntake .intake-icon{font-size:31px!important}
#stock #startCameraIntake b{font-size:24px!important}
#stock #startCameraIntake small{font-size:11px!important}
#stock #startPhotoIntake,#stock #startManualIntake,#stock .product-intake-grid [data-graded-import="stock"]{min-height:104px!important;padding:12px 8px!important;border-radius:12px!important}
#stock #startPhotoIntake .intake-icon,#stock #startManualIntake .intake-icon,#stock .product-intake-grid [data-graded-import="stock"] .graded-intake-icon{font-size:24px!important;margin-bottom:4px!important}
#stock #startPhotoIntake b,#stock #startManualIntake b,#stock .product-intake-grid [data-graded-import="stock"] b{font-size:17px!important}
#stock #startPhotoIntake small,#stock #startManualIntake small,#stock .product-intake-grid [data-graded-import="stock"] small{font-size:9.5px!important;line-height:1.25!important}
#stock .recognition-loading,#stock .recognition-ready,#stock .ai-recognition-panel{padding:13px!important}
#stockEntryPanel.ai-integrated{padding-top:10px!important}
#stockEntryPanel.ai-integrated .title{margin-bottom:8px!important}
#stockEntryPanel .product-result-card,#stockEntryPanel .ai-result-card{padding:12px!important}
#stockEntryPanel .market-price-card{margin-top:9px!important;padding:11px!important}
#stockEntryPanel .market-price-main{font-size:28px!important}
#stockEntryPanel .product-detail-grid{gap:8px!important}
#stockEntryPanel .product-detail-grid>div{padding:8px!important}
#stockEntryPanel .btn{min-height:46px!important}
@media(max-width:620px){
  #stock .product-intake-grid{grid-template-columns:1fr 1fr!important}
  #stock #startCameraIntake{grid-column:1/-1!important}
  #stock #startPhotoIntake,#stock #startManualIntake,#stock .product-intake-grid [data-graded-import="stock"]{min-height:100px!important}
}
</style>
'''
if 'stock-ui-review-v19' not in s:
    s=s.replace('</head>',marker+'\n</head>',1)

# Cache-bust index itself by SW version only; graded asset below.
for asset in ('graded-integration.js',):
    pat=r'('+re.escape(asset)+r')(?:\?v=[^"\']+)?'
    s,n=re.subn(pat,lambda m:m.group(1)+'?v=23.9.0',s)
    if n<1: raise SystemExit('Safety stop: graded asset reference missing')
p.write_text(s)

# Graded recognition copy/presentation only.
p=Path('graded-integration.js')
s=p.read_text()
if 'function picker' not in s or 'GRADED SLAB IDENTIFIED' not in s:
    raise SystemExit('Safety stop: graded integration baseline missing')
s=s.replace("Stored as USER_CONFIRMED, not machine verified.","Your selection is saved as a manual grader confirmation.")
s=s.replace("'ACE · ASSUMED'","'ACE · NEEDS CONFIRMATION'")
s=s.replace('Confirm grader manually','Confirm grader')
s=s.replace('USE SELECTED GRADER','CONFIRM GRADER')
s=s.replace('GRADED SLAB IDENTIFIED','VERIFIED GRADED CANDIDATE')
s=s.replace('CURRENT GRADED MARKET','GRADED MARKET')

# Tighten injected graded CSS without changing DOM/functionality.
extra="""
/* STOCK RECOGNITION UI v1.9 */
.graded-stock-v3,.graded-stock-compact{padding:14px!important}
.graded-stock-identity{padding:12px!important;margin-top:9px!important}
.graded-stock-name,.gsc-name{font-size:22px!important}
.graded-stock-sub,.gsc-sub{font-size:13px!important}
.graded-stock-meta,.gsc-slabmeta{margin-top:9px!important}
.graded-stock-market-v3,.gsc-market{margin-top:10px!important;padding:11px!important}
.graded-stock-actions,.gsc-actions{margin-top:10px!important;gap:8px!important}
.graded-stock-actions button,.gsc-actions button{min-height:50px!important}
.graded-stock-assumed,.gsc-assumed{font-size:10.5px!important;line-height:1.35!important}
"""
needle="`;document.head.appendChild(s)}"
if extra.strip() not in s:
    if needle not in s: raise SystemExit('Safety stop: graded style close anchor missing')
    s=s.replace(needle,extra+needle,1)
p.write_text(s)

# SW cache only.
p=Path('sw.js')
s=p.read_text();s,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v23.9.0-stock-ui';",s,count=1)
if n!=1: raise SystemExit('Safety stop: SW cache anchor missing')
p.write_text(s)

checks={
 'index.html':['stock-ui-review-v19','PHOTO LIBRARY','MANUAL ENTRY','graded-integration.js?v=23.9.0'],
 'graded-integration.js':['VERIFIED GRADED CANDIDATE','NEEDS CONFIRMATION','manual grader confirmation','STOCK RECOGNITION UI v1.9'],
 'sw.js':['gengrail-log-v23.9.0-stock-ui']
}
for f,needles in checks.items():
    text=Path(f).read_text()
    for n in needles:
        if n not in text: raise SystemExit(f'Safety stop: {n!r} missing from {f}')
