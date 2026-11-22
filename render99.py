from PIL import Image, ImageDraw, ImageFont
import math
import os

W = H = 1024
PAPER = (243, 232, 204)
INK = (34, 47, 43)
MUTED = (83, 91, 78)
RED = (174, 57, 43)
GREEN = (82, 111, 91)
GOLD = (201, 151, 62)
BLUE = (82, 117, 139)
NIGHT = (43, 62, 75)
WHITE = (250, 246, 232)

SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SERIF_B = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
im = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(im)

def font(px, bold=False, serif=False):
    path = SERIF_B if serif else (SANS_B if bold else SANS)
    return ImageFont.truetype(path, px)

def label(x, y, s, px, color=INK, bold=False, serif=False, anchor=None):
    d.text((x, y), s, font=font(px, bold, serif), fill=color, anchor=anchor)

def text_width(s, px, bold=False, serif=False):
    return d.textbbox((0, 0), s, font=font(px, bold, serif))[2]

def fit_line(s, x, y, maxw, px, color=INK, bold=False, serif=False):
    while px > 8 and text_width(s, px, bold, serif) > maxw:
        px -= 1
    label(x, y, s, px, color, bold, serif)
    return px

def wrapped(s, x, y, maxw, px, maxlines, color=INK, bold=False, serif=False, leading=2):
    words = s.split()
    lines, line = [], ''
    for word in words:
        trial = (line + ' ' + word).strip()
        if text_width(trial, px, bold, serif) <= maxw or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        while lines[-1] and text_width(lines[-1] + '…', px, bold, serif) > maxw:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + '…'
    for i, row in enumerate(lines):
        label(x, y + i * (px + leading), row, px, color, bold, serif)
    return len(lines) * (px + leading)

def line(x1, y1, x2, y2, color=INK, width=2):
    d.line((x1, y1, x2, y2), fill=color, width=width)

def box(x1, y1, x2, y2, fill, outline=None, width=1, radius=0):
    if radius:
        d.rounded_rectangle((x1, y1, x2, y2), radius, fill=fill, outline=outline, width=width)
    else:
        d.rectangle((x1, y1, x2, y2), fill=fill, outline=outline, width=width)

def ellipse(x1, y1, x2, y2, fill, outline=None, width=1):
    d.ellipse((x1, y1, x2, y2), fill=fill, outline=outline, width=width)

