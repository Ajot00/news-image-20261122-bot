from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (243, 232, 204)
INK = (34, 47, 43)
MUTED = (83, 91, 78)
RED = (174, 57, 43)
GREEN = (82, 111, 91)
GOLD = (201, 151, 62)
BLUE = (93, 126, 143)
PALE = (224, 211, 177)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'

im = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(im)

def f(size, face='sans'):
    path = {'sans': FONT, 'bold': BOLD, 'serif': SERIF}[face]
    return ImageFont.truetype(path, int(size))

def text(x, y, s, size, color=INK, face='sans', anchor=None):
    d.text((x, y), s, font=f(size, face), fill=color, anchor=anchor)

def measure(s, size, face='sans'):
    return d.textbbox((0, 0), s, font=f(size, face))[2]

def wrap(s, width, size, face='sans', max_lines=None):
    words = s.split()
    lines, line = [], ''
    for word in words:
        trial = (line + ' ' + word).strip()
        if line and measure(trial, size, face) > width:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines[-1] and measure(lines[-1] + '…', size, face) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + '…'
    return lines

def paragraph(x, y, s, width, size, color=INK, face='sans', leading=None, max_lines=None):
    leading = leading or int(size * 1.22)
    lines = wrap(s, width, size, face, max_lines)
    for i, line in enumerate(lines):
        text(x, y + i * leading, line, size, color, face)
    return y + len(lines) * leading

def line(x1, y1, x2, y2, color=PALE, width=1):
    d.line((x1, y1, x2, y2), fill=color, width=width)

stories = [
    ('ANTALYA, TÜRKİYE · CLIMATE', 'COP31 closes in on a deal at dawn',
     "After running past Friday's close, presidents unveil a package nearly 200 nations can accept.", 'Reuters'),
    ('MANAMA, BAHRAIN · WAR', 'Iran says it hit US radars in Bahrain',
     'Tehran says missiles and drones hit US radars at al-Riffa and Awali; Bahrain reports a fire, no injuries.', 'IRNA · Al Jazeera'),
    ('HONG KONG · POLITICS', 'Hong Kong votes for its Election Committee',
     'About 5,700 voters choose the 1,500-strong body that picks the chief executive.', 'China Daily · SCMP'),
    ('GULF OF FINLAND · WAR AT SEA', 'Russian ship still burning in Finnish waters',
     'Finland leads the rescue as the Sparta II fire rages on.', 'Reuters'),
    ('WELLINGTON · CRICKET', "Pant's 128 puts India 629/6", "India's highest tally in New Zealand; lead 261 at lunch on day four.", 'Reuters'),
    ('PATNA, INDIA · INFRASTRUCTURE', 'Modi opens Nitish Setu bridge', 'PM inaugurates the bridge linking Patna and Vaishali districts.', 'PTI'),
    ('TALLINN · SECURITY', 'Estonia to shut its Russia border on 1 Dec', 'All five crossings shut after a sabotage bid; families rush to cross.', 'Reuters'),
    ('GAZA · AID', 'Strike hits food aid vehicle', 'Three Palestinians die in an air attack.', 'Al Jazeera · Reuters'),
    ('BRASÍLIA · HEALTH', 'Bolsonaro in intensive care', 'Ex-president stable, breathing on his own.', 'AP'),
    ('SINALOA, MEXICO · CARTELS', "Mexico captures 'El Chapo Isidro'", 'FBI top-ten fugitive flown to the capital; 11 killed in the operation.', 'AP'),
    ('WASHINGTON · SECURITY', 'US airlines warned of terror threat', 'Carriers warned of a possible attack before Thanksgiving.', 'Reports'),
    ('BASRA, IRAQ · DISASTER', 'Four die in fire at Basra power plant', 'A blaze at an electricity facility also injures 35 in the city.', 'Reuters'),
    ('TURIN · TENNIS', 'Zverev meets Alcaraz for ATP Finals title', 'Top two seeds clash at 17:00 GMT.', 'ATP'),
]

