import math,sys,os
sys.path.insert(0,'tools')
from draw import S
pi=math.pi
OUT='docs/img/ref/';os.makedirs(OUT,exist_ok=True)
F='#eef3fb';B='#0a3d91';R='#c33';G='#2e7d32';P2='#f6e7c8';GR='#999';SD='#d6e0f2';SL='#c3d0ea'
FT='font-family="Arial,Helvetica,sans-serif"'
def pl(s,pts,c='#111',w=1.6,d=None,fill='none',close=False):
    q=' '.join('%.1f,%.1f'%s.p(*t) for t in pts);tg='polygon' if close else 'polyline'
    s.e.append(f'<{tg} points="{q}" fill="{fill}" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{d}"' if d else '')+' stroke-linejoin="round"/>')
def arc(cx,cy,r,a1,a2,n=60):return [(cx+r*math.cos(a1+(a2-a1)*i/n),cy+r*math.sin(a1+(a2-a1)*i/n)) for i in range(n+1)]
def cp(cx,cy,r,n=72):return arc(cx,cy,r,0,2*pi,n)[:-1]
def hole(s,x,y,r,c='#111',fill='white',w=1.6,d=None):pl(s,cp(x,y,r),c,w,d,fill,True)
def num(s,x,y,t):
    a,b=s.p(x,y);s.e.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="10" fill="{B}"/><text x="{a:.1f}" y="{b+4.5:.1f}" font-size="13" font-weight="bold" {FT} text-anchor="middle" fill="white">{t}</text>')
def dot(s,x,y,c=B,r=4):
    a,b=s.p(x,y);s.e.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r}" fill="{c}"/>')
def cap(s,x,t):s.txt(x,s.h-14,t,14,px=True,bold=True)
def rot(pts,a,c=(0,0)):
    ca,sa=math.cos(a),math.sin(a);return [(c[0]+(x-c[0])*ca-(y-c[1])*sa,c[1]+(x-c[0])*sa+(y-c[1])*ca) for x,y in pts]
def ah(s,x1,y1,x2,y2,c=B):
    L=math.hypot(x2-x1,y2-y1);ux,uy=(x2-x1)/L,(y2-y1)/L
    s.e.append(f'<polygon points="{x2:.1f},{y2:.1f} {x2-ux*10-uy*4:.1f},{y2-uy*10+ux*4:.1f} {x2-ux*10+uy*4:.1f},{y2-uy*10-ux*4:.1f}" fill="{c}"/>')
def A(s,x1,y1,x2,y2,t='',both=False,c=B,d=None):
    s.e.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1.4"'+(f' stroke-dasharray="{d}"' if d else '')+'/>');ah(s,x1,y1,x2,y2,c)
    if both:ah(s,x2,y2,x1,y1,c)
    if t:T(s,(x1+x2)/2,(y1+y2)/2-7,t,12)
def T(s,x,y,t,sz=13,anc='middle',c=B,b=False):
    s.e.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{sz}" {FT} text-anchor="{anc}"'+(' font-weight="bold"' if b else '')+f' fill="{c}">{t}</text>')
def BX(s,x,y,w,h,t='',f=F,sz=13,c='#111',d=None,tc='#111'):
    s.e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{f}" stroke="{c}" stroke-width="1.4"'+(f' stroke-dasharray="{d}"' if d else '')+'/>')
    ls=t.split('|') if t else []
    for i,l in enumerate(ls):T(s,x+w/2,y+h/2+sz*0.35+(i-(len(ls)-1)/2)*(sz+4),l,sz,c=tc)
def adim(s,cx,cy,r,a1,a2,t):
    pl(s,arc(cx,cy,r,a1,a2,30),B,0.9);x,y=cx+r*math.cos(a2),cy+r*math.sin(a2);s.arrow(x,y,-math.sin(a2),math.cos(a2))
    x,y=cx+r*math.cos(a1),cy+r*math.sin(a1);s.arrow(x,y,math.sin(a1),-math.cos(a1))
    m=(a1+a2)/2;s.txt(cx+(r+3/s.k*4)*math.cos(m),cy+(r+12/s.k)*math.sin(m)-4/s.k,t,anc='start')
def ground(s,x0,x1,y):
    pl(s,[(x0,y),(x1,y)],'#111',1.2);n=int((x1-x0)/3)
    for i in range(n+1):xx=x0+i*(x1-x0)/n;pl(s,[(xx,y),(xx-2,y-2.5)],'#111',0.8)
