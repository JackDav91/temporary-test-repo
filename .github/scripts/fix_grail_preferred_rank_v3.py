from pathlib import Path
p=Path('grail-hub.js')
s=p.read_text()
old="""    e.liquidityPass=e.landed<=num(g.availableGrailPlanLiquidity);
    e.safe=e.qualityPass&&e.liquidityPass;
    if(e.preferredPass)e.rankScore=Math.min(100,(e.rankScore||0)+8);
    e.rankScore=modeScore(e,g);"""
new="""    e.liquidityPass=e.landed<=num(g.availableGrailPlanLiquidity);
    e.safe=e.qualityPass&&e.liquidityPass;
    e.rankScore=modeScore(e,g);
    if(e.preferredPass)e.rankScore=Math.min(100,e.rankScore+8);"""
if old not in s:
    raise SystemExit('Preferred-ranking anchor not found')
s=s.replace(old,new,1)
p.write_text(s)

p=Path('index.html')
s=p.read_text().replace('grail-hub.js?v=23.1.0','grail-hub.js?v=23.1.1')
if 'grail-hub.js?v=23.1.1' not in s:
    raise SystemExit('Grail Hub cache reference not updated')
p.write_text(s)

p=Path('sw.js')
s=p.read_text().replace("gengrail-log-v23.1.0-discovery-home","gengrail-log-v23.1.1-discovery-home")
if 'gengrail-log-v23.1.1-discovery-home' not in s:
    raise SystemExit('Service worker cache reference not updated')
p.write_text(s)