briefs = [
    ('14', 'BAYELSA', 'Boat toll 24; search continues', 'NEMA'),
    ('15', 'WASHINGTON', 'Nvidia faces SEC accounting probe', 'Media'),
    ('16', 'JERUSALEM', 'Eisenkot opens Likud coalition talks', 'Maariv'),
    ('17', 'TEHRAN', 'Iran to ration power as grid strains', 'ST'),
    ('18', 'CANBERRA', "Marles: US budget office 'wrong' on AUKUS", 'ABC'),
    ('19', 'MANILA', 'Chinese bomber turns back 170 km from capital', 'AP'),
    ('20', 'MELBOURNE', 'Board backs Cummins as Test captain', 'ABC'),
    ('21', 'NEW YORK', 'Gupta jailed 19 years in Pannun plot', 'Court'),
    ('22', 'TOKYO', 'Japan to train on Indian ranges, first', 'Reports'),
    ('23', 'WASHINGTON', 'Hegseth curbs US–Canada drills', 'Reports'),
    ('24', 'RANCHI', 'Cyclone Akvan axes 14 eastern India flights', 'Reports'),
    ('25', 'KYIV', 'Two killed in overnight Russian strikes', 'Officials'),
    ('26', 'KYIV', "Zelenskyy calls Putin a 'murderer'.", 'Reports'),
    ('27', 'LAS VEGAS', 'Verstappen on pole for Grand Prix', 'Reuters'),
    ('28', 'LIVERPOOL', 'Liverpool host Manchester United at Anfield', 'BBC'),
    ('29', 'MARKETS', 'Bitcoin holds above $60,000', 'Markets'),
    ('30', 'MOGADISHU', 'Somalia expels UAE envoy', 'Reports'),
    ('31', 'COPENHAGEN', 'Denmark expels Russian attaché', 'Guardian'),
    ('32', 'BRUSSELS', 'Air traffic halts for 23 Nov national strike', 'ST'),
    ('33', 'BERLIN', 'IG Metall widens car and shipyard strikes', 'Reuters'),
    ('34', 'LISBON', 'Thousands march over living costs', 'Reuters'),
    ('35', 'DHAKA', '30 Awami League homes set on fire', 'TOI'),
]

# Masthead and date
text(22, 7, 'THE WORLD IN ONE DAY', 13, RED, 'bold')
text(1002, 7, '35 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026', 11, INK, 'bold', 'ra')
text(22, 24, 'Sunday 22 November 2026', 64, INK, 'serif')
text(22, 111, 'COP31 near a deal at dawn · Iran says it hit US radars in Bahrain · Hong Kong votes', 16, RED, 'bold')

# Six-item number strip
numbers = [('~200', 'nations at COP31'), ('03:00', 'GMT objection deadline'), ('2', 'radars Iran says it hit'),
           ('629/6', "India's record total"), ('723', 'Hong Kong seats'), ('700,000', 'displaced in Ethiopia')]
nx = [22, 188, 354, 520, 686, 852]
for i, (value, caption) in enumerate(numbers):
    if i:
        line(nx[i] - 13, 148, nx[i] - 13, 193, (198, 186, 153), 1)
    text(nx[i], 137, value, 32, INK, 'bold')
    paragraph(nx[i], 172, caption, 145, 10, MUTED, 'sans', 11, 2)

# Region tabs with explicit region counts
regions = [('EUROPE 11', GREEN), ('MIDDLE EAST 5', RED), ('AMERICAS 7', BLUE),
           ('ASIA-PACIFIC 6', (99, 110, 82)), ('AFRICA 2', GOLD), ('OCEANIA 3', (81, 118, 126)), ('WORLD 1', MUTED)]
