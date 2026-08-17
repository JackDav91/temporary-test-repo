from pathlib import Path

css=Path('home-compact.css').read_text()
if 'HOME UI REVIEW v1.4' not in css:
    raise SystemExit('Safety stop: expected Home UI v1.4 baseline')

marker='''

/* HOME UI REVIEW v1.5 — dynamic viewport fill. Presentation only. */
@media (max-width:520px){
  body.home-page{
    height:100dvh !important;
    min-height:100dvh !important;
    padding-top:6px !important;
    padding-bottom:4px !important;
    overflow:hidden !important;
  }
  body.home-page .app{
    height:calc(100dvh - 10px) !important;
    min-height:0 !important;
    overflow:hidden !important;
    display:flex !important;
    flex-direction:column !important;
  }
  body.home-page .brand{
    flex:0 0 auto !important;
  }
  body.home-page .home-screen{
    display:flex !important;
    flex-direction:column !important;
    flex:1 1 auto !important;
    min-height:0 !important;
    overflow:hidden !important;
  }
  body.home-page .home-screen > .panel,
  body.home-page .home-command-title,
  body.home-page .gengrail-performance-ticker{
    flex:0 0 auto !important;
  }
  body.home-page .home-menu{
    flex:1 1 auto !important;
    min-height:0 !important;
    display:grid !important;
    grid-template-columns:repeat(2,minmax(0,1fr)) !important;
    grid-template-rows:repeat(3,minmax(0,1fr)) !important;
    align-content:stretch !important;
  }
  body.home-page .home-menu button{
    min-height:0 !important;
    height:100% !important;
  }
  body.home-page .gengrail-performance-ticker{
    margin:6px 0 0 !important;
    overflow:hidden !important;
  }
  body.home-page .gengrail-ticker-track{
    padding-left:12px !important;
    padding-right:12px !important;
  }
}
'''
if 'HOME UI REVIEW v1.5' not in css:
    css += marker
Path('home-compact.css').write_text(css)

idx=Path('index.html').read_text()
if 'home-compact.css?v=23.4.0' not in idx and 'home-compact.css?v=23.5.0' not in idx:
    raise SystemExit('Safety stop: Home stylesheet cache reference missing')
idx=idx.replace('home-compact.css?v=23.4.0','home-compact.css?v=23.5.0')
Path('index.html').write_text(idx)

sw=Path('sw.js').read_text()
if "const C='gengrail-log-v23.4.0-home-ui';" not in sw and "const C='gengrail-log-v23.5.0-home-dvh';" not in sw:
    raise SystemExit('Safety stop: service worker cache baseline missing')
sw=sw.replace("const C='gengrail-log-v23.4.0-home-ui';","const C='gengrail-log-v23.5.0-home-dvh';")
Path('sw.js').write_text(sw)

for f,needles in {
 'home-compact.css':['HOME UI REVIEW v1.5','height:100dvh !important','height:calc(100dvh - 10px)','grid-template-rows:repeat(3,minmax(0,1fr))'],
 'index.html':['home-compact.css?v=23.5.0'],
 'sw.js':['gengrail-log-v23.5.0-home-dvh']
}.items():
    text=Path(f).read_text()
    for n in needles:
        if n not in text:
            raise SystemExit(f'Safety stop: {n} missing from {f}')
