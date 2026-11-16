import sys;sys.path.insert(0,'.')
from model import *
import numpy as np
A=build()
F=[(x,tz(x)) for x in np.linspace(-87,TRK[0][0],600)]
def bz(x):
    z=35
    for xf,zf in F:
        if abs(x-xf)<35:z=max(z,zf+np.sqrt(35**2-(x-xf)**2))
    return z
pts=[(x,bz(x)) for x in range(230,-30,-12)]+[(TX,z) for z in range(80,151,10)]
for x,z in pts:
    b=cq.Workplane().sphere(34.5).translate((x,0,z));hit=[]
    for c,s in A:
        v=s.val().intersect(b.val()).Volume()
        if v>0.5:hit.append((c,round(v)))
    print(round(x),round(z,1),hit)
