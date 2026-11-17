import cadquery as cq,math
W=cq.Workplane;pi=math.pi
G=8;HD=4
def pl(x0,x1,y0,y1,t):return W().box(x1-x0,y1-y0,t).translate(((x0+x1)/2,(y0+y1)/2,t/2))
def cz(r,z0,z1,x=0,y=0):return W().circle(r).extrude(z1-z0).translate((x,y,z0))
def holes(m,pts,d,t=1000):return m.cut(W().pushPoints(pts).circle(d/2).extrude(t).translate((0,0,-t/2)))
def grid(a0,a1,b0,b1):
    xs=[a0+G*i for i in range(int(round((a1-a0)/G))+1)];ys=[b0+G*i for i in range(int(round((b1-b0)/G))+1)]
    return [(x,y) for x in xs for y in ys]
def dflat(r,z0,z1,flat=0.5):
    return cz(r,z0,z1).cut(pl(r-flat,r+1,-r-1,r+1,z1-z0+2).translate((0,0,z0-1)))
def ring(r0,r1,z0,z1):return W().circle(r1).circle(r0).extrude(z1-z0).translate((0,0,z0))
P={}
def part(code,name,sub,qty=1,dims=None,note=''):
    def d(fn):P[code]=dict(code=code,name=name,sub=sub,fn=fn,qty=qty,dims=dims or [],note=note,place=[]);return fn
    return d
def rot(m,ops):
    for ax,a in ops:m=m.rotate((0,0,0),{'x':(1,0,0),'y':(0,1,0),'z':(0,0,1)}[ax],a)
    return m
def place(code,ops,t):P[code]['place'].append((ops,t))
# ---------- standard motor / servo ----------
def motor():
    m=cz(18,-60,0).union(cz(6,0,2)).union(dflat(3,2,22))
    m=holes(m,[(12*math.cos(pi/4+i*pi/2),12*math.sin(pi/4+i*pi/2)) for i in range(4)],2.5,8)
    return m.union(pl(-5,5,-24,-18,10).translate((0,0,-58)))
def servo():
    m=pl(-20,20,-10,10,36.5).union(pl(-27,27,-10,10,2.5).translate((0,0,26.5)))
    m=holes(m,[(x,y) for x in(-24,24) for y in(-5,5)],4.2)
    return m.union(cz(6,36.5,38,x=10)).union(cz(2.9,38,42,x=10))
MOT=['Body Ø36 × 60, front face at z = 0','Boss Ø12 × 2','Shaft Ø6 × 20 with a 0.5 flat (D-shaft)','4 holes Ø2.5 (M3) on Ø24, at 45°','Connector block 10 × 6 × 10 at the back']
SRV=['Body 40 × 20 × 36.5','Tabs 54 × 20 × 2.5 at height 26.5, 4 holes Ø4.2 on 48 × 10','Output shaft 10 from the body center: collar Ø12 × 1.5, spline Ø5.8 × 4']
# ---------- 1 chassis ----------
@part('1.1','Base plate','1',dims=['288 × 288 × 3, corners R8','Holes Ø4 on the 8 mm grid: x, y = −140 … 140 (36 × 36), centered'])
def p11():return holes(pl(-144,144,-144,144,3).edges('|Z').fillet(8),grid(-140,140,-140,140),4)
place('1.1',[],(0,0,15))
def railholes():
    return [p for p in grid(-140,140,8,32) if math.hypot(p[0],p[1]-27)>9]
