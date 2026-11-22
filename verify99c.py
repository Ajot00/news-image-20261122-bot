from PIL import Image
from pathlib import Path
import re

p=Path('out/candidate99c.png')
im=Image.open(p).convert('RGB')
assert im.size==(1024,1024), im.size
assert p.stat().st_size<=1024*1024, p.stat().st_size
assert Image.open(p).format=='JPEG'
PAPER=(243,232,204)
strips=[(0,0,1024,5),(0,1019,1024,1024),(0,0,5,1024),(1019,0,1024,1024)]
means=[]
for x0,y0,x1,y1 in strips:
    pix=[im.getpixel((x,y)) for y in range(y0,y1) for x in range(x0,x1)]
    mean=tuple(round(sum(c[i] for c in pix)/len(pix)) for i in range(3)); means.append(mean)
    assert max(abs(mean[i]-PAPER[i]) for i in range(3))<8, mean

headlines=[
'COP31 closes in on a deal at dawn','Iran says it hit US radars in Bahrain','Hong Kong votes for its Election Committee',
'Russian ship still burning in Finnish waters','Pant’s 128 puts India 629/6','Modi opens Nitish Setu bridge',
'Estonia to shut its Russia border on 1 Dec','Strike hits food aid vehicle','Bolsonaro in intensive care',
'Mexico captures “El Chapo Isidro”','US airlines warned of terror threat','Four die in fire at Basra power plant',
'Zverev meets Alcaraz for ATP Finals title']
chips=['~200 NATIONS','2 BASES','723 SEATS','16 CREW SAFE','629/6','BRIDGE OPENS','1 DEC','3 KILLED','ICU','11 KILLED','AL-QAEDA LINK','4 DEAD','17:00 GMT']
brief_leads=['BAYELSA, NIGERIA','WASHINGTON','JERUSALEM','TEHRAN','CANBERRA','MANILA','MELBOURNE','NEW YORK','TOKYO','WASHINGTON','RANCHI','KYIV','KYIV','LAS VEGAS','LIVERPOOL','MARKETS','MOGADISHU','COPENHAGEN','BRUSSELS','BERLIN']
assert len(headlines)+20==33
assert len(chips)==13
for s in headlines+chips+brief_leads:
    assert '…' not in s and '...' not in s, s
source=Path('render99c.py').read_text()
for s in chips:
    assert repr(s) in source, f'missing chip inventory: {s}'
for s in headlines:
    assert repr(s) in source, f'missing headline inventory: {s}'
for s in brief_leads:
    assert repr(s) in source, f'missing brief lead inventory: {s}'
# Check the page grid/card background at the exposed paper gutters between cells.
samples=[(20,205),(347,250),(20,421),(217,500),(415,500),(613,500),(811,500),(1009,421),
         (20,579),(217,600),(415,600),(613,600),(811,600),(656,800)]
for pt in samples:
    c=im.getpixel(pt)
    assert max(abs(c[i]-PAPER[i]) for i in range(3))<18, (pt,c)
assert re.search(r'33 STORIES · 7 REGIONS',source)
assert re.search(r'EUROPE 10.*MIDDLE EAST 5.*AMERICAS 7.*ASIA-PACIFIC 5.*AFRICA 2.*OCEANIA 3.*WORLD 1',source)
print('PASS: 33-story inventory (13 headlines, 20 brief leads); 13 exact chips listed; 1024x1024 JPEG; <=1 MiB; outer-strip mean RGB near paper; sampled cell gutters paper-colored.')
print('Outer strip mean RGB:',means,'; file bytes:',p.stat().st_size)
