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
SEC='#c5d3ee';P2='#f6e7c8'
def section(shape,base,normal,proj):
    fc=cq.Face.makePlane(600,600,basePnt=base,dir=normal)
    r=shape.val().intersect(fc)
    out=[]
    for fa in r.Faces():
        ws=[fa.outerWire()]+fa.innerWires();cmd=[]
        for w in ws:
            pts=[proj(w.positionAt(i/240,'length').toTuple()) for i in range(240)]
            cmd+=[('M',)+pts[0]]+[('L',)+p for p in pts[1:]]+[('Z',)]
        out.append(cmd)
    return out
def drawsec(s,shape,base,normal,proj,col=SEC):
    for c in section(shape,base,normal,proj):s.pd(c,True,col)
def bb():
    blk=W('XZ').center(0,3).rect(40,6).extrude(-14).union(W('XZ').center(0,15).rect(20,18).extrude(-14)).union(W('XZ').center(0,24).circle(10).extrude(-14))
    blk=blk.cut(W().pushPoints([(-15,7),(15,7)]).circle(2).extrude(6)).translate((0,23,0))
    sh=W('XZ').center(0,24).circle(4).extrude(50,both=True).faces('<Y or >Y').chamfer(0.5)
    b1=blk.cut(sh);b2=b1.mirror('XZ')
    s=S(860,500,5);s.at(150,330)
    s.pd([('M',-20,0),('L',20,0),('L',20,6),('L',10,6),('L',10,24),('A',10,0,0,-10,24),('L',-10,6),('L',-20,6),('Z',)])
    s.circ(0,24,4);s.cl(0,-4,0,38);s.cl(-24,24,24,24)
    for x in(-15,15):s.hid(x-2,0,x-2,6);s.hid(x+2,0,x+2,6);s.cl(x,-3,x,9)
    s.dim(-20,0,20,0,-30,'40')
    s.dim(-15,0,15,0,-56,'30');s.dim(20,0,20,6,-26,'6');s.dim(20,0,20,24,-56,'24');s.dim(-10,14,10,14,0,'20')
    s.lead(-7.07,31.07,135,30,'R10',0);s.lead(0,24,60,40,'Ø8 (Boolean)',4);s.lead(15,6,70,50,'Ø4 × 2',0)
    s.txt(150,470,'FRONT (one block)',13,px=True)
    s.at(600,250)
    s.rrect(-50,-4,100,8)
    for y0 in(23,-37):
        s.rrect(y0,-20,14,40);s.rect(y0,-10,14,20)
        for x in(-15,15):s.circ(y0+7,x,2)
    s.cl(-54,0,54,0)
    s.dim(-50,-20,50,-20,-60,'100');s.dim(-30,20,30,20,24,'60');s.dim(23,20,37,20,48,'14');s.dim(-37,-15,-37,15,30,'30')
    s.txt(600,470,'TOP (assembly)',13,px=True)
    s.note('Shaft Ø8 × 100, chamfer 0.5. Block centers 30 from the middle. Second block = Mirror (part) across the mid plane.',60)
    return [b1,b2,sh],s
def latch():
    fr=W('XZ').polyline([(0,0),(70,0),(70,30),(58,30),(58,10),(0,10)]).close().extrude(20,both=True)
    tp=W().moveTo(15,15).lineTo(70,10).lineTo(70,-10).lineTo(15,-15).threePointArc((0,0),(15,15)).close().extrude(40)
    m=fr.intersect(tp).cut(W().center(15,0).circle(4).extrude(40)).cut(W('YZ').center(0,22).circle(3).extrude(80))
    s=S(780,650,6);s.at(150,250)
    s.poly([(0,0),(70,0),(70,30),(58,30),(58,10),(0,10)]);s.hid(11,0,11,10);s.hid(19,0,19,10);s.hid(58,19,70,19);s.hid(58,25,70,25);s.cl(15,-3,15,13);s.cl(54,22,74,22)
    s.dim(0,0,70,0,-30,'70');s.dim(70,0,70,30,-30,'30');s.dim(0,0,0,10,30,'10');s.dim(58,30,70,30,24,'12');s.dim(70,0,70,22,-60,'22');s.lead(64,25,60,40,'Ø6 through the hook',0)
    s.txt(700,200,'FRONT',13,px=True)
    s.at(150,480)
    s.pd([('M',15,15),('L',70,10),('L',70,-10),('L',15,-15),('A',15,0,1,15,15),('Z',)]);s.line(58,10.9,58,-10.9,'#111',1.2);s.circ(15,0,4);s.cl(-3,0,74,0)
    s.dim(70,-10,70,10,-30,'20');s.dim(0,-15,15,-15,-40,'15');s.lead(15-10.6,10.6,135,25,'R15',0);s.lead(15,0,60,60,'Ø8',4)
    s.txt(700,480,'TOP',13,px=True)
    s.note('Extrude the front view (both directions), extrude the top view, Intersect. Then the two holes.',640)
    return [m],s
