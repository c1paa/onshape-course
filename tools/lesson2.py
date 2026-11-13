import math,sys,json,os
sys.path.insert(0,'tools')
import cadquery as cq
from draw import S
W=cq.Workplane;pi=math.pi
OUT='docs/img/l2/';os.makedirs(OUT,exist_ok=True)
def iso(shape,fn):
    p=OUT+fn
    cq.exporters.export(shape,p,opt={'width':300,'height':220,'marginLeft':12,'marginTop':12,'showAxes':False,'projectionDir':(1,-1.2,0.9),'showHidden':False,'strokeWidth':-1})
    t=open(p).read();i=t.index('<g transform');j=t.rindex('</svg>')
    t=t[:i]+'<rect width="300" height="220" fill="white"/><g transform="matrix(-1 0 0 -1 300 220)">'+t[i:j]+'</g>'+t[j:]
    open(p,'w').write(t)
R={}
def hull2(r1,r2,d):
    sf=(r1-r2)/d;cf=math.sqrt(1-sf*sf);A=(r1*sf,r1*cf);B=(d+r2*sf,r2*cf)
    return A,B,W().moveTo(*A).lineTo(*B).threePointArc((d+r2,0),(B[0],-B[1])).lineTo(A[0],-A[1]).threePointArc((-r1,0),A).close()
def hullpath(s,A,B,r1,r2,dx=0):
    s.pd([('M',)+A,('L',)+B,('A',r2,1,1,B[0],-B[1]),('L',A[0],-A[1]),('A',r1,1,1)+A,('Z',)])
def arcslot_cq(R,a1,a2,w):
    r=w/2;p=lambda rr,a:(rr*math.cos(math.radians(a)),rr*math.sin(math.radians(a)))
    am=(a1+a2)/2;e2=(R*math.cos(math.radians(a2))+r*math.cos(math.radians(a2+90)),R*math.sin(math.radians(a2))+r*math.sin(math.radians(a2+90)))
    e1=(R*math.cos(math.radians(a1))+r*math.cos(math.radians(a1-90)),R*math.sin(math.radians(a1))+r*math.sin(math.radians(a1-90)))
    return W().moveTo(*p(R+r,a1)).threePointArc(p(R+r,am),p(R+r,a2)).threePointArc(e2,p(R-r,a2)).threePointArc(p(R-r,am),p(R-r,a1)).threePointArc(e1,p(R+r,a1)).close()
def arcslot_d(R,a1,a2,w):
    r=w/2;p=lambda rr,a:(rr*math.cos(math.radians(a)),rr*math.sin(math.radians(a)))
    return [('M',)+p(R+r,a1),('A',R+r,0,0)+p(R+r,a2),('A',r,0,0)+p(R-r,a2),('A',R-r,0,1)+p(R-r,a1),('A',r,0,0)+p(R+r,a1),('Z',)]
items=[]
def item(k,title,group,text=''):
    def d(fn):items.append(dict(k=k,title=title,group=group,text=text,fn=fn));return fn
    return d

@item('c1','Rounded rectangle','min','Target: **3 dimensions**. Centered on the origin.')
def c1():
    m=W().rect(60,30).extrude(4).edges('|Z').fillet(5)
    s=S(560,300,5);s.at(240,160);s.rrect(-30,-15,60,30,5);s.cl(-36,0,36,0);s.cl(0,-20,0,20)
    s.dim(-30,15,30,15,24);s.dim(30,-15,30,15,-30);s.lead(-30+1.46,15-1.46,135,25,'R5 × 4',0)
    return m,s
