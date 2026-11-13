import math,sys,json,os
sys.path.insert(0,'tools')
import cadquery as cq
from draw import S
W=cq.Workplane;pi=math.pi
OUT='docs/img/adv/';os.makedirs(OUT,exist_ok=True)
def iso(shape,fn):
    p=OUT+fn
    cq.exporters.export(shape,p,opt={'width':300,'height':220,'marginLeft':12,'marginTop':12,'showAxes':False,'projectionDir':(1,-1.2,0.9),'showHidden':False,'strokeWidth':-1})
    t=open(p).read();i=t.index('<g transform');j=t.rindex('</svg>')
    t=t[:i]+'<rect width="300" height="220" fill="white"/><g transform="matrix(-1 0 0 -1 300 220)">'+t[i:j]+'</g>'+t[j:]
    open(p,'w').write(t)
R={}
def shaft():
    m=W('XZ').polyline([(0,0),(0,3),(7,3),(7,4),(63,4),(63,3),(70,3),(70,0)]).close().revolve(360,(0,0,0),(1,0,0))
    m=m.faces('<X or >X').chamfer(0.5)
    s=S(760,260,8);s.at(90,140)
    s.poly([(0,3),(7,3),(7,4),(63,4),(63,3),(70,3),(70,-3),(63,-3),(63,-4),(7,-4),(7,-3),(0,-3)])
    s.cl(-3,0,73,0);s.dim(0,4,70,4,40,'70');s.dim(0,4,7,4,18,'7');s.dim(63,4,70,4,18,'7')
    s.dim(70,-3,70,3,-30,'Ø6');s.dim(35,-4,35,4,0,'Ø8')
    s.note('Revolve this profile around the axis. Chamfer 0.5 × 45° on both end edges.',245)
    return m,s
def wheel(N=6,D=96):
    r=D/2
    p=[(4,-10),(10,-10),(10,-2),(r-6,-2),(r-6,-10),(r,-10),(r,10),(r-6,10),(r-6,2),(10,2),(10,10),(4,10)]
    m=W('XZ').polyline(p).close().revolve(360,(0,0,0),(0,1,0))
    m=m.edges(cq.selectors.BoxSelector((-1,-1,-3),(1,1,3))).edges('%CIRCLE').fillet(2)
    h=W().center(30,0).circle(8).extrude(5).translate((0,0,-2.5))
    for i in range(N):m=m.cut(h.rotate((0,0,0),(0,0,1),360*i/N))
    es=[e for e in m.edges().vals() if e.geomType()=='CIRCLE' and abs(math.hypot(e.Center().x,e.Center().y)-30)<0.5]
    return m.newObject(es).fillet(1)