@part('1.2','Side rail','1',2,['288 × 40 × 3','Holes Ø4: 4 … 284 step 8 from the left end, rows 8, 16, 24, 32 from the bottom edge','Axle hole Ø10 in the middle (144 from the end), 27 from the bottom; no grid holes closer than 9 to it'])
def p12():return holes(pl(-144,144,0,40,3),railholes(),4).cut(cz(5,-1,4,0,27))
place('1.2',[('x',90)],(0,144,18));place('1.2',[('x',90)],(0,-141,18))
@part('1.3','Rear crossbar','1',dims=['282 × 32 × 3','Holes Ø4: 9 … 273 step 8 from the left end, rows 8, 16, 24 from the bottom edge','Switch cutout 19 × 13 in the middle, center 16 from the bottom'])
def p13():return holes(pl(-141,141,0,32,3),[p for p in grid(-132,132,8,24) if abs(p[0])>16],4).cut(pl(-9.5,9.5,9.5,22.5,10).translate((0,0,-2)))
place('1.3',[('x',90),('z',-90)],(-141,0,18))
@part('1.4','L-bracket','1',6,['Angle 24 long, legs 16 × 16, thickness 3','Each leg: 3 holes Ø4 at −8, 0, 8 along the length','Horizontal leg: holes 9 from the corner; vertical leg: holes 8 above the bottom'])
def p14():
    m=pl(-12,12,0,16,3).union(pl(-12,12,0,3,16))
    m=holes(m,[(x,9) for x in(-8,0,8)],4)
    return m.cut(W('XZ').pushPoints([(x,8) for x in(-8,0,8)]).circle(2).extrude(-10).translate((0,-2,0)))
for x in(-100,100):
    place('1.4',[('z',180)],(x,141,18));place('1.4',[],(x,-141,18))
for y in(-28,28):place('1.4',[('z',-90)],(-141,y,18))
# ---------- 2 drive ----------
@part('2.1','Drive motor (standard motor)','2',2,MOT,'Same model for every motor on the robot.')
def p21():return motor()
place('2.1',[('x',-90)],(0,128,45));place('2.1',[('x',90)],(0,-128,45))
@part('2.2','Motor mount','2',2,['Vertical plate 48 × 52 × 4, foot 48 × 24 × 4','Center hole Ø13 at 27 above the bottom','4 holes Ø3.2 on Ø24 around it, at 45°','Foot: 4 holes Ø4 at x = ±12, 8 and 16 from the back face','Fillet R4 inside the bend'])
def p22():
    m=pl(-24,24,0,24,4).union(pl(-24,24,20,24,52))
    m=m.edges(cq.selectors.NearestToPointSelector((0,20,4))).fillet(4)
    m=holes(m,[(x,y) for x in(-12,12) for y in(8,16)],4)
    m=m.cut(W('XZ').workplane(offset=-30).center(0,27).circle(6.5).extrude(20))
    return m.cut(W('XZ').workplane(offset=-30).pushPoints([(12*math.cos(pi/4+i*pi/2),27+12*math.sin(pi/4+i*pi/2)) for i in range(4)]).circle(1.6).extrude(20))
place('2.2',[],(0,108,18));place('2.2',[('z',180)],(0,-108,18))
@part('2.3','Wheel','2',2,['Ø90 × 20, rim 6 thick (Ø78 inside)','Hub Ø24, 5 spokes 8 wide','Center hole Ø7, 4 holes Ø3 on Ø16','Tread: 30 grooves 1.5 deep, 2 wide'])
def p23():
    m=ring(39,45,-10,10).union(cz(12,-10,10))
    for i in range(5):m=m.union(pl(0,40,-4,4,20).translate((0,0,-10)).rotate((0,0,0),(0,0,1),90+72*i))
    m=m.cut(cz(3.5,-11,11))
    m=holes(m,[(8*math.cos(i*pi/2),8*math.sin(i*pi/2)) for i in range(4)],3)
    g=pl(43.5,46,-1,1,22).translate((0,0,-11))
    for i in range(30):m=m.cut(g.rotate((0,0,0),(0,0,1),12*i))
    return m
place('2.3',[('x',-90)],(0,160,45));place('2.3',[('x',90)],(0,-160,45))
@part('2.4','Wheel hub','2',2,['Disc Ø24 × 5','D-bore Ø6 with flat (fits the motor shaft)','4 holes Ø3 on Ø16'])
def p24():
    m=cz(12,0,5).cut(dflat(3.05,-1,6,0.5));return holes(m,[(8*math.cos(i*pi/2),8*math.sin(i*pi/2)) for i in range(4)],3)
