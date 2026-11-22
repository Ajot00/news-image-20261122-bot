from PIL import Image, ImageDraw, ImageFont
import os

W=H=1024
PAPER=(243,232,204); INK=(34,47,43); MUTED=(83,91,78); RED=(174,57,43)
GREEN=(82,111,91); GOLD=(201,151,62); NIGHT=(30,48,62); BLUE=(73,111,132)
im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im)
base='/usr/share/fonts/truetype/dejavu/'
def font(name,size): return ImageFont.truetype(base+name,size)
ser=lambda n:font('DejaVuSerif-Bold.ttf',n)
sans=lambda n:font('DejaVuSans.ttf',n)
bold=lambda n:font('DejaVuSans-Bold.ttf',n)
def txt(x,y,s,f= sans(12),c=INK): d.text((x,y),s,font=f,fill=c)
def fit(s,f,maxw):
    while d.textbbox((0,0),s,font=f)[2]>maxw and len(s)>1: s=s[:-1]
    return s
def wrap(s,f,w,limit=2):
    words=s.split(); lines=[]; cur=''
    for word in words:
        q=(cur+' '+word).strip()
        if d.textbbox((0,0),q,font=f)[2]<=w: cur=q
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    return lines[:limit]
def lines(x,y,s,f,c,w,leading,limit=2):
    for j,line in enumerate(wrap(s,f,w,limit)): txt(x,y+j*leading,line,f,c)
