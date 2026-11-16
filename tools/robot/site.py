import sys,os,shutil;sys.path.insert(0,'.');sys.path.insert(0,'..')
from model import *
import render,drawings
R='../../docs/robot';I='../../docs/img/robot'
os.makedirs(R,exist_ok=True);os.makedirs(I,exist_ok=True)
A=build();T,K=render.tri(A)
render.view(T,K,22,-38,I+'/robot-1.png');render.view(T,K,22,140,I+'/robot-2.png');render.view(T,K,0,-90,I+'/robot-side.png')
subs=sorted(SUB,key=int)
def fn(c):return 'p'+c.replace('.','-')
L=['# Team robot','','Every student builds one subassembly of about 5 parts. Together they make a small shooter robot: the intake roller pushes a ball (Ø70) up the curved track, the ball rises through the middle of the turret and the flywheel throws it out along the hood.','',
'![Robot](../img/robot/robot-1.png){width=49%} ![Robot, back](../img/robot/robot-2.png){width=49%}','','![Side view](../img/robot/robot-side.png){width=70%}','',
'## Coordinates','','All parts are placed in one robot coordinate system: **X** forward, **Y** left, **Z** up, origin in the middle of the base plate on the floor. Base grid: holes Ø4, pitch 8, plates 3 thick.','',
'## Subassemblies','','| # | Subassembly | Student | Parts |','|---|---|---|---|']
for s in subs:
    n,w=SUB[s];ps=[c for c in P if P[c]['sub']==s]
    L.append(f'| {s} | [{n}](sub-{s}.md) | {w} | {len(ps)} |')
L+=['','!!! note "Standard motor and servo"','    Every motor on the robot (drive, intake, shooter) is the same simplified model: [2.1](sub-2.md#p2-1). The servo: [7.4](sub-7.md#p7-4). Each student models his own copy from that drawing.','']
open(R+'/index.md','w').write('\n'.join(L))
for s in subs:
    n,w=SUB[s];ps=[c for c in P if P[c]['sub']==s]
    T2,K2=render.tri(A,s);render.view(T2,K2,22,-38,f'{I}/sub-{s}.png')
    L=[f'# {s}. {n}','',f'**Student:** {w}','',f'![{n}](../img/robot/sub-{s}.png){{width=60%}}','','| Part | Name | Qty |','|---|---|---|']
    for c in ps:L.append(f'| [{c}](#{fn(c)}) | {P[c]["name"]} | {P[c]["qty"]} |')
    L.append('')
    for c in ps:
        drawings.drawing(c,f'{I}/{fn(c)}.svg')
        L+=[f'## {c} {P[c]["name"]} {{#{fn(c)}}}','',f'![{c}](../img/robot/{fn(c)}.svg)','']
    open(f'{R}/sub-{s}.md','w').write('\n'.join(L))
    print('sub',s)