place('2.4',[('x',-90)],(0,145,45));place('2.4',[('x',90)],(0,-145,45))
# ---------- 3 casters ----------
@part('3.1','Caster housing','3',2,['Flange 40 × 20 × 3, R4, 2 holes Ø4 at x = ±12','Cup Ø24, from 3 to 12 below the flange top','Ball seat: sphere R7.2, center 8 below the flange top','Opening Ø13 at the bottom'])
def p31():
    m=pl(-24,24,-10,10,3).edges('|Z').fillet(4).translate((0,0,-3)).union(cz(12,-12,-3))
    m=holes(m,[(-16,0),(16,0)],4)
    return m.cut(W().sphere(7.2).translate((0,0,-8))).cut(cz(6.5,-13,-8))
place('3.1',[],(124,4,15));place('3.1',[],(-124,4,15))
@part('3.2','Caster ball','3',2,['Sphere Ø14'])
def p32():return W().sphere(7)
place('3.2',[],(124,4,7));place('3.2',[],(-124,4,7))
@part('3.3','Retaining ring','3',2,['Ring Ø24 / Ø12, 2 thick','Screwed under the cup'])
def p33():return ring(6,12,0,2)
place('3.3',[],(124,4,1));place('3.3',[],(-124,4,1))
# ---------- 4 intake ----------
def ispl():
    m=pl(0,120,0,80,3).edges('|Z').fillet(4)
    return holes(m,[(x,8) for x in(4,12,20,28,36,44)],4)
@part('4.1','Intake plate, motor side','4',dims=['96 × 80 × 3, corners R4','Mount holes Ø4 at (4, 8) and (12, 8)','Motor hole Ø13 at (80, 62)','4 holes Ø3.2 on Ø24 around it, at 45°'])
def p41():
    m=ispl().cut(cz(6.5,-1,4,104,62))
    return holes(m,[(104+12*math.cos(pi/4+i*pi/2),62+12*math.sin(pi/4+i*pi/2)) for i in range(4)],3.2)
place('4.1',[('x',90)],(96,99,18))
@part('4.2','Intake plate, free side','4',dims=['96 × 80 × 3, corners R4','Mount holes Ø4 at (4, 8) and (12, 8)','Shaft hole Ø8.2 at (80, 62)'])
def p42():return ispl().cut(cz(4.1,-1,4,104,62))
place('4.2',[('x',90)],(96,-96,18))
@part('4.3','Intake roller','4',dims=['Tube Ø30 × 186','12 grooves R2 along the length, centers on Ø30','Motor end: D-bore Ø6 × 18 deep; free end: bore Ø8 × 20 deep'])
def p43():
    m=cz(15,-93,93)
    g=cz(2,-94,94,15,0)
    for i in range(12):m=m.cut(g.rotate((0,0,0),(0,0,1),30*i))
    return m.cut(dflat(3.05,75,94,0.5)).cut(cz(4,-94,-73))
place('4.3',[('x',-90)],(200,0,80))
@part('4.4','Roller stub shaft','4',dims=['Ø8 × 32, chamfer 0.5 both ends'])
def p44():return cz(4,0,32).faces('<Z or >Z').chamfer(0.5)
place('4.4',[('x',90)],(200,-73,80))
@part('4.5','Intake motor (standard motor)','4',1,MOT)
def p45():return motor()
place('4.5',[('x',90)],(200,99,80))
@part('4.6','Intake bracket (same as 1.4)','4',4)
def p46():return p14()
for x in(108,132):place('4.6',[('z',180)],(x,-99,18));place('4.6',[],(x,99,18))
# ---------- 5 track ----------
TRK=[(196,4),(170,12),(150,21),(130,22),(110,22),(60,23),(0,30),(-40,40),(-68,52),(-87,72)]
def tcurve(n=80):
    from scipy.interpolate import PchipInterpolator as PI
    xs=[p[0] for p in TRK][::-1];zs=[p[1] for p in TRK][::-1];f=PI(xs,zs)
    import numpy as np
    X=np.linspace(-87,TRK[0][0],n);return [(float(x),float(f(x))) for x in X]
