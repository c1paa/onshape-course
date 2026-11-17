import sys,os,math,html;sys.path.insert(0,'.');sys.path.insert(0,'..')
from model import *
from dwg import D,hlr,bb,V,frame
import numpy as np
from OCP.TopoDS import TopoDS_Compound
from OCP.BRep import BRep_Builder
def comp(ss):
    c=TopoDS_Compound();b=BRep_Builder();b.MakeCompound(c)
    for s in ss:b.Add(c,s.val().wrapped)
    return cq.Workplane().add(cq.Shape.cast(c))
def poly(s,pts,w,d=None,c='#111'):
    q=' '.join('%.1f,%.1f'%s.p(*p) for p in pts)
    s.e.append(f'<polyline points="{q}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"'+(f' stroke-dasharray="{d}"' if d else '')+'/>')
def sheet(sub,A,out,f=0.9):
    I=[(c,s) for c,s in A if P[c]['sub']==sub]
    cnt={}
    for c,_ in I:cnt[c]=cnt.get(c,0)+1
    if len(set(cnt.values()))==1 and list(cnt.values())[0]>1:
        a0=np.array(I[0][1].val().Center().toTuple());J=[]
        for c in cnt:
            L=[s for cc,s in I if cc==c];J.append((c,min(L,key=lambda s:np.linalg.norm(np.array(s.val().Center().toTuple())-a0))))
        I=J
    f={'8':2.2,'7':(1.3,1.3,9),'6':(1.2,1.2,2),'2':1.6,'14':1.8,'12':1.6,'11':1.4,'10':1.3,'3':1.8}.get(sub,f)
    cen=np.mean([s.val().Center().toTuple() for c,s in I],axis=0)
    E=[]
    for c,s in I:
        d=np.array(s.val().Center().toTuple())-cen
        E.append((c,s.translate(tuple(d*np.array(f if isinstance(f,tuple) else (f,f,f))))))
    iv='isob' if sub=='3' else 'iso'
    ra=hlr(comp([s for c,s in I]),iv);re=hlr(comp([s for c,s in E]),iv);rs=hlr(comp([s for c,s in I]),'front')
    ba=bb(ra['vis']);be=bb(re['vis']);bs=bb(rs['vis']+rs['hid'])
    sa=ba[1]-ba[0];se=be[1]-be[0];ss=bs[1]-bs[0]
    ka=min(360/sa[0],380/sa[1]);kss=min(340/ss[0],380/ss[1]);ke=min(520/se[0],420/se[1])
    W0=1400;H0=int(120+max(sa[1]*ka,ss[1]*kss,se[1]*ke)+110)
    s=D(W0,H0,ka)
    def cap(x,y,t):
        s.e.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="14" font-family="Arial" text-anchor="middle" fill="#555">{t}</text>');s.occ.append((x-45,y-16,x+45,y+4))
    s.at(30-ba[0][0]*ka,110+ba[1][1]*ka)
    for l in ra['vis']:poly(s,l,1.2)
    cap(30+sa[0]*ka/2,135+sa[1]*ka,'Assembled'+(' (from below)' if iv=='isob' else ''))
    s.k=kss;x0=420;s.at(x0-bs[0][0]*kss,110+bs[1][1]*kss)
    for l in rs['hid']:poly(s,l,0.6,'4 3','#999')
    for l in rs['vis']:poly(s,l,1.2)
    cap(x0+ss[0]*kss/2,135+ss[1]*kss,'Side view')
    s.k=ke;ox=W0-30-se[0]*ke;s.at(ox-be[0][0]*ke,110+be[1][1]*ke)
    for l in re['vis']:poly(s,l,1.2)
    cap(ox+se[0]*ke/2,135+se[1]*ke,'Exploded')
    vp=np.array([p for l in re['vis'] for p in l])
    s.soft.append((ox,110,ox+se[0]*ke,110+se[1]*ke))
    cnt={}
    for c,_ in I:cnt[c]=cnt.get(c,0)+1
    done=set();mc=s.p(*((be[0]+be[1])/2))
    for c,sh in E:
        if c in done:continue
        done.add(c)
        own=hlr(sh,iv);pts=np.array([p for l in own['vis'] for p in l])
        if len(pts)==0:continue
        pc=pts.mean(0)
        dv=np.linalg.norm(vp[None,:,:]-pts[::max(1,len(pts)//200),None,:],axis=2).min(1)
        cand=pts[::max(1,len(pts)//200)][dv<0.3]
        if len(cand)==0:cand=pts
        a=cand[np.argmin(np.linalg.norm(cand-pc,axis=1))]
        px=s.p(*a);ang=math.degrees(math.atan2(-(px[1]-mc[1]),px[0]-mc[0]))
        t=c+(f' ×{cnt[c]}' if cnt[c]>1 else '')
        s.callout(a[0],a[1],0,t,ang,lens=(30,50,75,100,130,170,210))
    n,w=SUB[sub]
    s.e.append(f'<text x="16" y="52" font-size="14" font-family="Arial,Helvetica,sans-serif" fill="#444">{html.escape(f"Student: {w}")}</text>')
    s.svg(out,html.escape(f'Subassembly {sub}: {n}'))
if __name__=='__main__':
    o=sys.argv[1];os.makedirs(o,exist_ok=True);A=build()
    for sb in (sys.argv[2:] or sorted(SUB,key=int)):
        sheet(sb,A,f'{o}/asm-{sb}.svg');print('ok',sb)
