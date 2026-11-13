import math,sys,json,os
sys.path.insert(0,'tools')
import cadquery as cq
from draw import S
pi=math.pi
W=cq.Workplane
OUT='docs/img/tasks/'
os.makedirs(OUT,exist_ok=True)
T=[]
def task(id,title,topics,text=''):
    def d(fn):
        T.append(dict(id=id,title=title,topics=topics,text=text,fn=fn));return fn
    return d
def iso(shape,fn):
    p=OUT+fn
    cq.exporters.export(shape,p,opt={'width':300,'height':220,'marginLeft':12,'marginTop':12,'showAxes':False,'projectionDir':(1,-1.2,0.9),'showHidden':False,'strokeWidth':-1})
    t=open(p).read();i=t.index('<g transform');j=t.rindex('</svg>')
    t=t[:i]+'<rect width="300" height="220" fill="white"/><g transform="matrix(-1 0 0 -1 300 220)">'+t[i:j]+'</g>'+t[j:]
    open(p,'w').write(t)

@task(1,'Washer',['sketch','extrude'])
def t1():
    m=W().circle(10).circle(4).extrude(2)
    s=S(560,300,8);s.at(150,160);s.circ(0,0,10);s.circ(0,0,4);s.cl(-13,0,13,0);s.cl(0,-13,0,13)
    s.lead(0,0,40,40,'Ø20',10);s.lead(0,0,-130,50,'Ø8',4)
    s.at(380,160);s.rrect(0,-10,2,20);s.dim(0,10,2,10,24,'2')
    return m,s

@task(2,'Slotted plate',['sketch','extrude','slot'])
def t2():
    m=W().rect(60,30).extrude(4).faces('>Z').workplane().slot2D(26,6).cutThruAll()
    s=S(700,360,6);s.at(250,190);s.rrect(-30,-15,60,30);s.slot(0,0,26,6)
    s.cl(-36,0,36,0);s.cl(0,-20,0,20)
    s.dim(-30,15,30,15,30);s.dim(-30,-15,-30,15,30);s.dim(-13,-3,13,-3,-40,'26');s.lead(10,3,60,40,'R3 × 2')
    s.at(520,190);s.rrect(0,-15,4,30);s.dim(0,15,4,15,24,'4')
    return m,s

@task(3,'Gusset',['sketch','constraints','extrude'])
def t3():
    m=W().polyline([(0,0),(40,0),(0,40)]).close().extrude(4).faces('>Z').workplane(centerOption='ProjectedOrigin').center(12,12).hole(6)
    s=S(640,380,6);s.at(110,320);s.poly([(0,0),(40,0),(0,40)]);s.circ(12,12,3);s.cl(6,12,18,12);s.cl(12,6,12,18)
    s.dim(0,0,40,0,-26);s.dim(0,0,0,40,30);s.dim(0,0,12,0,-50,'12');s.dim(0,0,0,12,54,'12');s.lead(12,12,45,50,'Ø6',3)
    s.at(470,320);s.rrect(0,0,4,40);s.dim(0,40,4,40,24,'4')
    return m,s

@task(4,'Hex standoff',['sketch','polygon','extrude'])
def t4():
    m=W().polygon(6,10/math.cos(pi/6)).extrude(20).faces('>Z').workplane().hole(4)
    s=S(620,320,9);s.at(150,170);r=5/math.cos(pi/6)
    s.poly([(r*math.cos(a*pi/3),r*math.sin(a*pi/3)) for a in range(6)]);s.circ(0,0,2);s.cl(-8,0,8,0);s.cl(0,-8,0,8)
    s.dim(-6.5,-5,-6.5,5,30,'10 (across flats)');s.lead(0,0,40,50,'Ø4 through',2)
    s.at(360,170);s.rrect(0,-5,20,10);s.hid(0,2,20,2);s.hid(0,-2,20,-2);s.dim(0,5,20,5,30,'20')
    return m,s

@task(5,'Stepped block',['extrude New/Add/Remove','blind depth'])
def t5():
    m=W().box(50,30,10,centered=(True,True,False)).faces('>Z').workplane().rect(20,20).extrude(10).faces('>Z').workplane().hole(10,15)
    s=S(700,420,5);s.at(200,180);s.rrect(-25,-15,50,30);s.rect(-10,-10,20,20);s.circ(0,0,5);s.cl(-30,0,30,0);s.cl(0,-20,0,20)
    s.dim(-25,15,25,15,24);s.dim(-25,-15,-25,15,30);s.dim(10,-10,10,10,-30,'20');s.lead(0,0,40,60,'Ø10, depth 15',5)
    s.txt(200,290,'TOP',13,px=True)
    s.at(510,330);s.poly([(-25,0),(25,0),(25,10),(10,10),(10,20),(-10,20),(-10,10),(-25,10)]);s.hid(-5,5,-5,20);s.hid(5,5,5,20);s.hid(-5,5,5,5)
    s.dim(25,0,25,10,-30,'10');s.dim(10,10,10,20,-30,'10');s.dim(-5,20,-5,5,40,'15')
    s.txt(510,380,'FRONT',13,px=True)
    return m,s

@task(6,'Tee bar',['sketch on Front','extrude'])
def t6():
    m=W('XZ').polyline([(-20,30),(20,30),(20,25),(2.5,25),(2.5,0),(-2.5,0),(-2.5,25),(-20,25)]).close().extrude(-60)
    s=S(760,400,5);s.at(160,330);s.poly([(-20,30),(20,30),(20,25),(2.5,25),(2.5,0),(-2.5,0),(-2.5,25),(-20,25)])
    s.dim(-20,30,20,30,24);s.dim(-20,0,-20,30,30);s.dim(20,25,20,30,-30,'5');s.dim(-2.5,0,2.5,0,-24,'5')
    s.txt(160,385,'FRONT (profile)',13,px=True)
    s.at(360,280);s.rrect(0,-20,60,40);s.line(0,2.5,60,2.5,'#111',1,'5 3');s.line(0,-2.5,60,-2.5,'#111',1,'5 3');s.dim(0,20,60,20,24)
    s.txt(510,385,'TOP',13,px=True)
    return m,s

@task(7,'Rounded block',['fillet','chamfer'])
def t7():
    m=W().box(60,40,20,centered=(True,True,False)).edges('|Z').fillet(8).faces('>Z').chamfer(2)
    s=S(720,400,5);s.at(200,190);s.rrect(-30,-20,60,40,8);s.rect(-28,-18,56,36,6);s.cl(-35,0,35,0);s.cl(0,-25,0,25)
    s.dim(-30,20,30,20,24);s.dim(-30,-20,-30,20,30);s.lead(30-2.34,-20+2.34,-45,30,'R8 × 4')
    s.txt(200,330,'TOP',13,px=True)
    s.at(530,240);s.pd([('M',-30,0),('L',30,0),('L',30,18),('L',28,20),('L',-28,20),('L',-30,18),('Z',)])
    s.dim(30,0,30,20,-30,'20');s.note('Chamfer 2 × 45° on all top edges (after the fillets).',372)
    s.txt(530,330,'FRONT',13,px=True)
    return m,s