@item('c2','Square with 4 holes','min','Target: **3 dimensions**. Hint: a construction square through the hole centers, and Equal.')
def c2():
    m=W().rect(50,50).extrude(4).faces('>Z').workplane().rect(34,34,forConstruction=True).vertices().hole(6)
    s=S(560,390,4.4);s.at(240,200);s.rrect(-25,-25,50,50)
    for x in(-17,17):
        for y in(-17,17):s.circ(x,y,3)
    s.line(-17,-17,17,-17,'#c33',0.8,'6 3');s.line(17,-17,17,17,'#c33',0.8,'6 3');s.line(17,17,-17,17,'#c33',0.8,'6 3');s.line(-17,17,-17,-17,'#c33',0.8,'6 3')
    s.dim(-25,25,25,25,24,'50');s.dim(-25,-25,-17,-25,-24,'8');s.lead(17,17,40,40,'Ø6 × 4',3)
    s.note('Square 50 × 50, centered. Holes 8 from both edges.',380)
    return m,s
@item('c3','Hex nut','min','Target: **2 dimensions**. Which polygon option gives "across flats" directly?')
def c3():
    m=W().polygon(6,13/math.cos(pi/6)).extrude(5).faces('>Z').workplane().hole(6)
    s=S(520,300,9);s.at(220,150);r=6.5/math.cos(pi/6)
    s.poly([(r*math.cos(a*pi/3),r*math.sin(a*pi/3)) for a in range(6)]);s.circ(0,0,3);s.e.append('')
    s.dim(-9,-6.5,-9,6.5,30,'13 A/F');s.lead(0,0,45,40,'Ø6',3)
    return m,s
@item('c4','Cam (two circles + tangents)','min','Target: **3 dimensions**.')
def c4():
    A,B,w=hull2(20,10,50);m=w.extrude(4)
    s=S(620,300,4.6);s.at(170,150);hullpath(s,A,B,20,10);s.cl(-25,0,64,0);s.cl(0,-24,0,24);s.cl(50,-14,50,14)
    s.dim(0,-20,50,-20,-40,'50');s.lead(-14.1,14.1,135,25,'R20',0);s.lead(50+7.07,7.07,45,30,'R10',0)
    return m,s
@item('c5','Trapezoid with a hole','min','Target: **4 dimensions**. The hole is in the middle of the height, on the axis (Midpoint, Symmetric).')
def c5():
    m=W().polyline([(-30,0),(30,0),(15,25),(-15,25)]).close().extrude(4).cut(W().center(0,12.5).circle(4).extrude(4))
    s=S(560,320,5.5);s.at(270,260);s.poly([(-30,0),(30,0),(15,25),(-15,25)]);s.circ(0,12.5,4);s.cl(0,-4,0,29)
    s.dim(-30,0,30,0,-30,'60');s.dim(-15,25,15,25,24,'30');s.dim(30,0,30,25,-50,'25');s.lead(0,12.5,40,50,'Ø8',4)
    return m,s
@item('c6','Slotted bar with 3 holes','min','Target: **3 dimensions**. End holes are concentric with the slot ends; the middle one sits at the midpoint.')
def c6():
    m=W().slot2D(80,16).extrude(4).cut(W().pushPoints([(-32,0),(0,0),(32,0)]).circle(3).extrude(4))
    s=S(620,260,5.5);s.at(310,130);s.slot(0,0,80,16,True)
    for x in(-32,0,32):s.circ(x,0,3)
    s.cl(-46,0,46,0);s.dim(-40,8,40,8,24,'80');s.dim(40,-8,40,8,-30,'16');s.lead(32,0,-50,40,'Ø6 × 3',3)
    return m,s

@item('m1','Mirror: bracket','demo','Draw the **right half** only, then sketch **Mirror** about a vertical construction line through the origin.')
def m1():
    h=[(0,0),(30,0),(30,10),(15,25),(15,40),(0,40)];full=h+[(-x,y) for x,y in reversed(h)][1:-1]
    m=W().polyline(full).close().extrude(4).cut(W().pushPoints([(-22,5),(22,5),(0,32)]).circle(3).extrude(4))
    s=S(560,430,5.5);s.at(290,330);s.poly(full)
    for p in[(-22,5),(22,5),(0,32)]:s.circ(*p,3)
    s.cl(0,-4,0,44)
    s.dim(-30,0,30,0,-30,'60');s.dim(30,0,30,10,-24,'10');s.dim(15,25,15,40,-50,'15');s.dim(-15,40,15,40,24,'30');s.dim(0,0,22,0,-55,'22');s.lead(22,5,40,40,'Ø6 × 3',3)
    s.dim(-30,0,-30,40,40,'40');s.cl(-15,40,-33,40);s.note('Sloped edge from (30, 10) to (15, 25).',420)
    return m,s