def rect(box,fill,outline=None,width=1): d.rectangle(box,fill=fill,outline=outline,width=width)
def line(points,fill,width=1): d.line(points,fill=fill,width=width)
def ellipse(box,fill,outline=None,width=1): d.ellipse(box,fill=fill,outline=outline,width=width)
def poly(points,fill): d.polygon(points,fill=fill)
def scene(i,box):
    x,y,w,h=box
    rect((x,y,x+w,y+h),(222,213,187))
    # small architecture intentionally uses local normalized coordinates
    def X(a): return int(x+a*w)
    def Y(a): return int(y+a*h)
    def R(a,b,c,e,col,ol=None,wd=1): rect((X(a),Y(b),X(c),Y(e)),col,ol,wd)
    def L(pts,col,wd=1): line([(X(a),Y(b)) for a,b in pts],col,wd)
    def E(a,b,c,e,col,ol=None,wd=1): ellipse((X(a),Y(b),X(c),Y(e)),col,ol,wd)
    def P(pts,col): poly([(X(a),Y(b)) for a,b in pts],col)
    if i==1:
        R(0,0,1,1,(77,98,103)); R(0,0,.25,1,(119,145,150))
        for k in range(4): R(.03+k*.055,.14,.065+k*.055,.72,(202,210,194))
        R(.30,.12,.96,.72,(46,64,69)); R(.30,.62,.96,.74,(111,88,63))
        for k in range(6): R(.34+k*.10,.43,.39+k*.10,.60,(79,104,99))
        R(.56,.23,.73,.34,(179,150,91)); txt(X(.59),Y(.23),'COP31',bold(max(8,int(h*.10))),PAPER)
        R(.65,.48,.68,.63,INK); P([(.62,.50),(.71,.50),(.69,.46),(.64,.46)],INK)
        E(.79,.03,.93,.19,(204,188,151)); line([(X(.86),Y(.04)),(X(.86),Y(.10)),(X(.90),Y(.12))],RED,2)
        for k in range(7): R(.33+k*.085,.68,.36+k*.085,.77,[RED,GREEN,GOLD,BLUE][k%4])
        for r in range(3):
            for c in range(7): R(.34+c*.085,.80+r*.055,.40+c*.085,.83+r*.055,(37,53,58))
    elif i==2:
        R(0,0,1,1,(27,44,61));
        for k in range(12):
            a=((k*37+9)%int(w))/w; b=((k*19+3)%int(h*.52))/h
            E(a,b,a+.012,b+.035,(205,197,160))
        R(0,.78,1,1,(29,48,57));
        for k in range(8): R(k*.13,.80+(k%3)*.05,k*.13+.05,.90,(89,102,91))
        # radar tower and dishes
        R(.22,.26,.25,.82,(84,111,119)); L([(.15,.50),(.31,.50)],GOLD,3); L([(.20,.48),(.28,.32)],(171,193,190),3); E(.19,.29,.29,.37,(117,148,153),GOLD,2)
        R(.75,.54,.77,.82,(89,108,111)); L([(.70,.60),(.82,.60)],GOLD,2); E(.70,.51,.82,.60,(126,150,149),GOLD,2)
        for pts in [[(.37,.07),(.48,.25),(.63,.39)],[ (.53,.02),(.59,.22),(.72,.37)],[(.68,.08),(.73,.24),(.84,.35)]]: L(pts,(247,196,121),2)
        L([(.12,.85),(.25,.56),(.36,.78)],(194,185,130),2); L([(.86,.85),(.71,.57),(.61,.78)],(194,185,130),2)
        E(.47,.83,.61,.91,(202,86,48));
    elif i==3:
        R(0,0,1,1,(156,139,111)); R(0,.70,1,1,(89,89,72));
        R(.04,.13,.34,.65,(185,173,143));
        for k in range(3): R(.38+k*.16,.20,.49+k*.16,.67,(71,75,67)); R(.39+k*.16,.23,.48+k*.16,.63,(141,112,91))
        R(.07,.52,.32,.57,(80,67,55));
        for k in range(5): R(.09+k*.04,.48,.12+k*.04,.52,PAPER)
        R(.72,.46,.96,.89,(35,48,48),GOLD,2); R(.79,.11,.95,.24,(225,210,170)); txt(X(.80),Y(.13),'POLL',bold(9),INK)
        for a in [.42,.58,.74]: E(a,.32,a+.05,.43,(197,156,115)); R(a+.01,.42,a+.04,.60,(43,60,55)); E(a+.01,.29,a+.04,.33,(42,48,43))
        for k in range(3): R(.78+k*.05,.50+k*.04,.82+k*.05,.56+k*.04,PAPER)
    elif i==4:
        R(0,0,1,1,NIGHT); R(0,.69,1,1,(29,60,74))
        for k in range(6): L([(0,.75+k*.045),(1,.70+k*.045)],(63,97,108),2)
        P([(.13,.59),(.20,.51),(.77,.53),(.92,.62),(.84,.72),(.25,.75)],(58,71,72)); R(.42,.39,.72,.56,(73,79,74)); R(.50,.32,.63,.40,(104,100,82))
        P([(.50,.52),(.54,.28),(.58,.43),(.63,.24),(.66,.50),(.72,.54)],(225,105,43)); P([(.54,.49),(.57,.36),(.60,.50),(.64,.34),(.67,.53)],GOLD)
        E(.50,.07,.64,.28,(83,93,96)); E(.56,.02,.75,.22,(57,68,75))
        P([(.79,.74),(.90,.66),(.99,.71),(.96,.80),(.81,.80)],(169,139,96)); L([(.75,.65),(.90,.39),(.98,.66)],(244,222,155),3)
        E(.69,.14,.78,.20,(76,88,91)); L([(.72,.17),(.75,.12)],(76,88,91),3)
    elif i==5:
        R(0,0,1,1,(77,99,89)); R(.04,.04,.95,.70,(61,83,77));
        for k in range(5): L([(.05,.15+k*.1),(.95,.15+k*.1)],(96,117,96),1)
        R(.70,.02,.96,.12,(31,62,49),GOLD,2); txt(X(.72),Y(.04),'629/6',bold(13),(228,215,150))
        for k in range(3): R(.04+k*.07,.73,.09+k*.07,.97,(102,82,64))
        # striker and keeper
        E(.38,.27,.45,.37,(199,145,98)); L([(.42,.36),(.43,.56),(.32,.63)],INK,5); L([(.43,.48),(.55,.34)],INK,4); L([(.43,.54),(.49,.66)],INK,4); L([(.39,.40),(.32,.30)],INK,4)
        E(.82,.51,.88,.57,(186,138,97)); L([(.85,.56),(.82,.70),(.89,.71)],INK,4)
        for k in range(3): R(.79+k*.045,.70,.81+k*.045,.81,PAPER); R(.785+k*.045,.68,.815+k*.045,.71,RED)
        E(.56,.31,.59,.34,RED)
        for k in range(4): R(.91,.03+k*.09,.94,.10+k*.09,GOLD)
    elif i==6:
        R(0,0,1,1,(166,197,176)); R(0,.53,.45,1,(53,119,151)); R(.57,.53,1,1,(53,119,151)); R(.45,.48,.57,1,(111,105,85))
        for a in [.20,.78]: R(a-.035,.12,a+.035,.62,(97,76,61)); R(a-.045,.12,a+.045,.17,GOLD)
        for k in range(7): L([(.20,.15),(.45+k*.017,.53)],(83,71,60),1); L([(.78,.15),(.57-k*.017,.53)],(83,71,60),1)
        L([(.20,.40),(.78,.40)],(75,68,58),2); L([(.15,.60),(.85,.60)],(74,65,54),2)
        for a in [.43,.55]: R(a,.65,a+.045,.70,(193,181,146));
        for k in range(4): R(.19+k*.04,.10,.21+k*.04,.15,[RED,GOLD,GREEN][k%3])
    elif i==7:
        R(0,0,1,1,(77,83,92)); R(0,.58,1,1,(52,62,65));
        for k in range(7): L([(k*.15,.25),(k*.15,.78)],(117,119,109),2)
        R(.69,.17,.83,.50,(51,62,67)); R(.73,.21,.80,.28,(236,205,128)); R(.03,.56,.45,.60,(197,57,44)); L([(.42,.57),(.62,.34)],PAPER,4)
        for k in range(3):
            a=.12+k*.18; R(a,.67,a+.12,.76,(68,93,104)); E(a+.02,.63,a+.10,.70,(92,111,115)); E(a+.015,.74,a+.045,.78,INK); E(a+.085,.74,a+.115,.78,INK)
        for k in range(3): E(.54+k*.10,.51,.58+k*.10,.61,(181,140,105)); R(.55+k*.1,.60,.58+k*.1,.69,(48,65,66)); R(.59+k*.1,.61,.61+k*.1,.67,GOLD)
        R(.03,.28,.16,.47,(74,85,82)); R(.08,.21,.12,.28,GOLD)
    elif i==8:
        R(0,0,1,1,(190,142,83)); R(0,.68,1,1,(132,103,66)); E(.79,.06,.96,.24,(232,171,83))
        for k in range(5): L([(0,.75+k*.04),(1,.70+k*.04)],(163,129,78),1)
        R(.10,.39,.60,.70,(224,220,199)); R(.16,.30,.49,.42,(242,235,211)); R(.14,.53,.25,.64,RED); P([(.12,.53),(.20,.50),(.22,.59),(.14,.62)],PAPER)
        R(.66,.46,.92,.70,(236,227,202)); R(.72,.37,.87,.48,(245,235,210))
        R(.11,.72,.36,.90,(173,70,51)); P([(.11,.72),(.22,.60),(.36,.72)],RED); L([(.19,.72),(.19,.90)],PAPER,2)
        for k in range(4): R(.29+k*.06,.52-(k%2)*.09,.34+k*.06,.60-(k%2)*.09,(149,110,66))
        for a in [.48,.57]: E(a,.55,a+.035,.61,(118,83,57)); R(a+.005,.60,a+.03,.70,(42,65,61)); L([(a+.01,.62),(a-.02,.68)],INK,2)
    elif i==9:
        R(0,0,1,1,(185,199,186)); R(.70,.06,.96,.34,(205,218,207)); L([(.83,.06),(.83,.34)],(139,158,145),2)
        R(.08,.52,.78,.68,(70,94,94)); R(.12,.41,.75,.54,(211,202,178)); R(.16,.50,.65,.70,(190,181,160))
        E(.16,.43,.25,.53,(192,148,116)); R(.24,.47,.64,.62,(67,87,87))
        for a in [.72,.88]: R(a,.20,a+.09,.39,(40,57,56),GOLD,1); L([(a+.01,.30),(a+.025,.30),(a+.04,.25),(a+.055,.34),(a+.08,.27)],(107,204,139),2); R(a+.02,.39,a+.07,.46,(87,103,94))
        L([(.08,.18),(.08,.76)],INK,3); L([(.04,.76),(.13,.76)],INK,2); E(.04,.10,.13,.22,(220,221,201)); L([(.085,.22),(.085,.46)],(104,141,156),2)
        E(.48,.31,.54,.38,(169,122,93)); R(.49,.37,.55,.51,(55,75,69)); L([(.52,.40),(.61,.51)],INK,3)
    elif i==10:
        R(0,0,1,1,(34,44,57)); P([(0,.74),(.12,.53),(.29,.69),(.44,.48),(.60,.67),(.78,.51),(1,.70),(1,1),(0,1)],(43,51,58)); R(.14,.52,.82,.79,(116,94,68)); R(.23,.43,.43,.57,(131,105,73)); R(.58,.39,.73,.55,(131,105,73))
        P([(.14,.64),(.26,.31),(.39,.64)],(198,174,126)); L([(.17,.64),(.23,.43),(.29,.64)],(238,220,173),2)
        E(.55,.14,.69,.21,(79,91,98)); L([(.57,.17),(.65,.17)],(79,91,98),3); L([(.65,.22),(.49,.67),(.85,.68)],(229,213,157),3)
        for a in [.37,.62]: E(a,.59,a+.05,.67,(181,140,101)); L([(a+.02,.66),(a+.01,.78)],INK,4); L([(a+.01,.70),(a-.03,.75)],INK,3)
        R(.79,.67,.94,.74,(72,78,77)); E(.81,.64,.87,.70,(235,200,109)); E(.89,.64,.95,.70,(235,200,109))
    elif i==11:
        R(0,0,1,1,(103,80,93)); R(0,.50,1,1,(66,74,82)); R(0,.40,1,.55,(192,119,82))
        for k in range(3): E(.08+k*.20,.04,.40+k*.2,.30,(133,96,102),None); 
        R(.78,.18,.88,.64,(56,67,76)); R(.80,.10,.86,.22,(202,165,118)); R(.82,.03,.84,.11,(219,195,144))
        # airplane foreground
        P([(.09,.67),(.47,.65),(.68,.69),(.49,.72),(.24,.72),(.18,.82),(.13,.82),(.16,.72)],(210,214,204)); P([(.34,.67),(.42,.51),(.48,.52),(.45,.67)],(172,190,190)); P([(.57,.68),(.68,.60),(.72,.61),(.65,.69)],(172,190,190))
        R(.79,.47,.97,.78,(233,213,150),INK,2); P([(.88,.51),(.96,.72),(.80,.72)],RED); txt(X(.855),Y(.59),'!',bold(12),PAPER)
        P([(.68,.14),(.75,.06),(.82,.14),(.79,.26),(.69,.27)],(194,207,192)); P([(.71,.13),(.76,.08),(.80,.14)],(194,207,192))
    elif i==12:
        R(0,0,1,1,(89,64,60)); R(0,.72,1,1,(55,58,57)); R(.10,.43,.43,.79,(87,91,82)); R(.51,.34,.87,.79,(77,82,76))
        for a in [.20,.33,.63,.78]: R(a,.14,a+.055,.48,(91,95,87)); P([(a,.14),(a+.02,.05),(a+.055,.14)],(80,85,82))
        P([(.58,.40),(.63,.17),(.68,.39),(.72,.20),(.77,.47),(.85,.36),(.84,.57),(.57,.58)],(219,89,38)); P([(.62,.47),(.66,.29),(.70,.49),(.76,.32),(.80,.52)],GOLD)
        E(.12,.63,.18,.70,(197,144,106)); R(.14,.69,.17,.82,INK); E(.35,.63,.41,.70,(197,144,106)); R(.37,.69,.40,.82,INK)
        R(.02,.76,.20,.85,(177,60,42)); R(.05,.72,.13,.77,(219,195,130)); E(.04,.82,.09,.88,INK); E(.14,.82,.19,.88,INK)
        L([(.16,.74),(.42,.54),(.69,.49)],(174,203,213),4)
    elif i==13:
        R(0,0,1,1,(78,96,81)); R(.08,.18,.92,.83,(68,116,81));
        for k in range(4): R(.02,.05+k*.11,.98,.09+k*.11,(81+k*4,91+k*3,82))
        L([(.08,.22),(.92,.22)],PAPER,1); L([(.08,.79),(.92,.79)],PAPER,1); L([(.50,.22),(.50,.79)],PAPER,1); L([(.08,.51),(.92,.51)],PAPER,2)
        L([(.07,.50),(.93,.50)],(218,217,194),3); R(.47,.46,.53,.50,(220,208,158))
        for a in [.22,.74]: E(a,.31,a+.055,.39,(191,143,101)); L([(a+.03,.39),(a+.03,.55)],INK,4); L([(a+.03,.46),(a-.03,.41)],INK,3); L([(a+.03,.54),(a-.01,.63)],INK,3)
        R(.04,.36,.09,.74,(91,74,61)); R(.02,.33,.12,.37,GOLD); E(.78,.80,.91,.95,GOLD); R(.80,.89,.89,.95,(164,119,45)); E(.44,.43,.47,.46,PAPER)