def chip(x, y, s, maxw, px=12, color=RED, pad=7, h=23):
    while px > 8 and text_width(s, px, True) + 2 * pad > maxw:
        px -= 1
    ww = min(maxw, text_width(s, px, True) + 2 * pad)
    box(x, y, x + ww, y + h, color, radius=3)
    label(x + pad, y + (h - px) // 2 - 1, s, px, WHITE, True)
    return ww

def scene(kind, x, y, w, h, compact=False):
    # Every panel is a bounded, flat-vector editorial scene.
    box(x, y, x+w, y+h, (226, 218, 194), outline=(215, 202, 171), width=1)
    sx, sy = w / 300, h / 130
    def X(a): return int(x + a*sx)
    def Y(a): return int(y + a*sy)
    def B(a,b,c,e,col,outline=None,ww=1): box(X(a),Y(b),X(c),Y(e),col,outline,ww)
    def E(a,b,c,e,col,outline=None,ww=1): ellipse(X(a),Y(b),X(c),Y(e),col,outline,ww)
    def L(a,b,c,e,col=INK,ww=2): line(X(a),Y(b),X(c),Y(e),col,max(1,int(ww*sx)))
    def P(points,col): d.polygon([(X(a),Y(b)) for a,b in points], fill=col)
    if kind == 1:  # climate negotiation
        B(0,0,300,130,(230,218,185)); B(0,88,300,130,(196,180,145))
        for i in range(6):
            hx=38+i*43
            E(hx-7,40,hx+7,54,[RED,GREEN,BLUE,GOLD,(110,89,74)][i%5])
            B(hx-7,54,hx+7,82,NIGHT if i%2 else GREEN)
            L(hx,80,hx-5,88,INK,2); L(hx,80,hx+6,88,INK,2)
        B(18,82,278,91,(93,70,51)); B(18,77,278,82,(160,122,77))
        E(18,50,48,80,BLUE); L(33,80,33,96,MUTED,3); L(23,96,44,96,MUTED,3)
        E(250,16,282,48,WHITE,RED,2); L(266,20,266,32,RED,2); L(266,32,273,36,RED,2)
        for xx in (63,117,171,225): B(xx,8,xx+8,21,GOLD)
    elif kind == 2:  # Bahrain radar and incoming fire
        B(0,0,300,130,NIGHT); B(0,93,300,130,(33,45,52))
        for bx,bh in ((18,48),(62,65),(111,38),(157,58),(212,44),(252,70)):
            B(bx,93-bh,bx+30,93,(51,75,88))
            for wy in range(60,91,12):
                for wx in range(bx+6,bx+25,10): B(wx,wy,wx+4,wy+5,GOLD)
        for rx in (74,222):
            E(rx-18,49,rx+18,70,WHITE); B(rx-2,70,rx+2,77,WHITE)
        for a,b,c,e in ((35,5,116,60),(175,2,149,58),(270,7,201,60)):
            L(a,b,c,e,(237,198,143),2); E(c-4,e-4,c+4,e+4,(255,160,63))
        E(112,86,151,105,(229,104,46)); E(124,82,145,101,(245,163,65))
    elif kind == 3:  # polling station
        B(0,0,300,130,(224,217,195)); B(12,87,288,98,(128,99,67))
        B(74,56,187,105,(45,62,70)); B(94,51,167,61,(45,62,70))
        P([(123,37),(145,39),(145,72),(123,68)], WHITE); P([(128,43),(141,45),(141,57),(128,55)], GOLD)
        for i,c in enumerate((RED,BLUE,GREEN)):
            hx=31+i*32
            E(hx-7,42,hx+7,56,(190,143,103)); B(hx-11,56,hx+11,84,c)
            B(hx-12,84,hx-5,99,INK); B(hx+5,84,hx+12,99,INK)
        B(207,30,273,83,WHITE,(93,91,79),2); label(X(213),Y(39),'POLL',11,RED,True)
        B(226,16,251,31,RED)
    elif kind == 4:  # burning ship and rescue boat
        B(0,0,300,130,NIGHT); B(0,83,300,130,(45,74,86))
        P([(25,72),(270,72),(245,105),(58,105)],(42,52,58))
        B(69,50,191,73,(101,106,98)); B(83,39,120,50,(133,132,116)); B(126,43,169,50,(133,132,116))
        for fx,fy in ((117,43),(143,34),(161,41),(183,39)):
            P([(fx,fy+23),(fx-10,fy+6),(fx-2,fy-5),(fx+2,fy+4),(fx+11,fy-4),(fx+8,fy+18)],(230,112,43))
        for i in range(3): E(118+i*17,19-i*3,141+i*16,37-i*2,(112,112,103))
        P([(219,89),(274,89),(265,101),(229,101)],(190,157,105)); B(235,78,254,89,WHITE)
    elif kind == 5:  # cricket
        B(0,0,300,130,(205,220,183)); B(0,86,300,130,(113,145,93))
        B(215,12,286,48,(44,77,59)); label(X(220),Y(18),'629/6',14,WHITE,True)
        for sx0 in (165,174,183): L(sx0,75,sx0,100,WHITE,3)
        E(80,29,97,46,(183,139,99)); L(88,47,105,72,BLUE,7); L(102,58,133,37,INK,5)
        L(105,71,93,98,INK,5); L(105,71,124,98,INK,5); L(128,41,143,25,(150,103,67),5)
        E(140,18,149,27,RED)
    elif kind == 6:  # bridge
        B(0,0,300,130,(222,217,187)); B(0,78,300,130,(82,137,165))
        B(0,0,39,85,(111,148,91)); B(260,0,300,85,(111,148,91))
        B(68,24,81,96,(93,81,65)); B(218,24,231,96,(93,81,65)); B(35,75,270,82,(101,81,62))
        L(75,24,75,75,GOLD,3); L(225,24,225,75,GOLD,3)
        for xx in range(82,222,12):
            L(75,28,xx,75,(135,110,79),1); L(225,28,xx,75,(135,110,79),1)
        B(112,65,136,74,RED); E(116,61,123,68,WHITE); E(128,61,135,68,WHITE)
        B(166,65,190,74,BLUE); E(170,61,177,68,WHITE); E(182,61,189,68,WHITE)
    elif kind == 7:  # border crossing queue
        B(0,0,300,130,(218,222,206)); B(0,85,300,130,(163,157,129))
        B(38,36,117,84,(183,174,142)); B(49,24,107,37,(106,119,92)); B(67,11,94,25,RED)
        B(152,49,270,57,RED); B(160,49,177,57,WHITE); B(193,49,210,57,WHITE); B(226,49,243,57,WHITE)
        for hx in (135,113,91):
            E(hx-5,58,hx+5,68,(187,142,99)); B(hx-8,68,hx+8,88,BLUE if hx%2 else GREEN)
            B(hx-9,87,hx-3,101,INK); B(hx+3,87,hx+9,101,INK)
            B(hx+9,78,hx+19,89,GOLD)
        L(174,53,174,98,MUTED,3)
    elif kind == 8:  # aid truck and supplies
        B(0,0,300,130,(218,207,177)); B(0,91,300,130,(168,147,111))
        B(178,47,220,86,(147,128,97)); B(221,38,255,86,(171,149,107)); B(259,49,289,86,(135,117,87))
        B(38,50,198,91,WHITE,(108,111,100),2); B(198,61,239,91,(225,224,210),(108,111,100),2)
        E(65,82,92,108,INK); E(189,82,216,108,INK); E(206,82,231,108,INK)
        B(98,60,135,84,(232,221,202)); B(110,63,121,80,RED); B(105,68,126,75,RED)
        B(12,107,294,109,(125,113,93))
    elif kind == 9:  # ICU bed, patient, monitor
        B(0,0,300,130,(219,222,211)); B(0,95,300,130,(172,167,145))
        B(26,58,190,68,(97,109,100)); B(39,43,153,59,WHITE); B(34,64,43,99,MUTED); B(177,64,185,99,MUTED)
        E(54,39,73,57,(198,157,121)); B(70,47,133,58,(202,194,168))
        L(210,40,210,103,MUTED,4); B(200,29,224,44,WHITE,(107,111,97),1); L(212,44,212,58,BLUE,2)
        B(230,50,282,89,(46,70,69)); L(235,71,243,71,GREEN,2); L(243,71,249,60,GREEN,2); L(249,60,255,79,GREEN,2); L(255,79,265,67,GREEN,2); L(265,67,277,67,GREEN,2)
    elif kind == 10:  # helicopter, desert, cuffs
        B(0,0,300,130,(214,221,207)); B(0,86,300,130,(201,177,124))
        P([(0,86),(78,68),(151,86),(234,62),(300,78),(300,94)],(185,157,106))
        E(108,27,160,52,NIGHT); P([(157,37),(192,25),(195,30),(160,44)],NIGHT); B(127,21,143,27,INK); L(119,20,151,20,INK,3)
        L(123,52,116,59,INK,4); L(150,52,157,59,INK,4)
        E(126,89,164,113,None,RED,4); E(154,89,192,113,None,RED,4); L(155,99,165,99,RED,4)
    elif kind == 11:  # airliner and warning
        B(0,0,300,130,(207,221,222)); B(0,92,300,130,(206,195,164))
        P([(20,53),(119,49),(158,17),(169,19),(151,51),(248,46),(275,52),(249,60),(151,60),(172,91),(160,93),(118,61),(20,59)],WHITE)
        for k in range(3):
            d.arc((X(225+k*7),Y(66-k*7),X(274+k*7),Y(116+k*7)),190,280,fill=BLUE,width=2)
        P([(101,77),(132,77),(116,49)],GOLD); label(X(112),Y(55),'!',15,INK,True)
    elif kind == 12:  # plant fire
        B(0,0,300,130,(211,218,207)); B(0,90,300,130,(163,157,133))
        B(38,47,128,96,(116,125,113)); B(132,58,230,96,(93,111,105)); B(66,22,81,47,(104,111,103)); B(71,9,87,25,(94,100,94))
        for fx,fy in ((156,54),(178,48),(199,55)):
            P([(fx,fy+29),(fx-10,fy+9),(fx-3,fy-2),(fx+3,fy+9),(fx+11,fy+2),(fx+7,fy+28)],(232,109,43))
        E(164,21,189,41,(114,115,105)); E(180,12,205,34,(132,128,115))
        B(235,83,277,103,RED); B(245,72,267,84,WHITE); E(242,98,253,111,INK); E(264,98,275,111,INK)
    elif kind == 13:  # tennis court and trophy
        B(0,0,300,130,(103,139,91)); P([(35,10),(233,10),(267,111),(14,111)],(76,123,83))
        P([(55,23),(216,23),(240,97),(38,97)],(156,184,119)); L(137,23,137,97,WHITE,2); L(47,60,229,60,WHITE,2)
        L(105,56,165,56,WHITE,3); L(105,64,165,64,WHITE,3); L(105,56,105,64,WHITE,2); L(165,56,165,64,WHITE,2)
        E(72,39,83,50,(193,149,103)); L(77,50,89,73,BLUE,5); L(88,71,78,87,INK,4); L(89,71,101,87,INK,4); L(89,59,99,43,INK,3)
        E(183,69,194,80,(193,149,103)); L(188,80,176,94,RED,5); L(178,92,168,103,INK,4); L(179,92,192,103,INK,4)
        B(262,30,282,38,GOLD); P([(264,38),(280,38),(277,55),(267,55)],GOLD); B(263,55,282,59,GOLD); B(261,59,284,64,GOLD)

stories = [
('ANTALYA, TÜRKIYE · CLIMATE','COP31 closes in on a deal at dawn','Near-final package for ~200 nations; objections close 03:00 GMT, approval at 06:00.','Reuters','~200 NATIONS','reported',1),
('MANAMA, BAHRAIN · WAR','Iran says it hit US radars in Bahrain','Tehran claims missiles and drones hit two bases; Bahrain reports a fire, no injuries.','IRNA · Al Jazeera','2 BASES','claim',2),
('HONG KONG · POLITICS','Hong Kong votes for its Election Committee','5,700 voters select chief-executive electors; 856 candidates contest 723 seats. Polls close 6pm.','China Daily · SCMP','723 SEATS','reported',3),
('GULF OF FINLAND · WAR AT SEA','Russian ship still burning in Finnish waters','Finland leads rescue as Sparta II burns.','Reuters','16 CREW SAFE','reported',4),
('WELLINGTON · CRICKET','Pant\'s 128 puts India 629/6','India\'s record NZ total; lead 261 at lunch.','Reuters','629/6','reported',5),
('PATNA, INDIA · INFRASTRUCTURE','Modi opens Nitish Setu bridge','New bridge links Patna and Vaishali.','PTI','BRIDGE OPENS','reported',6),
('TALLINN · SECURITY','Estonia to shut its Russia border on 1 Dec','Five crossings close 1 Dec after sabotage bid; families hurry across.','Reuters','1 DEC','reported',7),
('GAZA · AID','Strike hits food aid vehicle','Three Palestinians die in air attack.','Al Jazeera · Reuters','3 KILLED','reported',8),
('BRASÍLIA · HEALTH','Bolsonaro in intensive care','Ex-president stable, breathing unaided.','AP','ICU','reported',9),
('SINALOA, MEXICO · CARTELS','Mexico captures \'El Chapo Isidro\'','Fugitive flown to capital; 11 killed.','AP','11 KILLED','reported',10),
('WASHINGTON · SECURITY','US airlines warned of terror threat','Possible al-Qaeda-linked attack warned before Thanksgiving.','Reports','AL-QAEDA LINK','reported',11),
('BASRA, IRAQ · DISASTER','Four die in fire at Basra power plant','Plant fire injures 35 in the city.','Reuters','4 DEAD','reported',12),
('TURIN · TENNIS','Zverev meets Alcaraz for ATP Finals title','Top two seeds clash at 17:00 GMT.','ATP','17:00 GMT','scheduled',13),
]

briefs = [
('14','BAYELSA, NIGERIA','Boat toll rises to 24.','NEMA'),('15','WASHINGTON','Nvidia faces SEC probe.','Media'),
('16','JERUSALEM','Eisenkot opens Likud talks.','Maariv'),('17','TEHRAN','Iran to ration electricity.','ST'),
('18','CANBERRA','Marles calls US report wrong.','ABC'),('19','MANILA','Bomber turns back 170 km out.','AP'),
('20','MELBOURNE','Cummins keeps Test captaincy.','ABC'),('21','NEW YORK','Gupta jailed 19 years.','Court'),
('22','TOKYO','Japan to train on Indian ranges.','Reports'),('23','WASHINGTON','Hegseth curbs US–Canada meets.','Reports'),
('24','RANCHI','Cyclone Akvan axes 14 flights.','Reports'),('25','KYIV','Two killed in Russian strikes.','Officials'),
('26','KYIV','Zelenskyy calls Putin murderer.','Reports'),('27','LAS VEGAS','Verstappen on Grand Prix pole.','Reuters'),
('28','LIVERPOOL','Liverpool host Manchester United.','BBC'),('29','MARKETS','Bitcoin holds above $60,000.','Markets'),
('30','MOGADISHU','Somalia expels UAE envoy.','Reports'),('31','COPENHAGEN','Russian attaché expelled over plot.','Guardian'),
('32','BRUSSELS','Air traffic strike set for Monday.','ST'),('33','BERLIN','IG Metall widens strikes.','Reuters'),
('34','LISBON','Thousands march over living costs.','Reuters'),('35','DHAKA','30 Awami League homes burned.','TOI'),
]

# Identity and date masthead.
label(22, 7, 'THE WORLD IN ONE DAY', 13, RED, True)
fit_line('35 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026', 387, 8, 615, 12, INK, True)
fit_line('Sunday 22 November 2026', 20, 29, 984, 84, INK, False, True)
fit_line('COP31 near a deal at dawn · Iran says it hit US radars in Bahrain · Hong Kong votes', 22, 126, 980, 16, RED, True)

# Six quantified facts.
facts = [('~200','nations at COP31'),('03:00','GMT objection deadline'),('2','radars Iran says it hit'),('629/6','India at lunch'),('723','Hong Kong seats'),('700,000','displaced in southern Ethiopia')]
starts = [20,188,357,527,696,857]
widths = [154,154,154,154,148,147]
for i, ((n, cap), xx, ww) in enumerate(zip(facts, starts, widths)):
    fit_line(n, xx, 155, ww, 31 if len(n)<7 else 27, INK, True)
    fit_line(cap, xx, 190, ww, 11, MUTED)
    if i < 5: line(xx+ww+4, 160, xx+ww+4, 204, (193,177,145), 1)

# Regional coverage ribbon.
regions = [('EUROPE 11',RED),('MIDDLE EAST 5',INK),('AMERICAS 7',GREEN),('ASIA-PACIFIC 6',BLUE),('AFRICA 2',GOLD),('OCEANIA 3',MUTED),('WORLD 1',RED)]
rx, rw = 20, 984 // 7
for i,(name,col) in enumerate(regions):
    xx = rx + i*rw
    box(xx, 212, xx+rw-4, 233, col, radius=3)
    label(xx+7, 222, name, 12, WHITE, True)

# Three major lead stories.
colx = [20, 355, 690]
for idx, (place, head, deck, source, badge, tag, artid) in enumerate(stories[:3]):
    xx = colx[idx]
    scene(artid, xx, 240, 314, 110)
    chip(xx+8, 247, badge, 146, 12, RED, 7, 23)
    chip(xx+7, 355, tag.upper(), 88, 10, INK, 6, 19)
    fit_line(place, xx+105, 358, 202, 10, MUTED, True)
    wrapped(head, xx+7, 378, 305, 22, 2, INK, True, True, 1)
    wrapped(deck, xx+7, 424, 305, 13, 2, MUTED, False, False, 1)
    fit_line(source, xx+7, 461, 305, 10, RED, True)

# Ten additional scene cards with concrete chips inside each picture.
small_y = [484, 632]
card_w, gap = 190, 8
for j, (place, head, deck, source, badge, tag, artid) in enumerate(stories[3:]):
    row, c = divmod(j, 5)
    xx = 20 + c*(card_w+gap)
    yy = small_y[row]
    scene(artid, xx, yy, card_w, 60, True)
    chip(xx+4, yy+4, badge, 143, 10, RED, 5, 19)
    chip(xx+4, yy+62, tag.upper(), 77, 9, INK, 5, 17)
    fit_line(place, xx+85, yy+65, 103, 9, MUTED, True)
    wrapped(head, xx+3, yy+82, card_w-6, 14, 3, INK, True, True, 0)
    wrapped(deck, xx+3, yy+124, card_w-6, 10, 1, MUTED, False, False, 0)
    fit_line(source, xx+3, yy+137, card_w-6, 9, RED, True)

# Equirectangular simplified world map with clearly numbered red city pins.
mx,my,mw,mh = 20, 778, 300, 172
box(mx,my,mx+mw,my+mh,(232,224,200),outline=(202,187,155),width=1)
continents = [
 [(16,32),(34,17),(61,18),(78,29),(71,42),(81,53),(69,66),(60,84),(50,99),(42,88),(39,70),(28,62),(23,48)],
 [(70,100),(84,105),(91,122),(86,144),(77,162),(69,150),(70,133),(63,118)],
 [(135,31),(153,25),(165,31),(181,28),(194,38),(214,36),(222,47),(207,56),(190,52),(182,63),(168,58),(158,48),(145,51),(135,43)],
 [(158,61),(174,63),(184,78),(180,97),(171,116),(160,107),(154,91),(150,76)],
 [(214,98),(228,93),(245,100),(255,112),(247,121),(233,119),(222,111)],
 [(250,66),(267,59),(286,67),(290,79),(277,84),(264,78)]
]
for poly in continents:
    d.polygon([(mx+a,my+b) for a,b in poly],fill=(191,190,159))
coords=[(30.7,36.9),(50.6,26.2),(114.2,22.3),(26.2,60.5),(174.8,-41.3),(85.1,25.6),(24.7,59.4),(34.5,31.5),(-47.9,-15.8),(-108.5,25.6),(-77,38.9),(47.8,30.5),(7.7,45.1)]
for n,(lon,lat) in enumerate(coords,1):
    px=mx+(lon+180)/360*mw
    py=my+(90-lat)/180*mh
    ellipse(px-7,py-7,px+7,py+7,RED,WHITE,1)
    label(px,py-1,str(n),8,WHITE,True,anchor='mm')
label(mx+7,my+mh-20,'WHERE IT HAPPENED',9,INK,True)
label(mx+7,my+mh-9,'Red numbers mark stories 1–13',8,MUTED)

# Briefs are split into two measured columns with strong bold leads.
bx, by, bw, bh = 336, 778, 668, 172
label(bx,by-2,'ALSO ON SUNDAY 22 NOVEMBER — 22 MORE STORIES',13,RED,True)
for i,(num, lead, body, src) in enumerate(briefs):
    c = 0 if i < 11 else 1
    r = i if i < 11 else i-11
    x0 = bx + c*337
    y0 = by + 19 + r*14
    label(x0,y0,num,11,RED,True)
    label(x0+21,y0,lead,14,INK,True)
    leadw=text_width(lead,14,True)
    bodyx=x0+25+leadw
    maxw=330-(bodyx-x0)
    body_px=fit_line(body,bodyx,y0,maxw,11,MUTED)
    # Source abbreviation is retained as the final visible token when it fits.
    body_width=text_width(body,body_px)
    if bodyx-x0+body_width+text_width(' '+src,9)<330:
        label(bodyx+body_width+3,y0,src,9,RED,True)

# The day-boundary note is prominent, legible and internally consistent.
box(20, 949, 1004, 1000, PAPER, RED, 2, 4)
date1='Wires read up to 17:00 UTC, Sunday 22 November 2026. Left out: Peru quake (20 Nov local), Poland missiles (19 Nov), Kerch Bridge strikes (earlier this week), Shenzhen summit (19 Nov).'
date2='Not yet happened: COP31 final approval, ATP champion, Vegas winner. Every story above happened or was first reported Sunday 22 November 2026 in at least one time zone. Claims are attributed.'
fit_line(date1,28,953,968,11,INK,False)
fit_line(date2,28,976,968,11,INK,False)
fit_line('Sources named beside stories · Drawings and map original · THE WORLD IN ONE DAY · SUNDAY 22 NOVEMBER 2026 · ONE PAGE',22,1003,980,9,MUTED,True)

os.makedirs('out', exist_ok=True)
im.save('out/candidate99.png', format='JPEG', quality=89, subsampling=0, optimize=False, progressive=False)
