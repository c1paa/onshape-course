import sys;sys.path.insert(0,'.')
from model import *
from OCP.BRepAdaptor import BRepAdaptor_Surface as BA
import numpy as np
A=build();H=[]
for i,(c,s) in enumerate(A):
    for f in s.val().Faces():
        if f.geomType()=='CYLINDER':
            cy=BA(f.wrapped).Cylinder();r=cy.Radius()
            if r<=2.2:
                ax=cy.Axis();p=np.array(ax.Location().Coord());d=np.array(ax.Direction().Coord())
                H.append((i,c,p,d,r))
seen=set()
for i,c,p,d,r in H:
    if c in('1.1','1.2','1.3'):continue
    ok=False
    for j,c2,p2,d2,r2 in H:
        if j==i:continue
        if abs(abs(d@d2)-1)<1e-4 and np.linalg.norm(np.cross(p2-p,d))<0.3:ok=True;break
    k=(c,tuple(np.round(p,1)))
    if not ok and k not in seen:seen.add(k);print('lonely',c,np.round(p,1),np.round(d,2),round(2*r,2))