def tz(x):
    from scipy.interpolate import PchipInterpolator as PI
    xs=[p[0] for p in TRK][::-1];zs=[p[1] for p in TRK][::-1];return float(PI(xs,zs)(x))
def tsp(dz=0):
    return [(x,z+dz) for x,z in TRK]
@part('5.1','Track floor','5',dims=['Curved floor 3 thick, 82 wide (y = ±41)','Top surface through the points (x, z), x from the back end: (0, 72) (19, 52) (47, 40) (87, 30) (147, 23) (207, 21.5) (227, 21.5) (257, 11) (283, 4)','Smooth spline through the points; sketch it on the Front plane'])
def p51():
    a=tsp();b=tsp(-3)[::-1]
    return W('XZ').moveTo(*a[0]).spline(a[1:],includeCurrent=True).lineTo(*b[0]).spline(b[1:],includeCurrent=True).close().extrude(41,both=True)
place('5.1',[],(0,0,0))
@part('5.2','Track wall','5',2,['Follows the floor curve, 25 high above the floor top','3 thick, inner face at y = ±38'])
def p52():
    a=tsp();b=tsp(25)[::-1]
    return W('XZ').moveTo(*a[0]).spline(a[1:],includeCurrent=True).lineTo(*b[0]).spline(b[1:],includeCurrent=True).close().extrude(-3).translate((0,38,0))
P['5.2']['place']=[([],(0,0,0)),([],(0,-79,0))]
@part('5.3','Chimney back wall','5',dims=['76 × 38 × 3 (y × z)','Closes the back end of the track; the turret rings guide the ball above it'])
def p53():return pl(-90,-87,-38,38,38)
place('5.3',[],(0,0,70))
def sup(h):
    m=pl(-1.5,1.5,-30,30,h).union(pl(-1.5,10.5,-30,30,3))
    return holes(m,[(6,-20),(6,20)],4,8)
def sh(x):return round(min(tz(x+d) for d in(-1.5,0,1.5))-3-18-0.3,1)
@part('5.4','Track support, low','5')
def p54():return sup(sh(-42))
place('5.4',[],(-42,0,18))
@part('5.5','Track support, high','5')
def p55():return sup(sh(-66))
place('5.5',[],(-66,0,18))
# ---------- 7 turret base ----------
TX=-52
POST=[(-4,52),(-4,-52),(-100,52),(-100,-52)]
@part('7.1','Turret post','7',4,['Ø12 × 92','Ø3.3 (M4 tap) holes 10 deep in both ends'])
def p71():return cz(6,0,92).cut(cz(1.65,-1,10)).cut(cz(1.65,82,93))
P['7.1']['place']=[([],(x,y,18)) for x,y in POST]
@part('7.2','Lower bearing ring','7',dims=['Ring Ø156 / Ø96, 4 thick','4 holes Ø4.2 at the post positions: (±48, ±52) from the center'])
def p72():return holes(ring(48,78,0,4),[(x-TX,y) for x,y in POST],4.2)
place('7.2',[],(TX,0,110))
@part('7.3','Servo tower','7',dims=['Base 60 × 30 × 4, 4 holes Ø4 at x = −22, 26 and y = −10, 6','Two walls 6 × 20 × 84 under the servo tabs','M4 holes Ø3.3 in the wall tops, 48 apart'])
def p73():
    m=pl(-30,30,-15,15,4).union(pl(-27,-21,-10,10,88)).union(pl(21,27,-10,10,88))
    m=holes(m,[(x,y) for x in(-22,26) for y in(-10,6)],4,8)
    return m.cut(W().pushPoints([(x,y) for x in(-24,24) for y in(-5,5)]).circle(1.65).extrude(10).translate((0,0,80)))
