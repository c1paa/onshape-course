import sys,os,math,html;sys.path.insert(0,'.');sys.path.insert(0,'..')
from model import *
from draw import S
from dwg import D,pj
from ann import AN
import numpy as np
from OCP.HLRBRep import HLRBRep_Algo,HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax2,gp_Pnt,gp_Dir
V={'front':((0,-1,0),(1,0,0)),'top':((0,0,1),(1,0,0)),'right':((1,0,0),(0,1,0)),'iso':((1,-1,0.8),(1,1,0))}
def hlr(sh,v):
    sh=sh.val() if hasattr(sh,'val') else sh
    d,x=V[v];a=HLRBRep_Algo();a.Add(sh.wrapped)
    a.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0,0,0),gp_Dir(*d),gp_Dir(*x))));a.Update();a.Hide()
    h=HLRBRep_HLRToShape(a);vis,hid,cir,arcs=[],[],[],[]
    for g,L in((h.VCompound(),vis),(h.OutLineVCompound(),vis),(h.HCompound(),hid)):
        if g is None or g.IsNull():continue
        for e in cq.Shape.cast(g).Edges():
            t=e.geomType()
            if t=='LINE':L.append([e.startPoint().toTuple()[:2],e.endPoint().toTuple()[:2]]);continue
            n=max(8,int(e.Length()/1.5));L.append([p.toTuple()[:2] for p in e.positions(np.linspace(0,1,n))])
            if t=='CIRCLE' and L is vis:
                c=e.arcCenter().toTuple()[:2]
                if e.IsClosed():cir.append((round(c[0],2),round(c[1],2),round(e.radius(),2)))
                else:
                    m=e.positionAt(0.5);sw=e.Length()/e.radius()*57.3
                    arcs.append((round(c[0],2),round(c[1],2),round(e.radius(),2),m.x,m.y,sw))
    G={}
    for a in arcs:G.setdefault(a[:3],[]).append(a)
    arcs=[]
    for kk,L in G.items():
        if sum(a[5] for a in L)>=358:cir.append(kk)
        else:arcs+=[a[:5] for a in L if a[5]<=100 or a[2]>=20]
    cir=sorted(set(cir));cir=[c for c in cir if not any(abs(c[0]-d[0])<0.05 and abs(c[1]-d[1])<0.05 and 0<d[2]-c[2]<0.8 for d in cir)]
    return vis,hid,cir,arcs
def bb(ls):
    a=np.array([p for l in ls for p in l]);return a.min(0),a.max(0)
def pl2(s,pts,w=1.5,d=None,c='#111'):
    q=' '.join('%.1f,%.1f'%s.p(*p) for p in pts)
    s.e.append(f'<polyline points="{q}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"'+(f' stroke-dasharray="{d}"' if d else '')+'/>')
def fmt(v):
    r=round(v)
    return '%g'%(r if abs(v-r)<0.08 else round(v,1))
def thin(L):
    o=[]
    for a in sorted(L):
        if not o or a-o[-1]>0.15:o.append(a)
    if len(o)>16:o=[o[0],o[1],o[-1]]
    return o
def pats(cir,mn,mx):
    by={}
    for c in cir:by.setdefault(c[2],[]).append(c)
    out=[];used=set()
    for r,cs in by.items():
        if len(cs)<3 or len(cs)>16:continue
        for cen in [(c[0],c[1]) for c in cir if c[2]>r]+[((mn[0]+mx[0])/2,(mn[1]+mx[1])/2)]:
            G={}
            for c in cs:
                if c in used:continue
                d=math.hypot(c[0]-cen[0],c[1]-cen[1])
                if d>0.5:G.setdefault(round(d,1),[]).append(c)
            for R,ps in G.items():
                n=len(ps)
                if n<3:continue
                A=sorted(math.degrees(math.atan2(p[1]-cen[1],p[0]-cen[0]))%360 for p in ps)
                sp=[(A[(i+1)%n]-A[i])%360 for i in range(n)]
                if max(sp)-min(sp)>0.5:continue
                out.append((cen,R,r,ps));used.update(ps)
    return out,used
