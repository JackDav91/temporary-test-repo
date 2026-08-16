from pathlib import Path
import re
import subprocess

# 1. Grail Hub JS
subprocess.run(['python3','.github/scripts/grail_discovery_layout_patch_v1.py'],check=True)

# 2. Grail Hub CSS
p=Path('grail-hub.css')
s=p.read_text()
if 'GENGRAIL GRAIL HUB v1.3' not in s:
    raise SystemExit('Safety stop: expected Grail Hub CSS v1.3')
s=s.replace('GENGRAIL GRAIL HUB v1.3 — Buying command centre + live Opportunity Stream','GENGRAIL GRAIL HUB v1.4 — width containment + daily discovery',1)
s += '''

/* v1.4 — Safari width containment + daily discovery */
html.grail-hub-open,body.grail-hub-open{overflow:hidden!important;overflow-x:hidden!important;max-width:100%!important}
.grail-hub-overlay{width:100%!important;max-width:100vw!important;overflow-x:hidden!important;box-sizing:border-box!important;overscroll-behavior-x:none}
.grail-hub-shell{width:100%!important;max-width:760px!important;min-width:0!important;box-sizing:border-box!important;overflow-x:hidden!important}
.grail-hub-shell *,
.grail-stream-toolbar,.grail-stream-search,.grail-stream-summary,.grail-stream-results,
.grail-opportunity,.grail-opportunity-main,.grail-opportunity-top,.grail-opportunity-grid,
.grail-plan-preview,.grail-plan-preview-grid,.grail-plan-basket,.grail-plan-basket-row{min-width:0;max-width:100%;box-sizing:border-box}
.grail-opportunity h3,.grail-opportunity-sub,.grail-opportunity-reason,.grail-plan-basket-row span,
.grail-stream-hint,.grail-discovery-row span{overflow-wrap:anywhere;word-break:break-word}
.grail-opportunity-top{overflow:hidden}.grail-opportunity-rank{flex:0 0 auto}
.grail-stream-results,.grail-hub-section{width:100%;overflow-x:hidden}
.grail-discovery-row{display:flex;align-items:center;gap:8px;margin-top:8px;min-width:0}
.grail-discovery-row button{margin:0!important;flex:0 0 auto;background:#17351f!important;color:#9be8af!important;border:1px solid #3d8751!important;border-radius:8px!important;padding:8px 10px!important;font-size:8.5px!important;font-weight:950!important;white-space:nowrap}
.grail-discovery-row span{color:#878d87;font-size:8.5px;line-height:1.3;min-width:0}
@media(max-width:520px){.grail-discovery-row{align-items:flex-start;flex-direction:column}.grail-discovery-row button{width:100%!important}.grail-stream-search{grid-template-columns:minmax(0,1fr) auto}.grail-stream-search button{max-width:125px;padding-left:10px!important;padding-right:10px!important}}
'''
p.write_text(s)

# 3. Home compact — force flex container to consume exactly the dynamic viewport.
p=Path('home-compact.css')
s=p.read_text()
if 'GENGRAIL HOME COMPACT v1' not in s:
    raise SystemExit('Safety stop: expected Home Compact v1')
s=s.replace('GENGRAIL HOME COMPACT v1 — single-screen command centre','GENGRAIL HOME COMPACT v2 — responsive full-height command centre',1)
old='''body.home-page .app{\n  min-height:calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 10px);\n  display:flex;\n  flex-direction:column;\n  max-width:840px;\n}'''
new='''body.home-page .app{\n  height:calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 10px);\n  min-height:0;\n  overflow:hidden;\n  display:flex;\n  flex-direction:column;\n  max-width:840px;\n}'''
if old not in s:
    raise SystemExit('Home app height anchor not found')
s=s.replace(old,new,1)
old='''body.home-page .home-menu button{\n  min-height:0 !important;\n  height:auto !important;\n  padding:8px 30px 8px 9px !important;'''
new='''body.home-page .home-menu button{\n  min-height:0 !important;\n  height:100% !important;\n  padding:10px 30px 10px 9px !important;'''
if old not in s:
    raise SystemExit('Home tile anchor not found')
s=s.replace(old,new,1)
p.write_text(s)

# 4. Cache bust only the three additive presentation/Hub assets.
p=Path('index.html')
s=p.read_text()
for asset,version in [('grail-hub.css','23.0.0'),('grail-hub.js','23.0.0'),('home-compact.css','23.0.0')]:
    pattern=r'('+re.escape(asset)+r')(?:\?v=[^"\']+)?'
    s,n=re.subn(pattern,lambda m:m.group(1)+'?v='+version,s)
    if n<1:
        raise SystemExit(f'Cache reference not found for {asset}')
p.write_text(s)

# Safety gates
checks={
'grail-hub.js':['v1.6 — daily discovery foundation + layout restore','function buildDailySheet','function lockLayout','function restoreLayout','BUILD DAILY SHEET','opportunities/search'],
'grail-hub.css':['v1.4 — width containment + daily discovery','overflow-x:hidden','grail-discovery-row'],
'home-compact.css':['HOME COMPACT v2','height:calc(100dvh','height:100% !important'],
'index.html':['recognise-card','graded-integration.js','gengrail-ebay.js','grail-hub.js?v=23.0.0','grail-hub.css?v=23.0.0','home-compact.css?v=23.0.0']
}
for file,needles in checks.items():
    text=Path(file).read_text()
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'Safety stop: {needle!r} missing from {file}')