place('7.3',[],(-62,-90,18))
@part('7.4','Turret servo (standard servo)','7',1,SRV)
def p74():return servo()
place('7.4',[],(-62,-90,79.5))
# ---------- 8 turret platform ----------
RH=[(63*math.cos(i*pi/2),63*math.sin(i*pi/2)) for i in range(4)]
@part('8.1','Turret platform','8',dims=['Ring Ø190 / Ø96, 4 thick','Holes Ø3.3: shooter brackets, camera base and guide tube (positions on the drawing)'])
def p81():
    m=ring(48,95,0,4)
    return holes(m,RH+[(x,y) for x in(-15,15) for y in(-61,61)]+[(70,-10),(70,10)]+[(51.5*math.cos(pi/4+i*pi/2),51.5*math.sin(pi/4+i*pi/2)) for i in range(4)],3.3)
place('8.1',[],(TX,0,122))
@part('8.2','Upper bearing ring','8',dims=['Ring Ø152 / Ø100, 4 thick'])
def p82():return holes(ring(50,76,0,4),RH,3.3)
place('8.2',[],(TX,0,114))
@part('8.3','Turret gear','8',dims=['Spur gear: module 1, 160 teeth, 4 thick (pitch Ø160)','Bore Ø96'])
def p83():return holes(ring(48,81,0,4),RH,3.3)
place('8.3',[],(TX,0,118))
@part('8.4','Servo pinion','8',dims=['Spur gear: module 1, 20 teeth, 4 thick (pitch Ø20)','Spline bore Ø5.8 (fits the servo output)'])
def p84():return cz(11,0,4).cut(cz(2.9,-3,5))
place('8.4',[],(TX,-90,118))
@part('8.5','Ball guide tube','8',dims=['Tube Ø84 / Ø76, 15 high (stops 1 below the flywheel)','Flange Ø110 × 3, cut flat to 100 × 98, 4 holes Ø3.3 on Ø103 at 45°'])
def p85():return holes(ring(38,42,0,15).union(ring(38,55,0,3).intersect(pl(-50,50,-49,49,3))),[(51.5*math.cos(pi/4+i*pi/2),51.5*math.sin(pi/4+i*pi/2)) for i in range(4)],3.3)
place('8.5',[],(TX,0,126))
@part('8.6','Shooter bracket','8',2,['L-bracket 60 long, legs 12 × 12, 3 thick','Holes Ø3.3, 2 per leg at 15 and 45 from one end, 8 from the corner'])
def p86():
    m=pl(0,60,0,12,3).union(pl(0,60,0,3,12))
    m=holes(m,[(x,8) for x in(15,45)],3.3)
    return m.cut(W('XZ').pushPoints([(x,8) for x in(15,45)]).circle(1.65).extrude(-10).translate((0,-2,0)))
P['8.6']['place']=[([],(-82,53,126)),([('z',180)],(-22,-53,126))]
# ---------- 9 shooter ----------
FX,FZ=-110,190
def splate():
    m=pl(-165,5,126,290,3).edges('|Z').fillet(8)
    m=holes(m,[(x,134) for x in(-67,-37)],3.3)
    return m
@part('9.1','Shooter plate, motor side','9',dims=['170 × 164 × 3, corners R8','Motor hole Ø13 on the flywheel axis, 4 holes Ø3.2 on Ø24 around it at 45°','Hood bracket holes Ø3.3: 80 from the flywheel axis, at 0° and 45°','2 bottom holes Ø3.3, 8 from the bottom edge (to the shooter brackets)'])
def p91():
    m=splate().cut(cz(6.5,-1,4,FX,FZ))
    m=holes(m,[(FX+12*math.cos(pi/4+i*pi/2),FZ+12*math.sin(pi/4+i*pi/2)) for i in range(4)],3.2)
    return holes(m,HB,3.3)
