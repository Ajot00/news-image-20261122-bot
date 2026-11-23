# candidate99f — news-image-20261122 cycle 5 (D1 + photorealistic render)
# Design: references-cycle5.md (D1) + cycle5-spec.md. Same 36 stories as 99e.
# All art is code-drawn (no photographs — RULES.txt line 62 licence clause).
from PIL import Image, ImageDraw, ImageFont
import os, random

W = H = 1024
PAPER = (243, 232, 204); INK = (34, 47, 43); MUTED = (83, 91, 78)
RED = (174, 57, 43); GREEN = (82, 111, 91); GOLD = (201, 151, 62)
NIGHT = (30, 48, 62); BLUE = (73, 111, 132)
im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
base = '/usr/share/fonts/truetype/dejavu/'
lib = '/usr/share/fonts/truetype/liberation/'
def font(name, size): return ImageFont.truetype(base + name, size)
ser = lambda n: font('DejaVuSerif-Bold.ttf', n)
sans = lambda n: font('DejaVuSans.ttf', n)
bold = lambda n: font('DejaVuSans-Bold.ttf', n)
lser = lambda n: ImageFont.truetype(lib + 'LiberationSerif-Bold.ttf', n)
lita = lambda n: ImageFont.truetype(lib + 'LiberationSerif-Italic.ttf', n)
def txt(x, y, s, f=sans(12), c=INK): d.text((x, y), s, font=f, fill=c)
def fit(s, f, maxw):
    while d.textbbox((0, 0), s, font=f)[2] > maxw and len(s) > 1: s = s[:-1]
    return s
def wrap(s, f, w, limit=2):
    words = s.split(); lines = []; cur = ''
    for word in words:
        q = (cur + ' ' + word).strip()
        if d.textbbox((0, 0), q, font=f)[2] <= w: cur = q
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines[:limit]
def lines(x, y, s, f, c, w, leading, limit=2):
    for j, ln in enumerate(wrap(s, f, w, limit)): txt(x, y + j * leading, ln, f, c)
def rect(box, fill, outline=None, width=1): d.rectangle(box, fill=fill, outline=outline, width=width)
def line(points, fill, width=1): d.line(points, fill=fill, width=width)
def ellipse(box, fill, outline=None, width=1): d.ellipse(box, fill=fill, outline=outline, width=width)
def poly(points, fill): d.polygon(points, fill=fill)

# ---- photographic light tools (all deterministic) ----
def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def vgrad(x0, y0, x1, y1, c0, c1):
    h = max(1, y1 - y0)
    for k in range(h):
        d.rectangle((x0, y0 + k, x1, y0 + k), fill=lerp(c0, c1, k / h))
def hgrad(x0, y0, x1, y1, c0, c1):
    w = max(1, x1 - x0)
    for k in range(w):
        d.rectangle((x0 + k, y0, x0 + k, y1), fill=lerp(c0, c1, k / w))
def glow(cx, cy, rx, ry, core, edge, steps=7):
    for k in range(steps, 0, -1):
        t = k / steps
        d.ellipse((cx - rx * t, cy - ry * t, cx + rx * t, cy + ry * t), fill=lerp(edge, core, 1 - t))
def grain(x0, y0, x1, y1, seed, n, cols, r=1):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.randint(x0, x1); y = rnd.randint(y0, y1)
        d.ellipse((x, y, x + r, y + r), fill=cols[rnd.randrange(len(cols))])
def shimmer(x0, y0, x1, y1, seed, n, col):
    rnd = random.Random(seed)
    for _ in range(n):
        y = rnd.randint(y0, y1); a = rnd.randint(x0, x1 - 30)
        d.line([(a, y), (a + rnd.randint(8, 30), y)], fill=col, width=1)