def ebox():
    o=W().box(80,60,36,centered=(True,True,False)).edges('|Z').fillet(6)
    o=o.cut(W().workplane(offset=2.5).rect(75,55).extrude(31).edges('|Z').fillet(3.5))
    bp=[(x,y) for x in(-32,32) for y in(-22,22)]
    o=o.union(W().workplane(offset=2.5).pushPoints(bp).circle(4).extrude(31)).cut(W().pushPoints(bp).circle(1.7).extrude(36))
    base=o.intersect(W().box(100,80,30,centered=(True,True,False)));lid=o.intersect(W().box(100,80,6,centered=(True,True,False)).translate((0,0,30)))
    s=S(1010,470,4.6);s.at(260,240)
    s.rrect(-40,-30,80,60,6);s.e.append(f'<rect x="{260-37.5*4.6:.1f}" y="{240-27.5*4.6:.1f}" width="{75*4.6:.1f}" height="{55*4.6:.1f}" rx="{3.5*4.6:.1f}" fill="none" stroke="#111" stroke-width="1" stroke-dasharray="5 3"/>')
    for p in bp:s.circ(*p,1.7);s.e.append(f'<circle cx="{260+p[0]*4.6:.1f}" cy="{240-p[1]*4.6:.1f}" r="{4*4.6:.1f}" fill="none" stroke="#111" stroke-width="1" stroke-dasharray="5 3"/>')
    s.cl(-44,0,44,0);s.cl(0,-34,0,34);s.line(-44,22,44,22,'#c33',1.2,'12 3 2 3');s.txt(-46,23,'A',14,bold=True);s.txt(46,23,'A',14,bold=True)
    s.dim(-40,30,40,30,24,'80');s.dim(-40,-30,-40,30,30,'60');s.dim(-32,-30,32,-30,-26,'64');s.dim(40,-22,40,22,-30,'44')
    s.lead(32,22,40,40,'Ø3.4 × 4 through',1.7);s.lead(-40+1.76,30-1.76,135,20,'R6 × 4',0)
    s.txt(260,420,'TOP',13,px=True)
    s.at(740,340)
    drawsec(s,base,(0,22,0),(0,1,0),lambda p:(p[0],p[2]));drawsec(s,lid,(0,22,0),(0,1,0),lambda p:(p[0],p[2]),P2)
    s.line(-44,30,44,30,'#c33',1,'12 3 2 3')
    s.dim(40,0,40,36,-30,'36');s.dim(40,0,40,30,-60,'30');s.dim(-40,0,-40,2.5,30,'2.5');s.dim(-40,33.5,-40,36,30,'2.5');s.lead(37.5,15,160,40,'wall 2.5',0)
    s.txt(740,420,'SECTION A-A',13,px=True)
    s.note('Hollow box, top closed. Bosses from the floor up to the ceiling. Split at 30: base (blue) and lid (yellow). Bosses Ø8.',458)
    return [base,lid.translate((0,0,10))],s