def link(s,x0,a,ghost=False,n=2):
    L=8*n;o=arc(L,0,4,-pi/2,pi/2,20)+arc(-L,0,4,pi/2,3*pi/2,20);o=rot([(x+x0,y) for x,y in o],a)
    c=GR if ghost else '#111';pl(s,o,c,1.2 if ghost else 1.6,'5 3' if ghost else None,F if not ghost else 'none',True)
    for k in range(-n,n+1):
        cx,cy=rot([(x0+8*k,0)],a)[0];pl(s,cp(cx,cy,2,40),c,1.2 if ghost else 1.6,'5 3' if ghost else None,'white' if not ghost else 'none',True)
def kplate(s,x,y,n,m,col=F):
    s.rrect(x,y,n*8,m*8,4,col)
    for i in range(n):
        for j in range(m):hole(s,x+4+8*i,y+4+8*j,2)
def iso(x,y,z):return ((x-y)*math.cos(pi/6),(x+y)*math.sin(pi/6)+z)
def ell(r,z,cx=0,cy=0,n=96):return [iso(cx+r*math.cos(2*pi*i/n),cy+r*math.sin(2*pi*i/n),z) for i in range(n)]
def hull(p):
    p=sorted(set(p))
    def h(q):
        o=[]
        for a in q:
            while len(o)>1 and (o[-1][0]-o[-2][0])*(a[1]-o[-2][1])-(o[-1][1]-o[-2][1])*(a[0]-o[-2][0])<=0:o.pop()
            o.append(a)
        return o
    return h(p)[:-1]+h(p[::-1])[:-1]
def cyl(s,r,z0,z1):pl(s,hull(ell(r,z0)+ell(r,z1)),close=True,fill=SD);pl(s,ell(r,z1),close=True,fill=F)
def inside(p,poly):
    c=False;n=len(poly)
    for i in range(n):
        (x1,y1),(x2,y2)=poly[i],poly[(i+1)%n]
        if (y1>p[1])!=(y2>p[1]) and p[0]<x1+(p[1]-y1)*(x2-x1)/(y2-y1):c=not c
    return c
def plate(s,x0,y0,x1,y1,h,hl=None):
    pl(s,[iso(x0,y0,0),iso(x1,y0,0),iso(x1,y0,h),iso(x0,y0,h)],close=True,fill=SD)
    pl(s,[iso(x0,y0,0),iso(x0,y1,0),iso(x0,y1,h),iso(x0,y0,h)],close=True,fill=SL)
    pl(s,[iso(x0,y0,h),iso(x1,y0,h),iso(x1,y1,h),iso(x0,y1,h)],close=True,fill=F)
    if hl:
        cx,cy,r=hl;c=ell(r,h,cx,cy,120);pl(s,c,close=True,fill='white')
        k=sorted([q for q in ell(r,0,cx,cy,120) if inside(q,c)]);pl(s,k,w=1)
def trim():
    s=S(640,300,7);r=8;yc=8;yi=yc-math.sqrt(r*r-9);a0=math.atan2(yi-yc,3)
    s.at(160,150)
    pl(s,arc(0,yc,r,a0,2*pi+pi-a0));pl(s,[(3,yi),(3,-12),(-3,-12),(-3,yi)])
    pl(s,arc(0,yc,r,pi-a0,2*pi+a0),R,3);pl(s,[(3,yi),(3,yc)],R,3);pl(s,[(-3,yi),(-3,yc)],R,3)
    cap(s,160,'Before: click the red pieces')
    s.at(480,150)
    pl(s,arc(0,yc,r,a0,2*pi+pi-a0)+[(-3,yi),(-3,-12),(3,-12)],close=True,fill=F)
    cap(s,480,'After')
    s.svg(OUT+'trim.svg')
def extrude():
    s=S(700,280,4.5);h=6
    s.at(175,150)
    pl(s,[iso(-24,-16,0),iso(24,-16,0),iso(24,16,0),iso(-24,16,0)],GR,1,'5 3',close=True,fill='#f6f6f6')
    pl(s,[iso(-20,-12,0),iso(20,-12,0),iso(20,12,0),iso(-20,12,0)],B,1.6,close=True,fill='#dfe8f8')
    pl(s,ell(5,0,n=60),B,1.6,close=True,fill='white')
    cap(s,175,'Sketch')
    s.at(520,165)
    plate(s,-20,-12,20,12,h,(0,0,5))
    l=iso(-20,12,0);s.dim(l[0],l[1],l[0],l[1]+h,28,'Depth')
    cap(s,520,'Extrude')
    s.svg(OUT+'extrude.svg')