@task(8,'D-shaft',['extrude','chamfer','remove'],'Order matters: make the round shaft, chamfer both ends, then cut the flat (1 deep).')
def t8():
    m=W('YZ').circle(6).extrude(50).faces('<X or >X').chamfer(1).cut(W().box(60,20,10,centered=(False,True,False)).translate((-5,0,5)))
    s=S(700,320,8);s.at(130,170);r=math.sqrt(11)
    s.pd([('M',-r,5),('A',6,1,0,r,5),('Z',)]);s.cl(-8,0,8,0);s.cl(0,-8,0,8)
    s.lead(0,0,-120,40,'Ø12',6);s.dim(-6,-6,-6,5,40,'11')
    s.txt(130,300,'END',13,px=True)
    s.at(280,170);s.pd([('M',1,-6),('L',49,-6),('L',50,-5),('L',50,4),('L',49,5),('L',1,5),('L',0,4),('L',0,-5),('Z',)])
    s.cl(-3,0,53,0);s.dim(0,5,50,5,30,'50');s.note('Chamfer 1 × 45° on both ends. Flat: 1 deep, full length.',60)
    s.txt(480,300,'SIDE (flat on top)',13,px=True)
    return m,s

@task(9,'Rounded L-bracket',['sketch','extrude','fillet','holes'])
def t9():
    m=(W('XZ').polyline([(0,0),(40,0),(40,4),(4,4),(4,30),(0,30)]).close().extrude(-20)
       .edges('|Y').edges(cq.selectors.NearestToPointSelector((4,10,4))).fillet(4)
       .edges('|Y').edges(cq.selectors.NearestToPointSelector((0,10,0))).fillet(8))
    m=m.cut(W().center(26,10).circle(2.5).extrude(10)).cut(W('YZ').center(10,19).circle(2.5).extrude(10,both=True))
    s=S(800,460,6);s.at(110,360)
    s.pd([('M',8,0),('L',40,0),('L',40,4),('L',8,4),('A',4,0,0,4,8),('L',4,30),('L',0,30),('L',0,8),('A',8,0,0,8,0),('Z',)])
    s.dim(0,0,40,0,-30);s.dim(0,0,0,30,30);s.dim(40,0,40,4,-24,'4');s.dim(0,30,4,30,24,'4')
    s.lead(8-4*0.707,8-4*0.707,30,60,'R4 inside');s.lead(8-8*0.707,8-8*0.707,-120,40,'R8 outside')
    s.cl(26,-2,26,6);s.cl(-2,19,6,19);s.dim(0,0,26,0,-56,'26');s.dim(0,0,0,19,64,'19')
    s.txt(230,450,'FRONT (profile)',13,px=True)
    s.at(500,340);s.rrect(0,0,40,20);s.circ(26,10,2.5);s.cl(26,5,26,15);s.cl(21,10,31,10);s.dim(40,0,40,20,-30,'20');s.lead(26,10,60,40,'Ø5',2.5);s.note('One Ø5 hole in each leg, centered on the width.',60)
    s.txt(620,450,'TOP',13,px=True)
    return m,s

@task(10,'Knob',['extrude','fillet','chamfer','blind hole'])
def t10():
    m=W().circle(15).extrude(12).faces('>Z').edges().fillet(3).faces('<Z').edges().chamfer(1).faces('<Z').workplane().hole(6,8)
    s=S(640,340,7);s.at(150,180);s.circ(0,0,15);s.circ(0,0,12);s.e.append('');s.cl(-18,0,18,0);s.cl(0,-18,0,18);s.lead(0,0,40,40,'Ø30',15)
    s.txt(150,320,'TOP',13,px=True)
    s.at(420,250);s.pd([('M',-14,0),('L',14,0),('L',15,1),('L',15,9),('A',3,0,0,12,12),('L',-12,12),('A',3,0,0,-15,9),('L',-15,1),('Z',)])
    s.hid(-3,0,-3,8);s.hid(3,0,3,8);s.hid(-3,8,3,8);s.dim(15,0,15,12,-30,'12');s.dim(-3,0,-3,8,60,'8')
    s.lead(14.1,11.1,40,30,'R3');s.lead(14.5,0.5,-30,30,'1 × 45°');s.note('Blind hole Ø6, depth 8, from the bottom face.',300)
    s.txt(420,320,'FRONT',13,px=True)
    return m,s