def vbr(T=4):
    m=W().box(60,40,T,centered=(True,False,False)).union(W().box(60,T,45,centered=(True,False,False)))
    m=m.edges(cq.selectors.NearestToPointSelector((0,T+0.01,T+0.01))).fillet(4)
    g=W('YZ').polyline([(T,T),(T+25,T),(T,T+25)]).close().extrude(4).translate((26,0,0))
    m=m.union(g).union(g.mirror('YZ'))
    m=m.cut(W().pushPoints([(-15,28),(15,28)]).circle(2.5).extrude(T))
    m=m.cut(W('XZ').center(0,30).slot2D(24,6).extrude(-T)).cut(W('XZ').pushPoints([(-20,15),(20,15)]).circle(2.5).extrude(-T))
    return m
def vb():
    m=vbr(4);s=S(940,460,4)
    s.at(215,330);s.rrect(-30,0,60,45);s.slot(0,30,24,6);s.circ(-20,15,2.5);s.circ(20,15,2.5);s.cl(0,-3,0,48);s.cl(-15,30,15,30)
    s.dim(-30,0,30,0,-26,'60');s.dim(-30,0,-30,45,30,'45');s.dim(-12,33,12,33,24,'24');s.dim(30,0,30,30,-30,'30');s.dim(30,27,30,33,-60,'6');s.dim(-20,0,20,0,-50,'40');s.dim(-30,0,-30,15,60,'15')
    s.lead(20,15,40,40,'Ø5 × 2',2.5)
    s.txt(215,440,'FRONT (wall)',13,px=True)
    s.at(420,330)
    s.pd([('M',0,0),('L',40,0),('L',40,4),('L',8,4),('A',4,0,0,4,8),('L',4,45),('L',0,45),('Z',)])
    s.poly([(4,4),(29,4),(4,29)]);s.pd([('M',8,4),('L',8,4),('Z',)])
    s.dim(0,0,40,0,-26,'40');s.dim(40,0,40,4,-24,'#t');s.dim(0,45,4,45,24,'#t');s.dim(4,4,4,29,-50,'25');s.lead(5.17,5.17,-135,30,'R4',0)
    s.txt(500,440,'SIDE',13,px=True)
    s.at(730,330);s.rrect(-30,0,60,40);s.line(-30,4,30,4,'#111',1.2);s.rect(26,4,4,25);s.rect(-30,4,4,25);s.circ(-15,28,2.5);s.circ(15,28,2.5)
    s.dim(-15,40,15,40,24,'30');s.dim(30,0,30,28,-30,'28');
    s.txt(730,440,'TOP',13,px=True)
    s.note('Variable t = 4. Gussets 4 thick, legs 25, flush with the sides: model one, then Mirror. Cuts: Through all / Up to next. Check with t = 6.',60)
    return [m],s