def ends():
    s=S(780,290,6);t=['Blind','Up to next','Through all']
    for i in range(3):
        cx=140+i*250;s.at(cx,70);e=[-5,-8,-24][i]
        for y0,y1 in((0,-8),(-16,-24)):
            if e<=y1:pl(s,[(-16,y0),(-3,y0),(-3,y1),(-16,y1)],close=True,fill=F);pl(s,[(3,y0),(16,y0),(16,y1),(3,y1)],close=True,fill=F)
            elif e<y0:pl(s,[(-16,y0),(-3,y0),(-3,e),(3,e),(3,y0),(16,y0),(16,y1),(-16,y1)],close=True,fill=F)
            else:pl(s,[(-16,y0),(16,y0),(16,y1),(-16,y1)],close=True,fill=F)
        pl(s,[(-20,0),(20,0)],R,1,'8 3')
        s.line(0,3,0,e+0.6,B,1.2);s.arrow(0,e,0,-1)
        cap(s,cx,t[i])
    s.at(140,70);s.txt(-20,1.2,'sketch plane',12,anc='start')
    s.svg(OUT+'extrude-ends.svg')
def revolute():
    s=S(720,300,5)
    s.at(200,190)
    link(s,-16,0);link(s,16,0,True);link(s,16,pi/5)
    pl(s,arc(0,0,40,0.05,pi/5-0.04,30),B,1.2);q=rot([(40,0)],pi/5)[0];s.arrow(*q,-math.sin(pi/5),math.cos(pi/5))
    dot(s,0,0,B,3.5)
    cap(s,200,'Top: free to rotate')
    v=S(720,300,3.6);v.at(560,170)
    v.rrect(-36,0,40,3);v.rrect(-4,3,40,3)
    for x in(-2,2):v.hid(x,0,x,6)
    v.cl(0,-10,0,20)
    pl(v,[(math.cos(t)*8,16+math.sin(t)*2.2) for t in [pi*1.1+i*pi*1.6/30 for i in range(31)]],B,1.2);v.arrow(8*math.cos(pi*2.7),16+2.2*math.sin(pi*2.7),1,0.3)
    v.txt(-2,21,'Z',14,anc='end',bold=True)
    s.e+=v.e;cap(s,560,'Side: one axis')
    s.svg(OUT+'revolute.svg')
def interface():
    s=S(700,360,1)
    BX(s,10,10,680,330,'',f='white')
    BX(s,10,10,680,38,'Toolbar: Sketch, Extrude, Fillet…',f=SD)
    BX(s,10,48,180,212,'Feature list|(every step)',f=F)
    BX(s,10,260,180,80,'Parts',f=F)
    BX(s,190,48,500,252,'',f='white')
    T(s,440,180,'Graphics area',15,c='#666')
    BX(s,600,58,80,56,'View cube',f=F,sz=12)
    BX(s,190,300,500,40,'Tabs: Part Studio 1 · Assembly 1 · +',f=SD,sz=12)
    s.svg(OUT+'interface.svg')
def navigation():
    s=S(700,330,1);cx,cy=350,160
    s.e.append(f'<rect x="{cx-60}" y="{cy-95}" width="120" height="190" rx="60" fill="{F}" stroke="#111" stroke-width="1.6"/>')
    s.e.append(f'<line x1="{cx-60}" y1="{cy-15}" x2="{cx+60}" y2="{cy-15}" stroke="#111" stroke-width="1.2"/><line x1="{cx}" y1="{cy-95}" x2="{cx}" y2="{cy-15}" stroke="#111" stroke-width="1.2"/>')
    s.e.append(f'<rect x="{cx-9}" y="{cy-75}" width="18" height="38" rx="9" fill="white" stroke="#111" stroke-width="1.4"/>')
    def ld(x1,y1,x2,y2,t,anc):
        s.e.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{B}" stroke-width="0.9"/>')
        s.e.append(f'<circle cx="{x1}" cy="{y1}" r="3" fill="{B}"/>');T(s,x2+(6 if anc=='start' else -6),y2+5,t,14,anc)
    ld(cx-32,cy-50,cx-130,cy-50,'Left: select','end')
    ld(cx+34,cy-60,cx+130,cy-80,'Right drag: rotate','start')
    ld(cx+9,cy-56,cx+130,cy-40,'Wheel: zoom','start')
    ld(cx+9,cy-46,cx+130,cy,'Wheel drag: pan','start')
    for i,(k,t) in enumerate([('F','fit all'),('N','look at face')]):
        x=40+i*170;s.e.append(f'<rect x="{x}" y="{290}" width="30" height="28" rx="4" fill="white" stroke="#111" stroke-width="1.4"/>');T(s,x+15,309,k,14,c='#111',b=True);T(s,x+40,309,t,14,'start')
    s.svg(OUT+'navigation.svg')
def units():
    s=S(700,170,8)
    s.at(80,100);s.rrect(0,0,25.4,6);s.dim(0,6,25.4,6,24,'1 in');cap(s,180,'Typed')
    s.at(420,100);s.rrect(0,0,25.4,6);s.dim(0,6,25.4,6,24,'25.4');cap(s,520,'Shown in mm')
    s.svg(OUT+'units.svg')
