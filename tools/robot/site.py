import sys,os,shutil;sys.path.insert(0,'.');sys.path.insert(0,'..')
from model import *
import render,drawings,asm
R='../../docs/robot';I='../../docs/img/robot'
os.makedirs(R,exist_ok=True);os.makedirs(I,exist_ok=True)
A=build();T,K=render.tri(A) if not os.environ.get('IDX') else (0,0)
if not os.environ.get('IDX'):render.view(T,K,22,-38,I+'/robot-1.png');render.view(T,K,22,140,I+'/robot-2.png');render.view(T,K,0,-90,I+'/robot-side.png')
subs=sorted(SUB,key=int)
def fn(c):return 'p'+c.replace('.','-')
L=['# Team robot','','Every student builds one subassembly of about 5 parts. Together they make a small shooter robot: the intake roller pushes a ball (Ø70) up the curved track, the ball rises through the middle of the turret and the flywheel throws it out along the hood.','',
'![Robot](../img/robot/robot-1.png){width=49%} ![Robot, back](../img/robot/robot-2.png){width=49%}','','![Side view](../img/robot/robot-side.png){width=70%}','',
'!!! warning "Read this first"','    This robot is a **training example**. It is not connected to FTC and does not follow FTC rules — it only has a similar structure (drive, intake, turret, shooter).','',"## How to work in Onshape","",
"1. **Each of you makes your own Onshape document** for your subassembly. Name it `Surname_teamtask_Subassembly`, for example `Ivanov_teamtask_Intake`.",
"2. **Every part gets its own Part Studio.** Click **+** at the bottom left → **Create Part Studio**. Rename the tab with the part number and name, for example `4.3 Intake roller`.","",
"    ![Create Part Studio](../img/robot/howto-part-studio.png){width=45%}","",
"3. When all parts are ready, click **+** → **Create Assembly**, insert your parts and put them together as on the assembly sheet of your subassembly.",
"4. **Share the document with Vlad.** Click **Share** at the top right.","",
"    ![Share button](../img/robot/howto-share-button.png){width=45%}","",
"    On the **Individuals** tab type `vglazunov@isl.cy`, choose **Can edit**, tick **Copy**, **Export** and **Comment**, then click **Share**.","",
"    ![Share with Vlad](../img/robot/howto-share-email.png){width=60%}","",
"5. Copy the link of your document from the browser address bar and paste it into the field below. You can change it later.","",
'<div class="cl-link" data-task="robot"></div>',"",
'## Coordinates','','All parts are placed in one robot coordinate system: **X** forward, **Y** left, **Z** up, origin in the middle of the base plate on the floor. Base grid: holes Ø4, pitch 8, plates 3 thick.','',
'## Subassemblies','','| # | Subassembly | Student | Parts |','|---|---|---|---|']
for s in subs:
    n,w=SUB[s];ps=[c for c in P if P[c]['sub']==s]
    L.append(f'| {s} | [{n}](sub-{s}.md) | {w} | {len(ps)} |')
L+=['','!!! note "Standard motor and servo"','    Every motor on the robot (drive, intake, shooter) is the same simplified model: [2.1](sub-2.md#p2-1). The servo: [6.4](sub-6.md#p6-4). Each student models his own copy from that drawing.','']
open(R+'/index.md','w').write('\n'.join(L))
for s in ([] if os.environ.get('IDX') else subs):
    n,w=SUB[s];ps=[c for c in P if P[c]['sub']==s]
    T2,K2=render.tri(A,hl=s);render.view(T2,K2,-25 if s=='3' else 22,-38,f'{I}/sub-{s}.png')
    asm.sheet(s,A,f'{I}/asm-{s}.svg')
    L=[f'# {s}. {n}','',f'**Student:** {w}','','## Where it goes','',f'![{n} on the robot](../img/robot/sub-{s}.png){{width=60%}}','','## Assembly','',f'![Assembly](../img/robot/asm-{s}.svg)','','## Parts','','| Part | Name | Qty |','|---|---|---|']
    if s=='7':i=L.index('## Parts');L[i:i]=['## How the turret turns','','There is no shaft: the ball goes up through the middle. The bushing on 7.2 goes through the Ø96 hole of the fixed ring 6.2, so the turret is centred on it and turns around it.','','![Turret section](../img/robot/turret-bushing.png)','']
    for c in ps:L.append(f'| [{c}](#{fn(c)}) | {P[c]["name"]} | {P[c]["qty"]} |')
    L.append('')
    for c in ps:
        f=f'{I}/{fn(c)}.svg';drawings.drawing(c,f);e='svg'
        if os.path.getsize(f)>1500000:
            import cairosvg;cairosvg.svg2png(url=f,write_to=f[:-3]+'png',output_width=1600);os.remove(f);e='png'
        L+=[f'### {c} {P[c]["name"]} {{#{fn(c)}}}','',f'![{c}](../img/robot/{fn(c)}.{e})','']
    open(f'{R}/sub-{s}.md','w').write('\n'.join(L))
    print('sub',s)
