import math,sys,os
sys.path.insert(0,'tools')
import cadquery as cq
from draw import S
W=cq.Workplane;pi=math.pi
OUT='docs/img/l3/';os.makedirs(OUT,exist_ok=True)
def iso(shapes,fn):
    sh=cq.Compound.makeCompound([x.val() for x in shapes]);p=OUT+fn
    cq.exporters.export(W().newObject([sh]),p,opt={'width':300,'height':220,'marginLeft':12,'marginTop':12,'showAxes':False,'projectionDir':(1,-1.2,0.9),'showHidden':False,'strokeWidth':-1})
    t=open(p).read();i=t.index('<g transform');j=t.rindex('</svg>')
    t=t[:i]+'<rect width="300" height="220" fill="white"/><g transform="matrix(-1 0 0 -1 300 220)">'+t[i:j]+'</g>'+t[j:]
    open(p,'w').write(t)
def a():
    sh=W('XZ').center(0,20).circle(5).extrude(25,both=True)
    br=W().box(40,20,30,centered=(True,True,False)).cut(sh)
    s=S(760,380,5);s.at(180,320);s.rrect(-20,0,40,30);s.circ(0,20,5);s.cl(-24,20,24,20);s.cl(0,-4,0,34)
    s.dim(-20,0,20,0,-30,'40');s.dim(-20,0,-20,30,30,'30');s.dim(20,0,20,20,-30,'20');s.lead(0,20,45,40,'shaft Ø10',5)
    s.txt(180,370,'FRONT',13,px=True)
    s.at(520,320);s.rrect(-10,0,20,30);s.rect(-25,15,50,10);s.cl(-28,20,28,20)
    s.dim(-25,25,25,25,40,'50');s.dim(-10,0,10,0,-30,'20');s.txt(520,370,'SIDE',13,px=True)
    s.note('Two parts: shaft Ø10 × 50 (centered) and bracket 40 × 20 × 30. Hole = Boolean Subtract, keep tools.',60)
    return [br,sh],s
def b():
    fr=W('XZ').polyline([(0,0),(60,0),(60,15),(30,40),(0,40)]).close().extrude(-40)
    tp=W().polyline([(0,0),(40,0)]).threePointArc((60,20),(40,40)).lineTo(0,40).close().extrude(40)
    m=fr.intersect(tp)
    s=S(620,620,5);s.at(120,290);s.poly([(0,0),(60,0),(60,15),(30,40),(0,40)])
    s.dim(0,0,60,0,-26,'60');s.dim(0,0,0,40,30,'40');s.dim(60,0,60,15,-30,'15');s.dim(0,40,30,40,24,'30')
    s.txt(540,200,'FRONT',13,px=True)
    s.at(120,560);s.pd([('M',0,0),('L',40,0),('A',20,0,0,40,40),('L',0,40),('Z',)]);s.cl(40,16,40,24);s.cl(36,20,44,20)
    s.dim(0,0,40,0,-26,'40');s.dim(0,0,0,40,30,'40');s.lead(40+14.1,20+14.1,45,30,'R20',0)
    s.txt(540,460,'TOP',13,px=True)
    s.note('Extrude the front view 40 deep, extrude the top view 40 high, then Intersect.',610)
    return [m],s
def c():
    box=W().box(60,40,30,centered=(True,True,False)).edges('|Z').fillet(5)
    pk=W().workplane(offset=3).rect(54,34).extrude(27).edges('|Z').fillet(2)
    box=box.cut(pk)
    base=box.intersect(W().box(80,60,24,centered=(True,True,False)));lid=box.intersect(W().box(80,60,6,centered=(True,True,False)).translate((0,0,24)))
    s=S(800,400,5);s.at(220,200);s.rrect(-30,-20,60,40,5);s.rect(-27,-17,54,34,2)
    s.dim(-30,20,30,20,24,'60');s.dim(-30,-20,-30,20,30,'40');s.lead(-30+1.46,20-1.46,135,25,'R5 × 4',0);s.lead(27-0.6,17-0.6,40,40,'pocket: offset 3, R2',0)
    s.txt(220,340,'TOP',13,px=True)
    s.at(590,330);s.rect(-30,0,60,30);s.hid(-27,3,-27,30);s.hid(27,3,27,30);s.hid(-27,3,27,3)
    s.line(-34,24,34,24,'#c33',1,'10 3 2 3');s.dim(30,0,30,30,-30,'30');s.dim(30,0,30,24,-60,'24');s.dim(-30,0,-30,3,30,'3')
    s.txt(590,380,'FRONT (split at 24)',13,px=True)
    return [base,lid.translate((0,0,8))],s