def photo(i, box):
    x, y, w, h = box
    def X(a): return int(x + a * w)
    def Y(a): return int(y + a * h)
    def R(a, b, c, e, col, ol=None, wd=1): rect((X(a), Y(b), X(c), Y(e)), col, ol, wd)
    def L(pts, col, wd=1): line([(X(a), Y(b)) for a, b in pts], col, wd)
    def E(a, b, c, e, col, ol=None, wd=1): ellipse((X(a), Y(b), X(c), Y(e)), col, ol, wd)
    def P(pts, col): poly([(X(a), Y(b)) for a, b in pts], col)
    def VG(a, b, c0, c1): vgrad(X(a), Y(b), X(1), Y(1), c0, c1)
    if i == 1:  # COP31 — dawn hall, warm light
        vgrad(x, y, x + w, y + h, (233, 178, 112), (168, 186, 166))
        glow(X(.82), Y(.16), int(w * .16), int(h * .22), (255, 226, 150), (233, 178, 112))
        E(.78, .06, .90, .24, (255, 232, 170))
        R(0, .48, 1, 1, (52, 74, 72))
        for k in range(6):  # lit delegate windows
            R(.06 + k * .16, .56, .15 + k * .16, .74, (247, 196, 121))
            R(.06 + k * .16, .80, .15 + k * .16, .94, (214, 178, 110))
        E(.38, .30, .62, .52, (120, 168, 150), (52, 74, 72), 3)  # globe
        P([(.40, .52), (.44, .38), (.50, .52)], (120, 168, 150))
        P([(.52, .52), (.58, .36), (.62, .52)], (120, 168, 150))
        for k in range(7):  # flags
            R(.06 + k * .135, .94, .12 + k * .135, 1, [RED, GREEN, GOLD, BLUE][k % 4])
        grain(x, y, x + w, y + int(h * .4), 11, 40, [(255, 240, 200), (240, 200, 140)])
        R(.04, .06, .30, .18, (36, 52, 50))
        txt(X(.07), Y(.075), 'COP31', bold(max(9, int(h * .11))), PAPER)
    elif i == 2:  # BAHRAIN — D1 bright display-type anchor
        vgrad(x, y, x + w, y + h, (240, 231, 201), (226, 211, 172))
        R(0, .06, 1, .09, RED)
        t1 = 'BAHRAIN'; t2 = 'STRUCK'
        f1 = lser(46); f2 = lser(46)
        w1 = d.textbbox((0, 0), t1, font=f1)[2]; w2 = d.textbbox((0, 0), t2, font=f2)[2]
        txt(x + (w - w1) // 2, y + int(h * .13), t1, f1, INK)
        txt(x + (w - w2) // 2, y + int(h * .42), t2, f2, RED)
        line([(X(.18), Y(.68)), (X(.82), Y(.68))], RED, 2)
        R(.485, .74, .515, .85, INK)  # small radar mast, centred
        E(.44, .72, .56, .80, (60, 72, 70), INK, 2)
        L([(.50, .76), (.62, .76)], GOLD, 2)
        E(.04, .10, .12, .22, (255, 214, 120))  # small sun disc, left
        grain(x, y + int(h * .85), x + w, y + h, 21, 24, [(200, 182, 140)])
    elif i == 3:  # KYIV — night barrage, fire glow
        vgrad(x, y, x + w, y + h, (14, 26, 46), (40, 56, 76))
        grain(x, y, x + w, y + int(h * .35), 31, 60, [(205, 197, 160), (240, 230, 190)])
        R(0, .62, 1, 1, (16, 26, 34))
        for k in range(9):  # skyline with lit windows
            a = .02 + k * .105; hh = .24 + ((k * 37) % 30) / 100
            R(a, .62 - hh, a + .075, .62, (36, 52, 64))
            for j in range(2):
                R(a + .015 + j * .03, .62 - hh + .05, a + .03 + j * .03, .62 - hh + .09, (247, 196, 121))
        glow(X(.36), Y(.74), int(w * .13), int(h * .14), (255, 150, 60), (255, 120, 40))
        E(.28, .66, .44, .82, (255, 139, 63)); E(.33, .70, .39, .77, (255, 196, 80))
        glow(X(.73), Y(.77), int(w * .10), int(h * .11), (255, 150, 60), (255, 120, 40))
        E(.66, .70, .80, .84, (255, 139, 63))
        for pts in [[(.10, .06), (.22, .22), (.38, .34)], [(.55, .02), (.62, .18), (.78, .30)],
                    [(.82, .08), (.76, .24), (.66, .34)]]:
            L(pts, (247, 196, 121), 2)  # drone trails
        L([(.06, .90), (.20, .60), (.32, .88)], (244, 222, 155), 2)
        L([(.92, .90), (.78, .62), (.66, .86)], (244, 222, 155), 2)
        R(.46, .30, .54, .62, (52, 66, 74))
    elif i == 14:  # HONG KONG — polling day, warm daylight
        vgrad(x, y, x + w, y + h, (196, 212, 222), (232, 220, 190))
        glow(X(.85), Y(.12), int(w * .12), int(h * .16), (255, 236, 170), (232, 220, 190))
        R(0, .68, 1, 1, (128, 118, 88))
        R(.06, .22, .32, .68, (214, 200, 168))  # ballot box
        R(.06, .22, .32, .30, (172, 140, 96))
        L([(.16, .26), (.22, .26)], INK, 3)
        R(.68, .48, .92, .88, (47, 57, 54), GOLD, 2)  # voting booth
        R(.71, .62, .89, .68, (233, 222, 193))
        for a in [.34, .50, .66]:  # voters
            E(a, .30, a + .09, .44, (232, 184, 136))
            R(a + .015, .43, a + .07, .68, (45, 67, 60))
        R(.68, .14, .90, .28, (239, 224, 190))
        txt(X(.70), Y(.16), 'POLL', bold(9), INK)
        for k in range(3): R(.74 + k * .06, .52 + k * .04, .78 + k * .06, .58 + k * .04, PAPER)
        grain(x, y, x + w, y + int(h * .3), 141, 24, [(255, 250, 230)])
    elif i == 4:  # SPARTA II — ship fire at dusk, sea
        vgrad(x, y, x + w, y + h, (96, 116, 134), (226, 148, 84))
        R(0, .66, 1, 1, (40, 62, 74))
        shimmer(x, y + int(h * .70), x + w, y + int(h * .95), 41, 26, (226, 148, 84))
        P([(.13, .59), (.20, .51), (.77, .53), (.92, .62), (.84, .72), (.25, .75)], (58, 71, 72))
        R(.42, .39, .72, .56, (73, 79, 74)); R(.50, .32, .63, .40, (104, 100, 82))
        glow(X(.60), Y(.42), int(w * .12), int(h * .14), (255, 140, 50), (226, 148, 84))
        P([(.50, .52), (.54, .28), (.58, .43), (.63, .24), (.66, .50), (.72, .54)], (225, 105, 43))
        P([(.54, .49), (.57, .36), (.60, .50), (.64, .34), (.67, .53)], GOLD)
        E(.50, .07, .64, .28, (83, 93, 96)); E(.56, .02, .75, .22, (57, 68, 75))
        P([(.79, .74), (.90, .66), (.99, .71), (.96, .80), (.81, .80)], (169, 139, 96))
        L([(.75, .65), (.90, .39), (.98, .66)], (244, 222, 155), 3)
        E(.69, .14, .78, .20, (76, 88, 91)); L([(.72, .17), (.75, .12)], (76, 88, 91), 3)
        grain(x, y, x + w, y + int(h * .25), 42, 20, [(255, 220, 170)])
    elif i == 5:  # CRICKET — bright day match
        vgrad(x, y, x + w, y + int(h * .45), (168, 205, 228), (226, 232, 210))
        vgrad(x, y + int(h * .45), x + w, y + h, (96, 146, 92), (58, 108, 66))
        glow(X(.85), Y(.10), int(w * .12), int(h * .15), (255, 240, 180), (226, 232, 210))
        R(.62, .02, .88, .12, (31, 62, 49), GOLD, 2)
        txt(X(.64), Y(.04), '720/9', bold(13), (228, 215, 150))
        R(.30, .55, .70, .95, (206, 184, 140))  # pitch
        for k in range(3): R(.04 + k * .07, .73, .09 + k * .07, .97, (102, 82, 64))
        E(.38, .27, .45, .37, (199, 145, 98))  # batsman
        L([(.42, .36), (.43, .56), (.32, .63)], INK, 5)
        L([(.43, .48), (.55, .34)], INK, 4); L([(.43, .54), (.49, .66)], INK, 4)
        L([(.39, .40), (.32, .30)], INK, 4)
        E(.82, .51, .88, .57, (186, 138, 97))  # keeper
        L([(.85, .56), (.82, .70), (.89, .71)], INK, 4)
        for k in range(3):
            R(.79 + k * .045, .70, .81 + k * .045, .81, PAPER)
            R(.785 + k * .045, .68, .815 + k * .045, .71, RED)
        E(.56, .31, .59, .34, RED)
        for k in range(4): R(.91, .03 + k * .09, .94, .10 + k * .09, GOLD)
        grain(x, y + int(h * .5), x + w, y + h, 51, 30, [(140, 180, 120), (70, 120, 80)])
    elif i == 6:  # BRIDGE — sky, river shimmer, cables
        vgrad(x, y, x + w, y + h, (150, 190, 205), (226, 222, 196))
        glow(X(.80), Y(.12), int(w * .13), int(h * .16), (255, 238, 175), (226, 222, 196))
        R(0, .53, .45, 1, (53, 119, 151)); R(.57, .53, 1, 1, (53, 119, 151))
        R(.45, .48, .57, 1, (111, 105, 85))
        shimmer(x, y + int(h * .60), x + w, y + int(h * .95), 61, 22, (200, 220, 225))
        for a in [.20, .78]:
            R(a - .035, .12, a + .035, .62, (97, 76, 61)); R(a - .045, .12, a + .045, .17, GOLD)
        for k in range(7):
            L([(.20, .15), (.45 + k * .017, .53)], (83, 71, 60), 1)
            L([(.78, .15), (.57 - k * .017, .53)], (83, 71, 60), 1)
        L([(.20, .40), (.78, .40)], (75, 68, 58), 2); L([(.15, .60), (.85, .60)], (74, 65, 54), 2)
        for a in [.43, .55]: R(a, .65, a + .045, .70, (193, 181, 146))
        for k in range(4): R(.19 + k * .04, .10, .21 + k * .04, .15, [RED, GOLD, GREEN][k % 3])
    elif i == 7:  # TALLINN — border fence at dusk
        vgrad(x, y, x + w, y + h, (120, 128, 148), (216, 178, 130))
        glow(X(.76), Y(.30), int(w * .11), int(h * .14), (255, 210, 130), (216, 178, 130))
        R(0, .58, 1, 1, (52, 62, 65))
        for k in range(7): L([(k * .15, .25), (k * .15, .78)], (117, 119, 109), 2)
        R(.69, .17, .83, .50, (51, 62, 67))  # booth
        R(.73, .21, .80, .28, (236, 205, 128))
        R(.03, .56, .45, .60, (197, 57, 44)); L([(.42, .57), (.62, .34)], PAPER, 4)
        for k in range(3):  # cars with headlights
            a = .12 + k * .18
            R(a, .67, a + .12, .76, (68, 93, 104))
            E(a + .02, .63, a + .10, .70, (92, 111, 115))
            E(a + .015, .74, a + .045, .78, INK); E(a + .085, .74, a + .115, .78, INK)
            glow(X(a + .06), Y(.72), int(w * .05), int(h * .06), (255, 240, 170), (216, 178, 130), 4)
        for k in range(3):
            E(.54 + k * .10, .51, .58 + k * .10, .61, (181, 140, 105))
            R(.55 + k * .1, .60, .58 + k * .1, .69, (48, 65, 66))
            R(.59 + k * .1, .61, .61 + k * .1, .67, GOLD)
        R(.03, .28, .16, .47, (74, 85, 82)); R(.08, .21, .12, .28, GOLD)
    elif i == 8:  # GAZA — aid vehicle, dusty daylight
        vgrad(x, y, x + w, y + h, (222, 206, 170), (196, 168, 128))
        glow(X(.86), Y(.12), int(w * .12), int(h * .15), (255, 238, 180), (222, 206, 170))
        R(0, .68, 1, 1, (166, 141, 101))
        for k in range(5): L([(0, .75 + k * .04), (1, .70 + k * .04)], (194, 162, 112), 1)
        R(.06, .38, .67, .72, (237, 235, 218))  # truck body
        R(.13, .27, .55, .43, (249, 244, 224))
        R(.15, .48, .27, .65, RED); L([(.21, .51), (.21, .62)], PAPER, 3); L([(.16, .565), (.26, .565)], PAPER, 3)
        R(.66, .46, .92, .70, (236, 227, 202)); R(.72, .37, .87, .48, (245, 235, 210))
        R(.11, .72, .36, .90, (173, 70, 51))
        P([(.11, .72), (.22, .60), (.36, .72)], RED); L([(.19, .72), (.19, .90)], PAPER, 2)
        for k in range(4): R(.29 + k * .06, .52 - (k % 2) * .09, .34 + k * .06, .60 - (k % 2) * .09, (149, 110, 66))
        for a in [.48, .57]:
            E(a, .55, a + .035, .61, (118, 83, 57)); R(a + .005, .60, a + .03, .70, (42, 65, 61))
            L([(a + .01, .62), (a - .02, .68)], INK, 2)
        grain(x, y + int(h * .65), x + w, y + h, 81, 36, [(150, 125, 90), (180, 155, 120)])
    elif i == 9:  # BOLSONARO — hospital room, warm window light
        vgrad(x, y, x + w, y + h, (228, 232, 222), (206, 212, 200))
        R(.70, .06, .96, .34, (242, 245, 231)); L([(.83, .06), (.83, .34)], (105, 127, 116), 2)
        glow(X(.83), Y(.20), int(w * .12), int(h * .15), (255, 244, 200), (228, 232, 222))
        R(.08, .52, .78, .68, (49, 69, 70))  # bed frame
        R(.12, .41, .75, .54, (224, 215, 192))  # mattress
        R(.16, .50, .65, .70, (202, 191, 169))
        E(.16, .43, .25, .53, (192, 148, 116))  # patient head
        R(.24, .47, .64, .62, (67, 87, 87))
        for a in [.72, .88]:  # monitors
            R(a, .20, a + .09, .39, (40, 57, 56), GOLD, 1)
            L([(a + .01, .30), (a + .025, .30), (a + .04, .25), (a + .055, .34), (a + .08, .27)], (111, 255, 137), 4)
            R(a + .02, .39, a + .07, .46, (61, 81, 73))
        L([(.08, .18), (.08, .76)], INK, 3); L([(.04, .76), (.13, .76)], INK, 2)
        E(.04, .10, .13, .22, (220, 221, 201)); L([(.085, .22), (.085, .46)], (104, 141, 156), 2)
        E(.48, .31, .54, .38, (169, 122, 93)); R(.49, .37, .55, .51, (55, 75, 69))
        L([(.52, .40), (.61, .51)], INK, 3)
    elif i == 10:  # SINALOA — desert dusk, plane on runway
        vgrad(x, y, x + w, y + h, (198, 132, 96), (96, 84, 110))
        glow(X(.80), Y(.30), int(w * .14), int(h * .16), (255, 190, 110), (198, 132, 96))
        P([(0, .74), (.12, .53), (.29, .69), (.44, .48), (.60, .67), (.78, .51), (1, .70), (1, 1), (0, 1)], (86, 92, 91))
        R(0, .74, 1, 1, (66, 62, 66))
        L([(.65, .22), (.49, .67), (.85, .68)], (229, 213, 157), 3)  # flight path
        P([(.09, .67), (.47, .65), (.68, .69), (.49, .72), (.24, .72), (.18, .82), (.13, .82), (.16, .72)], (210, 214, 204))
        P([(.34, .67), (.42, .51), (.48, .52), (.45, .67)], (172, 190, 190))
        P([(.57, .68), (.68, .60), (.72, .61), (.65, .69)], (172, 190, 190))
        for a in [.37, .62]:
            E(a, .59, a + .05, .67, (181, 140, 101))
            L([(a + .02, .66), (a + .01, .78)], INK, 4); L([(a + .01, .70), (a - .03, .75)], INK, 3)
        R(.79, .67, .94, .74, (72, 78, 77))
        E(.81, .64, .87, .70, (235, 200, 109)); E(.89, .64, .95, .70, (235, 200, 109))
        grain(x, y, x + w, y + int(h * .3), 101, 26, [(255, 210, 150)])
    elif i == 11:  # AIRLINES — blue sky, jet, beacon
        vgrad(x, y, x + w, y + h, (126, 168, 198), (214, 226, 232))
        glow(X(.82), Y(.14), int(w * .11), int(h * .14), (255, 242, 190), (214, 226, 232))
        for k in range(3): E(.08 + k * .20, .04, .40 + k * .2, .30, (233, 236, 240), None)
        R(0, .50, 1, 1, (66, 74, 82)); R(0, .40, 1, .55, (192, 119, 82))
        R(.78, .18, .88, .64, (56, 67, 76)); R(.80, .10, .86, .22, (202, 165, 118))
        R(.82, .03, .84, .11, (219, 195, 144))
        P([(.09, .67), (.47, .65), (.68, .69), (.49, .72), (.24, .72), (.18, .82), (.13, .82), (.16, .72)], (210, 214, 204))
        P([(.34, .67), (.42, .51), (.48, .52), (.45, .67)], (172, 190, 190))
        P([(.57, .68), (.68, .60), (.72, .61), (.65, .69)], (172, 190, 190))
        R(.79, .47, .97, .78, (233, 213, 150), INK, 2)  # warning sign
        P([(.88, .51), (.96, .72), (.80, .72)], RED)
        txt(X(.855), Y(.59), '!', bold(12), PAPER)
        P([(.68, .14), (.75, .06), (.82, .14), (.79, .26), (.69, .27)], (194, 207, 192))
        P([(.71, .13), (.76, .08), (.80, .14)], (194, 207, 192))
        glow(X(.90), Y(.62), int(w * .07), int(h * .08), (255, 120, 80), (233, 213, 150), 4)
    elif i == 12:  # BASRA — industrial fire at dusk
        vgrad(x, y, x + w, y + h, (150, 110, 88), (74, 70, 66))
        R(0, .72, 1, 1, (78, 76, 67))
        R(.10, .43, .43, .79, (108, 105, 86)); R(.51, .34, .87, .79, (99, 93, 77))
        for a in [.20, .33, .63, .78]:  # cooling towers
            R(a, .14, a + .055, .48, (91, 95, 87))
            P([(a, .14), (a + .02, .05), (a + .055, .14)], (80, 85, 82))
        glow(X(.70), Y(.40), int(w * .16), int(h * .18), (255, 150, 55), (150, 110, 88))
        P([(.58, .40), (.63, .17), (.68, .39), (.72, .20), (.77, .47), (.85, .36), (.84, .57), (.57, .58)], (255, 119, 43))
        P([(.62, .47), (.66, .29), (.70, .49), (.76, .32), (.80, .52)], (255, 205, 82))
        E(.12, .63, .18, .70, (197, 144, 106)); R(.14, .69, .17, .82, INK)
        E(.35, .63, .41, .70, (197, 144, 106)); R(.37, .69, .40, .82, INK)
        R(.02, .76, .20, .85, (177, 60, 42)); R(.05, .72, .13, .77, (219, 195, 130))
        E(.04, .82, .09, .88, INK); E(.14, .82, .19, .88, INK)
        L([(.16, .74), (.42, .54), (.69, .49)], (174, 203, 213), 4)
        grain(x, y + int(h * .55), x + w, y + h, 121, 30, [(255, 170, 90), (120, 100, 85)])

top = [('ANTALYA, TÜRKIYE · CLIMATE', 'COP31 closes in on a deal at dawn', 'After running past Friday’s close, presidents unveil a package nearly 200 nations can accept. Objections shut at 03:00 GMT; approval opens at 06:00.', 'REUTERS', '~200 NATIONS'), ('MANAMA, BAHRAIN · WAR', 'Iran says it hit US radars in Bahrain', 'Tehran says missiles and drones hit US radars at al-Riffa and Awali; Bahrain says a civilian site caught fire, no injuries.', 'IRNA · AL JAZEERA', '2 BASES'), ('KYIV, UKRAINE · WAR', 'Russia’s overnight barrage: 186 drones, 161 downed', 'Moscow fired 186 drones and 3 ballistic missiles overnight; Ukraine shot down or jammed 161. Strikes hit 18 sites; 2 killed in Kyiv.', 'OFFICIALS · REUTERS', '161 DOWNED')]
# small: (kicker, headline, deck, source, chip, banner colour by region)
AP = (125, 91, 66); EU = (82, 111, 91); OC = (70, 105, 95); AM = (93, 112, 127)
small = [('HONG KONG · POLITICS', 'Hong Kong votes for its Election Committee', '5,700 voters choose the Election Committee; 856 candidates chase 723 seats.', 'CHINA DAILY · SCMP', '723 SEATS', AP), ('GULF OF FINLAND · WAR AT SEA', 'Russian ship still burning in Finnish waters', 'Finland leads rescue as Sparta II fire rages on.', 'REUTERS', '16 CREW SAFE', EU), ('WELLINGTON · CRICKET', 'India declare 720/9 — a record in NZ', 'Pant’s 128 and Rahul’s 136 take India past NZ’s biggest Test total; declared at 720/9.', 'REUTERS', '720/9', OC), ('PATNA, INDIA · INFRASTRUCTURE', 'Modi opens Nitish Setu bridge', 'PM inaugurates bridge linking Patna and Vaishali districts.', 'PTI', 'BRIDGE OPENS', AP), ('TALLINN · SECURITY', 'Estonia to shut its Russia border on 1 Dec', 'All five crossings shut after sabotage bid; families rush to cross.', 'REUTERS', '1 DEC', EU), ('GAZA · AID', 'Strike hits food aid vehicle', 'Three Palestinians die in an air attack.', 'AL JAZEERA · REUTERS', '3 KILLED', RED), ('BRASÍLIA · HEALTH', 'Bolsonaro in intensive care', 'Ex-president stable, breathing on his own.', 'AP', 'ICU', AM), ('SINALOA, MEXICO · CARTELS', 'Mexico captures “El Chapo Isidro”', 'FBI top-ten fugitive flown to capital; 11 killed in operation.', 'AP', '11 KILLED', AM), ('WASHINGTON · SECURITY', 'US airlines warned of terror threat', 'Carriers warned of possible al-Qaeda-linked attack before Thanksgiving.', 'REPORTS', 'AL-QAEDA LINK', AM), ('BASRA, IRAQ · DISASTER', 'Four die in fire at Basra power plant', 'Blaze at electricity facility also injures 35 in the city.', 'REUTERS', '4 DEAD', RED)]

# Masthead and page furniture
rect((0, 8, 1023, 28), (0, 0, 0))
txt(24, 10, 'THE WORLD IN ONE DAY · 36 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026', bold(9), PAPER)
txt(24, 27, 'Sunday 22 November 2026', ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf', 85), INK)
txt(24, 124, "COP31's final text lands at dawn · Iran says it hit US radars in Bahrain · 186 drones over Ukraine overnight", ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf', 14), RED)
nums = [('~200', 'nations at COP31 talks'), ('03:00', 'GMT objection deadline'), ('186', 'drones over Ukraine overnight'), ('720/9', 'India’s record total in NZ'), ('723', 'Hong Kong seats'), ('700,000', 'displaced in Ethiopia')]
for k, (a, b) in enumerate(nums):
    x = 24 + k * 164
    if k: line([(x - 9, 133), (x - 9, 173)], (181, 169, 143), 1)
    txt(x, 142, a, bold(20), INK); txt(x, 164, b, sans(8), MUTED)
tabs = [('EUROPE 12', GREEN), ('MIDDLE EAST 5', RED), ('AMERICAS 7', (93, 112, 127)), ('ASIA-PACIFIC 6', (125, 91, 66)), ('AFRICA 2', (132, 112, 69)), ('OCEANIA 3', (82, 111, 91)), ('WORLD 1', INK)]
for k, (s, c) in enumerate(tabs):
    x = 24 + k * 139; rect((x, 177, x + 133, 195), c); txt(x + 5, 179, s, bold(9), PAPER)
txt(24, 198, 'THE DAY IN UTC · 03:00 GMT COP31 objections close · 06:00 approval session · 05:30 Vegas GP ends · 17:00 GMT ATP final · 9am–6pm Hong Kong polls · 01:24 WIB BepiColombo Mercury orbit', bold(7), RED)

for k, row in enumerate(top):
    x = 24 + k * 330; photo(k + 1, (x, 220, 316, 140))
    rect((x + 174, 222, x + 310, 241), GOLD); txt(x + 178, 223, row[4], bold(10), INK)
    rect((x, 340, x + 236, 357), RED); txt(x + 5, 341, fit(('CLAIM · ' if k == 1 else 'REPORTED · ') + row[0], bold(8), 226), bold(8), PAPER)
    lines(x, 361, row[1], ser(18), INK, 315, 20, 2)
    lines(x, 402, row[2], sans(9), INK, 315, 11, 3); txt(x, 436, row[3], bold(8), MUTED)

# D1 section header over the 10 small stories
rect((24, 446, 1000, 464), INK)
txt(32, 449, 'THE DAY IN TEN', bold(11), PAPER)
rt = 'THE STORIES THAT MOVED THE WORLD'
txt(992 - d.textbbox((0, 0), rt, font=bold(8))[2], 451, rt, bold(8), PAPER)

scene_ids = [14, 4, 5, 6, 7, 8, 9, 10, 11, 12]
for k, row in enumerate(small):
    col = k % 5; rr = k // 5; x = 24 + col * 198; y = 470 + rr * 150
    photo(scene_ids[k], (x, y, 188, 68))
    ellipse((x + 158, y + 2, x + 182, y + 26), PAPER, RED, 2); txt(x + 165, y + 5, str(k + 4), bold(12), RED)
    rect((x + 91, y + 20, x + 185, y + 37), GOLD); txt(x + 94, y + 22, row[4], bold(8), INK)
    rect((x, y + 69, x + 188, y + 84), row[5])
    txt(x + 3, y + 71, fit(('CLAIM · ' if k in (2, 8) else 'REPORTED · ') + row[0], bold(6), 182), bold(6), PAPER)
    lines(x, y + 88, row[1], ser(12), INK, 188, 12, 2)
    lines(x, y + 113, row[2], sans(8), INK, 188, 8, 2); txt(x, y + 130, row[3], bold(6), MUTED)

# world map — solid, high contrast: blue ocean, solid beige land
mx, my, mw, mh = 24, 782, 300, 122
rect((mx, my, mx + mw, my + mh), (176, 203, 216))
txt(mx, 762, 'WHERE IT HAPPENED', bold(10), RED)
def mp(lon, lat): return (mx + (lon + 180) / 360 * mw, my + (90 - lat) / 180 * mh)
continents = [[(-168, 70), (-145, 72), (-125, 55), (-117, 32), (-105, 20), (-97, 16), (-83, 9), (-79, 25), (-66, 48), (-88, 60), (-110, 70)],
 [(-81, 12), (-68, 8), (-51, -2), (-44, -20), (-54, -54), (-69, -48), (-77, -25)],
 [(-11, 36), (4, 58), (31, 70), (58, 55), (43, 38), (29, 34), (19, 10), (4, -35), (-8, -28), (-17, 7)],
 [(32, 35), (50, 55), (90, 68), (130, 54), (160, 58), (178, 47), (148, 33), (125, 8), (106, -5), (78, 8), (63, 25)],
 [(112, -11), (153, -10), (154, -39), (133, -44), (114, -27)]]
for pts in continents:
    poly([mp(a, b) for a, b in pts], (214, 192, 148))
    d.line([mp(a, b) for a, b in pts] + [mp(*pts[0])], fill=(160, 138, 92), width=1)
txt(mx, my + mh + 3, 'WORLD MAP · RED NUMBERS MARK STORIES 1–13', bold(8), MUTED)
coords = [(30.7, 36.9), (50.6, 26.2), (30.5, 50.5), (114.2, 22.3), (26.2, 60.5), (174.8, -41.3), (85.1, 25.6), (24.7, 59.4), (34.5, 31.5), (-47.9, -15.8), (-108.5, 25.6), (-77, 38.9), (47.8, 30.5)]
offset = {0: (-16, -14), 1: (14, -12), 2: (16, -12), 4: (14, 10), 7: (-24, 10), 11: (12, 12)}
for k, (lon, lat) in enumerate(coords):
    px, py = mp(lon, lat); ox, oy = offset.get(k, (0, 0)); qx, qy = px + ox, py + oy
    if ox or oy: line([(px, py), (qx, qy)], RED, 1)
    ellipse((qx - 6, qy - 6, qx + 6, qy + 6), RED, PAPER, 1); txt(qx - 3, qy - 5, str(k + 1), bold(8), PAPER)

briefs = [('BAYELSA, NIGERIA', 'Boat toll rises to 24.', 'NEMA'), ('WASHINGTON', 'Nvidia faces SEC accounting probe.', 'MEDIA'), ('JERUSALEM', 'Eisenkot opens coalition talks with Likud.', 'MAARIV'), ('TEHRAN', 'Iran to ration electricity as grid strains.', 'ST'), ('CANBERRA', 'Marles says US budget office is “wrong” on AUKUS subs.', 'ABC'), ('MANILA', 'Chinese bomber turns back 170 km from capital.', 'AP'), ('MELBOURNE', 'Cummins keeps Test captaincy; board backs him.', 'ABC'), ('NEW YORK', 'Gupta jailed 19 years in Pannun plot.', 'COURT'), ('TOKYO', 'Japan to train on Indian ranges, a first.', 'REPORTS'), ('WASHINGTON', 'Hegseth curbs US–Canada military gatherings.', 'REPORTS'), ('RANCHI', 'Cyclone Akvan axes 14 flights.', 'REPORTS'), ('KYIV', 'Two killed in overnight Russian strikes.', 'OFFICIALS'), ('KYIV', 'Zelenskyy calls Putin a “murderer”.', 'REPORTS'), ('LAS VEGAS', 'Verstappen on pole for Grand Prix.', 'REUTERS'), ('LIVERPOOL', 'Liverpool host Manchester United at Anfield.', 'BBC'), ('MARKETS', 'Bitcoin holds above $60,000.', 'MARKET'), ('MOGADISHU', 'Somalia expels UAE ambassador, recalls envoy.', 'REPORTS'), ('COPENHAGEN', 'Denmark expels Russian attaché over rapper plot.', 'GUARDIAN'), ('BRUSSELS', 'Air traffic to halt in 23 Nov strike.', 'ST'), ('BERLIN', 'IG Metall widens car and shipyard strikes.', 'REUTERS'), ('LISBON', 'Thousands march on living costs.', 'REUTERS'), ('DHAKA', '30 Awami League homes set on fire.', 'TOI'), ('TURIN', 'Zverev meets Alcaraz for the ATP title.', 'ATP')]
brief_bodies = ['Toll reaches 24', 'SEC probe reported', 'Likud talks open', 'Power rationing planned',
    'AUKUS budget called “wrong”', 'Bomber turns back 170 km', 'Board backs Test captain',
    'Gupta jailed 19 years', 'Indian range training begins', 'US-Canada gatherings curbed',
    'Akvan cancels 14 flights', 'Two killed in strikes', 'Zelenskyy calls Putin “murderer”',
    'Verstappen takes pole', 'Host United at Anfield', 'Bitcoin above $60,000',
    'UAE envoy expelled, recalled', 'Russian attaché expelled', 'Strike halts air traffic',
    'Car, shipyard strikes widen', 'Thousands march on living costs', '30 Awami League homes burned', 'ATP final at 17:00 GMT']
txt(346, 774, 'ALSO ON SUNDAY 22 NOVEMBER — 23 MORE STORIES', bold(9), RED)
for k, row in enumerate(briefs):
    col = k // 12; rr = k % 12; x = 346 + col * 324; y = 790 + rr * 10
    n = 14 + k; txt(x, y, f'{n:02}', bold(9), RED)
    lead_x = x + 22; txt(lead_x, y, row[0], bold(11), INK)
    body_x = lead_x + d.textbbox((0, 0), row[0], font=bold(11))[2] + 5
    txt(body_x, y + 1, brief_bodies[k], sans(9), INK)
    source_x = body_x + d.textbbox((0, 0), brief_bodies[k], font=sans(9))[2] + 4
    txt(source_x, y + 1, '· ' + row[2], sans(9), INK)

# date check and footer
rect((22, 918, 1002, 987), PAPER, RED, 2)
check = 'Wires read up to 17:00 UTC, Sunday 22 November 2026. Tonight’s barrage was 186 drones, not the 400 of Friday. Left out as other days’ news: Peru earthquake (20 Nov local), Russian missiles landing in Poland (19 Nov), Kerch Bridge strikes (earlier this week), Shenzhen summit (19 Nov).'
check2 = 'Counted as Sunday’s news: the Bahrain strikes (late Saturday night, first reported early Sunday) and the Sparta II fire (hit Saturday, still burning Sunday). Not yet happened: COP31 final approval, ATP champion, Vegas winner. Every story above happened, or was first reported, on Sunday 22 November 2026 in at least one time zone. Claims by governments and armed groups are attributed.'
txt(30, 922, 'DATE CHECK — CHECKED, AND LEFT OUT ON PURPOSE', bold(9), RED)
lines(30, 935, check, sans(8), INK, 962, 10, 2); lines(30, 958, check2, sans(8), INK, 962, 10, 2)
txt(24, 991, fit('Sources named beside each story. REPORTED — confirmed by outlet · CLAIM — one side’s claim, unverified · Original drawings and map · SUNDAY 22 NOVEMBER 2026', sans(8), 976), sans(8), MUTED)

os.makedirs('out', exist_ok=True)
im.save('out/candidate99f.png', format='JPEG', quality=82, subsampling=0)