top=[('ANTALYA, TÜRKIYE · CLIMATE','COP31 closes in on a deal at dawn','After running past Friday’s close, presidents unveil a package nearly 200 nations can accept. Objections shut at 03:00 GMT; approval opens at 06:00.','REUTERS','~200 NATIONS'),('MANAMA, BAHRAIN · WAR','Iran says it hit US radars in Bahrain','Tehran says missiles and drones hit US radars at al-Riffa and Awali; Bahrain says a civilian site caught fire, no injuries.','IRNA · AL JAZEERA','2 BASES'),('HONG KONG · POLITICS','Hong Kong votes for its Election Committee','About 5,700 voters choose members of the 1,500-strong body that picks the chief executive. Polls run 9am to 6pm; 856 candidates chase 723 seats.','CHINA DAILY · SCMP','723 SEATS')]
small=[('GULF OF FINLAND · WAR AT SEA','Russian ship still burning in Finnish waters','Finland leads rescue as Sparta II fire rages on.','REUTERS','16 CREW SAFE'),('WELLINGTON · CRICKET','Pant’s 128 puts India 629/6','India’s highest tally in New Zealand; lead 261 at lunch on day four.','REUTERS','629/6'),('PATNA, INDIA · INFRASTRUCTURE','Modi opens Nitish Setu bridge','PM inaugurates bridge linking Patna and Vaishali districts.','PTI','BRIDGE OPENS'),('TALLINN · SECURITY','Estonia to shut its Russia border on 1 Dec','All five crossings shut after sabotage bid; families rush to cross.','REUTERS','1 DEC'),('GAZA · AID','Strike hits food aid vehicle','Three Palestinians die in an air attack.','AL JAZEERA · REUTERS','3 KILLED'),('BRASÍLIA · HEALTH','Bolsonaro in intensive care','Ex-president stable, breathing on his own.','AP','ICU'),('SINALOA, MEXICO · CARTELS','Mexico captures “El Chapo Isidro”','FBI top-ten fugitive flown to capital; 11 killed in operation.','AP','11 KILLED'),('WASHINGTON · SECURITY','US airlines warned of terror threat','Carriers warned of possible al-Qaeda-linked attack before Thanksgiving.','REPORTS','AL-QAEDA LINK'),('BASRA, IRAQ · DISASTER','Four die in fire at Basra power plant','Blaze at electricity facility also injures 35 in the city.','REUTERS','4 DEAD'),('TURIN · TENNIS','Zverev meets Alcaraz for ATP Finals title','Top two seeds clash at 17:00 GMT.','ATP','17:00 GMT')]

