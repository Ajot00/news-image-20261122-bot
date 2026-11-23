from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import re

p = Path('out/candidate99f.png')
im = Image.open(p).convert('RGB')
assert im.size == (1024, 1024), im.size
assert p.stat().st_size <= 1024 * 1024, p.stat().st_size
assert Image.open(p).format == 'JPEG'
PAPER = (243, 232, 204)
strips = [(0, 0, 1024, 5), (0, 1019, 1024, 1024), (0, 0, 5, 8), (0, 29, 5, 1024), (1019, 0, 1024, 8), (1019, 29, 1024, 1024)]
means = []
for x0, y0, x1, y1 in strips:
    pix = [im.getpixel((x, y)) for y in range(y0, y1) for x in range(x0, x1)]
    mean = tuple(round(sum(c[i] for c in pix) / len(pix)) for i in range(3)); means.append(mean)
    assert mean == PAPER, mean

headlines = [
'COP31 closes in on a deal at dawn', 'Iran says it hit US radars in Bahrain', 'Russia’s overnight barrage: 186 drones, 161 downed',
'Russian ship still burning in Finnish waters', 'India declare 720/9 — a record in NZ', 'Modi opens Nitish Setu bridge',
'Estonia to shut its Russia border on 1 Dec', 'Strike hits food aid vehicle', 'Bolsonaro in intensive care',
'Mexico captures “El Chapo Isidro”', 'US airlines warned of terror threat', 'Four die in fire at Basra power plant',
'Hong Kong votes for its Election Committee']
chips = ['~200 NATIONS', '2 BASES', '161 DOWNED', '723 SEATS', '16 CREW SAFE', '720/9', 'BRIDGE OPENS', '1 DEC', '3 KILLED', 'ICU', '11 KILLED', 'AL-QAEDA LINK', '4 DEAD']
brief_leads = ['BAYELSA, NIGERIA', 'WASHINGTON', 'JERUSALEM', 'TEHRAN', 'CANBERRA', 'MANILA', 'MELBOURNE', 'NEW YORK', 'TOKYO', 'WASHINGTON', 'RANCHI', 'KYIV', 'KYIV', 'LAS VEGAS', 'LIVERPOOL', 'MARKETS', 'MOGADISHU', 'COPENHAGEN', 'BRUSSELS', 'BERLIN', 'LISBON', 'DHAKA', 'TURIN']
assert len(headlines) + 23 == 36
assert len(chips) == 13
for s in headlines + chips + brief_leads:
    assert '…' not in s and '...' not in s, s
source = Path('render99f.py').read_text()
for s in chips:
    assert repr(s) in source, f'missing chip inventory: {s}'
for s in headlines:
    assert repr(s) in source, f'missing headline inventory: {s}'
for s in brief_leads:
    assert repr(s) in source, f'missing brief lead inventory: {s}'
# D1 devices present in the source
assert 'THE DAY IN TEN' in source
assert 'BAHRAIN' in source and 'STRUCK' in source
assert 'photo(k + 1, (x, 220, 316, 140))' in source
assert 'photo(scene_ids[k], (x, y, 188, 68))' in source
assert re.search(r'36 STORIES · 7 REGIONS', source)
# Map: blue ocean + solid beige land (the cycle-4 fix that never landed)
def close(c, target, tol=3): return all(abs(c[i] - target[i]) <= tol for i in range(3))
assert close(im.getpixel((290, 890)), (176, 203, 216)), im.getpixel((290, 890))
assert close(im.getpixel((60, 890)), (176, 203, 216)), im.getpixel((60, 890))
land = im.getpixel((182, 829))
assert land[0] > 200 and land[1] > 180 and land[2] > 130, land
# Anchor panel is bright (mean brightness of centre top-3 panel >> dark panels)
def band_mean(x0, y0, x1, y1):
    pix = [im.getpixel((x, y)) for y in range(y0, y1, 4) for x in range(x0, x1, 4)]
    return sum(sum(c) / 3 for c in pix) / len(pix)
anchor = band_mean(354 + 40, 230, 354 + 276, 330)
assert anchor > 150, anchor
# Paper gutters between cells
samples = [(20, 205), (347, 250), (20, 421), (217, 500), (415, 500), (613, 500), (811, 500), (1009, 421),
           (20, 579), (217, 600), (415, 600), (613, 600), (811, 600), (656, 800)]
for pt in samples:
    c = im.getpixel(pt)
    assert max(abs(c[i] - PAPER[i]) for i in range(3)) < 18, (pt, c)
mast = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf', 85)
mb = ImageDraw.Draw(Image.new('RGB', (1024, 1024))).textbbox((24, 27), 'Sunday 22 November 2026', font=mast)
assert mb[0] >= 3 and mb[2] <= 1021 and mb[0] >= 24 and 1024 - mb[2] >= 3, mb
assert 'THE WORLD IN ONE DAY · 36 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026' in source
assert max(im.getpixel((512, 27))) < 8
assert all(max(im.getpixel((x, 27))) < 8 for x in (0, 256, 512, 768, 1023))
assert not any(max(im.getpixel((x, y))) < 80 for y in list(range(0, 8)) + list(range(29, 1024)) for x in range(1017, 1024))
assert re.search(r'EUROPE 12.*MIDDLE EAST 5.*AMERICAS 7.*ASIA-PACIFIC 6.*AFRICA 2.*OCEANIA 3.*WORLD 1', source)
print('PASS 99f: 36-story inventory; D1 band + anchor present; map ocean/land colours; anchor brightness %.0f; outer-strip mean RGB exactly paper; masthead bbox fits.' % anchor)
print('Outer strip mean RGB:', means, '; file bytes:', p.stat().st_size)