HB=[(FX+80*math.cos(math.radians(a)),FZ+80*math.sin(math.radians(a))) for a in(0,45)]
@part('9.2','Shooter plate, free side','9',dims=['Same outline as 9.1','Bearing hole Ø8.2 on the flywheel axis','Same hood and bottom holes as 9.1'])
def p92():return holes(splate().cut(cz(4.1,-1,4,FX,FZ)),HB,3.3)
P['9.1']['place']=[([('x',90)],(0,53,0))];P['9.2']['place']=[([('x',90)],(0,-50,0))]
@part('9.3','Flywheel','9',dims=['Ø96 × 40','Rim 8 thick, web 6 thick in the middle, hub Ø24','6 holes Ø16 on Ø56 in the web','Bore Ø8'])
def p93():
    m=ring(40,48,-20,20).union(cz(40,-3,3)).union(cz(12,-20,20))
    m=holes(m,[(28*math.cos(i*pi/3),28*math.sin(i*pi/3)) for i in range(6)],16)
    return m.cut(cz(4,-21,21))
place('9.3',[('x',90)],(FX,0,FZ))
@part('9.4','Flywheel shaft','9',dims=['Ø8 × 87, chamfer 0.5 both ends'])
def p94():return cz(4,0,87).faces('<Z or >Z').chamfer(0.5)
place('9.4',[('x',90)],(FX,31,FZ))
@part('9.5','Shaft coupler','9',dims=['Ø16 × 29','Bore Ø8 × 10 from one end, D-bore Ø6 × 19 from the other','Set-screw holes Ø2.5 at 5 and 20 from the Ø8 end'])
def p95():
    m=cz(8,0,29).cut(cz(4,-1,10)).cut(dflat(3.05,10,30,0.5))
    return m.cut(W('YZ').pushPoints([(0,5),(0,20)]).circle(1.25).extrude(10))
place('9.5',[('x',-90)],(FX,21,FZ))
@part('9.6','Shooter motor (standard motor)','9',1,MOT)
def p96():return motor()
place('9.6',[('x',90)],(FX,53,FZ))
# ---------- 10 hood ----------
HR=108;HA=(-15,55)
HL=[(FX+104*math.cos(math.radians(a)),FZ+104*math.sin(math.radians(a))) for a in(0,45)]
def sect(r0,r1):
    q=lambda r,a:(FX+r*math.cos(math.radians(a)),FZ+r*math.sin(math.radians(a)))
    a0,a1=HA;am=(a0+a1)/2
    return W('XZ').moveTo(*q(r0,a0)).threePointArc(q(r0,am),q(r0,a1)).lineTo(*q(r1,a1)).threePointArc(q(r1,am),q(r1,a0)).close()
@part('10.1','Hood','10',dims=['Shell: arc R108 (inside) / R111, from −15° to 55° around the flywheel axis, 94 wide','Two side lips 3 thick, R100 … R108, flush with the shell ends','Lip holes Ø3.3 at R104, at 0° and 45° (M3 screw + nut to the bracket)','Angles from the flywheel axis: 0° = forward, positive = up'])
def p101():
    m=sect(HR,HR+3).extrude(47,both=True)
    for y in(-47,44):m=m.union(sect(100,HR).extrude(-3).translate((0,y,0)))
    return m.cut(W('XZ').pushPoints(HL).circle(1.65).extrude(60,both=True))
place('10.1',[],(0,0,0))
@part('10.2','Hood bracket','10',2,['3 thick plate, sector R72 … R108 from −15° to 55° around the flywheel axis','2 holes Ø3.3 at R80, 0° and 45° (to the shooter plate)','2 holes Ø3.3 at R104, 0° and 45° (to the hood lips)'])
def p102():
    return sect(72,HR).extrude(-3).cut(W('XZ').pushPoints(HB+HL).circle(1.65).extrude(-10).translate((0,-2,0)))