# Masthead and page furniture
txt(24,7,'THE WORLD IN ONE DAY',bold(13),RED); txt(641,7,'35 STORIES · 7 REGIONS · SUNDAY 22 NOVEMBER 2026',bold(10),INK)
txt(25,29,'Sunday 22 November 2026',ser(62),INK)
txt(25,103,'COP31 near a deal at dawn · Iran says it hit US radars in Bahrain · Hong Kong votes',bold(14),RED)
nums=[('~200','nations at COP31 talks'),('03:00','GMT objection deadline'),('2','radars Iran says hit'),('629/6','India at lunch'),('723','Hong Kong seats'),('700,000','displaced in Ethiopia')]
for k,(a,b) in enumerate(nums):
    x=24+k*164
    if k: line([(x-9,130),(x-9,174)],(181,169,143),1)
    txt(x,124,a,bold(27),INK); txt(x,157,b,sans(9),MUTED)
tabs=[('EUROPE 11',GREEN),('MIDDLE EAST 5',RED),('AMERICAS 7',(93,112,127)),('ASIA-PACIFIC 6',(125,91,66)),('AFRICA 2',(132,112,69)),('OCEANIA 3',(82,111,91)),('WORLD 1',INK)]
for k,(s,c) in enumerate(tabs):
    x=24+k*139; rect((x,177,x+133,197),c); txt(x+5,180,s,bold(10),PAPER)

