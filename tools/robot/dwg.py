import sys,os,math,html;sys.path.insert(0,'.');sys.path.insert(0,'..')
from model import *
from draw import S
import numpy as np
from OCP.HLRBRep import HLRBRep_Algo,HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax2,gp_Pnt,gp_Dir
from OCP.TopoDS import TopoDS_Compound
from OCP.BRep import BRep_Builder
from ann import AN
V={'front':((0,-1,0),(1,0,0)),'top':((0,0,1),(1,0,0)),'right':((1,0,0),(0,1,0)),'iso':((1,-1,0.8),(1,1,0)),'isob':((1,-1,-0.8),(1,1,0))}
NM={'front':'Front','top':'Top','right':'Right'}
BL='#0a3d91'
def frame(v):
    d,x=V[v];d=np.array(d,float);d/=np.linalg.norm(d);x=np.array(x,float);x-=d*(x@d);x/=np.linalg.norm(x);return x,np.cross(d,x)
def pj(v,p):
    x,y=frame(v);p=np.array(p,float);return float(p@x),float(p@y)
def fmt(v):
    r=round(v)
    return '%g'%(r if abs(v-r)<0.06 else round(v,1))
def hlr(sh,v):
    if hasattr(sh,'val'):sh=sh.val()
    d,x=V[v];a=HLRBRep_Algo();a.Add(sh.wrapped)
    a.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0,0,0),gp_Dir(*d),gp_Dir(*x))));a.Update();a.Hide()
    h=HLRBRep_HLRToShape(a);vis,hid,arcs=[],[],[]
    for g,L in((h.VCompound(),vis),(h.OutLineVCompound(),vis),(h.HCompound(),hid)):
        if g is None or g.IsNull():continue
        for e in cq.Shape.cast(g).Edges():
            t=e.geomType()
            if t=='LINE':L.append([e.startPoint().toTuple()[:2],e.endPoint().toTuple()[:2]]);continue
            n=max(8,int(e.Length()/1.5));L.append([p.toTuple()[:2] for p in e.positions(np.linspace(0,1,n))])
            if t=='CIRCLE' and L is vis:
                c=e.arcCenter().toTuple()[:2];r=e.radius()
                if e.IsClosed():arcs.append((c[0],c[1],r,360.0,None));continue
                a0=math.degrees(math.atan2(e.startPoint().y-c[1],e.startPoint().x-c[0]))
                am=e.positionAt(0.5);am=math.degrees(math.atan2(am.y-c[1],am.x-c[0]))
                a1=math.degrees(math.atan2(e.endPoint().y-c[1],e.endPoint().x-c[0]))
                sw=(a1-a0)%360;
                if ((am-a0)%360)>sw:sw=360-sw
                arcs.append((c[0],c[1],r,sw,am))
    M={}
    for x,y,r,sw,am in arcs:
        k=(round(x,2),round(y,2),round(r,2));o=M.setdefault(k,[0,[]]);o[0]+=sw;o[1].append(am)
    cir=[k for k,o in M.items() if o[0]>=358]
    arc=[(k,o[1]) for k,o in M.items() if o[0]<358]
    cir=[c for c in cir if not any(abs(c[0]-d[0])<0.05 and abs(c[1]-d[1])<0.05 and 0<d[2]-c[2]<0.8 for d in cir)]
    return dict(vis=vis,hid=hid,cir=cir,arc=arc)
def bb(ls):
    a=np.array([p for l in ls for p in l]);return a.min(0),a.max(0)