P['10.2']['place']=[([],(0,47,0)),([],(0,-50,0))]
# ---------- 11 battery ----------
@part('11.1','Battery tray','11',dims=['Box 78 × 63 × 45, walls 2.5, open top','Vertical edges R5','Floor holes Ø4 at grid points (see drawing)'])
def p111():
    m=pl(0,78,0,63,45).edges('|Z').fillet(5).faces('>Z').shell(-2.5)
    return holes(m,[(x,y) for x in(16,64) for y in(17,49)],4,6)
place('11.1',[],(-140,59,18))
@part('11.2','Battery lid','11',dims=['78 × 63 × 3, R5, with a 2 mm lip inside the tray','Slot 20 × 4 for the strap'])
def p112():
    m=pl(0,78,0,63,3).edges('|Z').fillet(5).union(pl(2.5,75.5,2.5,60.5,2).translate((0,0,-2)).edges('|Z').fillet(2.5))
    return m.cut(pl(29,49,29.5,33.5,10).translate((0,0,-3)))
place('11.2',[],(-140,59,63))
@part('11.3','Battery (dummy)','11',dims=['70 × 55 × 40, vertical edges R3','Wire exit Ø8 × 4 on top, 10 from one end'])
def p113():return pl(0,70,0,55,38).edges('|Z').fillet(3).union(cz(4,38,40,10,27.5))
place('11.3',[],(-136,63,20.5))
@part('11.4','Lid knob','11',dims=['Ø16 × 8 with a 1 × 45° chamfer on top','Sits on the lid, 39 / 18 from the lid corner'])
def p114():return cz(8,0,8).faces('>Z').chamfer(1)
place('11.4',[],(-140+39,59+18,66))
# ---------- 12 control hub ----------
@part('12.1','Hub tray','12',dims=['48 × 63 × 22, walls 2, open top','4 bosses Ø6 / Ø2.5 inside, at 6 from the walls','Port cutout 30 × 10 in the front wall'])
def p121():
    m=pl(0,48,0,63,22).faces('>Z').shell(-2)
    m=m.union(W().pushPoints([(8,8),(40,8),(8,55),(40,55)]).circle(3).extrude(10).translate((0,0,2)))
    m=m.cut(W().pushPoints([(8,8),(40,8),(8,55),(40,55)]).circle(1.25).extrude(12))
    m=m.cut(pl(46,49,16,46,10).translate((0,0,8)))
    return holes(m,[(16,30),(32,30)],4,6)
place('12.1',[],(-140,-122,18))
@part('12.2','Hub cover','12',dims=['48 × 63 × 2 with 4 holes Ø3 matching the bosses','Vent slots 3 × 30, 6 of them'])
def p122():
    m=holes(pl(0,48,0,63,2),[(8,8),(40,8),(8,55),(40,55)],3)
    for i in range(6):m=m.cut(pl(10+i*5,13+i*5,16,46,4).translate((0,0,-1)))
    return m
place('12.2',[],(-140,-122,40))
@part('12.3','Control hub board','12',dims=['Board 40 × 55 × 2 on the bosses','Connector block 8 × 30 × 8 at the front'])
def p123():return pl(0,40,0,55,2).union(pl(32,40,12,42,8))
place('12.3',[],(-136,-118,30))
# ---------- 13 camera ----------
@part('13.1','Camera base','13',dims=['40 × 36 × 3','2 holes Ø3.3 at (18, 8) and (18, 28)'])
def p131():return holes(pl(0,40,0,36,3),[(18,8),(18,28)],3.3)
place('13.1',[],(0,-18,126))
@part('13.2','Camera fork','13',dims=['Two arms 30 × 12 × 3 on a 36 × 12 base','Pivot hole Ø3.2 at 22 above the base'])
def p132():
    m=pl(0,12,-18,18,3).union(pl(0,12,-18,-15,30)).union(pl(0,12,15,18,30))
    return m.cut(W('XZ').center(6,22).circle(1.6).extrude(20,both=True))