for k,row in enumerate(top):
    x=24+k*330; scene(k+1,(x,205,316,91));
    rect((x+197,207,x+310,224),GOLD); txt(x+201,208,row[4],bold(9),INK)
    rect((x,299,x+156,315),RED); txt(x+4,301,fit(row[0],bold(8),148),bold(8),PAPER)
    lines(x,318,row[1],ser(19),INK,315,21,2)
    lines(x,360,row[2],sans(10),INK,315,13,3); txt(x,402,row[3],bold(8),MUTED)

for k,row in enumerate(small):
    col=k%5; rr=k//5; x=24+col*198; y=421+rr*158
    scene(k+4,(x,y,188,61)); rect((x+92,y+2,x+185,y+16),GOLD); txt(x+95,y+3,row[4],bold(7),INK)
    rect((x,y+64,x+145,y+77),RED); txt(x+3,y+65,fit(row[0],bold(7),138),bold(7),PAPER)
    lines(x,y+80,row[1],ser(13),INK,188,15,2)
    lines(x,y+111,row[2],sans(9),INK,188,11,2); txt(x,y+136,row[3],bold(7),MUTED)

# compact world map with continent silhouettes
mx,my,mw,mh=24,744,300,153
rect((mx,my,mx+mw,my+mh),(232,222,195))
def mp(lon,lat): return (mx+(lon+180)/360*mw,my+(90-lat)/180*mh)
continents=[ [(-168,70),(-145,72),(-125,55),(-117,32),(-105,20),(-97,16),(-83,9),(-79,25),(-66,48),(-88,60),(-110,70)],
 [(-81,12),(-68,8),(-51,-2),(-44,-20),(-54,-54),(-69,-48),(-77,-25)],
 [(-11,36),(4,58),(31,70),(58,55),(43,38),(29,34),(19,10),(4,-35),(-8,-28),(-17,7)],
 [(32,35),(50,55),(90,68),(130,54),(160,58),(178,47),(148,33),(125,8),(106,-5),(78,8),(63,25)],
 [(112,-11),(153,-10),(154,-39),(133,-44),(114,-27)] ]
