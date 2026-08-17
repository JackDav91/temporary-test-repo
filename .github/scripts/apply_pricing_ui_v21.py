from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()
if '/* ---------- PRICING CALCULATOR ---------- */' not in s:
    raise SystemExit('Safety stop: Pricing Calculator baseline missing')

style=r'''
<style id="pricing-ui-review-v21">
/* PRICING UI REVIEW v2.1 — compact workflow + stronger decision hierarchy. Presentation only. */
#pricing .panel{padding:14px!important}
#pricing .pricing-purpose{margin:0 0 10px!important;font-size:11px!important;line-height:1.4!important;color:#aaa!important}
#pricing .pricing-ai-tools{margin-bottom:10px!important;gap:8px!important}
#pricing .pricing-ai-tools>label.btn,#pricing .pricing-ai-tools>[data-graded-import="pricing"]{min-height:66px!important;padding:10px!important;font-size:12px!important}
#pricing #pricingAiClear{min-height:42px!important}
#pricing .pricing-tabs{gap:7px!important;margin-bottom:10px!important}
#pricing .pricing-tab{padding:9px 5px!important}
#pricing .grid{gap:9px!important}
#pricing label{margin-bottom:4px!important}
#pricing input,#pricing select{padding:10px!important}

/* Fulfilment should read as one compact supporting row, not a second hero. */
#pricing #pricePostageSummary{margin:8px 0 0!important;padding:10px 12px!important;min-height:0!important;border-radius:10px!important;background:#08130c!important;border:1px solid #285236!important}
#pricing #pricePostageSummary *{margin-top:0!important;margin-bottom:0!important}
#pricing #pricePostageSummary br{display:none!important}
#pricing #pricePostageSummary .value,#pricing #pricePostageSummary b{font-size:14px!important}
#pricing #pricePostageSummary small,#pricing #pricePostageSummary span{font-size:9px!important}

#pricing #priceCalcBtn,#pricing .pricing-calculate{width:100%!important;min-height:50px!important;margin-top:10px!important;background:#e0ad16!important;color:#080808!important;border:1px solid #f2c84b!important;border-radius:10px!important;font-weight:950!important}

/* Result: guided value first, then compact economics, then decision. */
#pricing .pricing-result{margin-top:10px!important}
#pricing .pricing-hero{padding:12px!important;border-radius:12px!important;border-color:#d88a1e!important}
#pricing .pricing-hero small{font-size:9px!important}
#pricing .pricing-price{font-size:42px!important;margin:2px 0!important}
#pricing .pricing-profit{font-size:11px!important;line-height:1.35!important}
#pricing .pricing-stats,#pricing .pricing-stats-4{display:grid!important;grid-template-columns:1fr 1fr!important;gap:7px!important;margin-top:8px!important}
#pricing .pricing-stat{padding:8px!important;min-height:66px!important;display:flex!important;flex-direction:column!important;justify-content:center!important}
#pricing .pricing-stat span{font-size:8px!important}
#pricing .pricing-stat b{font-size:16px!important;margin-top:2px!important}
#pricing .pricing-decision{margin-top:9px!important;padding:10px!important;border-radius:10px!important}
#pricing .pricing-decision .word{font-size:28px!important}
#pricing .pricing-actions{gap:7px!important;margin-top:8px!important}
#pricing .pricing-actions .btn{min-height:44px!important;margin-top:0!important}

/* Assumptions/settings stay available but visually secondary. */
#pricing details{margin-top:8px!important}
#pricing details>summary{font-size:11px!important;color:#bbb!important;padding:8px 0!important}
#pricing .pricing-fee-note,#pricing .note{font-size:10px!important;line-height:1.4!important}
#pricing .pricing-profile,#pricing .buying-profile,#pricing [class*="buying-profile"]{padding:10px!important;margin-top:9px!important}

@media(max-width:520px){
 #pricing .pricing-price{font-size:38px!important}
 #pricing .pricing-stat{min-height:62px!important}
}
</style>
'''
if 'pricing-ui-review-v21' not in s:
    s=s.replace('</head>',style+'\n</head>',1)
p.write_text(s)

p=Path('sw.js')
s=p.read_text()
s,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v24.1.0-pricing-ui';",s,count=1)
if n!=1: raise SystemExit('Safety stop: service worker cache anchor missing')
p.write_text(s)

for f,needles in {
 'index.html':['pricing-ui-review-v21','#pricing #pricePostageSummary','.pricing-decision .word'],
 'sw.js':['gengrail-log-v24.1.0-pricing-ui']
}.items():
    text=Path(f).read_text()
    for needle in needles:
        if needle not in text: raise SystemExit(f'Safety stop: {needle!r} missing from {f}')