@item('p1','Circular pattern: flange with notches','demo','Two sketch circular patterns: 6 holes, and 6 notches on the rim shifted by 30°.')
def p1():
    m=W().circle(25).circle(5).extrude(4).cut(W().polarArray(17,0,360,6).circle(4).extrude(4)).cut(W().polarArray(25,30,360,6).circle(3).extrude(4))
    s=S(560,340,5);s.at(220,175)
    n=6;b=2*math.asin(3/50);p=lambda a,r:(r*math.cos(a),r*math.sin(a));ang=[(pi/6+i*pi/3-b,pi/6+i*pi/3+b) for i in range(n)]
    cmd=[('M',)+p(ang[0][1],25)]
    for i in range(n):j=(i+1)%n;cmd+=[('A',25,0,0)+p(ang[j][0],25),('A',3,0,1)+p(ang[j][1],25)]
    s.pd(cmd+[('Z',)]);s.circ(0,0,5)
    for i in range(6):s.circ(17*math.cos(i*pi/3),17*math.sin(i*pi/3),4)
    s.e.append(f'<circle cx="220" cy="175" r="{17*5}" fill="none" stroke="#c33" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    s.lead(0,0,-40,40,'Ø50',25);s.lead(17,0,30,50,'Ø8 × 6 on Ø34',4);s.lead(25*math.cos(5*pi/6)+3*0.87,25*math.sin(5*pi/6)-1.5,150,30,'R3 × 6, at 30°',0);s.note('Center hole Ø10.',330)
    return m,s
@item('o1','Offset: frame','demo','Draw the outer outline, then **Offset** it 5 inward. Extrude the region between the two outlines.')
def o1():
    A,B,w=hull2(20,12,60);out=w.extrude(3);inn=hull2(15,7,60)[2].extrude(3)
    m=out.cut(inn)
    s=S(620,320,4.4);s.at(190,160);hullpath(s,A,B,20,12)
    A2,B2,_=hull2(15,7,60);hullpath(s,A2,B2,15,7)
    s.cl(-25,0,77,0);s.cl(0,-24,0,24);s.cl(60,-16,60,16)
    s.dim(0,-20,60,-20,-40,'60');s.lead(-14.1,14.1,135,25,'R20',0);s.lead(60+8.5,8.5,45,30,'R12',0);s.lead(30,-15.8,-60,40,'wall 5 (Offset)',0)
    s.note('Thickness 3.',310)
    return m,s

@item('a','Intake arm plate','model','Uses: tangent, Mirror, polygon (circumscribed), circular pattern, Offset, Trim, sketch fillet. One sketch, Extrude 5.')
def la():
    A,B,w=hull2(16,10,80);m=w.extrude(5)
    pk=hull2(11,5,80)[2].extrude(5).cut(W().circle(21).extrude(5)).cut(W().center(80,0).circle(15).extrude(5)).edges('|Z').fillet(2)
    m=m.cut(pk)
    m=m.cut(W().polygon(6,8/math.cos(pi/6)).extrude(5).rotate((0,0,0),(0,0,1),30))
    m=m.cut(W().polarArray(11,45,360,4).circle(2).extrude(5)).cut(W().center(80,0).circle(2.5).extrude(5))
    s=S(760,400,6);s.at(150,200);hullpath(s,A,B,16,10)
    A3,B3,_=hull2(11,5,80);dx,dy=B3[0]-A3[0],B3[1]-A3[1]
    def hit(cx,R,first):
        aa=dx*dx+dy*dy;bb=2*(dx*(A3[0]-cx)+dy*A3[1]);cc=(A3[0]-cx)**2+A3[1]**2-R*R
        d=math.sqrt(bb*bb-4*aa*cc);tt=(-bb+d)/(2*aa) if first else (-bb-d)/(2*aa)
        return (A3[0]+tt*dx,A3[1]+tt*dy)
    P1=hit(0,21,True);P2=hit(80,15,False)
    s.pd([('M',)+P1,('L',)+P2,('A',15,0,0,P2[0],-P2[1]),('L',P1[0],-P1[1]),('A',21,0,0)+P1,('Z',)],False)
    r=4/math.cos(pi/6);s.poly([(r*math.cos(pi/6+a*pi/3),r*math.sin(pi/6+a*pi/3)) for a in range(6)],False)
    for i in range(4):a=pi/4+i*pi/2;s.circ(11*math.cos(a),11*math.sin(a),2)
    s.e.append(f'<circle cx="150" cy="200" r="{11*6}" fill="none" stroke="#c33" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    s.circ(80,0,2.5);s.cl(-20,0,94,0)
    s.dim(0,-16,80,-16,-50,'80');s.lead(-11.3,11.3,135,25,'R16',0);s.lead(80+7.07,7.07,45,30,'R10',0)
    s.lead(0,0,-100,90,'hex 8 A/F',4);s.lead(11*0.707,11*0.707,70,60,'Ø4 × 4 on Ø22, at 45°',2);s.lead(80,0,-60,60,'Ø5',2.5)
    s.note('Pocket: Offset the outline 5 inward, Trim it with circles R21 (around the hub) and R15 (around the end), corners R2.',385)
    return m,s
@item('b','Adjustable motor mount','model','Uses: center rectangle, sketch chamfer, concentric, arc + Offset for slots, circular pattern, Symmetric. One sketch, Extrude 4.')
def lb():
    m=W().rect(70,50).extrude(4).edges('|Z').chamfer(5)
    m=m.cut(W().circle(12).extrude(4))
    for i in range(4):m=m.cut(arcslot_cq(18,-15+90*i,15+90*i,4).extrude(4))
    m=m.cut(W().pushPoints([(x,y) for x in(-29,29) for y in(-19,19)]).circle(2).extrude(4))
    s=S(720,420,5.2);s.at(280,215);s.poly([(-30,-25),(30,-25),(35,-20),(35,20),(30,25),(-30,25),(-35,20),(-35,-20)]);s.circ(0,0,12)
    for i in range(4):s.pd(arcslot_d(18,-15+90*i,15+90*i,4),False)
    for x in(-29,29):
        for y in(-19,19):s.circ(x,y,2)
    s.e.append(f'<circle cx="280" cy="215" r="{18*5.2:.1f}" fill="none" stroke="#c33" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    s.cl(-40,0,40,0);s.cl(0,-30,0,30)
    s.dim(-35,25,35,25,24,'70');s.dim(-35,-25,-35,25,30,'50');s.dim(-29,-25,29,-25,-24,'58');s.dim(35,-19,35,19,-30,'38')
    s.lead(0,0,200,40,'Ø24',12);s.lead(-32.5,22.5,135,25,'5 × 45° × 4',0);s.lead(29,-19,-45,30,'Ø4 × 4',2)
    s.note('4 slots: arc R18 from −15° to +15°, concentric with Ø24, Offset 2 to both sides, round ends.',405)
    return m,s

for it in items:
    m,s=it['fn']();v=m.val().Volume();R[it['k']]=dict(v=round(v),title=it['title'],group=it['group'],text=it['text'])
    s.svg(OUT+it['k']+'.svg',it['title']);iso(m,it['k']+'-3d.svg');print(it['k'],round(v))
json.dump(R,open('tools/lesson2.json','w'),indent=1,ensure_ascii=False)