def d(t=4):
    m=W().box(60,40,t,centered=(True,False,False)).union(W().box(60,t,40,centered=(True,False,False)))
    m=m.cut(W().pushPoints([(-18,24),(18,24)]).circle(2.5).extrude(t))
    m=m.cut(W('XZ').center(0,26).slot2D(20,6).extrude(-t))
    s=S(820,580,4.5);s.at(90,500);s.poly([(0,0),(40,0),(40,4),(4,4),(4,40),(0,40)])
    s.dim(0,0,40,0,-30,'40');s.dim(0,0,0,40,30,'40');s.dim(40,0,40,4,-24,'#t');s.dim(0,40,4,40,24,'#t')
    s.txt(180,565,'SIDE',13,px=True)
    s.at(430,520);s.rrect(-30,0,60,40);s.circ(-18,24,2.5);s.circ(18,24,2.5);s.line(-30,4,30,4,'#111',1)
    s.dim(-30,0,30,0,-26,'60');s.dim(-18,24,18,24,0,'36');s.dim(30,4,30,24,-30,'20');s.lead(18,24,40,30,'Ø5 × 2',2.5)
    s.txt(700,470,'TOP',13,px=True)
    s.at(430,300);s.rrect(-30,0,60,40);s.slot(0,26,20,6);s.cl(-14,26,14,26);s.cl(0,20,0,32)
    s.dim(-10,29,10,29,30,'20');s.dim(30,0,30,26,-30,'26');s.dim(30,23,30,29,-60,'6')
    s.txt(700,200,'FRONT (wall)',13,px=True)
    s.note('Slot centered on the wall. All cuts: Through all / Up to next, never a typed depth.',60)
    return [m],s
def e():
    m=W('XZ').polyline([(-20,30),(-20,0),(20,0),(20,30)]).offset2D(1.25,'intersection').extrude(-100)
    m=W('XZ').polyline([(-20,30),(-20,0),(20,0),(20,30),(17.5,30),(17.5,2.5),(-17.5,2.5),(-17.5,30)]).close().extrude(-100)
    m=m.cut(W().pushPoints([(0,18+16*i) for i in range(5)]).circle(2).extrude(3))
    s=S(880,340,5);s.at(130,270);s.poly([(-20,30),(-20,0),(20,0),(20,30),(17.5,30),(17.5,2.5),(-17.5,2.5),(-17.5,30)])
    s.dim(-20,0,20,0,-30,'40');s.dim(20,0,20,30,-30,'30');s.dim(-20,30,-17.5,30,24,'2.5')
    s.txt(130,330,'END',13,px=True)
    s.at(300,170);s.rrect(0,-20,100,40)
    for i in range(5):s.circ(18+16*i,0,2)
    s.cl(-4,0,104,0);s.dim(0,20,100,20,24,'100');s.dim(0,-20,18,-20,-26,'18');s.dim(18,-20,34,-20,-26,'16');s.lead(82,0,120,40,'Ø4 × 5',2)
    s.txt(550,330,'BOTTOM',13,px=True)
    s.note('Sketch one open U line (no thickness). Extrude with Thin, 2.5, to the inside.',60)
    return [m],s
def f():
    hs=[(x,y) for x in(-22,22) for y in(-12,12)]
    bp=W().rect(60,40).extrude(4).edges('|Z').fillet(4).cut(W().pushPoints(hs).circle(2).extrude(4))
    st=[W().center(*p).circle(4).circle(2).extrude(20).translate((0,0,4)) for p in hs]
    tp=bp.translate((0,0,24))
    s=S(800,400,5);s.at(230,210);s.rrect(-30,-20,60,40,4)
    for p in hs:s.circ(*p,2);s.e.append(f'<circle cx="{230+p[0]*5}" cy="{210-p[1]*5}" r="20" fill="none" stroke="#111" stroke-width="1" stroke-dasharray="5 3"/>')
    s.dim(-30,20,30,20,24,'60');s.dim(-30,-20,-30,20,30,'40');s.dim(-22,-20,22,-20,-26,'44');s.dim(30,-12,30,12,-30,'24');s.lead(22,12,40,40,'Ø4 × 4',2);s.lead(30-1.17,-20+1.17,-45,25,'R4 × 4',0)
    s.txt(230,370,'TOP (plates are the same)',13,px=True)
    s.at(600,330);s.rect(-30,0,60,4);s.rect(-30,24,60,4);s.rect(-26,4,8,20);s.rect(18,4,8,20)
    s.dim(30,0,30,4,-24,'4');s.dim(30,4,30,24,-24,'20');s.dim(30,24,30,28,-24,'4');s.lead(-26,14,160,40,'standoff Ø8 / Ø4',0)
    s.txt(600,380,'FRONT',13,px=True)
    s.note('6 parts in one Part Studio. Standoffs and top plate are drawn with Use from the base plate.',60)
    return [bp,tp]+st,s
L=[('a','Shaft and bracket',a),('b','Part from two views',b),('c','Box with a lid',c),('d','Bracket with "up to" cuts',d),('e','Thin channel',e),('f','Plate stack',f)]
for k,t,fn in L:
    sh,s=fn();s.svg(OUT+k+'.svg',t);iso(sh,k+'-3d.svg');print(k)