rx = 22
for label, col in regions:
    ww = measure(label, 11, 'bold') + 19
    d.rounded_rectangle((rx, 200, rx + ww, 220), radius=4, fill=col)
    text(rx + 9, 203, label, 11, PAPER, 'bold')
    rx += ww + 8

def art_box(x, y, w, h, kind):
    d.rounded_rectangle((x, y, x + w, y + h), radius=5, fill=(225, 221, 199))
    # Quiet landscape base and sun make each panel read as a drawn vignette.
    d.ellipse((x + w - 42, y + 8, x + w - 24, y + 26), fill=GOLD)
    d.rectangle((x + 1, y + h - 13, x + w - 1, y + h - 1), fill=(205, 211, 189))
    mid = x + w // 2
    if kind == 0:  # climate summit: globe and negotiating table
        d.ellipse((mid - 25, y + 10, mid + 25, y + 60), fill=(104, 146, 151), outline=INK, width=2)
        d.arc((mid - 18, y + 12, mid + 18, y + 58), 40, 300, fill=PAPER, width=2)
        d.arc((mid - 24, y + 25, mid + 24, y + 45), 0, 180, fill=PAPER, width=2)
        d.rectangle((x + 34, y + h - 29, x + w - 34, y + h - 23), fill=(130, 91, 64))
        for px in (x + 62, x + w - 62):
            d.ellipse((px - 9, y + h - 46, px + 9, y + h - 28), fill=RED)
            d.line((px, y + h - 28, px, y + h - 14), fill=INK, width=3)
        d.ellipse((x + w - 80, y + 10, x + w - 52, y + 38), outline=RED, width=2)
        d.line((x + w - 66, y + 14, x + w - 66, y + 24), fill=RED, width=2)
    elif kind == 1:  # Gulf night: skyline, radar dishes, trails
        for j, bh in enumerate((20, 30, 24, 39, 26, 32)):
            bx = x + 20 + j * (w - 40) // 6
            d.rectangle((bx, y + h - 14 - bh, bx + 23, y + h - 14), fill=(64, 86, 100))
            d.rectangle((bx + 5, y + h - 13 - bh, bx + 8, y + h - 16), fill=GOLD)
        for px in (x + 74, x + w - 80):
            d.arc((px - 17, y + 15, px + 17, y + 44), 180, 360, fill=PAPER, width=3)
            d.line((px, y + 30, px, y + 49), fill=PAPER, width=2)
        d.line((x + 14, y + 15, x + 62, y + 29), fill=RED, width=2)
        d.line((x + w - 62, y + 13, x + w - 20, y + 25), fill=RED, width=2)
    elif kind == 2:  # ballot and polling place
        d.rectangle((x + 48, y + 18, x + w - 48, y + h - 14), fill=(185, 153, 105), outline=INK, width=2)
        d.polygon([(x + 45, y + 19), (mid, y + 5), (x + w - 45, y + 19)], fill=RED)
        d.rectangle((mid - 25, y + h - 37, mid + 25, y + h - 14), fill=(128, 93, 63))
        d.polygon([(mid - 10, y + 20), (mid + 8, y + 28), (mid - 8, y + 34)], fill=PAPER)
    elif kind in (3, 6, 10, 11):  # ship / bridge / aircraft / power station
        if kind == 3:
            d.polygon([(x + 37, y + h - 23), (x + w - 35, y + h - 23), (x + w - 53, y + h - 10), (x + 52, y + h - 10)], fill=(65, 94, 111))
            d.rectangle((mid - 31, y + 14, mid + 30, y + h - 24), fill=(176, 177, 151), outline=INK)
            for k in range(4): d.ellipse((mid - 23 + k * 13, y + 8 - (k % 2) * 4, mid - 15 + k * 13, y + 16), fill=RED)
                
        elif kind == 6:
            d.polygon([(x + 30, y + h - 12), (x + 48, y + 22), (x + 63, y + h - 12)], fill=(117, 127, 111))
            d.polygon([(x + w - 65, y + h - 12), (x + w - 49, y + 22), (x + w - 32, y + h - 12)], fill=(117, 127, 111))
            d.line((x + 43, y + 27, x + w - 42, y + 27), fill=RED, width=4)
            d.line((x + 48, y + 27, x + 48, y + h - 12), fill=INK, width=2)
            d.line((x + w - 49, y + 27, x + w - 49, y + h - 12), fill=INK, width=2)
        elif kind == 10:
            d.polygon([(mid - 42, y + 30), (mid + 34, y + 13), (mid + 18, y + 32), (mid + 53, y + 39), (mid + 48, y + 45), (mid + 13, y + 39), (mid - 10, y + 52), (mid - 4, y + 37)], fill=BLUE)
            d.line((mid - 37, y + 30, mid - 54, y + 37), fill=RED, width=2)
        else:
            d.rectangle((x + 42, y + 27, x + w - 42, y + h - 12), fill=(119, 132, 117), outline=INK, width=2)
            for px in (x + 62, x + w - 63):
                d.rectangle((px - 6, y + 10, px + 6, y + 28), fill=(90, 103, 102))
                d.line((px, y + 7, px, y + 1), fill=RED, width=2)
    elif kind in (4, 12):  # cricket equipment / tennis match
        if kind == 4:
            d.polygon([(x + 50, y + 10), (x + 60, y + 10), (x + 54, y + 31),
                       (x + 49, y + 38), (x + 44, y + 35)], fill=GOLD, outline=INK)
            d.line((x + 49, y + 36, x + 46, y + 42), fill=INK, width=3)
            d.ellipse((x + 82, y + 12, x + 92, y + 22), fill=RED, outline=INK)
            for px in (x + w - 47, x + w - 39, x + w - 31):
                d.line((px, y + 13, px, y + 39), fill=INK, width=2)
            d.line((x + w - 49, y + 39, x + w - 29, y + 39), fill=INK, width=2)
        else:
            d.ellipse((mid - 24, y + 10, mid + 24, y + 56), fill=(103, 139, 102), outline=INK, width=2)
            d.line((mid - 15, y + 20, mid + 15, y + 46), fill=PAPER, width=2)
            d.line((mid + 15, y + 20, mid - 15, y + 46), fill=PAPER, width=2)
            d.ellipse((x + 40, y + 16, x + 49, y + 25), fill=GOLD)
            d.ellipse((x + w - 51, y + 42, x + w - 42, y + 51), fill=GOLD)
    elif kind in (5, 7, 8, 9):  # bridge / aid / hospital / capture
        if kind == 5:
            d.arc((x + 28, y + 15, x + w - 28, y + h + 30), 180, 360, fill=RED, width=4)
            d.line((x + 25, y + h - 14, x + w - 25, y + h - 14), fill=INK, width=3)
            for px in range(x + 54, x + w - 45, 35): d.line((px, y + 33, px, y + h - 14), fill=INK, width=1)
        elif kind == 7:
            d.rectangle((x + 42, y + 19, x + w - 42, y + h - 13), fill=(176, 158, 121), outline=INK, width=2)
            d.rectangle((mid - 13, y + h - 37, mid + 13, y + h - 13), fill=RED)
            d.ellipse((mid + 20, y + 15, mid + 37, y + 32), fill=GOLD)
        elif kind == 8:
            d.rectangle((x + 49, y + 20, x + 55, y + 39), fill=BLUE, outline=INK)
            d.rectangle((x + 54, y + 28, x + w - 38, y + 33), fill=(193, 199, 185), outline=INK)
            d.rectangle((x + 60, y + 22, x + 76, y + 28), fill=PAPER, outline=INK)
            d.line((x + 55, y + 39, x + w - 35, y + 39), fill=INK, width=2)
            d.line((x + 65, y + 39, x + 65, y + 43), fill=INK, width=2)
            d.line((x + w - 43, y + 39, x + w - 43, y + 43), fill=INK, width=2)
            d.rectangle((x + w - 70, y + 8, x + w - 44, y + 28), fill=PAPER, outline=INK)
            d.rectangle((x + w - 60, y + 11, x + w - 54, y + 25), fill=RED)
            d.rectangle((x + w - 64, y + 15, x + w - 50, y + 21), fill=RED)
        else:
            d.ellipse((mid - 24, y + 12, mid + 24, y + 60), fill=(198, 174, 139), outline=INK, width=2)
            d.arc((mid - 36, y + 30, mid + 36, y + 68), 180, 360, fill=GREEN, width=5)
    else:  # security, border, fire
        d.polygon([(mid, y + 8), (mid + 34, y + 20), (mid + 29, y + 48), (mid, y + h - 8), (mid - 29, y + 48), (mid - 34, y + 20)], fill=(163, 172, 150), outline=INK)
        d.line((mid - 12, y + 32, mid - 2, y + 42, mid + 16, y + 22), fill=RED, width=3)

