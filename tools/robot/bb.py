import sys;sys.path.insert(0,'.')
from model import *
A=build()
for c,s in A:
    if c in sys.argv[1:]:
        b=s.val().BoundingBox();print(c,[round(v,1) for v in(b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax)])
