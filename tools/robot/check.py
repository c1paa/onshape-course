import sys;sys.path.insert(0,'.')
from model import *
A=build()
print(len(P),'parts',len(A),'instances')
bad=[]
import itertools
bbs=[(c,s,s.val().BoundingBox()) for c,s in A]
for (c1,s1,b1),(c2,s2,b2) in itertools.combinations(bbs,2):
    if b1.xmax<b2.xmin or b2.xmax<b1.xmin or b1.ymax<b2.ymin or b2.ymax<b1.ymin or b1.zmax<b2.zmin or b2.zmax<b1.zmin:continue
    v=s1.val().intersect(s2.val()).Volume()
    if v>0.5:bad.append((c1,c2,round(v,1)))
for b in bad:print(b)
