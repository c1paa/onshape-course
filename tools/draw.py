import math
class S:
    def __init__(s,w,h,k=4):
        s.w,s.h,s.k,s.e=w,h,k,[]
        s.ox,s.oy=0,0
    def at(s,x,y):s.ox,s.oy=x,y
    def p(s,x,y):return s.ox+x*s.k,s.oy-y*s.k
    def line(s,x1,y1,x2,y2,c='#111',w=1.6,d=None):
        a,b=s.p(x1,y1);c2,e=s.p(x2,y2)
        s.e.append(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c2:.1f}" y2="{e:.1f}" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{d}"' if d else '')+'/>')
    def cl(s,x1,y1,x2,y2):s.line(x1,y1,x2,y2,'#c33',0.8,'10 3 2 3')
    def hid(s,x1,y1,x2,y2):s.line(x1,y1,x2,y2,'#111',1,'5 3')
    def disc(s,x,y,r):
        a,b=s.p(x,y);s.e.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r*s.k:.1f}" fill="#eef3fb" stroke="#111" stroke-width="1.6"/>')
    def circ(s,x,y,r,w=1.6,cm=True):
        a,b=s.p(x,y);s.e.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r*s.k:.1f}" fill="none" stroke="#111" stroke-width="{w}"/>')
        if cm and r*s.k>=4 and r*s.k<=60:
            e=r+4/s.k;s.e.append(f'<g stroke="#c33" stroke-width="0.7" stroke-dasharray="6 2 1.5 2"><line x1="{a-e*s.k:.1f}" y1="{b:.1f}" x2="{a+e*s.k:.1f}" y2="{b:.1f}"/><line x1="{a:.1f}" y1="{b-e*s.k:.1f}" x2="{a:.1f}" y2="{b+e*s.k:.1f}"/></g>')
    def path(s,pts,close=True):
        q=' '.join('%.1f,%.1f'%s.p(*t) for t in pts)
        s.e.append(f'<polygon points="{q}" fill="#eef3fb" stroke="#111" stroke-width="1.6"/>' if close else f'<polyline points="{q}" fill="none" stroke="#111" stroke-width="1.6"/>')
    def pd(s,cmds,fill=True,col=None):
        o=''
        for c in cmds:
            if c[0]=='M' or c[0]=='L':o+='%s%.1f,%.1f '%((c[0],)+s.p(c[1],c[2]))
            elif c[0]=='A':
                x,y=s.p(c[4],c[5]);o+='A%.1f,%.1f 0 %d %d %.1f,%.1f '%(c[1]*s.k,c[1]*s.k,c[2],c[3],x,y)
            else:o+='Z '
        s.e.append(f'<path d="{o}" fill="{col or ("#eef3fb" if fill else "none")}" fill-rule="evenodd" stroke="#111" stroke-width="1.6"/>')
    def slot(s,cx,cy,L,W,fill=False):
        r=W/2;a=L/2-r
        s.pd([('M',cx-a,cy+r),('L',cx+a,cy+r),('A',r,0,1,cx+a,cy-r),('L',cx-a,cy-r),('A',r,0,1,cx-a,cy+r),('Z',)],fill)
    def poly(s,pts,fill=True):
        q=' '.join('%.1f,%.1f'%s.p(*t) for t in pts)
        c=fill if isinstance(fill,str) else ("#eef3fb" if fill else "none")
        s.e.append(f'<polygon points="{q}" fill="{c}" stroke="#111" stroke-width="1.6"/>')
    def rect(s,x,y,w,h,r=0):
        a,b=s.p(x,y+h);s.e.append(f'<rect x="{a:.1f}" y="{b:.1f}" width="{w*s.k:.1f}" height="{h*s.k:.1f}" rx="{r*s.k:.1f}" fill="none" stroke="#111" stroke-width="1.6"/>')
    def rrect(s,x,y,w,h,r=0,col="#eef3fb"):
        a,b=s.p(x,y+h);s.e.append(f'<rect x="{a:.1f}" y="{b:.1f}" width="{w*s.k:.1f}" height="{h*s.k:.1f}" rx="{r*s.k:.1f}" fill="{col}" stroke="#111" stroke-width="1.6"/>')
    def txt(s,x,y,t,sz=15,anc='middle',rot=0,px=False,bold=False):
        a,b=(x,y) if px else s.p(x,y)
        tr=f' transform="rotate({rot} {a:.1f} {b:.1f})"' if rot else ''
        s.e.append(f'<text x="{a:.1f}" y="{b:.1f}" font-size="{sz}" font-family="Arial,Helvetica,sans-serif" text-anchor="{anc}"'+(' font-weight="bold"' if bold else '')+f' fill="#0a3d91"{tr}>{t}</text>')
    def arrow(s,x,y,dx,dy):
        a,b=s.p(x,y);L=math.hypot(dx,dy);ux,uy=dx/L,-dy/L
        p1=(a-ux*9-uy*3,b-uy*9+ux*3);p2=(a-ux*9+uy*3,b-uy*9-ux*3)
        s.e.append(f'<polygon points="{a:.1f},{b:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="#0a3d91"/>')
    def dim(s,x1,y1,x2,y2,off,t=None):
        dx,dy=x2-x1,y2-y1;L=math.hypot(dx,dy);nx,ny=-dy/L,dx/L
        o=off/s.k;a=(x1+nx*o,y1+ny*o);b=(x2+nx*o,y2+ny*o)
        g=2/s.k*math.copysign(1,off);e=6/s.k*math.copysign(1,off)
        s.line(x1+nx*g,y1+ny*g,a[0]+nx*e,a[1]+ny*e,'#0a3d91',0.8)
        s.line(x2+nx*g,y2+ny*g,b[0]+nx*e,b[1]+ny*e,'#0a3d91',0.8)
        s.line(*a,*b,'#0a3d91',0.9)
        s.arrow(*a,-dx,-dy);s.arrow(*b,dx,dy)
        if t is None:t=('%g'%round(L,2))
        mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
        ux,uy=dx/L,dy/L
        px,py=(-uy,ux) if (ux>1e-9 or (abs(ux)<1e-9 and uy<0)) else (uy,-ux)
        if not(py>1e-9 or (abs(py)<1e-9 and px<0)):px,py=-px,-py
        if L*s.k<30:
            q=16/s.k;s.line(*b,b[0]+ux*q,b[1]+uy*q,'#0a3d91',0.9)
            tx,ty=b[0]+ux*(q+2/s.k),b[1]+uy*(q+2/s.k)
            if abs(uy)<1e-9:s.txt(tx,ty-5/s.k,t,anc='start' if ux>0 else 'end')
            else:s.txt(tx+4/s.k,ty-5/s.k if uy<0 else ty,t,anc='start')
            return
        ang=math.degrees(math.atan2(dy,dx))
        if ang>90 or ang<=-90:ang+=180
        q=4/s.k
        s.txt(mx+px*q,my+py*q,t,rot=-ang)
    def lead(s,x,y,ang,ln,t,r=0):
        c,sn=math.cos(math.radians(ang)),math.sin(math.radians(ang))
        sx,sy=x+c*r,y+sn*r;ex,ey=x+c*(r+ln/s.k),y+sn*(r+ln/s.k)
        s.line(sx,sy,ex,ey,'#0a3d91',0.8);s.arrow(sx,sy,-c,-sn)
        h=1 if c>=0 else -1;s.line(ex,ey,ex+h*40/s.k,ey,'#0a3d91',0.8)
        s.txt(ex+h*4/s.k,ey+3/s.k,t,anc='start' if h>0 else 'end')
    def note(s,t,y=None):
        s.e.append(f'<text x="16" y="{y or 52}" font-size="14" font-family="Arial,Helvetica,sans-serif" fill="#444">{t}</text>')
    def svg(s,fn,title=''):
        hd=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" width="{s.w}" height="{s.h}"><rect width="100%" height="100%" fill="white"/>'
        if title:hd+=f'<text x="16" y="28" font-size="20" font-weight="bold" font-family="Arial,Helvetica,sans-serif" fill="#111">{title}</text><text x="{s.w-16}" y="26" font-size="13" text-anchor="end" font-family="Arial,Helvetica,sans-serif" fill="#666">All dimensions in mm</text>'
        open(fn,'w').write(hd+''.join(s.e)+'</svg>')