for pts in continents: poly([mp(a,b) for a,b in pts],(157,169,148))
txt(mx,my+mh+3,'WORLD MAP · RED NUMBERS MARK STORIES 1–13',bold(8),MUTED)
coords=[(30.7,36.9),(50.6,26.2),(114.2,22.3),(26.2,60.5),(174.8,-41.3),(85.1,25.6),(24.7,59.4),(34.5,31.5),(-47.9,-15.8),(-108.5,25.6),(-77,38.9),(47.8,30.5),(7.7,45.1)]
offset={0:(5,-10),3:(-10,-8),6:(-9,10),12:(12,9)}
for k,(lon,lat) in enumerate(coords):
    px,py=mp(lon,lat); ox,oy=offset.get(k,(0,0)); qx,qy=px+ox,py+oy
    if ox or oy: line([(px,py),(qx,qy)],RED,1)
    ellipse((qx-6,qy-6,qx+6,qy+6),RED,PAPER,1); txt(qx-3,qy-5,str(k+1),bold(8),PAPER)

briefs=[('BAYELSA, NIGERIA','Boat toll rises to 24.','NEMA'),('WASHINGTON','Nvidia faces SEC accounting probe.','MEDIA'),('JERUSALEM','Eisenkot opens coalition talks with Likud.','MAARIV'),('TEHRAN','Iran to ration electricity as grid strains.','ST'),('CANBERRA','Marles says US budget office is “wrong” on AUKUS subs.','ABC'),('MANILA','Chinese bomber turns back 170 km from capital.','AP'),('MELBOURNE','Cummins keeps Test captaincy; board backs him.','ABC'),('NEW YORK','Gupta jailed 19 years in Pannun plot.','COURT'),('TOKYO','Japan to train on Indian ranges, a first.','REPORTS'),('WASHINGTON','Hegseth curbs US–Canada military gatherings.','REPORTS'),('RANCHI','Cyclone Akvan axes 14 flights.','REPORTS'),('KYIV','Two killed in overnight Russian strikes.','OFFICIALS'),('KYIV','Zelenskyy calls Putin a “murderer”.','REPORTS'),('LAS VEGAS','Verstappen on pole for Grand Prix.','REUTERS'),('LIVERPOOL','Liverpool host Manchester United at Anfield.','BBC'),('MARKETS','Bitcoin holds above $60,000.','MARKET'),('MOGADISHU','Somalia expels UAE ambassador, recalls envoy.','REPORTS'),('COPENHAGEN','Denmark expels Russian attaché over rapper plot.','GUARDIAN'),('BRUSSELS','Air traffic to halt in 23 Nov strike.','ST'),('BERLIN','IG Metall widens car and shipyard strikes.','REUTERS'),('LISBON','Thousands march on living costs.','REUTERS'),('DHAKA','30 Awami League homes set on fire.','TOI')]
brief_bodies=['Toll reaches 24','SEC probe reported','Likud talks open','Power rationing planned',
    'AUKUS budget called “wrong”','Bomber turns back 170 km','Board backs Test captain',
    'Gupta jailed 19 years','Indian range training begins','US-Canada gatherings curbed',
    'Akvan cancels 14 flights','Two killed in strikes','Zelenskyy calls Putin “murderer”',
    'Verstappen takes pole','Host United at Anfield','Bitcoin above $60,000',
    'UAE envoy expelled, recalled','Russian attaché expelled','Strike halts air traffic',
    'Car, shipyard strikes widen','Thousands march on living costs','30 Awami League homes burned']
