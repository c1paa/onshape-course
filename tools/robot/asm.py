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
    f={'9':2.2,'8':(1.3,1.3,9),'7':(1.2,1.2,2),'2':1.6,'15':1.8,'13':1.6,'12':1.4,'11':1.3,'3':1.8}.get(sub,f)
    cen=np.mean([s.val().Center().toTuple() for c,s in I],axis=0)
    E=[]
    for c,s in I:
        d=np.array(s.val().Center().toTuple())-cen
        E.append((c,s.translate(tuple(d*np.array(f if isinstance(f,tuple) else (f,f,f))))))
    ra=hlr(comp([s for c,s in I]),'iso');re=hlr(comp([s for c,s in E]),'iso')
    ba=bb(ra['vis']);be=bb(re['vis'])
    sa=ba[1]-ba[0];se=be[1]-be[0]
    ka=min(520/sa[0],460/sa[1]);ke=min(640/se[0],460/se[1])
    W0=1400;H0=int(120+max(sa[1]*ka,se[1]*ke)+120)
    s=D(W0,H0,ka)
    s.at(40-ba[0][0]*ka,120+ba[1][1]*ka)
    for l in ra['vis']:poly(s,l,1.2)
    s.e.append(f'<text x="{40+sa[0]*ka/2:.0f}" y="{140+sa[1]*ka:.0f}" font-size="14" font-family="Arial" text-anchor="middle" fill="#555">Assembled</text>')
    s.k=ke;ox=W0-40-se[0]*ke;s.at(ox-be[0][0]*ke,120+be[1][1]*ke)
    for l in re['vis']:poly(s,l,1.2)
    s.e.append(f'<text x="{ox+se[0]*ke/2:.0f}" y="{140+se[1]*ke:.0f}" font-size="14" font-family="Arial" text-anchor="middle" fill="#555">Exploded</text>');s.occ.append((ox+se[0]*ke/2-40,140+se[1]*ke-16,ox+se[0]*ke/2+40,140+se[1]*ke+4))
    vp=np.array([p for l in re['vis'] for p in l])
    s.soft.append((ox,120,ox+se[0]*ke,120+se[1]*ke))
    cnt={}
    for c,_ in I:cnt[c]=cnt.get(c,0)+1
    done=set();mc=s.p(*((be[0]+be[1])/2))
    for c,sh in E:
        if c in done:continue
        done.add(c)
        own=hlr(sh,'iso');pts=np.array([p for l in own['vis'] for p in l])
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
