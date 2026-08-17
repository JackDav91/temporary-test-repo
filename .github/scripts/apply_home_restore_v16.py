from pathlib import Path

css=Path('home-compact.css').read_text()
if 'HOME UI REVIEW v1.5' not in css:
    raise SystemExit('Safety stop: expected Home v1.5 baseline')

marker='''

/* HOME UI REVIEW v1.6 — restore the larger scrolling command-centre composition. */
@media (max-width:520px){
  html,body.home-page{
    min-height:100% !important;
    height:auto !important;
  }
  body.home-page{
    overflow-x:hidden !important;
    overflow-y:auto !important;
    padding-top:calc(env(safe-area-inset-top) + 8px) !important;
    padding-bottom:calc(env(safe-area-inset-bottom) + 18px) !important;
  }
  body.home-page .app{
    height:auto !important;
    min-height:0 !important;
    overflow:visible !important;
    display:block !important;
  }
  body.home-page .brand{
    margin:0 0 12px !important;
  }
  body.home-page .brand img{
    height:150px !important;
    max-height:150px !important;
  }
  body.home-page .home-screen{
    display:block !important;
    min-height:0 !important;
    overflow:visible !important;
    padding:0 2px 8px !important;
  }
  body.home-page .home-screen > .panel{
    margin-top:8px !important;
    padding:12px 12px !important;
    border-radius:14px !important;
  }
  body.home-page .home-screen > .panel .title{
    font-size:14px !important;
    margin-bottom:10px !important;
  }
  body.home-page .home-screen > .panel .kpi{
    padding:10px 6px !important;
  }
  body.home-page .home-screen > .panel .kpi small{
    font-size:8px !important;
  }
  body.home-page .home-screen > .panel .kpi b{
    font-size:15px !important;
  }
  body.home-page .home-command-title{
    margin:14px 0 12px !important;
    font-size:10px !important;
    letter-spacing:.24em !important;
  }
  body.home-page .home-menu{
    display:grid !important;
    grid-template-columns:repeat(2,minmax(0,1fr)) !important;
    grid-template-rows:none !important;
    gap:10px !important;
    min-height:0 !important;
    height:auto !important;
  }
  body.home-page .home-menu button{
    min-height:154px !important;
    height:auto !important;
    padding:16px 38px 14px 14px !important;
    border-radius:17px !important;
    border-width:2px !important;
  }
  body.home-page .home-menu button:after{
    right:12px !important;
    font-size:34px !important;
  }
  body.home-page .home-icon svg{
    width:36px !important;
    height:36px !important;
  }
  body.home-page .home-menu .home-icon{
    margin-bottom:8px !important;
  }
  body.home-page .home-menu .home-label{
    font-size:21px !important;
    line-height:1 !important;
  }
  body.home-page .home-menu .home-sub{
    font-size:11px !important;
    line-height:1.12 !important;
    margin-top:6px !important;
    max-width:96% !important;
  }
  body.home-page .gengrail-performance-ticker{
    display:block !important;
    margin:10px 0 0 !important;
    min-height:34px !important;
    overflow:hidden !important;
  }
  body.home-page .gengrail-ticker-track{
    padding:8px 12px !important;
  }
  body.home-page .gengrail-ticker-item{
    font-size:9.5px !important;
    padding:0 12px !important;
  }
  body.home-page .gengrail-ticker-item b{
    font-size:10.5px !important;
  }
}
@media (max-width:390px){
  body.home-page .brand img{height:138px !important;max-height:138px !important}
  body.home-page .home-menu button{min-height:142px !important}
  body.home-page .home-menu .home-label{font-size:19px !important}
  body.home-page .home-menu .home-sub{font-size:10px !important}
}
'''
if 'HOME UI REVIEW v1.6' not in css:
    css += marker
Path('home-compact.css').write_text(css)

idx=Path('index.html').read_text()
if 'home-compact.css?v=23.5.0' not in idx and 'home-compact.css?v=23.6.0' not in idx:
    raise SystemExit('Safety stop: Home stylesheet cache reference missing')
idx=idx.replace('home-compact.css?v=23.5.0','home-compact.css?v=23.6.0')
Path('index.html').write_text(idx)

sw=Path('sw.js').read_text()
if "const C='gengrail-log-v23.5.0-home-dvh';" not in sw and "const C='gengrail-log-v23.6.0-home-scroll';" not in sw:
    raise SystemExit('Safety stop: service worker cache baseline missing')
sw=sw.replace("const C='gengrail-log-v23.5.0-home-dvh';","const C='gengrail-log-v23.6.0-home-scroll';")
Path('sw.js').write_text(sw)

for f,needles in {
 'home-compact.css':['HOME UI REVIEW v1.6','overflow-y:auto','min-height:154px','gengrail-performance-ticker'],
 'index.html':['home-compact.css?v=23.6.0'],
 'sw.js':['gengrail-log-v23.6.0-home-scroll']
}.items():
    text=Path(f).read_text()
    for n in needles:
        if n not in text:
            raise SystemExit(f'Safety stop: {n} missing from {f}')
