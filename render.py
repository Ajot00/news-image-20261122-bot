from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
PAPER = (243, 232, 204)
INK = (34, 47, 43)
MUTED = (83, 91, 78)
RED = (174, 57, 43)
GREEN = (82, 111, 91)
GOLD = (201, 151, 62)
im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(size, bold=False):
    return ImageFont.truetype(bold_path if bold else font_path, size)

def text(x, y, s, size, color=INK, bold=False):
    d.text((x, y), s, font=font(size, bold), fill=color)

def wrap_words(s, f, width):
    out, line = [], ""
    for word in s.split():
        test = word if not line else line + " " + word
        if d.textbbox((0, 0), test, font=f)[2] <= width:
            line = test
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out

def paragraph(x, y, s, size, width, color=MUTED, max_lines=3, gap=3):
    f = font(size)
    lines = wrap_words(s, f, width)[:max_lines]
    for i, line in enumerate(lines):
        d.text((x, y + i * (size + gap)), line, font=f, fill=color)

def rule(y, x1=34, x2=990, color=INK, width=2):
    d.line((x1, y, x2, y), fill=color, width=width)

# Masthead
text(34, 20, "THE WORLD", 39, INK, True)
d.line((279, 27, 279, 76), fill=RED, width=4)
text(299, 24, "SUNDAY 22 NOVEMBER 2026", 30, RED, True)
text(35, 70, "WORLD NEWS  /  ONE DAY, SIX CONTINENTS", 14, MUTED, True)
rule(98, color=INK, width=4)

# Dominant COP31 lead with flat Antalya scene.
text(36, 112, "COP31: STILL NO DEAL", 38, RED, True)
text(38, 161, "ANTALYA  ·  CLIMATE SUMMIT", 15, GREEN, True)
paragraph(38, 190,
          "Talks run into Sunday with no agreement as about 200 nations stay deadlocked on fossil fuels and the $120bn adaptation target. EU climate chief Hoekstra: “good deal or no deal”.",
          20, 558, INK, 4, 5)
# Sun, mountains and sea: hand-drawn vector shapes, no external art.
d.rectangle((650, 126, 986, 319), fill=(233, 219, 183))
d.ellipse((826, 148, 902, 224), fill=GOLD)
d.polygon([(650, 262), (728, 190), (786, 250), (843, 177), (927, 263), (986, 220), (986, 319), (650, 319)], fill=(126, 145, 112))
d.polygon([(650, 273), (725, 224), (784, 279), (852, 219), (923, 276), (986, 239), (986, 319), (650, 319)], fill=(91, 116, 99))
d.rectangle((650, 278, 986, 319), fill=(90, 145, 151))
for yy in (288, 299, 310):
    d.line((671, yy, 965, yy), fill=(172, 192, 171), width=2)
text(663, 323, "ANTALYA · TALKS OVERNIGHT", 12, GREEN, True)
rule(350, color=RED, width=4)

# Six equal news cards, in the specified order.
cards = [
    ("UKRAINE: 2 KILLED IN OVERNIGHT STRIKES", "Russian strikes across Ukraine overnight; at least two people killed."),
    ("SPARTA II STILL BURNING", "After Saturday’s drone strike in the Gulf of Finland, firefighting continues off Loviisa. All 16 crew evacuated; Finland tightens air and sea curbs."),
    ("BASRA FIRE: 4 DEAD", "Fire at an electricity plant in Basra, Iraq, kills four and injures 35."),
    ("MODI OPENS NITISH SETU", "PM Narendra Modi inaugurates the bridge linking Patna and Vaishali districts in Bihar."),
    ("ESTONIA TO SHUT RUSSIA BORDER", "Tallinn will close its Russia border; Moscow decries a “new Iron Curtain”."),
    ("HEGSETH LIMITS US–CANADA TIES", "Pentagon curbs informal military gatherings with Canadian counterparts."),
]
left, right, gutter = 36, 988, 22
cw = (right-left-2*gutter)//3
card_y = [365, 511]
for idx, (head, body) in enumerate(cards):
    row, col = divmod(idx, 3)
    x, y = left + col*(cw+gutter), card_y[row]
    if col:
        d.line((x-11, y, x-11, y+130), fill=(184, 169, 137), width=1)
    d.ellipse((x, y+5, x+9, y+14), fill=RED)
    hf = font(18, True)
    lines = wrap_words(head, hf, cw-17)[:2]
    for j, line in enumerate(lines):
        d.text((x+16, y+j*22), line, font=hf, fill=INK)
    paragraph(x, y+49, body, 16, cw-8, MUTED, 3, 3)
    if row == 0:
        d.line((x, y+137, x+cw, y+137), fill=(184, 169, 137), width=1)