@task(11,'Bolt-circle flange',['circular pattern','construction circle'])
def t11():
    m=W().circle(30).circle(10).extrude(6).faces('>Z').workplane().polarArray(22,0,360,6).hole(5)
    s=S(680,400,4.8);s.at(220,210);s.circ(0,0,30);s.circ(0,0,10)
    for i in range(6):s.circ(22*math.cos(i*pi/3),22*math.sin(i*pi/3),2.5)
    s.e.append(f'<circle cx="220" cy="210" r="{22*4.8:.1f}" fill="none" stroke="#c33" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    s.cl(-34,0,34,0);s.cl(0,-34,0,34)
    s.lead(0,0,-40,40,'Ø60',30);s.lead(0,0,200,50,'Ø20',10);s.lead(11,19.05,60,40,'Ø5 × 6 on Ø44',2.5)
    s.at(500,210);s.rrect(0,-30,6,60);s.dim(0,30,6,30,24,'6')
    return m,s

@task(12,'Grid plate',['linear pattern (2 directions)','fillet'])
def t12():
    pts=[(-32+8*i,-32+8*j) for i in range(9) for j in range(9)]
    m=W().rect(80,80).extrude(3).edges('|Z').fillet(5).faces('>Z').workplane().pushPoints(pts).hole(4)
    s=S(680,500,4.4);s.at(240,240);s.rrect(-40,-40,80,80,5)
    for p in pts:s.circ(*p,2)
    s.dim(-40,40,40,40,24);s.dim(-40,-40,-40,40,30);s.dim(-40,-40,-32,-40,-24,'8');s.dim(-32,-40,-24,-40,-44,'8')
    s.lead(32,32,40,40,'Ø4 × 81 (9 × 9)',2);s.lead(40-1.46,-40+1.46,-40,30,'R5 × 4')
    s.at(520,240);s.rrect(0,-40,3,80);s.dim(0,40,3,40,24,'3')
    return m,s

@task(13,'Lightening plate',['sketch pattern','fillet','remove'])
def t13():
    m=W().rect(120,40).extrude(4).edges('|Z').fillet(4).faces('>Z').workplane().pushPoints([(-44+22*i,0) for i in range(5)]).rect(16,24).cutThruAll()
    m=m.edges('|Z').edges(cq.selectors.BoxSelector((-58,-13,-1),(58,13,5))).fillet(3)
    s=S(760,395,5);s.at(380,190);s.rrect(-60,-20,120,40,4)
    for i in range(5):s.rect(-52+22*i,-12,16,24,3)
    s.dim(-60,20,60,20,24);s.dim(-60,-20,-60,20,30);s.dim(-52,-12,-36,-12,-36,'16');s.dim(-44,-20,-22,-20,-54,'22');s.dim(52,-12,52,12,-24,'24')
    s.lead(-22+8,12,60,30,'5 windows, R3 corners');s.lead(60-1.17,20-1.17,40,20,'R4 × 4')
    s.note('Thickness 4. Windows cut through.',375)
    return m,s

@task(14,'Notched disk',['circular pattern','remove'])
def t14():
    m=W().circle(25).circle(4).extrude(5)
    cut=W().polarArray(25,0,360,12).circle(3).extrude(5)
    m=m.cut(cut)
    s=S(640,400,5.5);s.at(220,210);n=12
    cmd=[]
    for i in range(n):
        a=i*2*pi/n;da=math.asin(1.5/12.5)*2
        a1=a-math.atan2(3,25)*1.0;a2=a+math.atan2(3,25)
    ang=[]
    for i in range(n):
        a=i*2*pi/n;b=2*math.asin(3/50);ang.append((a-b,a+b))
    p=lambda a,r:(r*math.cos(a),r*math.sin(a))
    cmd.append(('M',)+p(ang[0][1],25))
    for i in range(n):
        j=(i+1)%n;cmd.append(('A',25,0,0)+p(ang[j][0],25));cmd.append(('A',3,0,1)+p(ang[j][1],25))
    s.pd(cmd+[('Z',)]);s.circ(0,0,4);s.cl(-29,0,29,0);s.cl(0,-29,0,29)
    s.lead(0,0,60,50,'Ø50',25);s.lead(0,0,200,40,'Ø8',4);s.note('12 notches R3, centers on the Ø50 rim.',390)
    s.at(480,210);s.rrect(0,-25,5,50);s.dim(0,25,5,25,24,'5')
    return m,s

@task(15,'Heat sink',['extrude Add','feature pattern'])
def t15():
    m=W().box(40,30,4,centered=(True,True,False)).faces('>Z').workplane().pushPoints([(-18+6*i,0) for i in range(7)]).rect(2,30).extrude(16)
    s=S(760,380,6);s.at(210,300)
    pts=[(-20,0),(20,0),(20,4)]
    for i in range(6,-1,-1):x=-18+6*i;pts+=[(x+1,4),(x+1,20),(x-1,20),(x-1,4)]
    pts+=[(-20,4)];s.poly(pts)
    s.dim(-20,0,20,0,-30);s.dim(-20,0,-20,4,30,'4');s.dim(-20,4,-20,20,54,'16');s.dim(-19,20,-17,20,24,'2');s.dim(-18,20,-12,20,50,'6')
    s.txt(210,370,'FRONT (7 fins)',13,px=True)
    s.at(520,200);s.rrect(-20,-15,40,30)
    for i in range(7):s.rect(-19+6*i,-15,2,30)
    s.dim(20,-15,20,15,-30,'30');s.txt(520,320,'TOP',13,px=True)
    return m,s

@task(16,'Pillow block',['mirror','extrude Add','sketch on side face'])
def t16():
    m=W().box(60,20,8,centered=(True,True,False)).faces('>Z').workplane().rect(30,20).extrude(24)
    m=m.cut(W('XZ').center(0,20).circle(6).extrude(20,both=True)).cut(W().pushPoints([(-22,0),(22,0)]).circle(2.5).extrude(8))
    s=S(800,480,5);s.at(190,380);s.poly([(-30,0),(30,0),(30,8),(15,8),(15,32),(-15,32),(-15,8),(-30,8)]);s.circ(0,20,6)
    s.cl(0,-3,0,36);s.cl(-9,20,9,20);s.hid(-24.5,0,-24.5,8);s.hid(-19.5,0,-19.5,8);s.hid(24.5,0,24.5,8);s.hid(19.5,0,19.5,8)
    s.dim(-30,0,30,0,-30);s.dim(-15,32,15,32,24);s.dim(30,0,30,8,-30,'8');s.dim(15,0,15,32,-70,'32');s.dim(-15,0,-15,20,40,'20')
    s.lead(0,20,45,50,'Ø12 through',6);s.txt(190,455,'FRONT',13,px=True)
    s.at(560,240);s.rrect(-30,-10,60,20);s.rect(-15,-10,30,20);s.circ(-22,0,2.5);s.circ(22,0,2.5);s.cl(-35,0,35,0)
    s.dim(-22,-10,22,-10,-26,'44');s.dim(30,-10,30,10,-24,'20');s.lead(-22,0,120,40,'Ø5 × 2',2.5)
    s.txt(560,345,'TOP',13,px=True);s.note('Model one side, then Mirror it.',472)
    return m,s

@task(17,'Fork',['mirror','extrude Add','hole across'])
def t17():
    m=W().box(40,20,10,centered=(True,True,False))
    pr=W().box(8,20,40,centered=(True,True,False)).translate((16,0,10))
    m=m.union(pr).union(pr.mirror('YZ'))
    m=m.cut(W('YZ').workplane(offset=-25).center(0,42).circle(3).extrude(50))
    s=S(640,480,6);s.at(220,400);s.poly([(-20,0),(20,0),(20,50),(12,50),(12,10),(-12,10),(-12,50),(-20,50)])
    s.hid(-20,45,-12,45);s.hid(-20,39,-12,39);s.hid(12,45,20,45);s.hid(12,39,20,39);s.cl(-24,42,24,42)
    s.dim(-20,0,20,0,-30);s.dim(-20,0,-20,10,30,'10');s.dim(-20,0,-20,50,60,'50');s.dim(12,50,20,50,24,'8');s.dim(20,0,20,42,-34,'42')
    s.lead(16,42,45,60,'Ø6 through both prongs');s.txt(220,462,'FRONT',13,px=True)
    s.at(500,240);s.rrect(-10,-20,20,40);s.dim(-10,-20,10,-20,-24,'20');s.txt(500,462,'SIDE',13,px=True)
    return m,s

@task(18,'Split clamp',['remove','sketch on side face','slot'])
def t18():
    m=W().box(40,20,20,centered=(True,True,False))
    m=m.cut(W('XZ').workplane(offset=-10).center(0,10).circle(6).extrude(20))
    m=m.cut(W().box(2,20,10,centered=(True,True,False)).translate((0,0,10)))
    m=m.cut(W('YZ').workplane(offset=-20).center(0,15).circle(1.75).extrude(40))
    s=S(660,460,7);s.at(240,330);s.poly([(-20,0),(20,0),(20,20),(1,20),(1,10),(-1,10),(-1,20),(-20,20)],True);s.circ(0,10,6)
    s.hid(-20,16.75,-1,16.75);s.hid(-20,13.25,-1,13.25);s.hid(1,16.75,20,16.75);s.hid(1,13.25,20,13.25)
    s.cl(-23,10,23,10);s.cl(0,1,0,22)
    s.dim(-20,0,20,0,-30);s.dim(20,0,20,20,-30,'20');s.dim(-1,20,1,20,24,'2');s.dim(-20,0,-20,15,30,'15')
    s.lead(-4.2,5.8,-135,30,'Ø12 through');s.lead(12,15,60,70,'Ø3.5 through')
    s.txt(240,425,'FRONT',13,px=True);s.at(520,260);s.rrect(-10,0,20,20);s.dim(-10,0,10,0,-30,'20');s.txt(520,425,'SIDE',13,px=True)
    s.note('Slot 2 wide goes from the top down into the bore. The Ø3.5 hole runs side to side (along the 40).',60)
    return m,s

@task(19,'Boolean: intersect',['Boolean intersect','two parts'],'Make two cylinders Ø40 × 40 as **separate parts** (New), one along Z and one along X, both centered on the origin. Then **Boolean → Intersect**. The result is one curved part.')
def t19():
    a=W().circle(20).extrude(20,both=True);b=W('YZ').circle(20).extrude(20,both=True)
    m=a.intersect(b)
    s=S(640,360,4.5);s.at(170,190);s.rrect(-20,-20,40,40);s.circ(0,0,20);s.cl(-26,0,26,0);s.cl(0,-26,0,26)
    s.dim(-20,20,20,20,24,'40');s.txt(170,330,'TOP: part A (Ø40) over part B (40 long)',12,px=True)
    s.at(460,190);s.rrect(-20,-20,40,40);s.circ(0,0,20);s.cl(-26,0,26,0);s.cl(0,-26,0,26)
    s.txt(460,330,'SIDE: the same, rotated 90°',12,px=True)
    return m,s

@task(20,'goBILDA-style bracket',['sheet-like L','fillet','linear pattern','mirror'])
def t20():
    m=(W('XZ').polyline([(0,0),(48,0),(48,2.5),(2.5,2.5),(2.5,48),(0,48)]).close().extrude(12,both=True)
       .edges('|Y').edges(cq.selectors.NearestToPointSelector((2.5,0,2.5))).fillet(2.5)
       .edges('|Y').edges(cq.selectors.NearestToPointSelector((0,0,0))).fillet(5))
    hb=[(x,y) for x in(16,24,32,40) for y in(-8,0,8)]
    m=m.cut(W().pushPoints(hb).circle(2).extrude(10).translate((0,0,-5)))
    m=m.cut(W('YZ').pushPoints([(y,x) for x,y in hb]).circle(2).extrude(10).translate((-5,0,0)))
    s=S(800,470,5);s.at(80,390)
    s.pd([('M',5,0),('L',48,0),('L',48,2.5),('L',5,2.5),('A',2.5,0,0,2.5,5),('L',2.5,48),('L',0,48),('L',0,5),('A',5,0,0,5,0),('Z',)])
    s.dim(0,0,48,0,-30);s.dim(0,0,0,48,30);s.dim(48,0,48,2.5,-24,'2.5');s.lead(1.46,1.46,-135,20,'R5');s.lead(3.23,3.23,45,40,'R2.5')
    s.txt(200,455,'FRONT (profile)',13,px=True)
    s.at(470,320);s.rrect(0,-12,48,24)
    for x,y in hb:s.circ(x,y,2)
    s.dim(0,-12,16,-12,-26,'16');s.dim(16,-12,24,-12,-46,'8');s.dim(48,-12,48,12,-30,'24');s.dim(48,0,48,8,-60,'8')
    s.lead(16,8,120,40,'Ø4 × 12 per leg',2);s.txt(590,445,'BOTTOM LEG',12,px=True);s.note('The vertical leg has the same 12-hole pattern.',60)
    return m,s

@task(21,'Spoked wheel, N spokes',['variables','feature pattern','extrude Add'],'Make **N** a Variable. Your model must rebuild without errors for any N. Submit with N = 5 and check the volume for N = 7 too.')
def t21(N=5):
    def mk(N):
        m=W().circle(50).circle(42).extrude(10).union(W().circle(12).extrude(10))
        sp=W().center(27,0).rect(30,8).extrude(10)
        for i in range(N):m=m.union(sp.rotate((0,0,0),(0,0,1),360*i/N))
        return m.cut(W().circle(4).extrude(10))
    m=mk(5);t21.v7=mk(7).val().Volume()
    s=S(700,420,3.2);s.at(220,220);s.circ(0,0,50);s.circ(0,0,42);s.circ(0,0,12);s.circ(0,0,4)
    for i in range(5):
        a=pi/2+i*2*pi/5;c,sn=math.cos(a),math.sin(a);px,py=-sn*4,c*4
        r1=math.sqrt(144-16);r2=math.sqrt(42*42-16)
        s.line(c*r1+px,sn*r1+py,c*r2+px,sn*r2+py);s.line(c*r1-px,sn*r1-py,c*r2-px,sn*r2-py)
    s.cl(-55,0,55,0);s.cl(0,-55,0,55)
    s.lead(0,0,-20,60,'Ø100',50);s.lead(0,0,-60,60,'Ø84',42);s.lead(0,0,200,90,'Ø24',12);s.lead(0,0,160,140,'Ø8',4)
    s.dim(-4,25,4,25,60,'8');s.txt(220,410,'N spokes, width 8 (N = 5 shown)',13,px=True)
    s.at(560,220);s.rrect(0,-50,10,100);s.dim(0,50,10,50,24,'10')
    return m,s

@task(22,'Hex-bore pulley',['stacked extrudes','polygon','circular pattern','chamfer'])
def t22():
    m=W().circle(20).extrude(3).faces('>Z').workplane().circle(15).extrude(10).faces('>Z').workplane().circle(20).extrude(3)
    m=m.edges(cq.selectors.RadiusNthSelector(0)).edges('not(%LINE)')
    m=W().circle(20).extrude(3).faces('>Z').workplane().circle(15).extrude(10).faces('>Z').workplane().circle(20).extrude(3)
    m=m.faces('>Z or <Z').edges().chamfer(0.5)
    m=m.cut(W().polygon(6,8/math.cos(pi/6)).extrude(16))
    m=m.cut(W().polarArray(11,45,360,4).circle(2.5).extrude(16))
    s=S(700,400,6);s.at(170,200);s.circ(0,0,20);s.circ(0,0,19.5);r=4/math.cos(pi/6)
    s.poly([(r*math.cos(a*pi/3),r*math.sin(a*pi/3)) for a in range(6)],False)
    for i in range(4):a=pi/4+i*pi/2;s.circ(11*math.cos(a),11*math.sin(a),2.5)
    s.e.append(f'<circle cx="170" cy="200" r="{11*6:.1f}" fill="none" stroke="#c33" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    s.cl(-23,0,23,0);s.cl(0,-23,0,23);
    s.lead(0,0,20,90,'hex 8 across flats',4);s.lead(7.78,7.78,45,40,'Ø5 × 4 on Ø22, at 45°',2.5)
    s.txt(170,360,'TOP',13,px=True)
    s.at(480,295);s.poly([(-20,0),(20,0),(20,3),(15,3),(15,13),(20,13),(20,16),(-20,16),(-20,13),(-15,13),(-15,3),(-20,3)])
    s.hid(-4,0,-4,16);s.hid(4,0,4,16);s.dim(-20,16,20,16,24,'40');s.dim(-15,3,15,3,-60,'30');s.dim(20,0,20,3,-24,'3');s.dim(-20,3,-20,13,30,'10');s.dim(20,13,20,16,-24,'3')
    s.note('Chamfer 0.5 on the outer edges of both flanges (top and bottom faces).',385)
    s.txt(480,360,'FRONT',13,px=True)
    return m,s

@task(23,'Servo mount plate',['sketch','chamfer','pattern','mirror'],'The cutout fits a standard servo (40.5 × 20.2). Tab holes are 48 apart along the servo and 10 across.')
def t23():
    m=W().rect(70,50).extrude(4).edges('|Z').chamfer(5)
    m=m.faces('>Z').workplane().rect(40.5,20.2).cutThruAll().faces('>Z').workplane().pushPoints([(x,y) for x in(-24,24) for y in(-5,5)]).hole(4)
    m=m.faces('>Z').workplane().pushPoints([(x,y) for x in(-29,29) for y in(-19,19)]).hole(4)
    s=S(700,430,5.5);s.at(260,220);s.poly([(-30,-25),(30,-25),(35,-20),(35,20),(30,25),(-30,25),(-35,20),(-35,-20)])
    s.rect(-20.25,-10.1,40.5,20.2)
    for x in(-24,24):
        for y in(-5,5):s.circ(x,y,2)
    for x in(-29,29):
        for y in(-19,19):s.circ(x,y,2)
    s.cl(-40,0,40,0);s.cl(0,-30,0,30)
    s.dim(-35,25,35,25,24,'70');s.dim(-35,-25,-35,25,30,'50');s.dim(-20.25,-10.1,20.25,-10.1,-30,'40.5');s.dim(20.25,-10.1,20.25,10.1,-60,'20.2')
    s.dim(-29,-25,29,-25,-24,'58');s.dim(35,-19,35,19,-30,'38')
    s.note('Servo tab holes Ø4 × 4: 48 apart along, 10 across (y = ±5).',405);s.lead(-29,19,120,40,'Ø4 × 4',2);s.lead(32.5,22.5,40,20,'5 × 45° × 4')
    s.at(560,220);s.rrect(0,-25,4,50);s.dim(0,25,4,25,24,'4')
    return m,s

@task(24,'Shooter side plate',['everything: fillet, patterns, mirror, remove'],'Origin = bottom-left corner. A combined task: plan the order of features before you start.')
def t24():
    m=W().center(80,50).rect(160,100).extrude(5).edges('|Z').fillet(10)
    c=lambda pts,d:W().pushPoints(pts).circle(d/2).extrude(5)
    m=m.cut(c([(110,60)],14)).cut(c([(40,55)],20)).cut(c([(40+16*math.cos(pi/4+i*pi/2),55+16*math.sin(pi/4+i*pi/2)) for i in range(4)],4))
    m=m.cut(c([(16+16*i,y) for i in range(9) for y in(8,92)],4))
    m=m.cut(W().pushPoints([(70,26),(92,26),(114,26)]).rect(16,24).extrude(5))
    m=m.edges('|Z').edges(cq.selectors.BoxSelector((61,13,-1),(123,39,6))).fillet(3)
    s=S(860,610,4);s.at(90,500);s.rrect(0,0,160,100,10)
    s.circ(110,60,7);s.circ(40,55,10)
    for i in range(4):a=pi/4+i*pi/2;s.circ(40+16*math.cos(a),55+16*math.sin(a),2)
    for i in range(9):s.circ(16+16*i,92,2);s.circ(16+16*i,8,2)
    for x in(70,92,114):s.rect(x-8,14,16,24,3)
    s.cl(102,60,118,60);s.cl(110,52,110,68);s.cl(28,55,52,55);s.cl(40,43,40,67)
    s.dim(0,100,160,100,24);s.dim(0,0,0,100,30);s.dim(0,0,40,0,-24,'40');s.dim(0,0,110,0,-60,'110');s.dim(160,0,160,60,-30,'60');s.dim(160,0,160,55,-60,'55')
    s.dim(0,8,0,92,64,'84');s.dim(16,100,32,100,48,'16')
    s.lead(110,60,45,50,'Ø14 (bearing)',7);s.lead(40,55,150,50,'Ø20',10);s.lead(51.31,66.31,60,60,'Ø4 × 4 on Ø32, at 45°',2)
    s.lead(144,8,-60,30,'Ø4 × 18',2)
    s.lead(2.93,97.07,135,20,'R10 × 4')
    s.note('Thickness 5. Hole rows at y = 8 and y = 92, x = 16, 32 … 144. Windows 16 × 24, R3, centers x = 70, 92, 114, y = 26.',598)
    return m,s

@task(25,'Grid plate with center window',['linear pattern','skip instances','fillet','remove'],'Same 8 mm grid as T12, but the 9 holes in the middle are replaced by a 20 × 20 window. Hint: pattern the holes, then use **Skip instances** in the pattern, or cut the window and delete the extra holes.')
def t25():
    pts=[(-32+8*i,-32+8*j) for i in range(9) for j in range(9) if not(abs(-32+8*i)<=8 and abs(-32+8*j)<=8)]
    m=W().rect(80,80).extrude(4).edges('|Z').fillet(4)
    m=m.cut(W().pushPoints(pts).circle(2).extrude(4))
    m=m.cut(W().rect(20,20).extrude(4).edges('|Z').fillet(4))
    s=S(800,660,6);s.at(300,330);s.rrect(-40,-40,80,80,4);s.rect(-10,-10,20,20,4)
    for p in pts:s.circ(*p,2)
    s.cl(-45,0,45,0);s.cl(0,-45,0,45)
    s.dim(-40,40,40,40,24);s.dim(-40,-40,-40,40,30);s.dim(-40,-40,-32,-40,-24,'8');s.dim(-32,-40,-24,-40,-44,'8')
    s.lead(32,32,40,40,'Ø4 × 72',2);s.lead(40-1.17,-40+1.17,-40,30,'R4 × 4');s.dim(-10,-7,10,-7,0,'20');s.dim(7,-10,7,10,0,'20');s.lead(-10+1.17,10-1.17,-45,20,'R4',0)
    s.at(660,330);s.rrect(0,-40,4,80);s.dim(0,40,4,40,24,'4')
    s.note('Thickness 4. Grid 9 × 9, pitch 8, centered. The middle 3 × 3 holes are not there.',645)
    return m,s

@task(26,'Rocker arm (one sketch)',['one sketch','tangent','mirror in sketch','circular + linear pattern in sketch'],'Rule: **one sketch, one Extrude**. Everything (outline and all holes) must be in a single fully defined sketch. Draw the top tangent line once and use the sketch **Mirror** about a construction centerline; use the sketch **Circular pattern** and **Linear pattern** tools for the holes.')
def t26():
    d,r1,r2=90,25,12;sf=(r1-r2)/d;cf=math.sqrt(1-sf*sf)
    A1=(r1*sf,r1*cf);B1=(d+r2*sf,r2*cf)
    m=(W().moveTo(*A1).lineTo(*B1).threePointArc((d+r2,0),(B1[0],-B1[1])).lineTo(A1[0],-A1[1]).threePointArc((-r1,0),A1).close().extrude(5))
    h=[((0,0),14),((d,0),8)]+[((18*math.cos(i*pi/2),18*math.sin(i*pi/2)),4) for i in range(4)]+[((30+10*i,0),6) for i in range(5)]
    for (x,y),dd in h:m=m.cut(W().center(x,y).circle(dd/2).extrude(5))
    s=S(860,470,5);s.at(190,230)
    s.pd([('M',)+A1,('L',)+B1,('A',r2,1,1,B1[0],-B1[1]),('L',A1[0],-A1[1]),('A',r1,1,1)+A1,('Z',)])
    for (x,y),dd in h:s.circ(x,y,dd/2)
    s.e.append(f'<circle cx="190" cy="230" r="{18*5}" fill="none" stroke="#c33" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    s.cl(-30,0,107,0);s.cl(0,-30,0,30);s.cl(d,-16,d,16)
    s.dim(0,-r1,d,-r1,-50,'90');s.dim(0,-r1,30,-r1,-26,'30');s.dim(30,0,40,0,-12,'10')
    s.lead(-r1*0.707,r1*0.707,135,30,'R25',0);s.lead(d+r2*0.707,r2*0.707,45,40,'R12',0)
    s.lead(0,0,-110,95,'Ø14',7);s.lead(d,0,-60,70,'Ø8',4)
    s.lead(0,18,60,70,'Ø4 × 4 on Ø36',2)
    s.lead(70,0,70,80,'Ø6 × 5',3)
    s.at(790,230);s.rrect(0,-25,5,50);s.dim(0,25,5,25,24,'5')
    s.note('Outline: R25 and R12 joined by two tangent lines. Symmetric about the centerline.',445)
    return m,s

ONE='Rule: **one sketch, one Extrude**. Everything in a single fully defined sketch.'
def arcslot(cx,cy,R,a1,a2,w):
    r=w/2;p=lambda rr,a:(cx+rr*math.cos(math.radians(a)),cy+rr*math.sin(math.radians(a)))
    return [('M',)+p(R+r,a1),('A',R+r,0,0)+p(R+r,a2),('A',r,0,0)+p(R-r,a2),('A',R-r,0,1)+p(R-r,a1),('A',r,0,0)+p(R+r,a1),('Z',)]
def cq_arcslot(cx,cy,R,a1,a2,w):
    r=w/2;p=lambda rr,a:(cx+rr*math.cos(math.radians(a)),cy+rr*math.sin(math.radians(a)))
    am=(a1+a2)/2
    return (W().moveTo(*p(R+r,a1)).threePointArc(p(R+r,am),p(R+r,a2)).threePointArc(p(R,a2+math.degrees(r/R)*1.0) if False else (cx+R*math.cos(math.radians(a2))+r*math.cos(math.radians(a2+90)),cy+R*math.sin(math.radians(a2))+r*math.sin(math.radians(a2+90))),p(R-r,a2))
            .threePointArc(p(R-r,am),p(R-r,a1)).threePointArc((cx+R*math.cos(math.radians(a1))+r*math.cos(math.radians(a1-90)),cy+R*math.sin(math.radians(a1))+r*math.sin(math.radians(a1-90))),p(R+r,a1)).close())

@task(27,'Tensioner plate',['one sketch','arc slot','concentric','pattern'],ONE+' The arc slot is centered on the pivot hole: a belt idler on it swings around the pivot.')
def t27():
    m=W().center(35,25).rect(70,50).extrude(4).edges('|Z').fillet(5)
    m=m.cut(W().center(10,10).circle(3).extrude(4)).cut(cq_arcslot(10,10,40,15,60,5).extrude(4))
    m=m.cut(W().pushPoints([(62,8),(62,42)]).circle(2).extrude(4))
    s=S(760,490,5.5);s.at(330,400);s.rrect(0,0,70,50,5);s.circ(10,10,3);s.pd(arcslot(10,10,40,15,60,5),False)
    s.circ(62,8,2);s.circ(62,42,2)
    s.line(10,10,10+46*math.cos(math.radians(15)),10+46*math.sin(math.radians(15)),'#c33',0.8,'10 3 2 3');s.line(10,10,10+46*math.cos(math.radians(60)),10+46*math.sin(math.radians(60)),'#c33',0.8,'10 3 2 3')
    s.cl(4,10,16,10);s.cl(10,4,10,16)
    s.dim(0,50,70,50,24);s.dim(0,0,0,50,30);s.dim(0,0,10,0,-24,'10');s.dim(0,0,0,10,60,'10');s.dim(0,0,62,0,-50,'62');s.dim(70,0,70,8,-26,'8');s.dim(70,8,70,42,-26,'34')
    s.lead(10,10,-120,40,'Ø6',3);s.lead(10+37.5*math.cos(math.radians(45)),10+37.5*math.sin(math.radians(45)),-135,30,'arc slot R40 (center line), width 5',0)
    s.lead(62,42,60,30,'Ø4 × 2',2)
    s.e.append(f'<text x="{330+10*5.5+60:.0f}" y="{400-10*5.5-8:.0f}" font-size="14" font-family="Arial" fill="#0a3d91">15°</text><text x="{330+10*5.5+18:.0f}" y="{400-10*5.5-62:.0f}" font-size="14" font-family="Arial" fill="#0a3d91">60°</text>')
    s.note('Thickness 4. Corners R5. Slot from 15° to 60°, angles measured from the horizontal through the pivot.',478)
    return m,s

@task(28,'Triangle link',['one sketch','tangent','circular pattern in sketch'],ONE+' Three bosses joined by tangent lines.')
def t28():
    R0=50/math.sqrt(3);P=[(R0*math.cos(pi/2+i*2*pi/3),R0*math.sin(pi/2+i*2*pi/3)) for i in range(3)]
    m=W().polyline(P).close().extrude(5)
    for p in P:m=m.union(W().center(*p).circle(10).extrude(5))
    hull=W()
    pts=[]
    for i in range(3):
        a=pi/2+i*2*pi/3
        for da in(-pi/3,pi/3):pts.append((P[i][0]+10*math.cos(a+da),P[i][1]+10*math.sin(a+da)))
    m=m.union(W().polyline(pts).close().extrude(5))
    m=m.cut(W().circle(8).extrude(5)).cut(W().pushPoints(P).circle(3).extrude(5))
    s=S(640,490,5);s.at(260,270)
    cmd=[('M',)+pts[1]]
    for i in range(3):
        j=(i+1)%3;cmd.append(('L',)+pts[2*j]);cmd.append(('A',10,0,0)+pts[2*j+1])
    s.pd(cmd+[('Z',)])
    for p in P:s.circ(*p,3)
    s.circ(0,0,8);s.e.append(f'<circle cx="260" cy="270" r="{R0*5:.1f}" fill="none" stroke="#c33" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    s.cl(-40,0,40,0);s.cl(0,-30,0,45)
    for i in range(3):s.line(*P[i],*P[(i+1)%3],'#c33',0.8,'10 3 2 3')
    s.dim(P[1][0],P[1][1],P[1][0],P[0][1],70,'43.3');s.dim(0,0,0,P[0][1],-60,'28.87');s.cl(P[1][0]-16,P[0][1],P[0][0]+2,P[0][1])
    s.dim(*P[1],*P[2],-40,'50 (equilateral)');s.lead(P[0][0],P[0][1]+10,60,30,'R10 × 3',0);s.lead(*P[2],30,50,'Ø6 × 3',3);s.lead(0,0,200,60,'Ø16',8)
    s.at(560,270);s.rrect(0,-25,5,50);s.dim(0,25,5,25,24,'5')
    s.note('Boss centers: equilateral triangle, side 50, centered on the Ø16 hole, one boss straight up.',478)
    return m,s

@task(29,'Hex pocket plate',['one sketch','polygon','two staggered linear patterns'],ONE+' Two patterns: one row of 7 and two rows of 6, shifted by half a step.')
def t29():
    hx=lambda x,y:W().polyline([(x+5/math.cos(pi/6)*math.cos(pi/6+k*pi/3),y+5/math.cos(pi/6)*math.sin(pi/6+k*pi/3)) for k in range(6)]).close().extrude(4)
    m=W().rect(110,64).extrude(4).edges('|Z').fillet(5)
    pts=[(-36+12*i,0) for i in range(7)]+[(-30+12*i,y) for i in range(6) for y in(-16,16)]
    for p in pts:m=m.cut(hx(*p))
    s=S(760,490,4.8);s.at(360,250);s.rrect(-55,-32,110,64,5);r=5/math.cos(pi/6)
    for x,y in pts:s.poly([(x+r*math.cos(pi/6+a*pi/3),y+r*math.sin(pi/6+a*pi/3)) for a in range(6)],False)
    s.cl(-60,0,60,0);s.cl(0,-36,0,36)
    s.dim(-55,32,55,32,24);s.dim(-55,-32,-55,32,30);s.dim(-36,-32,-24,-32,-24,'12');s.dim(-36,-32,-30,-32,-48,'6')
    s.dim(55,0,55,16,-30,'16');s.dim(55,-16,55,0,-30,'16');s.lead(30,16,60,40,'hex 10 A/F',0);s.lead(55-1.46,-32+1.46,-45,30,'R5 × 4',0)
    s.note('Hexes 10 across flats, flats vertical. Middle row: 7, x = −36 … 36. Rows y = ±16: 6, x = −30 … 30. Thickness 4, R5.',480)
    return m,s

@task(30,'Encoder disk',['one sketch','two circular patterns','construction circles'],ONE+' Two circular patterns with different counts.')
def t30():
    m=W().circle(30).circle(10).extrude(2)
    sl=W().center(24.5,0).rect(7,2).extrude(2)
    for i in range(24):m=m.cut(sl.rotate((0,0,0),(0,0,1),15*i))
    m=m.cut(W().polarArray(13,90,360,3).circle(1.6).extrude(2))
    s=S(640,470,6);s.at(250,240);s.circ(0,0,30);s.circ(0,0,10)
    for i in range(24):
        a=math.radians(15*i);c,sn=math.cos(a),math.sin(a)
        q=[(21,-1),(28,-1),(28,1),(21,1)];s.poly([(x*c-y*sn,x*sn+y*c) for x,y in q],False)
    for i in range(3):a=pi/2+i*2*pi/3;s.circ(13*math.cos(a),13*math.sin(a),1.6)
    s.e.append(f'<circle cx="250" cy="240" r="{13*6}" fill="none" stroke="#c33" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    s.cl(-34,0,34,0);s.cl(0,-34,0,34)
    s.lead(0,0,-40,60,'Ø60',30);s.lead(0,0,-140,30,'Ø20',10);s.lead(13*math.cos(pi/2+2*pi/3),13*math.sin(pi/2+2*pi/3),-150,90,'Ø3.2 × 3 on Ø26',1.6)
    s.dim(21,1,28,1,40,'7');s.lead(28*math.cos(math.radians(30)),28*math.sin(math.radians(30)),40,40,'24 slots, 2 wide, r 21 … 28',0)
    s.at(560,240);s.rrect(0,-30,2,60);s.dim(0,30,2,30,24,'2')
    s.note('One slot on the horizontal axis; one hole straight up.',455)
    return m,s

@task(31,'Five-window wheel',['one sketch','sketch fillet','circular pattern in sketch'],ONE+' Draw one window with its four R3 corners as sketch fillets, then pattern it.')
def t31():
    m=W().circle(40).circle(4).extrude(5)
    ring=W().circle(34).circle(14).extrude(5)
    for i in range(5):ring=ring.cut(W().center(20,0).rect(40,8).extrude(5).rotate((0,0,0),(0,0,1),90+72*i))
    ring=ring.edges('|Z').fillet(3)
    m=m.cut(ring)
    s=S(660,470,4.6);s.at(240,245)
    s.circ(0,0,40);s.circ(0,0,4)
    for i in range(5):
        a1=math.radians(90+72*i);a2=a1+math.radians(72)
        def bound(a,sg,r):
            x=r*math.cos(a);y=r*math.sin(a);return x,y
        r_in,r_out=14,34
        def off(a,sg,r):
            d=4/r;return a+sg*math.asin(4/r)
        p1=(r_out*math.cos(off(a1,1,34)),r_out*math.sin(off(a1,1,34)));p2=(r_out*math.cos(off(a2,-1,34)),r_out*math.sin(off(a2,-1,34)))
        p3=(r_in*math.cos(off(a2,-1,14)),r_in*math.sin(off(a2,-1,14)));p4=(r_in*math.cos(off(a1,1,14)),r_in*math.sin(off(a1,1,14)))
        s.pd([('M',)+p1,('A',34,0,0)+p2,('L',)+p3,('A',14,0,1)+p4,('Z',)],False)
    s.cl(-44,0,44,0);s.cl(0,-44,0,44)
    s.lead(0,0,-30,50,'Ø80',40);s.lead(0,0,-110,80,'Ø8',4)
    s.dim(-4,24,4,24,0,'8')
    s.at(540,245);s.rrect(0,-40,5,80);s.dim(0,40,5,40,24,'5')
    s.note('5 spokes, 8 wide, one straight up. Windows between r = 14 and r = 34, all corners R3. Thickness 5.',460)
    return m,s

@task(32,'Truss rail',['one sketch','two linear patterns','mirror in sketch'],ONE+' Triangles pointing up and down: two linear patterns, shifted by half a step.')
def t32():
    m=W().rect(220,30).extrude(4).edges('|Z').fillet(4)
    up=lambda x:W().polyline([(x-9,-9),(x+9,-9),(x,9)]).close().extrude(4)
    dn=lambda x:W().polyline([(x-9,9),(x+9,9),(x,-9)]).close().extrude(4)
    for k in range(8):m=m.cut(up(-84+24*k))
    for k in range(7):m=m.cut(dn(-72+24*k))
    m=m.cut(W().pushPoints([(x,y) for x in(-102,102) for y in(-8,8)]).circle(2.5).extrude(4))
    s=S(900,330,3.6);s.at(460,170);s.rrect(-110,-15,220,30,4)
    for k in range(8):x=-84+24*k;s.poly([(x-9,-9),(x+9,-9),(x,9)],False)
    for k in range(7):x=-72+24*k;s.poly([(x-9,9),(x+9,9),(x,-9)],False)
    for x in(-102,102):
        for y in(-8,8):s.circ(x,y,2.5)
    s.cl(-114,0,114,0)
    s.dim(-110,15,110,15,24);s.dim(110,-15,110,15,-30,'30');s.dim(-84,-9,-60,-9,-40,'24');s.dim(-93,-9,-75,-9,-62,'18');s.dim(-84,-9,-84,9,0,'18')
    s.dim(-110,-15,-102,-15,-26,'8');s.dim(-110,-8,-110,8,30,'16');s.lead(102,8,120,30,'Ø5 × 4',2.5)
    s.note('Triangles: base 18, height 18. Up: 8, centers x = −84 … 84. Down: 7, x = −72 … 72. Thickness 4.',316)
    return m,s

@task(33,'Keyhole plate',['one sketch','trim','2-direction pattern in sketch'],ONE+' Each keyhole is a circle plus a slot: trim the lines inside so one closed outline is left.')
def t33():
    m=W().rect(90,60).extrude(3).edges('|Z').fillet(4)
    for x in(-25,0,25):
        for y in(-12,12):m=m.cut(W().center(x,y).circle(4).extrude(3)).cut(W().center(x,y+4).rect(4,8).extrude(3)).cut(W().center(x,y+8).circle(2).extrude(3))
    s=S(700,460,5.5);s.at(300,240);s.rrect(-45,-30,90,60,4)
    for x in(-25,0,25):
        for y in(-12,12):
            a=math.asin(2/4);px=4*math.cos(a)
            s.pd([('M',x-2,y+px),('L',x-2,y+8),('A',2,0,1,x+2,y+8),('L',x+2,y+px),('A',4,1,1,x-2,y+px),('Z',)],False)
    s.cl(-50,0,50,0);s.cl(0,-34,0,34)
    s.dim(-45,30,45,30,24);s.dim(-45,-30,-45,30,30);s.dim(-25,-30,0,-30,-24,'25');s.dim(45,-12,45,12,-30,'24')
    s.lead(25,-12,-40,40,'Ø8 × 6',4);s.lead(45-1.17,-30+1.17,-45,25,'R4 × 4',0);s.dim(23,22,27,22,22,'4');s.dim(25,12,25,20,-34,'8');s.cl(21,20,29,20);s.lead(23.6,21.4,135,30,'R2',0)
    s.note('Thickness 3, corners R4. Keyholes in 3 columns × 2 rows. Slot width 4, its end R2 is 8 above the Ø8 center.',448)
    return m,s

@task(34,'Triangle gusset with holes',['one sketch','pattern + delete instances','fillet in sketch'],ONE+' Pattern the holes in 2 directions, then remove the ones that fall outside the triangle.')
def t34():
    m=W().polyline([(0,0),(80,0),(0,80)]).close().extrude(4)
    m=m.edges('|Z').fillet(6)
    pts=[(10+12*i,10+12*j) for i in range(4) for j in range(4) if i+j<=3]
    m=m.cut(W().pushPoints(pts).circle(2.5).extrude(4))
    s=S(660,560,5);s.at(120,460)
    q=[(0,0),(80,0),(0,80)];r=6
    c0=(6,6);c1=(80-6*(1+math.sqrt(2)),6);c2=(6,80-6*(1+math.sqrt(2)))
    d=6/math.tan(math.radians(22.5));e=d/math.sqrt(2)
    s.pd([('M',6,0),('L',80-d,0),('A',6,0,0,80-e,e),('L',e,80-e),('A',6,0,0,0,80-d),('L',0,6),('A',6,0,0,6,0),('Z',)])
    for a1,b1,a2,b2 in[(80-d,0,80,0),(80-e,e,80,0),(e,80-e,0,80),(0,80-d,0,80),(0,6,0,0),(6,0,0,0)]:s.line(a1,b1,a2,b2,'#555',0.8,'4 3')
    for p in pts:s.circ(*p,2.5)
    s.dim(0,0,80,0,-30);s.dim(0,0,0,80,30);s.dim(0,0,10,0,-56,'10');s.dim(10,0,22,0,-56,'12');s.dim(0,0,0,10,56,'10');s.dim(0,10,0,22,56,'12')
    s.lead(46,10,40,50,'Ø5 × 10',2.5);s.lead(80-e,e,60,40,'R6 × 3',0)
    s.at(560,460);s.rrect(0,0,4,80);s.dim(0,80,4,80,24,'4')
    s.note('Holes on a 12 grid from (10, 10); keep the 10 holes with i + j ≤ 3.',548);s.note('80 × 80: to the sharp corners (dashed), before the R6 fillets.',60)
    return m,s

res={}
for t in T:
    m,s=t['fn']()
    v=m.val().Volume();k='t%02d'%t['id'];res[k]=dict(v=v)
    if t['id']==21:res[k]['v7']=t21.v7
    s.svg(OUT+k+'.svg','T%02d · %s'%(t['id'],t['title']))
    iso(m,k+'-3d.svg')
    print(k,t['title'],'%.0f'%v,('N=7 %.0f'%t21.v7) if t['id']==21 else '')
json.dump({k:dict(**r,title=t['title'],topics=t['topics'],text=t['text']) for (k,r),t in zip(res.items(),T)},open('tools/tasks.json','w'),indent=1,ensure_ascii=False)