def hub():
    m=W('XZ').polyline([(4,0),(25,0),(25,4),(10,4),(10,24),(4,24)]).close().revolve(360,(0,0,0),(0,1,0))
    es=[e for e in m.edges().vals() if e.geomType()=='CIRCLE' and ((abs(e.radius()-25)<.01 and abs(e.Center().z-4)<.01) or (abs(e.radius()-10)<.01 and abs(e.Center().z-24)<.01))]
    m=m.newObject(es).chamfer(1)
    m=m.cut(W().polarArray(19,0,360,6).circle(2.5).extrude(4)).cut(W('YZ').center(0,16).circle(1.25).extrude(15))
    s=S(920,450,6);s.at(270,360)
    drawsec(s,m,(0,0,0),(0,1,0),lambda p:(p[0],p[2]))
    s.cl(0,-4,0,28);s.cl(14,16,24,16)
    s.dim(-25,0,25,0,-30,'Ø50');s.dim(-10,24,10,24,24,'Ø20');s.dim(25,0,25,4,-30,'4');s.dim(25,0,25,24,-60,'24');s.dim(-4,24,4,24,48,'Ø8')
    s.dim(-19,0,19,0,-56,'Ø38');s.dim(10,0,10,16,-110,'16');s.lead(-24.5,3.5,135,30,'1 × 45°',0)
    s.txt(270,440,'SECTION (Revolve profile = right half)',13,px=True)
    s.at(720,230);s.circ(0,0,25);s.circ(0,0,24);s.circ(0,0,10);s.circ(0,0,4)
    for i in range(6):a=i*pi/3;s.circ(19*math.cos(a),19*math.sin(a),2.5)
    s.e.append(f'<circle cx="720" cy="230" r="{19*6}" fill="none" stroke="#c33" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    s.cl(-29,0,29,0);s.cl(0,-29,0,29);s.lead(19*0.5,19*0.866,60,30,'Ø5 × 6 on Ø38',2.5)
    s.txt(720,440,'TOP',13,px=True)
    s.note('Revolve the profile, chamfer the two outer top edges, then hole + Circular pattern, then a radial Ø2.5 set-screw hole, one side only (Up to next).',60)
    return [m],s
def car():
    rail=W('YZ').polyline([(-15,0),(15,0),(15,4),(8,4),(8,14),(-8,14),(-8,4),(-15,4)]).close().extrude(60,both=True)
    c=W().box(40,36,22,centered=(True,True,False)).translate((0,0,4.5))
    c=c.cut(W('YZ').polyline([(-8.5,0),(8.5,0),(8.5,14.5),(-8.5,14.5)]).close().extrude(30,both=True))
    c=c.cut(W().pushPoints([(x,y) for x in(-12,12) for y in(-12,12)]).circle(2).extrude(30))
    s=S(900,760,6);s.at(250,300)
    drawsec(s,rail,(0,0,0),(1,0,0),lambda p:(p[1],p[2]));drawsec(s,c,(0,0,0),(1,0,0),lambda p:(p[1],p[2]),P2)
    s.cl(0,-3,0,30)
    s.dim(-15,0,15,0,-26,'30');s.dim(-15,0,-15,4,30,'4');s.dim(-8,14,8,14,0,'16');s.dim(15,4,15,14,-24,'10');s.dim(-18,26.5,18,26.5,24,'36');s.dim(18,4.5,18,26.5,-60,'22')
    s.lead(-8.25,12,135,40,'gap 0.5 all around',0)
    s.txt(560,220,'SECTION (rail blue, carriage yellow)',13,px=True)
    s.at(450,540);s.rrect(-60,-15,120,30);s.rrect(-20,-18,40,36,0,P2)
    for x in(-12,12):
        for y in(-12,12):s.circ(x,y,2)
    s.dim(-60,-15,60,-15,-70,'120');s.dim(-20,18,20,18,24,'40');s.dim(-12,-18,12,-18,-24,'24');s.dim(20,-12,20,12,-30,'24');s.lead(12,12,60,30,'Ø4 × 4',2)
    s.txt(450,748,'TOP',13,px=True)
    s.note('Two parts. The carriage channel: sketch on the carriage end face, Use the rail outline, Offset 0.5, Remove Through all.',60)
    return [rail,c],s
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
    s.at(600,330);s.rrect(-30,0,60,4);s.rrect(-30,24,60,4);s.rrect(-26,4,8,20);s.rrect(18,4,8,20)
    s.dim(30,0,30,4,-24,'4');s.dim(30,4,30,24,-24,'20');s.dim(30,24,30,28,-24,'4');s.lead(-26,14,160,40,'standoff Ø8 / Ø4',0)
    s.txt(600,380,'FRONT',13,px=True)
    s.note('6 parts in one Part Studio. Standoffs and top plate are drawn with Use from the base plate.',60)
    return [bp,tp]+st,s
L=[('l31','L3-1 · Bearing blocks',bb),('l32','L3-2 · Latch from two views',latch),('l33','L3-3 · Electronics box',ebox),('l34','L3-4 · Bracket with variable thickness',vb),('l35','L3-5 · Thin channel',e),('l36','L3-6 · Plate stack',f),('l37','L3-7 · Revolved hub',hub),('l38','L3-8 · Slide carriage',car)]
for k,t,fn in L:
    sh,s=fn();s.svg(OUT+k+'.svg',t);iso(sh,k+'-3d.svg');print(k)