def wheel_draw():
    s=S(900,540,4.2);s.at(240,440)
    q=[(4,-10),(10,-10),(10,-2),(42,-2),(42,-10),(48,-10),(48,10),(42,10),(42,2),(10,2),(10,10),(4,10)]
    s.poly([(b,a) for a,b in q])
    s.cl(-14,0,14,0)
    s.dim(-10,48,10,48,24,'20');s.dim(10,0,10,48,-55,'R48 (#D / 2)');s.dim(10,0,10,4,-105,'R4')
    s.lead(-2,30,170,40,'web 4, centered');s.lead(10,45,30,40,'rim 6 (r 42…48)');s.lead(-10,7,160,30,'hub r 4…10, 20 wide');s.lead(-2,42,150,40,'R2 × 4')
    s.txt(240,480,'HALF SECTION (axis at bottom)',12,px=True)
    s.at(650,300);s.circ(0,0,48);s.circ(0,0,42);s.circ(0,0,10);s.circ(0,0,4)
    for i in range(6):a=i*pi/3;s.circ(30*math.cos(a),30*math.sin(a),8)
    s.e.append(f'<circle cx="650" cy="300" r="{30*4.2:.1f}" fill="none" stroke="#c33" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    s.cl(-52,0,52,0);s.cl(0,-52,0,52)
    s.lead(30*math.cos(pi/3),30*math.sin(pi/3),60,50,'Ø16 × #N on Ø60',8);s.lead(0,0,-120,90,'Ø8 bore',4)
    s.txt(650,520,'FRONT (N = 6)',12,px=True)
    s.note('Revolve the half section. Then one Ø16 hole + Fillet R1 on its two edges, then Circular pattern of both with Reapply.',60)
    return s
def plate(b=False):
    m=W().center(80,50).rect(160,100).extrude(6).edges('|Z').fillet(8)
    m=m.cut(W().pushPoints([(20,6),(80,6),(140,6)]).circle(2).extrude(6))
    if b:m=m.cut(W().center(110,62).circle(4.25).extrude(6)).cut(W().center(110,62).circle(7).extrude(4).translate((0,0,2)))
    return m
def plate_draw():
    s=S(880,520,3.4);s.at(130,440);s.rrect(0,0,160,100,8)
    for x in(20,80,140):s.circ(x,6,2)
    s.circ(110,62,4.25);s.circ(110,62,7)
    s.cl(102,62,118,62);s.cl(110,54,110,70)
    s.dim(0,100,160,100,24);s.dim(0,0,0,100,30);s.dim(0,0,20,0,-24,'20');s.dim(20,0,80,0,-24,'60');s.dim(80,0,140,0,-24,'60');s.dim(0,0,110,0,-50,'110')
    s.dim(0,0,0,6,90,'6');s.dim(0,0,0,62,60,'62');s.lead(80,6,70,50,'Ø4 × 3',2);s.lead(2.34,97.66,135,20,'R8 × 4')
    s.lead(110,62,140,60,'B: counterbore',7)
    s.at(760,440);s.rrect(0,0,6,100);s.dim(0,100,6,100,24,'6 (#t)')
    s.note('Plate B hole: Ø8.5 through, counterbore Ø14 × 4 deep (outer face). Plate A: motor holes with Use (step 5).',512)
    return s
def base():
    m=W().center(80,20).rect(160,40).extrude(12)
    return m.cut(W().center(55,20).slot2D(70,10).extrude(12))
def base_draw():
    s=S(820,370,4);s.at(70,270);s.rrect(0,0,160,40);s.slot(55,20,70,10);s.cl(-4,20,164,20)
    s.dim(0,40,160,40,24);s.dim(0,0,0,40,30,'40 (#gap)');s.dim(20,15,90,15,-50,'70');s.dim(0,0,55,0,-24,'55')
    s.lead(80,25,45,40,'slot width 10');s.at(740,270);s.rrect(0,0,12,40);s.dim(0,40,12,40,24,'12')
    s.note('Later: tapped M4 holes in both side faces, placed with Use from the plate holes.',355)
    return s
def hopper():return W().box(60,52,40,centered=(True,True,False)).faces('>Z or >X').shell(-2)
def hopper_draw():
    s=S(700,410,4.5);s.at(200,360);s.rect(-30,0,60,40);s.hid(-28,2,30,2);s.hid(-28,2,-28,40);s.dim(-30,40,30,40,24,'60');s.dim(-30,0,-30,40,30,'40')
    s.txt(200,395,'FRONT',12,px=True)
    s.at(500,250);s.rect(-30,-26,60,52);s.rect(-28,-24,58,48);s.dim(-30,26,30,26,24,'60');s.dim(30,-26,30,26,-30,'52 (#gap + 2·#t)')
    s.txt(500,395,'TOP',12,px=True);s.note('Box 60 × 52 × 40, Shell 2 inward. Remove the top face and the +X face (towards the flywheel).',60)
    return s
def pusher():return W().box(20,30,6,centered=(True,True,False)).union(W().box(16,9.6,12,centered=(True,True,False)).translate((0,0,-12)))
def pusher_draw():
    s=S(640,370,6);s.at(160,230);s.poly([(-10,0),(10,0),(10,6),(-10,6)]);s.rect(-8,-12,16,12)
    s.dim(-10,6,10,6,24,'20');s.dim(-8,-12,8,-12,-24,'16');s.dim(10,0,10,6,-24,'6');s.dim(8,-12,8,0,-50,'12')
    s.txt(160,355,'FRONT',12,px=True)
    s.at(460,230);s.rect(-15,0,30,6);s.rect(-4.8,-12,9.6,12);s.dim(-15,6,15,6,24,'30');s.dim(-4.8,-12,4.8,-12,-24,'9.6')
    s.txt(460,355,'SIDE',12,px=True);s.note('Tongue 9.6 wide slides in the 10 wide slot of the base.',60)
    return s
def ball():return W('XZ').moveTo(0,-20).threePointArc((20,0),(0,20)).close().revolve(360,(0,-20,0),(0,20,0))
def hood():return W().box(60,40,2)
P=[('shaft','Shaft',shaft),('wheel','Flywheel',None),('plate','Side plate',None),('base','Base',None),('hopper','Hopper',None),('pusher','Pusher',None),('ball','Ball Ø40',None),('hood','Hood',None)]
m,s=shaft();R['shaft']=m.val().Volume();s.svg(OUT+'shaft.svg','Shaft');iso(m,'shaft-3d.svg')
m=wheel(6);R['wheel6']=m.val().Volume();R['wheel8']=wheel(8).val().Volume();R['wheel6_d100']=wheel(6,100).val().Volume();wheel_draw().svg(OUT+'wheel.svg','Flywheel');iso(m,'wheel-3d.svg')
m=plate();R['plateA0']=m.val().Volume();mb=plate(True);R['plateB']=mb.val().Volume();plate_draw().svg(OUT+'plate.svg','Side plate (A and B)');iso(mb,'plate-3d.svg')
m=base();R['base']=m.val().Volume();base_draw().svg(OUT+'base.svg','Base');iso(m,'base-3d.svg')
m=hopper();R['hopper']=m.val().Volume();hopper_draw().svg(OUT+'hopper.svg','Hopper');iso(m,'hopper-3d.svg')
m=pusher();R['pusher']=m.val().Volume();pusher_draw().svg(OUT+'pusher.svg','Pusher');iso(m,'pusher-3d.svg')
R['ball']=ball().val().Volume();R['hood']=hood().val().Volume()
for k,v in R.items():print(k,round(v))
json.dump({k:round(v) for k,v in R.items()},open('tools/advanced.json','w'),indent=1)