def card(index, x, y, w, big=False):
    loc, headline, deck, source = stories[index]
    panel_h = 66 if big else 44
    art_box(x, y, w, panel_h, index)
    # Number set into a quiet red medallion, separate from the illustration.
    d.ellipse((x + 7, y + 6, x + 30, y + 29), fill=RED)
    text(x + 18.5, y + 7, str(index + 1), 12 if big else 11, PAPER, 'bold', 'ma')
    cy = y + panel_h + (5 if big else 3)
    kicker_size = 9 if big else 8
    text(x, cy, loc, kicker_size, RED, 'bold')
    cy += 13 if big else 10
    hs = 20 if big else 16
    hl = paragraph(x, cy, headline, w, hs, INK, 'serif', 22 if big else 17, 2 if big else 3)
    deck_size = 12 if big else 9
    # The compact leads retain their exact facts while wrapping to a fixed line count.
    end = paragraph(x, hl + (2 if big else 1), deck, w, deck_size, MUTED, 'sans', 14 if big else 10, 2)
    text(x, y + 220 if big else end + 1, source, 9 if big else 8, MUTED)

# Three lead cards, then ten compact illustrated cells.
colw = 318
for i, x in enumerate((22, 353, 684)):
    if i:
        line(x - 13, 228, x - 13, 466, (204, 192, 161), 1)
    card(i, x, 228, colw, True)
