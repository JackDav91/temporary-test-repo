from pathlib import Path

css=Path('home-compact.css').read_text()
if 'GENGRAIL HOME COMPACT v1.1' not in css:
    raise SystemExit('Safety stop: expected Home Compact baseline')
marker='''

/* HOME UI REVIEW v1.4 — viewport-only correction. No navigation or business logic changes. */
@media (max-width:520px){
  body.home-page{
    height:100svh !important;
    min-height:100svh !important;
    overflow:hidden !important;
  }
  body.home-page .app{
    height:calc(100svh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 10px) !important;
    min-height:0 !important;
    overflow:hidden !important;
  }
  body.home-page .home-screen{
    flex:1 1 auto !important;
    min-height:0 !important;
    overflow:hidden !important;
  }
  body.home-page .home-menu{
    flex:1 1 auto !important;
    min-height:0 !important;
    grid-template-rows:repeat(3,minmax(0,1fr)) !important;
    align-content:stretch !important;
  }
  body.home-page .home-menu button{
    min-height:0 !important;
    height:100% !important;
  }
  body.home-page .gengrail-performance-ticker{
    flex:0 0 auto !important;
    overflow:hidden !important;
    margin:6px 0 0 !important;
  }
  body.home-page .gengrail-ticker-track{
    padding-left:12px !important;
    padding-right:12px !important;
  }
}
@supports not (height:100svh){
  @media (max-width:520px){
    body.home-page{height:100vh !important;min-height:100vh !important}
    body.home-page .app{height:calc(100vh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 10px) !important}
  }
}
'''
if 'HOME UI REVIEW v1.4' not in css:
    css += marker
Path('home-compact.css').write_text(css)

idx=Path('index.html').read_text()
old='home-compact.css?v=23.3.0'
if old not in idx and 'home-compact.css?v=23.4.0' not in idx:
    raise SystemExit('Safety stop: Home stylesheet reference missing')
idx=idx.replace(old,'home-compact.css?v=23.4.0')
Path('index.html').write_text(idx)

sw=Path('sw.js').read_text()
if "const C='gengrail-log-v23.3.0-snapshot-home';" not in sw and "const C='gengrail-log-v23.4.0-home-ui';" not in sw:
    raise SystemExit('Safety stop: service worker baseline missing')
sw=sw.replace("const C='gengrail-log-v23.3.0-snapshot-home';","const C='gengrail-log-v23.4.0-home-ui';")
Path('sw.js').write_text(sw)

for f,needles in {
 'home-compact.css':['HOME UI REVIEW v1.4','height:100svh','grid-template-rows:repeat(3,minmax(0,1fr))'],
 'index.html':['home-compact.css?v=23.4.0'],
 'sw.js':['gengrail-log-v23.4.0-home-ui']
}.items():
    text=Path(f).read_text()
    for n in needles:
        if n not in text: raise SystemExit(f'Safety stop: {n} missing from {f}')