def line():
    s=S(700,280,5)
    s.at(80,200);P=[(0,0),(40,0),(40,20),(15,30)];pl(s,P)
    for i,p in enumerate(P):num(s,*p,i+1)
    cap(s,180,'One click per point')
    s.at(520,140);s.circ(0,0,12,cm=False);pl(s,[(-24,-10),(24,10)],'#111',1.2,'8 4')
    dot(s,0,0,'#111',3);cap(s,520,'Construction line: dashed')
    s.svg(OUT+'line.svg')
def rectangle():
    s=S(760,250,4.2);xs=[130,380,630]
    s.at(xs[0],130);s.rrect(-18,-12,36,24);num(s,-18,-12,1);num(s,18,12,2);cap(s,xs[0],'Corner')
    s.at(xs[1],130);s.rrect(-18,-12,36,24);s.cl(-24,0,24,0);s.cl(0,-17,0,17);num(s,0,0,1);num(s,18,12,2);cap(s,xs[1],'Center point')
    s.at(xs[2],130);a=pi/9;P=rot([(-18,-12),(18,-12),(18,12),(-18,12)],a);pl(s,P,close=True,fill=F);num(s,*P[0],1);num(s,*P[1],2);num(s,*P[2],3);cap(s,xs[2],'3 point')
    s.svg(OUT+'rectangle.svg')
def circle():
    s=S(700,250,5)
    s.at(175,125);hole(s,0,0,16,fill=F);pl(s,[(0,0),(16*0.8,16*0.6)],B,1,'5 3');num(s,0,0,1);num(s,16*0.8,16*0.6,2);cap(s,175,'Center point')
    s.at(525,125);hole(s,0,0,16,fill=F)
    for i,a in enumerate([200,320,80]):num(s,16*math.cos(math.radians(a)),16*math.sin(math.radians(a)),i+1)
    cap(s,525,'3 point')
    s.svg(OUT+'circle.svg')
def arcs():
    s=S(760,250,4.4);xs=[130,380,630]
    s.at(xs[0],110);P=arc(0,-10,22,pi/6,5*pi/6);pl(s,P);num(s,*P[-1],1);num(s,*P[0],2);num(s,*P[30],3);cap(s,xs[0],'3 point')
    s.at(xs[1]-20,90);pl(s,[(-22,0),(8,0)]);P=arc(8,-12,12,pi/2,-pi/2+0.3);pl(s,P,B,2);num(s,8,0,1);num(s,*P[-1],2);cap(s,xs[1],'Tangent')
    s.at(xs[2],130);P=arc(0,0,20,pi/8,7*pi/8);pl(s,P);pl(s,[P[0],(0,0),P[-1]],GR,1,'5 3');num(s,0,0,1);num(s,*P[0],2);num(s,*P[-1],3);cap(s,xs[2],'Center point')
    s.svg(OUT+'arc.svg')
def polygon():
    s=S(700,330,8);r=12
    s.at(175,160);pl(s,cp(0,0,r),R,0.9,'8 3');P=[(r*math.cos(i*pi/3),r*math.sin(i*pi/3)) for i in range(6)];pl(s,P,close=True,fill=F)
    s.dim(-r,0,r,0,r*8+20,'24');cap(s,175,'Inscribed: corners on circle')
    s.at(525,160);pl(s,cp(0,0,r),R,0.9,'8 3');rr=r/math.cos(pi/6);P=[(rr*math.cos(pi/6+i*pi/3),rr*math.sin(pi/6+i*pi/3)) for i in range(6)];pl(s,P,close=True,fill=F)
    s.dim(-r,-rr/2,r,-rr/2,-75,'24 A/F');cap(s,525,'Circumscribed: flats on circle')
    s.svg(OUT+'polygon.svg')
def slot():
    s=S(700,240,6);s.at(330,115);s.slot(0,0,50,10,True);pl(s,[(-20,0),(20,0)],'#111',1.2,'8 4');dot(s,-20,0,'#111',3);dot(s,20,0,'#111',3)
    s.dim(-20,0,20,0,-58,'40');s.dim(20,-5,20,5,-50,'10')
    s.svg(OUT+'slot.svg')
def extend():
    s=S(760,240,4.4);xs=[130,380,630]
    for i in range(2):
        s.at(xs[i],125);hole(s,14,0,12,fill='none');e=-12 if i==0 else 14-math.sqrt(144-36)
        pl(s,[(-24,6),(e,6)])
        if i==0:pl(s,[(e,6),(14-math.sqrt(144-36),6)],R,1.6,'5 3')
    cap(s,xs[0],'Before: click the line');cap(s,xs[1],'After: up to the circle')
    s.at(xs[2],125);pl(s,[(-24,0),(4,0)]);pl(s,[(4,0),(24,0)],B,2.2);dot(s,4,0,'#111',4);dot(s,-24,0,'#111',3);dot(s,24,0,B,3);cap(s,xs[2],'Split: two lines')
    s.svg(OUT+'extend.svg')