def ordin(s,mn,mx,cir):
    if not cir:return
    k=s.k;c='#0a3d91'
    xs=thin([x-mn[0] for x,y,r in cir]);ys=thin([y-mn[1] for x,y,r in cir])
    for i,a in enumerate([0]+xs):
        x=mn[0]+a;h=(14+(i%3)*24)/k
        for cx,cy,r in cir:
            if abs(cx-x)<0.2:s.line(x,cy+r,x,mx[1],'#9ab',0.6,'2 3')
        s.line(x,mx[1]+3/k,x,mx[1]+h,c,0.7);s.txt(x+4/k,mx[1]+h+3/k,fmt(a),12,anc='start',rot=-90)
        q=s.p(x,mx[1]+h);s.occ.append((q[0]-12,q[1]-8*len(fmt(a))-6,q[0]+3,q[1]+2))
    for i,a in enumerate([0]+ys):
        y=mn[1]+a;h=(14+(i%3)*30)/k
        for cx,cy,r in cir:
            if abs(cy-y)<0.2:s.line(cx+r,y,mx[0],y,'#9ab',0.6,'2 3')
        s.line(mx[0]+3/k,y,mx[0]+h,y,c,0.7);s.txt(mx[0]+h+3/k,y-4/k,fmt(a),12,anc='start')
        q=s.p(mx[0]+h,y);s.occ.append((q[0],q[1]-12,q[0]+8*len(fmt(a))+6,q[1]+3))