for k,row in enumerate(briefs):
    col=k//11; rr=k%11; x=346+col*324; y=744+rr*14
    n=14+k; txt(x,y,f'{n:02}',bold(9),RED)
    lead_x=x+22; txt(lead_x,y,row[0],bold(11),INK)
    body_x=lead_x+d.textbbox((0,0),row[0],font=bold(11))[2]+5
    txt(body_x,y+1,brief_bodies[k],sans(9),INK)
    source_x=body_x+d.textbbox((0,0),brief_bodies[k],font=sans(9))[2]+4
    txt(source_x,y+1,'· '+row[2],sans(9),INK)

# date check and footer
rect((22,918,1002,987),PAPER,RED,2)
check='Wires read up to 17:00 UTC, Sunday 22 November 2026. Left out as other days’ news: Peru earthquake (20 Nov local), Russian missiles landing in Poland (19 Nov), Kerch Bridge strikes (earlier this week), Shenzhen summit (19 Nov).'
check2='Not yet happened: COP31 final approval, ATP champion, Vegas winner. Every story above happened, or was first reported, on Sunday 22 November 2026 in at least one time zone. Claims by governments and armed groups are attributed.'
lines(30,925,check,sans(8),INK,962,10,2); lines(30,948,check2,sans(8),INK,962,10,2)
txt(24,991,'Sources named beside each story. Drawings and map: original, drawn in code. · THE WORLD IN ONE DAY · SUNDAY 22 NOVEMBER 2026 · ONE PAGE',sans(8),MUTED)

os.makedirs('out',exist_ok=True)
im.save('out/candidate99b.png',format='JPEG',quality=89,subsampling=0)