place('13.2',[],(10,0,129))
@part('13.3','Camera body','13',dims=['26 × 26 × 18 box, lens Ø12 × 6 in front','Pivot holes Ø3.2 on the sides'])
def p133():return pl(-9,9,-13,13,26).union(cz(6,0,6).rotate((0,0,0),(0,1,0),90).translate((9,0,13))).cut(W('XZ').center(0,13).circle(1.6).extrude(20,both=True))
place('13.3',[],(16,0,138))
@part('13.4','Pivot pin','13',dims=['Ø3 × 40, head Ø6 × 2'])
def p134():return cz(1.5,0,40).union(cz(3,40,42))
place('13.4',[('x',90)],(16,21,151))
# ---------- 14 number plates ----------
@part('14.1','Number plate','14',2,['80 × 34 × 2, corners R4','Team number cut through, letters 18 high','2 holes Ø4 at (8, 20) and (72, 20), matching the rail grid'])
def p141():
    m=holes(pl(0,80,0,34,2).edges('|Z').fillet(4),[(8,20),(72,20)],4)
    try:m=m.cut(W().text('TLF',18,5,kind='bold').translate((40,15,0)))
    except Exception:pass
    return m
P['14.1']['place']=[([('x',90)],(52,146,22)),([('x',90),('z',180)],(132,-146,22))]
# ---------- 15 switch ----------
@part('15.1','Switch panel','15',dims=['56 × 32 × 3, corners R3','Cutout 19 × 13 in the middle','4 holes Ø4 at the crossbar grid'])
def p151():return holes(pl(-28,28,0,32,3).edges('|Z').fillet(3),[(x,y) for x in(-20,20) for y in(8,24)],4).cut(pl(-9.5,9.5,9.5,22.5,10).translate((0,0,-1)))
place('15.1',[('x',90),('z',-90)],(-144,0,18))
@part('15.2','Rocker switch (dummy)','15',dims=['Body 18.6 × 12.6 × 20 behind the panel','Bezel 21 × 15 × 2, rocker 14 × 9'])
def p152():return pl(-6.3,6.3,-9.3,9.3,20).translate((0,0,-20)).union(pl(-7.5,7.5,-10.5,10.5,2)).union(pl(-4.5,4.5,-7,7,3).translate((0,0,2)))
place('15.2',[('y',-90)],(-147,0,34))
@part('15.3','Switch guard','15',dims=['U guard 30 × 22, 2 thick, 12 deep','2 tabs with holes Ø4'])
def p153():
    m=pl(-15,15,0,2,22).union(pl(-15,-13,-12,0,22)).union(pl(13,15,-12,0,22)).union(pl(-25,-13,-12,-10,22)).union(pl(13,25,-12,-10,22))
    return m.cut(W('XZ').pushPoints([(x,z) for x in(-20,20) for z in(3,19)]).circle(2).extrude(-20).translate((0,-15,0)))
place('15.3',[('z',90)],(-159,0,23))
SUB={'1':('Chassis','Mirzo'),'2':('Drive module ×2','Luchezar'),'3':('Ball casters','Leonid'),'4':('Intake','Malika'),'5':('Ball track','Nikita'),'7':('Turret base','Alexey'),'8':('Turret platform + drive','Fedor'),'9':('Shooter','Andrey'),'10':('Hood','Mansur'),'11':('Battery box','Gulasal'),'12':('Control hub housing','Elias'),'13':('Camera mount','Jason'),'14':('Number plates','Arina'),'15':('Power switch','Alexandros')}
def build():
    out=[]
    for c,p in P.items():
        s=p['fn']();p['shape']=s
        for ops,t in p['place']:out.append((c,rot(s,ops).translate(t)))
    return out
