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

res={}
for t in T:
    m,s=t['fn']()
    v=m.val().Volume();k='t%02d'%t['id'];res[k]=dict(v=v)
    if t['id']==21:res[k]['v7']=t21.v7
    s.svg(OUT+k+'.svg','T%02d · %s'%(t['id'],t['title']))
    iso(m,k+'-3d.svg')
    print(k,t['title'],'%.0f'%v,('N=7 %.0f'%t21.v7) if t['id']==21 else '')
json.dump({k:dict(**r,title=t['title'],topics=t['topics'],text=t['text']) for (k,r),t in zip(res.items(),T)},open('tools/tasks.json','w'),indent=1,ensure_ascii=False)
