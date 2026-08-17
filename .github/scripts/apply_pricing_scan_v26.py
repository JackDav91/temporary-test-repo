from pathlib import Path
import re

# Pricing Scan Card v2.6
# Directly extends the existing Pricing recognition controls and handler.
# No appended runtime script block; no Stock/listing side effects.

p=Path('index.html')
s=p.read_text()

old_tools='''<div class="pricing-ai-tools">\n  <label class="btn alt">IMPORT CARD PHOTO<input accept="image/*" id="pricingAiPhoto" style="display:none" type="file"/></label>\n  <button class="btn alt" id="pricingAiClear" type="button">CLEAR CARD</button>\n</div>'''
new_tools='''<div class="pricing-ai-tools">\n  <label class="btn pricing-scan-card">SCAN CARD<input accept="image/*" capture="environment" id="pricingAiScan" style="display:none" type="file"/></label>\n  <label class="btn alt">CARD PHOTO<input accept="image/*" id="pricingAiPhoto" style="display:none" type="file"/></label>\n  <button class="btn alt" id="pricingAiClear" type="button">CLEAR CARD</button>\n</div>'''
if old_tools not in s:
    raise SystemExit('Safety stop: expected Pricing tool markup not found')
s=s.replace(old_tools,new_tools,1)

old_clear="function pricingAiClear(){pricingRecognition=null;if($('pricingAiPhoto'))$('pricingAiPhoto').value='';if($('priceCost'))$('priceCost').value='';if($('priceMarketValue'))$('priceMarketValue').value='0';pricingAiRender('idle');priceCalc()}"
new_clear="function pricingAiClear(){pricingRecognition=null;if($('pricingAiScan'))$('pricingAiScan').value='';if($('pricingAiPhoto'))$('pricingAiPhoto').value='';if($('priceCost'))$('priceCost').value='';if($('priceMarketValue'))$('priceMarketValue').value='0';pricingAiRender('idle');priceCalc()}"
if old_clear not in s:
    raise SystemExit('Safety stop: expected Pricing clear handler not found')
s=s.replace(old_clear,new_clear,1)

old_bind="$('priceCalcBtn').onclick=priceCalc;$('pricingAiPhoto').onchange=e=>pricingRecogniseFile(e.target.files?.[0]);$('pricingAiClear').onclick=pricingAiClear;"
new_bind="$('priceCalcBtn').onclick=priceCalc;$('pricingAiScan').onchange=e=>pricingRecogniseFile(e.target.files?.[0]);$('pricingAiPhoto').onchange=e=>pricingRecogniseFile(e.target.files?.[0]);$('pricingAiClear').onclick=pricingAiClear;"
if old_bind not in s:
    raise SystemExit('Safety stop: expected Pricing recognition binding not found')
s=s.replace(old_bind,new_bind,1)

if 'pricing-scan-card-v22' in s:
    raise SystemExit('Safety stop: obsolete injected Pricing scan script still present')
if s.count('id="pricingAiScan"') != 1:
    raise SystemExit('Safety stop: Pricing scan input count invalid')
if s.count("$('pricingAiScan').onchange") != 1:
    raise SystemExit('Safety stop: Pricing scan handler count invalid')
p.write_text(s)

p=Path('gengrail-theme.css')
css=p.read_text()
block='''\n/* ---------- PRICING SCAN CARD v2.6 ---------- */\n#pricing .pricing-ai-tools{display:grid!important;grid-template-columns:1fr 1fr!important;gap:8px!important}\n#pricing .pricing-scan-card{grid-column:1/-1!important;min-height:64px!important;margin:0!important;background:linear-gradient(180deg,#17140d,#10100d)!important;color:#f4f1eb!important;border:1px solid #8a6818!important;border-radius:11px!important;font-family:Impact,sans-serif!important;font-size:20px!important;letter-spacing:.04em!important;display:flex!important;align-items:center!important;justify-content:center!important}\n#pricing .pricing-ai-tools>label.btn.alt{margin:0!important;min-height:54px!important;display:flex!important;align-items:center!important;justify-content:center!important}\n#pricing #pricingAiClear{grid-column:1/-1!important;margin:0!important;min-height:42px!important}\n'''
if 'PRICING SCAN CARD v2.6' not in css:
    css += block
p.write_text(css)

p=Path('sw.js')
sw=p.read_text()
sw,n=re.subn(r"const C='[^']+';","const C='gengrail-log-v24.6.0-pricing-scan-direct';",sw,count=1)
if n!=1:
    raise SystemExit('Safety stop: service worker cache anchor missing')
p.write_text(sw)

# Final validation of the exact direct-wiring approach.
ix=Path('index.html').read_text()
assert '<label class="btn pricing-scan-card">SCAN CARD' in ix
assert 'capture="environment" id="pricingAiScan"' in ix
assert "$('pricingAiScan').onchange=e=>pricingRecogniseFile" in ix
assert 'pricing-scan-card-v22' not in ix
assert Path('sw.js').read_text().startswith("const C='gengrail-log-v24.6.0-pricing-scan-direct';")
print('Pricing scan direct patch validated')