def offset():
    s=S(700,270,4.2)
    s.at(175,130);s.rrect(-30,-18,60,36,8);s.rrect(-25,-13,50,26,3);s.lead(10,-15.5,-50,35,'5 inward',0);cap(s,175,'Closed outline')
    s.at(525,50);a1,a2=-pi*0.8,-pi*0.2;pl(s,arc(0,0,25,a1,a2),R,0.9,'8 3')
    P=arc(0,0,28,a1,a2)+arc(25*math.cos(a2),25*math.sin(a2),3,a2,a2+pi)+arc(0,0,22,a2,a1)+arc(25*math.cos(a1),25*math.sin(a1),3,a1+pi,a1+2*pi)
    pl(s,P,close=True,fill=F);s.lead(28*math.cos(-2*pi/3),28*math.sin(-2*pi/3),-150,40,'3 to both sides',0);cap(s,525,'Arc to slot')
    s.svg(OUT+'offset.svg')
def sfillet():
    s=S(760,250,4.4);xs=[130,380,630]
    for i in range(3):
        s.at(xs[i]-15,70)
        if i==0:pl(s,[(0,-30),(0,0),(30,0)]);dot(s,0,0,R,5)
        if i==1:pl(s,[(0,-30),(0,-10)]+arc(10,-10,10,pi,pi/2)+[(30,0)]);s.lead(10-7.07,-10+7.07,135,25,'R10',0)
        if i==2:pl(s,[(0,-30),(0,-8),(8,0),(30,0)]);s.lead(4,-4,-30,40,'8 × 45°',0)
    cap(s,xs[0],'Click the corner');cap(s,xs[1],'Fillet');cap(s,xs[2],'Chamfer')
    s.svg(OUT+'sketch-fillet.svg')
def smirror():
    h=[(0,0),(30,0),(30,10),(15,25),(15,40),(0,40)];m=[(-x,y) for x,y in h]
    s=S(700,300,4.8)
    s.at(175,250);pl(s,h,close=False);s.cl(0,-4,0,44);cap(s,175,'Half + axis')
    s.at(525,250);pl(s,h+m[::-1][1:-1],close=True,fill=F);s.cl(0,-4,0,44);cap(s,525,'Mirror')
    s.svg(OUT+'sketch-mirror.svg')
def slpat():
    s=S(700,250,5);s.at(230,140)
    for i in range(5):
        for j in range(2):hole(s,8*i,10*j,2,B if i==j==0 else '#111',w=2.4 if i==j==0 else 1.6)
    s.dim(0,10,8,10,24,'8');s.dim(32,0,32,10,-30,'10');s.lead(32,0,-50,40,'10× Ø4',2)
    s.svg(OUT+'sketch-linear-pattern.svg')
def scpat():
    s=S(700,280,5);s.at(330,140);pl(s,cp(0,0,18),R,0.8,'10 3 2 3');dot(s,0,0,'#111',3)
    for i in range(6):a=pi/2+i*pi/3;hole(s,18*math.cos(a),18*math.sin(a),3,B if i==0 else '#111',w=2.4 if i==0 else 1.6)
    s.lead(18*math.cos(pi/6),18*math.sin(pi/6),20,50,'6× Ø6 on Ø36',3)
    s.svg(OUT+'sketch-circular-pattern.svg')
def use():
    s=S(700,260,3.8)
    for i in range(2):
        s.at(175+350*i,130);c=GR if i==0 else '#111'
        pl(s,[(-30,-18),(30,-18),(30,18),(-30,18)],c,1.2 if i==0 else 1.6,None,'#f6f6f6' if i==0 else 'none',True)
        for x in(-24,24):
            for y in(-12,12):
                hole(s,x,y,2,c,'none',1.2 if i==0 else 1.6)
                if i:hole(s,x,y,4,B,'none',1.6)
    cap(s,175,'Other part: grey');cap(s,525,'Use: its edges in your sketch')
    s.svg(OUT+'use.svg')