line(22, 465, 1002, 465, (194, 181, 147), 1)
small_x = [22, 220, 418, 616, 814]
for idx in range(3, 8):
    x = small_x[idx - 3]
    if idx > 3: line(x - 10, 473, x - 10, 747, (210, 198, 166), 1)
    card(idx, x, 474, 188, False)
for idx in range(8, 13):
    x = small_x[idx - 8]
    line(x - 10 if idx > 8 else 22, 612, x - 10 if idx > 8 else 22, 747, (210, 198, 166), 1)
    card(idx, x, 613, 188, False)
line(22, 750, 1002, 750, (194, 181, 147), 1)

# World map panel. Coastlines are hand-drawn equirectangular silhouettes.
mx, my, mw, mh = 22, 762, 300, 171
text(mx, my, 'WHERE STORIES 1–13 HAPPENED', 10, RED, 'bold')
maptop, mapbot = my + 16, my + 139
mapleft, mapright = mx + 2, mx + mw - 2
def project(lon, lat):
    return (mapleft + (lon + 180) / 360 * (mapright - mapleft),
            maptop + (90 - lat) / 180 * (mapbot - maptop))
continents = [
    [(-168,68),(-145,72),(-126,57),(-124,43),(-111,30),(-97,18),(-83,9),(-77,25),(-66,45),(-56,52),(-61,63),(-82,70),(-105,73),(-130,70)],
    [(-81,12),(-70,9),(-52,4),(-35,-8),(-48,-28),(-54,-46),(-69,-56),(-76,-35),(-80,-10)],
    [(-11,36),(-10,54),(4,60),(18,70),(42,68),(61,57),(72,52),(91,55),(108,50),(127,45),(145,52),(165,60),(178,51),(160,39),(142,35),(127,20),(108,8),(95,8),(81,22),(68,25),(58,36),(42,39),(35,32),(28,36),(17,34),(7,37)],
    [(-17,35),(8,37),(33,31),(44,12),(50,-13),(38,-35),(19,-35),(8,-18),(-1,4),(-12,17)],
    [(112,-11),(132,-10),(153,-18),(150,-38),(130,-43),(115,-33)],
    [(-52,60),(-42,59),(-21,68),(-27,82),(-46,83),(-58,72)],
]
for poly in continents:
    pts = [project(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=(162, 174, 145))
    d.line(pts + [pts[0]], fill=(127, 145, 119), width=1)
# understated latitude guides
for lat in (-30, 0, 30, 60):
    yy = project(0, lat)[1]
    for xx in range(int(mapleft), int(mapright), 8):
        d.point((xx, int(yy)), fill=(208, 198, 167))
places = [(30.7,36.9),(50.6,26.2),(114.2,22.3),(26.2,60.5),(174.8,-41.3),(85.1,25.6),(24.7,59.4),(34.5,31.5),(-47.9,-15.8),(-108.5,25.6),(-77.0,38.9),(47.8,30.5),(7.7,45.1)]
for number, (lon, lat) in enumerate(places, 1):
    px, py = project(lon, lat)
    d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=RED, outline=PAPER, width=1)
    text(px, py - 6, str(number), 8, PAPER, 'bold', 'mm')