def drawing(code,out):
    p=P[code];sh=p['fn']()
    R={v:hlr(sh,v) for v in V}
    B={v:bb(R[v][0]+R[v][1]) for v in V}
    sz={v:B[v][1]-B[v][0] for v in V}
    W0,H0,g=1200,780,115
    k=min((W0-2*g-260)/(sz['front'][0]+sz['right'][0]+1e-9),(H0-2*g-60)/(sz['front'][1]+sz['top'][1]+1e-9),6)
    k=min(k,(W0-2*g)/(sz['front'][0]+1e-9))
    an=AN.get(code,[]);ext=0
    for op in an:
        if op[0]=='c':
            u=pj(op[1],op[2])[0];ext=max(ext,(B[op[1]][0][0]-u)*k+30)
    fx,fy=60+g*0.6+ext,175+sz['top'][1]*k+g
    org={'front':(fx,fy+sz['front'][1]*k),'top':(fx,fy-g),'right':(fx+sz['front'][0]*k+g,fy+sz['front'][1]*k)}
    Ht=int(org['front'][1]+90)
    s=D(W0,Ht,k);done=set();PX={};an=AN.get(code,[])
    mi,xi=B['iso'];ki=min(240/max(sz['iso']),k)
    s.soft.append((W0-30-sz['iso'][0]*ki,80,W0-30,80+sz['iso'][1]*ki))
    for v,(ox,oy) in org.items():
        s.soft.append((ox,oy-sz[v][1]*k,ox+sz[v][0]*k,oy))
        s.occ.append((ox+sz[v][0]*k/2-25,oy+(42 if v!='top' else 8),ox+sz[v][0]*k/2+25,oy+(62 if v!='top' else 26)))
        if v=='front':s.occ+=[(ox,oy+20,ox+sz[v][0]*k,oy+50),(ox-50,oy-sz[v][1]*k,ox-20,oy)]
        if v=='top':s.occ.append((ox-50,oy-sz[v][1]*k,ox-20,oy))
        if v=='right':s.occ.append((ox,oy+20,ox+sz[v][0]*k,oy+50))
    mv=max(('top','front','right'),key=lambda v:(len([c for c in R[v][2] if c[2]*k>=2]),v=='top'))
    for v,(ox,oy) in org.items():
        mn,mx=B[v];s.at(ox-mn[0]*k,oy+mn[1]*k);vis,hid,cir,arcs=R[v];PX[v]=(s.ox,s.oy)
        for l in hid:pl2(s,l,0.9,'5 3','#555')
        for l in vis:pl2(s,l,1.6)
        for x,y,r in cir:
            if r*k>=3:
                e=r+5/k;s.cl(x-e,y,x+e,y);s.cl(x,y-e,x,y+e)
        if v=='front':
            s.dim(mn[0],mn[1],mx[0],mn[1],-34,fmt(mx[0]-mn[0]));s.dim(mn[0],mn[1],mn[0],mx[1],34,fmt(mx[1]-mn[1]))
        if v=='top':s.dim(mn[0],mn[1],mn[0],mx[1],34,fmt(mx[1]-mn[1]))
        if v=='right':s.dim(mn[0],mn[1],mx[0],mn[1],-34,fmt(mx[0]-mn[0]))
        box=(ox,oy-sz[v][1]*k,ox+sz[v][0]*k,oy)
        cs0=[c for c in cir if c[2]*k>=2]
        PT,used=pats(cs0,mn,mx)
        for cen,Rr,r,ps in PT:
            a_,b_=s.p(*cen);s.e.append(f'<circle cx="{a_:.1f}" cy="{b_:.1f}" r="{Rr*k:.1f}" fill="none" stroke="#c33" stroke-width="0.7" stroke-dasharray="10 3 2 3"/>')
        if True:
            L=[c for c in cs0 if c not in used]
            outer=[c for c in L if abs(2*c[2]-(mx[0]-mn[0]))<0.3 and abs((mn[0]+mx[0])/2-c[0])<0.1]
            L=[c for c in L if not any(abs(c[0]-o[0])<0.05 and abs(c[1]-o[1])<0.05 for o in outer)]
            for cen,Rr,r,ps in PT:
                if not any(abs(cen[0]-o[0])<0.05 and abs(cen[1]-o[1])<0.05 for o in outer):L.append((cen[0],cen[1],0))
            for op in an:
                if op[0]=='o' and op[1]==v:L+=[pj(v,q)+(0,) for q in op[2]]
            ordin(s,mn,mx,L)
            for op in an:
                if op[0]=='c' and op[1]==v:
                    u,w=pj(v,op[2]);e=8/k;s.cl(u-e,w,u+e,w);s.cl(u,w-e,u,w+e)
            for op in an:
                if op[0]=='d' and op[1]==v:
                    _,_,p1,p2,off,mode=op[:6];q1,q2=pj(v,p1),pj(v,p2)
                    val={'h':abs(q2[0]-q1[0]),'v':abs(q2[1]-q1[1])}.get(mode,math.hypot(q2[0]-q1[0],q2[1]-q1[1]))
                    s.dimp(q1,q2,off,op[6] if len(op)>6 else fmt(val),mode)
        for cen,Rr,r,ps in PT:
            x,y,_=max(ps,key=lambda c:c[0]+c[1]);d=round(2*r,2)
            s.callout(x,y,r,f'{len(ps)}× Ø{fmt(d)} on Ø{fmt(2*Rr)}',45,box)
        grp={}
        for x,y,r in cir:
            if (x,y,r) in used:continue
            grp.setdefault(round(2*r,2),[]).append((x,y,r))
        for d,cs in sorted(grp.items(),key=lambda a:-a[0]):
            if d in done or d*k<4:continue
            done.add(d);x,y,r=max(cs,key=lambda c:(c[0]+c[1]));n=len(cs)
            s.callout(x,y,r,(f'{n}× ' if n>1 else '')+'Ø'+fmt(d),45,box)
        ag={}
        for x,y,r,mxp,myp in arcs:
            if r*k<2.5 or any(abs(r-c[2])<0.01 and abs(x-c[0])<0.05 and abs(y-c[1])<0.05 for c in cir):continue
            ag.setdefault(r,{})[(round(x,1),round(y,1))]=(x,y,mxp,myp)
        for r,dd in sorted(ag.items()):
            x,y,mxp,myp=max(dd.values(),key=lambda q:q[2]+q[3]);a=math.degrees(math.atan2(myp-y,mxp-x))
            n=len(dd);s.callout(mxp,myp,0,(f'{n}× ' if n>1 else '')+'R'+fmt(r),a,box)
        for op in an:
            if op[1]!=v:continue
            if op[0]=='n':
                q=pj(v,op[2]);s.callout(q[0],q[1],0,op[3],op[4] if len(op)>4 else 45,box)
        s.txt(ox+sz[v][0]*k/2,oy+22+(34 if v in('front','right') else 0),{'front':'Front','top':'Top','right':'Right'}[v],13,px=True)
    mn,mx=B['iso'];ki=min(240/max(sz['iso']),k);s.k=ki
    s.at(W0-30-sz['iso'][0]*ki-mn[0]*ki,80+mx[1]*ki)
    for l in R['iso'][0]:pl2(s,l,1.1)
    s.k=k
    sub,who=SUB[p['sub']]
    s.note(html.escape(f"Subassembly {p['sub']}: {sub} — {who}  ·  Quantity: {p['qty']}"),52)
    s.svg(out,html.escape(f"{code}  {p['name']}"))
if __name__=='__main__':
    o=sys.argv[1];os.makedirs(o,exist_ok=True)
    for c in (sys.argv[2:] or P):
        try:drawing(c,f'{o}/p{c.replace(".","-")}.svg');print('ok',c)
        except Exception as e:print('ERR',c,e)