def inter(a,b,p=2):return not(a[2]+p<b[0] or b[2]+p<a[0] or a[3]+p<b[1] or b[3]+p<a[1])
class D(S):
    def __init__(s,w,h,k):
        super().__init__(w,h,k);s.occ=[];s.parts=[];s.soft=[]
    def hit(s,b,pad=4):return any(inter(b,o,pad) for o in s.occ)
    def tb(s,x,y,t,sz=13,anc='start'):
        w=0.64*sz*len(t)
        x0={'start':x,'middle':x-w/2,'end':x-w}[anc];return (x0,y-sz*0.8,x0+w,y+sz*0.25)
    def T(s,x,y,t,sz=13,anc='start',c=BL):
        s.e.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{sz}" font-family="Arial,Helvetica,sans-serif" text-anchor="{anc}" fill="{c}">{html.escape(t)}</text>');s.occ.append(s.tb(x,y,t,sz,anc))
    def L(s,a,b,c=BL,w=0.8,d=None):
        s.e.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{d}"' if d else '')+'/>')
    def AR(s,p,ux,uy):
        p1=(p[0]-ux*9-uy*3,p[1]-uy*9+ux*3);p2=(p[0]-ux*9+uy*3,p[1]-uy*9-ux*3)
        s.e.append(f'<polygon points="{p[0]:.1f},{p[1]:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{BL}"/>')
    def segfree(s,a,b):
        for t in np.linspace(0.15,1,8):
            q=(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
            if s.hit((q[0],q[1],q[0],q[1]),1):return False
        return True
    def callout(s,x,y,r,t,pref=45,box=None,lens=(18,32,48,66,88,112,140)):
        cx,cy=s.p(x,y);rp=r*s.k;best=None
        angs=[pref+d for d in(0,-30,30,-60,60,90,-90,135,-135,180,120,-120,150,-150)]
        for ln in lens:
            for a in angs:
                c,sn=math.cos(math.radians(a)),-math.sin(math.radians(a))
                st=(cx+c*rp,cy+sn*rp);en=(st[0]+c*ln,st[1]+sn*ln);h=1 if c>=0 else -1
                tx=en[0]+h*4;b=s.tb(tx,en[1]-3,t,13,'start' if h>0 else 'end')
                if b[0]<4 or b[2]>s.w-4 or b[1]<44:continue
                if s.hit(b) or not s.segfree(st,en):continue
                pen=(1 if any(inter(b,o,2) for o in s.soft+([box] if box else [])) else 0)
                if best is None or pen<best[0]:best=(pen,st,en,h,tx,c,sn)
                if pen==0:break
            if best and best[0]==0:break
        if best is None:best=(0,(cx+rp,cy),(cx+rp+30,cy-30),1,cx+rp+34,0.7,-0.7)
        _,st,en,h,tx,c,sn=best
        w=0.64*13*len(t)
        s.L(st,en);s.AR(st,-c,-sn);s.L(en,(en[0]+h*(w+8),en[1]))
        s.T(tx,en[1]-3,t,13,'start' if h>0 else 'end')
        s.occ.append((min(st[0],en[0]),min(st[1],en[1]),max(st[0],en[0]),max(st[1],en[1])))
    def dimp(s,a,b,off,t,mode='a'):
        a=np.array(s.p(*a));b=np.array(s.p(*b))
        if mode=='h':
            y=(a[1] if off<0 else a[1]) ;base=max(a[1],b[1]) if off<0 else min(a[1],b[1]);y=base-off
            pa,pb=np.array([a[0],y]),np.array([b[0],y]);ea,eb=a,b
        elif mode=='v':
            base=min(a[0],b[0]) if off>0 else max(a[0],b[0]);x=base-off
            pa,pb=np.array([x,a[1]]),np.array([x,b[1]]);ea,eb=a,b
        else:
            d=b-a;n=np.array([d[1],-d[0]])/np.linalg.norm(d);pa,pb=a+n*off,b+n*off;ea,eb=a,b
        for e,p in((ea,pa),(eb,pb)):
            u=p-e;l=np.linalg.norm(u)
            if l>3:u/=l;s.L(e+u*2,p+u*6)
        d=pb-pa;l=np.linalg.norm(d)
        if l<1:return
        u=d/l;s.L(pa,pb,w=0.9)
        tw=0.64*13*len(t)
        if l<max(28,tw+6):
            s.AR(pa,u[0],u[1]);s.AR(pb,-u[0],-u[1]);s.L(pa-u*14,pa,w=0.9);s.L(pb,pb+u*16,w=0.9)
            q=pb+u*18
            if abs(u[1])<0.5:s.T(q[0]+2,q[1]+4,t)
            else:s.T(q[0]+4,q[1]+(4 if u[1]>0 else 0),t)
            return
        s.AR(pa,-u[0],-u[1]);s.AR(pb,u[0],u[1])
        m=(pa+pb)/2;ang=math.degrees(math.atan2(d[1],d[0]))
        if ang>90 or ang<=-90:ang+=180
        n=np.array([math.sin(math.radians(ang)),-math.cos(math.radians(ang))])
        q=m+n*4
        s.e.append(f'<text x="{q[0]:.1f}" y="{q[1]:.1f}" font-size="13" font-family="Arial,Helvetica,sans-serif" text-anchor="middle" fill="{BL}" transform="rotate({ang:.1f} {q[0]:.1f} {q[1]:.1f})">{html.escape(t)}</text>')
        hw=tw/2+2
        if abs(ang)<45:s.occ.append((q[0]-hw,q[1]-13,q[0]+hw,q[1]+3))
        else:s.occ.append((q[0]-13,q[1]-hw,q[0]+3,q[1]+hw))
        s.occ.append((min(pa[0],pb[0])-1,min(pa[1],pb[1])-1,max(pa[0],pb[0])+1,max(pa[1],pb[1])+1))
    def angd(s,c,R,a0,a1,t=None):
        cx,cy=s.p(*c);r=R*s.k
        if a1<a0:a0,a1=a1,a0
        P=lambda a,rr=r:(cx+rr*math.cos(math.radians(a)),cy-rr*math.sin(math.radians(a)))
        for a in(a0,a1):s.L((cx,cy),P(a,r+6),w=0.6)
        p0,p1=P(a0),P(a1);lg=1 if a1-a0>180 else 0
        s.e.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{r:.1f},{r:.1f} 0 {lg} 0 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{BL}" stroke-width="0.9"/>')
        for a,sg in((a0,1),(a1,-1)):
            p=P(a);s.AR(p,-math.sin(math.radians(a))*sg,-math.cos(math.radians(a))*sg)
        m=P((a0+a1)/2,r+12);s.T(m[0],m[1]+4,t or fmt(a1-a0)+'°',13,'middle')
    def pcd(s,c,R,a0=None,a1=None):
        cx,cy=s.p(*c);r=R*s.k
        if a0 is None:s.e.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="#c33" stroke-width="0.7" stroke-dasharray="10 3 2 3"/>');return
        P=lambda a:(cx+r*math.cos(math.radians(a)),cy-r*math.sin(math.radians(a)))
        p0,p1=P(a0-8),P(a1+8);lg=1 if a1-a0+16>180 else 0
        s.e.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{r:.1f},{r:.1f} 0 {lg} 0 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="#c33" stroke-width="0.7" stroke-dasharray="10 3 2 3"/>')
def poly(s,pts,w,d=None,c='#111'):
    q=' '.join('%.1f,%.1f'%s.p(*p) for p in pts)
    s.e.append(f'<polyline points="{q}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"'+(f' stroke-dasharray="{d}"' if d else '')+'/>')
def ang(c,p):return math.degrees(math.atan2(p[1]-c[1],p[0]-c[0]))%360
def patterns(cir,arc,mn,mx):
    cc=[(c[0],c[1]) for c in cir]+[(k[0],k[1]) for k,_ in arc if k[2]>6]
    bc=((mn[0]+mx[0])/2,(mn[1]+mx[1])/2)
    by={}
    for c in cir:by.setdefault(c[2],[]).append(c)
    used=set();out=[]
    for r,cs in sorted(by.items()):
        if len(cs)<2:continue
        for cen in cc+[bc]:
            feat=cen is not bc
            G={}
            for c in cs:
                if (c[0],c[1],c[2]) in used:continue
                d=math.hypot(c[0]-cen[0],c[1]-cen[1])
                if d>0.5:G.setdefault(round(d,1),[]).append(c)
            for R,ps in G.items():
                n=len(ps);A=sorted(ang(cen,p) for p in ps)
                if n>=3:
                    sp=[(A[(i+1)%n]-A[i])%360 for i in range(n)]
                    if max(sp)-min(sp)>0.5:continue
                elif n==2 and feat:
                    if abs(((A[1]-A[0])%360)-180)<0.5:continue
                else:continue
                out.append(dict(c=cen,R=R,r=r,ps=ps,A=A,feat=feat))
                for p in ps:used.add((p[0],p[1],p[2]))
    return out,used
def views_for(sh,code):
    a=AN.get(code,{})
    if 'views' in a:return a['views']
    b=sh.val().BoundingBox();e=[b.xlen,b.ylen,b.zlen];t=int(np.argmin(e))
    if e[t]<=4.5 and sorted(e)[1]>3*e[t]:
        return {0:['right','front'],1:['front','top' if e[0]>=e[2] else 'right'],2:['top','front']}[t]
    return ['top','front','right']
def drawing(code,out,sub=True):
    p=P[code];sh=p['fn']();a=AN.get(code,{})
    vs=views_for(sh,code)
    R={v:hlr(sh,v) for v in vs+['iso']}
    B={v:bb(R[v]['vis']+R[v]['hid']) for v in R}
    sz={v:B[v][1]-B[v][0] for v in R}
    g=120;W0=1200
    col0=[v for v in('top','front') if v in vs];row1=[v for v in('front','right') if v in vs]
    wl=max(sz[v][0] for v in col0) if col0 else 0
    wr=sz['right'][0] if 'right' in vs else 0
    hl=(sz['top'][1] if 'top' in vs else 0)+(sz['front'][1] if 'front' in vs else (sz['right'][1] if 'right' in vs else 0))
    nh=sum(1 for v in('top','front') if v in vs) if 'front' in vs or 'top' in vs else 1
    nw=1+(1 if 'right' in vs and 'front' in vs else 0)
    ww=(wl if col0 else 0)+(wr if 'right' in vs else 0)
    k=min((W0-150-g*nw-260)/max(ww,1),(740-g*nh)/max(hl,1),8)
    fx=80;ty=150
    org={}
    th=sz['top'][1]*k if 'top' in vs else 0
    if 'top' in vs:org['top']=(fx,ty+th)
    fyb=ty+th+(g if 'top' in vs else 0)
    hf=sz['front'][1]*k if 'front' in vs else sz['right'][1]*k
    if 'front' in vs:org['front']=(fx,fyb+hf)
    if 'right' in vs:org['right']=((fx+sz['front'][0]*k+g) if 'front' in vs else fx,fyb+hf)
    H=int(fyb+hf+110)
    s=D(W0,H,k)
    mni,mxi=B['iso'];ki=min(260/max(sz['iso']),k*1.2);s.k=ki
    io=(W0-30-sz['iso'][0]*ki-mni[0]*ki,70+mxi[1]*ki);s.at(*io)
    for l in R['iso']['vis']:poly(s,l,1.1)
    s.occ.append((io[0]+mni[0]*ki,io[1]-mxi[1]*ki,io[0]+mxi[0]*ki,io[1]-mni[1]*ki))
    s.k=k
    PX={}
    for v,(ox,oy) in org.items():
        mn,mx=B[v];s.at(ox-mn[0]*k,oy+mn[1]*k);PX[v]=(s.ox,s.oy)
        r=R[v]
        for l in r['hid']:poly(s,l,0.9,'5 3','#555')
        for l in r['vis']:poly(s,l,1.6)
        s.occ.append((ox,oy-sz[v][1]*k,ox+sz[v][0]*k,oy))
        s.T(ox+sz[v][0]*k/2,oy+(62 if v in('front',) or (v=='right' and 'front' not in vs) else 20) if v!='top' else oy+20,NM[v],13,'middle','#555')
    for v,(ox,oy) in org.items():
        s.ox,s.oy=PX[v];mn,mx=B[v];r=R[v]
        box=(ox,oy-sz[v][1]*k,ox+sz[v][0]*k,oy)
        cir=[c for c in r['cir'] if c[2]*k>=1.5]
        for x,y,rr in cir:
            if rr*k>=3:
                e=rr+4/k;s.cl(x-e,y,x+e,y);s.cl(x,y-e,x,y+e)
        pats,used=patterns(cir,r['arc'],mn,mx)
        locs=[]
        for q in pats:
            cen=q['c'];n=len(q['ps'])
            if n>=3:s.pcd(cen,q['R'])
            else:s.pcd(cen,q['R'],min(q['A']),max(q['A']))
        rest=[c for c in cir if (c[0],c[1],c[2]) not in used]
        outer=[c for c in rest if abs(2*c[2]-sz[v][0])<0.3 or abs(2*c[2]-sz[v][1])<0.3]
        cent=set((round(c[0],1),round(c[1],1)) for c in outer)
        by={}
        for c in rest:by.setdefault(round(c[2],2),[]).append(c)
        for rr,cs in sorted(by.items(),key=lambda t:-t[0]):
            n=len(cs);x,y,_=max(cs,key=lambda c:c[0]+c[1])
            s.callout(x,y,rr,(f'{n}× ' if n>1 else '')+'Ø'+fmt(2*rr),45,box)
            for c in cs:
                if (round(c[0],1),round(c[1],1)) not in cent:locs.append((c[0],c[1]))
        for q in pats:
            n=len(q['ps']);x,y,_=q['ps'][0]
            s.callout(x,y,q['r'],f'{n}× Ø'+fmt(2*q['r']),ang(q['c'],(x,y)),box)
            cen=q['c']
            if n>=3:
                am=q['A'][0]+180/n
                s.callout(cen[0]+q['R']*math.cos(math.radians(am)),cen[1]+q['R']*math.sin(math.radians(am)),0,'Ø'+fmt(2*q['R']),am,box)
                a0=min(q['A'],key=lambda t:min(t%(360/n),360/n-t%(360/n)))
                if min(a0%90,90-a0%90)>0.5:
                    b0=round(a0/90)*90 if False else (math.floor(a0/90)*90)
                    s.angd(cen,q['R']*0.75,b0,a0)
            else:
                A=q['A'];am=A[0]
                s.callout(cen[0]+q['R']*math.cos(math.radians(am)),cen[1]+q['R']*math.sin(math.radians(am)),0,'R'+fmt(q['R']),am+20,box)
                d=(A[1]-A[0])%360
                lo,hi=(A[0],A[0]+d) if d<=180 else (A[1],A[1]+360-d)
                s.angd(cen,q['R']*0.55,lo,hi)
                for t in A:
                    if min(t%90,90-t%90)>0.5 and abs(t-lo)<0.5:s.angd(cen,q['R']*0.4,math.floor(t/90)*90,t)
            if (round(cen[0],1),round(cen[1],1)) not in cent and not any(math.hypot(cen[0]-c[0],cen[1]-c[1])<0.05 for c in rest):locs.append(cen)
        arcs={}
        for kk,ams in r['arc']:
            if kk[2]*k<2:continue
            if any(math.hypot(kk[0]-q['c'][0],kk[1]-q['c'][1])<0.05 for q in pats) and kk[2]>6:pass
            arcs.setdefault(round(kk[2],2),[]).append((kk,ams))
        for rr,L in sorted(arcs.items()):
            if any(abs(rr-c[2])<0.01 for c in cir):continue
            n=len(set((round(kk[0],1),round(kk[1],1)) for kk,_ in L))
            kk,ams=L[0];am=ams[0]
            if am is None:continue
            s.callout(kk[0]+rr*math.cos(math.radians(am)),kk[1]+rr*math.sin(math.radians(am)),0,(f'{n}× ' if n>1 else '')+'R'+fmt(rr),am,box)
        for op in a.get(v,[]):
            if op[0]=='o':locs+=[pj(v,q) for q in op[1]]
        ordin(s,mn,mx,locs)
        if v=='front' or (v=='right' and 'front' not in vs) or (v=='top' and 'front' not in vs):
            s.dimp((mn[0],mn[1]),(mx[0],mn[1]),-28,fmt(mx[0]-mn[0]),'h')
        if v in('front','top') or (v=='right' and 'front' not in vs):
            s.dimp((mn[0],mn[1]),(mn[0],mx[1]),28,fmt(mx[1]-mn[1]),'v')
        if v=='right' and 'top' not in vs and 'front' in vs:
            s.dimp((mn[0],mn[1]),(mx[0],mn[1]),-28,fmt(mx[0]-mn[0]),'h')
        for op in a.get(v,[]):
            t=op[0]
            if t=='d':
                _,p1,p2,off,mode=op[:5];q1,q2=pj(v,p1),pj(v,p2)
                val={'h':abs(q2[0]-q1[0]),'v':abs(q2[1]-q1[1])}.get(mode,math.hypot(q2[0]-q1[0],q2[1]-q1[1]))
                s.dimp(q1,q2,off,op[5] if len(op)>5 else fmt(val),mode)
            elif t=='n':
                q=pj(v,op[1]);s.callout(q[0],q[1],0,op[2],op[3] if len(op)>3 else 45,box)
            elif t=='r':
                q=pj(v,op[1]);am=op[3];s.callout(q[0]+op[2]*math.cos(math.radians(am)),q[1]+op[2]*math.sin(math.radians(am)),0,'R'+fmt(op[2]),am,box)
            elif t=='a':
                q=pj(v,op[1]);s.angd(q,op[2],op[3],op[4],op[5] if len(op)>5 else None)
    who=SUB[p['sub']]
    s.e.append(f'<text x="16" y="52" font-size="14" font-family="Arial,Helvetica,sans-serif" fill="#444">{html.escape(f"Subassembly {p[chr(115)+chr(117)+chr(98)]}: {who[0]} — {who[1]}   ·   Quantity: {p[chr(113)+chr(116)+chr(121)]}")}</text>')
    s.svg(out,html.escape(f"{code}  {p['name']}"))
def ordin(s,mn,mx,locs):
    if not locs:return
    k=s.k
    def thin(L):
        o=[]
        for a in sorted(L):
            if not o or a-o[-1]>0.15:o.append(a)
        if len(o)>14:o=[o[0],o[1],o[-1]]
        return o
    xs=thin([x-mn[0] for x,y in locs]);ys=thin([y-mn[1] for x,y in locs])
    def lv(vals):
        last={};out=[]
        for a in vals:
            px=a*k;l=0
            while l in last and px-last[l]<15:l+=1
            last[l]=px;out.append(l)
        return out
    for a,l in zip([0]+xs,lv([0]+xs)):
        x=mn[0]+a;h=(14+l*26)
        for cx,cy in locs:
            if abs(cx-x)<0.2:s.line(x,cy,x,mx[1],'#9ab',0.6,'2 3')
        p0=s.p(x,mx[1]);s.L((p0[0],p0[1]-3),(p0[0],p0[1]-h),w=0.7)
        t=fmt(a);q=(p0[0]+4,p0[1]-h-3)
        s.e.append(f'<text x="{q[0]:.1f}" y="{q[1]:.1f}" font-size="12" font-family="Arial,Helvetica,sans-serif" fill="{BL}" transform="rotate(-90 {q[0]:.1f} {q[1]:.1f})">{t}</text>')
        s.occ.append((q[0]-12,q[1]-7*len(t)-2,q[0]+2,q[1]+2))
    for a,l in zip([0]+ys,lv([0]+ys)):
        y=mn[1]+a;h=(14+l*30)
        for cx,cy in locs:
            if abs(cy-y)<0.2:s.line(cx,y,mx[0],y,'#9ab',0.6,'2 3')
        p0=s.p(mx[0],y);s.L((p0[0]+3,p0[1]),(p0[0]+h,p0[1]),w=0.7)
        s.T(p0[0]+h+3,p0[1]+4,fmt(a),12)
if __name__=='__main__':
    o=sys.argv[1];os.makedirs(o,exist_ok=True)
    for c in (sys.argv[2:] or P):
        try:drawing(c,f'{o}/p{c.replace(".","-")}.svg');print('ok',c)
        except Exception as e:
            import traceback;traceback.print_exc();print('ERR',c,e)