text(mx, my + 151, 'Red numbers mark stories 1–13', 9, MUTED)

# 22 concise one-line briefs in a two-column ledger.
text(345, 762, 'ALSO ON SUNDAY', 11, RED, 'bold')
line(345, 779, 1002, 779, (194, 181, 147), 1)
brief_columns = (briefs[:11], briefs[11:])
for ci, group in enumerate(brief_columns):
    bx = 345 + ci * 329
    for ri, (num, place, body, source) in enumerate(group):
        yy = 783 + ri * 14
        text(bx, yy, num, 11, RED, 'bold')
        tx = bx + 23
        text(tx, yy, place, 11, INK, 'bold')
        event_x = tx + measure(place, 11, 'bold') + 5
        entry = body + ' · ' + source
        paragraph(event_x, yy + 1, entry, bx + 329 - event_x, 9, INK, 'sans', 10, 1)

# Red-bordered date discipline note, compact but complete.
box = (22, 944, 1002, 1004)
d.rectangle(box, outline=RED, width=2)
text(31, 947, 'DATE CHECK', 10, RED, 'bold')
date_note = ('Wires read to 17:00 UTC, 22 November 2026 · Left out: Peru earthquake (20 Nov local), Russian missiles in Poland (19 Nov), '
             'Kerch Bridge strikes (earlier this week), Shenzhen summit (19 Nov).')
paragraph(116, 947, date_note, 875, 9, INK, 'sans', 11, 1)
date_note2 = ('Not yet: COP31 final approval, ATP champion, Vegas winner · All above happened or were first reported Sunday 22 November 2026 in at least one time zone · '
              'Government and armed-group claims are attributed.')
paragraph(31, 972, date_note2, 960, 9, INK, 'sans', 11, 1)
text(22, 1008, 'Sources named beside each story · Drawings and map: original, drawn in code', 8, MUTED)
text(1002, 1008, 'THE WORLD IN ONE DAY · SUNDAY 22 NOVEMBER 2026 · ONE PAGE', 8, MUTED, 'bold', 'ra')

Path('out').mkdir(exist_ok=True)
im.save('out/candidate.png', format='JPEG', quality=89, subsampling=0)