def constraints():
    s=S(760,420,3.2);n=['Coincident','Concentric','Tangent','Perpendicular','Equal','Midpoint','Symmetric','Horizontal / Vertical']
    for k in range(8):
        cx,cy=95+190*(k%4),105+200*(k//4);s.at(cx,cy)
        if k==0:pl(s,[(-15,-8),(0,6)]);pl(s,[(0,6),(16,-6)]);dot(s,0,6,R,5)
        if k==1:hole(s,0,0,6,fill='none');hole(s,0,0,13,fill='none');dot(s,0,0,R,4)
        if k==2:hole(s,-4,-2,10,fill='none');pl(s,[(-18,8),(16,8)]);dot(s,-4,8,R,5)
        if k==3:pl(s,[(-16,-8),(16,-8)]);pl(s,[(-4,-8),(-4,14)]);pl(s,[(-4,-5),(-1,-5),(-1,-8)],R,1.4)
        if k==4:pl(s,[(-16,8),(10,8)]);pl(s,[(-10,-6),(16,-6)])
        if k==4:
            for x,y in((-3,8),(3,-6)):pl(s,[(x-1,y-2),(x+1,y+2)],R,1.6);pl(s,[(x+1,y-2),(x+3,y+2)],R,1.6)
        if k==5:pl(s,[(-18,-8),(18,-8)]);pl(s,[(0,-8),(8,12)]);dot(s,0,-8,R,5)
        if k==6:s.cl(0,-14,0,14);dot(s,-12,4,'#111',4);dot(s,12,4,'#111',4);pl(s,[(-12,4),(12,4)],R,1,'4 3')
        if k==7:pl(s,[(-18,-8),(10,-8)]);pl(s,[(14,-12),(14,14)])
        s.txt(cx,cy+68,n[k],14,px=True,bold=True)
    s.svg(OUT+'constraints.svg')
def dims():
    s=S(700,330,5);s.at(220,240);x=10/math.tan(pi/6);P=[(0,0),(60,0),(60,20),(60-x,30),(0,30)]
    pl(s,P,close=True,fill=F);hole(s,20,15,5)
    s.dim(0,0,60,0,-26,'60');s.dim(0,0,0,30,30,'30');s.dim(0,0,20,0,-56,'20');s.dim(60,0,60,20,-30,'20')
    pl(s,[(60-x,30),(66,30)],B,0.8);adim(s,60-x,30,12,-pi/6,0,'30°');s.lead(20-3.5,15+3.5,125,45,'Ø10',0)
    s.svg(OUT+'dimensions.svg')
def revolve():
    s=S(700,300,5)
    s.at(160,250);s.cl(0,-4,0,42);pl(s,[(5,0),(16,0),(16,5),(10,5),(10,36),(5,36)],close=True,fill=F)
    pl(s,[(math.cos(t)*7,40+math.sin(t)*2) for t in [pi*1.1+i*pi*1.6/30 for i in range(31)]],B,1.2);s.arrow(7*math.cos(pi*2.7),40+2*math.sin(pi*2.7),1,0.3)
    cap(s,175,'Half profile + axis')
    s.at(520,215);cyl(s,16,0,5);cyl(s,10,5,36);pl(s,ell(5,36),close=True,fill='white')
    cap(s,520,'Revolve 360°')
    s.svg(OUT+'revolve.svg')
def pfillet():
    s=S(700,250,4)
    s.at(175,120);s.rrect(-30,-18,60,36)
    for x in(-30,30):
        for y in(-18,18):dot(s,x,y,R,5)
    cap(s,175,'Select 4 edges')
    s.at(525,120);s.rrect(-30,-18,60,36,6);s.lead(-30+1.76,18-1.76,135,25,'R6 × 4',0);cap(s,525,'Fillet')
    s.svg(OUT+'fillet.svg')
def chamfer():
    s=S(700,250,5)
    s.at(95,150);s.rrect(0,0,40,16);dot(s,40,16,R,5);cap(s,175,'Select the edge')
    s.at(445,150);pl(s,[(0,0),(40,0),(40,12),(36,16),(0,16)],close=True,fill=F);s.lead(38,14,100,35,'4 × 45°',0);cap(s,525,'Chamfer')
    s.svg(OUT+'chamfer.svg')
def plpat():
    s=S(700,340,5);s.at(350,170);s.rrect(-48,-24,96,48,4)
    for i in range(11):
        for j in range(2):hole(s,-40+8*i,-16+32*j,2,B if (i,j)==(0,1) else '#111',w=2.4 if (i,j)==(0,1) else 1.6)
    s.dim(-40,16,-32,16,24+40,'8');s.dim(40,-16,40,16,-50,'32');s.lead(-40,-16,-130,70,'22× Ø4',2)
    s.svg(OUT+'linear-pattern.svg')
def pcpat():
    s=S(700,300,4.4);s.at(330,150);hole(s,0,0,30,fill=F);hole(s,0,0,8);pl(s,cp(0,0,20),R,0.8,'10 3 2 3')
    for i in range(6):a=pi/2+i*pi/3;hole(s,20*math.cos(a),20*math.sin(a),3,B if i==0 else '#111',w=2.4 if i==0 else 1.6)
    s.lead(20*math.cos(pi/6),20*math.sin(pi/6),20,70,'6× Ø6 on Ø40',3)
    s.svg(OUT+'circular-pattern.svg')
def pmirror():
    s=S(700,260,4)
    for i in range(2):
        s.at(175+350*i,120);s.cl(0,-26,0,26);s.rrect(10,-20,14,40)
        if i:s.rrect(-24,-20,14,40)
    cap(s,175,'Part + mid plane');cap(s,525,'Mirror')
    s.svg(OUT+'mirror.svg')
def nari():
    s=S(780,250,3.4);n=['New','Add','Remove','Intersect'];bk=[(-15,0),(15,0),(15,10),(-15,10)];E=[(0,4),(25,4),(25,14),(0,14)]
    res=[None,[(-15,0),(15,0),(15,4),(25,4),(25,14),(0,14),(0,10),(-15,10)],[(-15,0),(15,0),(15,4),(0,4),(0,10),(-15,10)],[(0,4),(15,4),(15,10),(0,10)]]
    for i in range(4):
        cx=110+190*i;s.at(cx-20,140)
        if i==0:pl(s,bk,close=True,fill=F);pl(s,E,close=True,fill=P2)
        else:pl(s,bk,GR,1,'5 3',close=True);pl(s,E,GR,1,'5 3',close=True);pl(s,res[i],close=True,fill=F)
        cap(s,cx,n[i])
    s.svg(OUT+'new-add-remove.svg')
def boolean():
    s=S(760,260,4);n=['Union','Subtract','Intersect']
    U=[(-15,-15),(15,-15),(15,1)]+arc(15,15,14,-pi/2,pi)+[(-15,15)]
    Sb=[(-15,-15),(15,-15),(15,1)]+arc(15,15,14,-pi/2,-pi)+[(-15,15)]
    I=[(15,15)]+arc(15,15,14,pi,3*pi/2)
    for i,P in enumerate([U,Sb,I]):
        cx=130+250*i;s.at(cx-5,120)
        pl(s,[(-15,-15),(15,-15),(15,15),(-15,15)],GR,1,'5 3',close=True);hole(s,15,15,14,GR,'none',1,'5 3');pl(s,P,close=True,fill=F)
        cap(s,cx,n[i])
    s.svg(OUT+'boolean.svg')
def split():
    s=S(700,280,4.4)
    s.at(175,220);s.rrect(-25,0,50,30);s.line(-32,24,32,24,R,1.2,'12 3 2 3');cap(s,175,'Plane through the part')
    s.at(525,220);s.rrect(-25,0,50,24);s.rrect(-25,30,50,6,0,P2);cap(s,525,'Split: two parts')
    s.svg(OUT+'split.svg')
def plane():
    s=S(760,260,3.6);xs=[130,380,630]
    s.at(xs[0],180);s.rrect(-25,0,50,10);s.line(-32,22,32,22,R,1.2,'12 3 2 3');s.dim(25,10,25,22,-30,'12');cap(s,xs[0],'Offset')
    s.at(xs[1],180);s.rrect(-20,0,40,20);s.line(0,-6,0,28,R,1.2,'12 3 2 3');s.dim(-20,20,0,20,24,'20');s.dim(0,20,20,20,24,'20');cap(s,xs[1],'Mid plane')
    s.at(xs[2]-70,180);s.rrect(-25,0,50,10);a=pi/4;s.line(25,10,25+30*math.cos(a),10+30*math.sin(a),R,1.2,'12 3 2 3');pl(s,[(25,10),(40,10)],B,0.8);adim(s,25,10,14,0,a,'45°');dot(s,25,10,'#111',4);cap(s,xs[2],'Line angle')
    s.svg(OUT+'plane.svg')
def insert():
    s=S(700,230,1)
    T(s,110,40,'Other document',13,c='#666');BX(s,20,55,180,110,'Kit plate',f=F)
    BX(s,300,90,70,40,'V1',f=P2)
    T(s,590,40,'Your document',13,c='#666');BX(s,500,55,180,110,'Assembly',f=F)
    A(s,200,110,300,110);A(s,370,110,500,110,'Insert')
    s.svg(OUT+'insert.svg')
def fix():
    s=S(700,250,4)
    s.at(175,150);kplate(s,-20,0,5,1);ground(s,-26,26,-2);cap(s,175,'Fixed: does not move')
    s.at(525,150);kplate(s,-20,0,5,1)
    for d in(1,-1):s.line(d*24,4,d*34,4,B,1.2);s.arrow(d*34,4,d,0);s.line(0,4+d*8,0,4+d*16,B,1.2);s.arrow(0,4+d*16,0,d)
    cap(s,525,'Not fixed: moves when dragged')
    s.svg(OUT+'fix.svg')
def mconn():
    s=S(700,270,5)
    s.at(195,150);kplate(s,-36,-4,5,1);dot(s,0,0,B,3);s.line(0,0,14,0,R,2);s.arrow(14,0,1,0);s.line(0,0,0,14,G,2);s.arrow(0,14,0,1)
    s.txt(15,1,'X',13,anc='start',bold=True);s.txt(1.5,15,'Y',13,anc='start',bold=True);cap(s,175,'Top: at the hole center')
    s.at(525,160);s.rrect(-20,0,40,3);s.hid(-2,0,-2,3);s.hid(2,0,2,3);s.line(0,3,0,20,B,2);s.arrow(0,20,0,1);s.line(0,3,14,3,R,2);s.arrow(14,3,1,0)
    s.txt(1.5,20,'Z',13,anc='start',bold=True);s.txt(15,4,'X',13,anc='start',bold=True);cap(s,525,'Side: Z out of the face')
    s.svg(OUT+'mate-connector.svg')
def fastened():
    s=S(700,280,4)
    br=lambda z:[(-12,z),(12,z),(12,z+3),(-9,z+3),(-9,z+22),(-12,z+22)]
    for i in range(2):
        s.at(175+350*i,200);s.rrect(-30,0,60,3);z=14 if i==0 else 3;pl(s,br(z),close=True,fill=P2)
        dot(s,4,3,B,4);dot(s,4,z,B,4)
        if i==0:s.line(16,z,16,5,B,1.2);s.arrow(16,4,0,-1)
    cap(s,175,'Connector on each part');cap(s,525,'Fastened')
    s.svg(OUT+'fastened.svg')
def slider():
    s=S(700,220,5);s.at(350,140);s.rrect(-50,0,100,6);s.cl(-56,3,56,3);s.rrect(-25,6,20,10,0,P2);pl(s,[(5,6),(25,6),(25,16),(5,16)],GR,1,'5 3',close=True)
    s.line(-15,20,15,20,B,1.2);s.arrow(15,20,1,0);s.arrow(-15,20,-1,0)
    s.svg(OUT+'slider.svg')
def variables():
    s=S(700,280,4.5)
    for i,t in enumerate((4,6)):
        s.at(110+350*i,230);pl(s,[(0,0),(40,0),(40,t),(t,t),(t,30),(0,30)],close=True,fill=F);s.dim(40,0,40,t,-24,'#t');cap(s,175+350*i,'#t = %d'%t)
    s.svg(OUT+'variables.svg')
def configs():
    s=S(760,220,3.6);C=[(5,1),(3,3),(7,2)]
    for i,(n,m) in enumerate(C):
        cx=130+250*i;s.at(cx,120);kplate(s,-n*4,-m*4,n,m);cap(s,cx,f'N = {n}, M = {m}')
    s.svg(OUT+'configurations.svg')
def versions():
    s=S(700,230,1);y=90
    s.e.append(f'<line x1="40" y1="{y}" x2="660" y2="{y}" stroke="#111" stroke-width="1.4"/>')
    for x in range(60,660,50):s.e.append(f'<circle cx="{x}" cy="{y}" r="5" fill="white" stroke="#111" stroke-width="1.4"/>')
    for x,t in((210,'V1'),(460,'V2')):s.e.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{B}"/>');BX(s,x-24,y-58,48,30,t,f=P2)
    T(s,40,y+30,'History: every change',13,'start',c='#666')
    BX(s,380,160,160,46,'Other document',f=F);A(s,460,y+10,460,160,'')
    T(s,470,y+42,'Insert',12,'start')
    s.svg(OUT+'versions.svg')
def derived():
    s=S(700,240,1)
    T(s,110,40,'Other document',13,c='#666');BX(s,20,55,180,130,'Base plate',f=F)
    T(s,530,40,'Your Part Studio',13,c='#666');BX(s,380,55,300,130,'',f='white')
    BX(s,410,120,240,40,'base plate (Derived)',f='#f6f6f6',c=GR,tc='#666',sz=12)
    BX(s,470,80,120,40,'new bracket',f=P2,sz=12)
    A(s,200,120,380,120,'Derived')
    s.svg(OUT+'derived.svg')
def impexp():
    s=S(700,260,1)
    BX(s,260,90,180,70,'Onshape',f=F,sz=15)
    BX(s,20,90,150,70,'Other CAD',f='white')
    BX(s,530,90,150,70,'3D printer|slicer',f='white')
    A(s,170,115,260,115,'STEP');A(s,260,140,170,140)
    A(s,440,125,530,125,'STL')
    s.svg(OUT+'import-export.svg')
for f in(trim,extrude,ends,revolute,interface,navigation,units,line,rectangle,circle,arcs,polygon,slot,extend,offset,sfillet,smirror,slpat,scpat,use,constraints,dims,revolve,pfillet,chamfer,plpat,pcpat,pmirror,nari,boolean,split,plane,insert,fix,mconn,fastened,slider,variables,configs,versions,derived,impexp):f()