rule(657, color=INK, width=2)

# The world map strip: muted landmass silhouettes with six red pins and large labels.
text(36, 667, "THE WORLD TODAY", 17, RED, True)
# Abstract, intentionally simplified continent shapes.
d.polygon([(88, 711),(119,697),(154,706),(166,721),(148,733),(133,750),(116,742),(104,727)], fill=(207, 201, 170))
d.polygon([(182, 742),(205,730),(226,740),(222,764),(210,779),(197,765)], fill=(207,201,170))
d.polygon([(411,706),(445,698),(474,710),(468,727),(442,730),(425,720)], fill=(207,201,170))
d.polygon([(450,734),(469,734),(479,758),(465,780),(452,761)], fill=(207,201,170))
d.polygon([(520,705),(570,697),(610,710),(635,727),(612,740),(576,733),(558,747),(532,730)], fill=(207,201,170))
d.polygon([(573,746),(599,745),(610,764),(598,780),(580,765)], fill=(207,201,170))
d.polygon([(704,710),(734,702),(764,711),(785,729),(763,740),(735,734)], fill=(207,201,170))
d.polygon([(843,746),(873,740),(894,751),(882,764),(855,763)], fill=(207,201,170))
pins = [(451,710), (531,711), (539,700), (565,735), (545,724), (880,753)]
for px,py in pins:
    d.ellipse((px-5,py-5,px+5,py+5), fill=RED, outline=PAPER, width=1)
for x, label in zip((38, 198, 358, 518, 678, 838),
                    ("ANTALYA", "UKRAINE", "BALTIC", "BASRA", "PATNA", "WELLINGTON")):
    text(x, 775, label, 14, INK, True)
rule(798, color=RED, width=3)

# Eight concise briefs, two orderly rows of four.
briefs = [
    ("AKVAN: 14 FLIGHTS AXED", "Cyclone disrupts flights at Ranchi."),
    ("CUMMINS KEEPS CAPTAINCY", "Cricket Australia backs him unanimously."),
    ("INDIA v NZ IN WELLINGTON", "First Test continues into day three."),
    ("TRUMP IN SHENZHEN", "APEC arrival; Xi–Putin trilateral planned."),
    ("ZELENSKYY: PUTIN A ‘MURDERER’", "After Trump calls Putin his friend."),
    ("GUPTA JAILED 19 YEARS", "Nikhil Gupta sentenced in Pannun case."),
    ("US AIRLINES WARNED", "Possible al-Qaeda-linked threats before Thanksgiving."),
    ("JAPAN TO TRAIN IN INDIA", "Japanese forces to use Indian ranges, a first."),
]
brief_left, brief_gap = 36, 16
bw = (952 - 3*brief_gap)//4
for idx, (head, body) in enumerate(briefs):
    row, col = divmod(idx, 4)
    x, y = brief_left + col*(bw+brief_gap), 814 + row*91
    if col:
        d.line((x-9, y, x-9, y+76), fill=(184,169,137), width=1)
    d.rectangle((x, y+3, x+6, y+9), fill=RED)
    hf = font(15, True)
    hlines = wrap_words(head, hf, bw-8)[:2]
    for j,line in enumerate(hlines):
        d.text((x+11, y+j*18), line, font=hf, fill=INK)
    paragraph(x, y+41, body, 14, bw-5, MUTED, 2, 2)
    if row == 0:
        d.line((x, y+81, x+bw, y+81), fill=(184,169,137), width=1)
rule(1004, color=INK, width=2)
text(36, 1008, "SUNDAY EDITION  ·  REPORTING FROM 6 REGIONS", 11, MUTED, True)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
im.save(out, format="JPEG", quality=89, optimize=True, progressive=False, subsampling=0)
