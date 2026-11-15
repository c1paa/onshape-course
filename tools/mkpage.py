import json
d=json.load(open('tools/tasks.json'))
d.update({
 't36':dict(title='Shaft and bracket',topics=['two parts','Boolean subtract, keep tools'],text='Make the shaft first (New), then the bracket block around it (New, so it does not merge). Then **Boolean → Subtract**: target = bracket, tool = shaft, tick **Keep tools**. Change the shaft to Ø12: the hole must follow.'),
 't37':dict(title='Part from two views',topics=['extrude','Boolean intersect'],text='Extrude the front view (New), extrude the top view (New), then **Boolean → Intersect**. Only the volume inside both is left.'),
 't38':dict(title='Box with a lid',topics=['remove','plane','split'],text='Box 60 × 40 × 30, pocket with a 3 mm wall and 3 mm floor (Extrude Remove from a sketch on the top face). Then **Plane** offset 24 from the bottom and **Split** the box: you get a lid and a base, two parts.'),
 't39':dict(title='Bracket with "up to" cuts',topics=['variables','through all / up to next'],text='Make `t` a **Variable** (4 mm). Holes and the slot are cut with **Through all** or **Up to next**. Then change `t` to 6: everything must still cut through.')})
def block(i,lvl='###'):
    k='t%02d'%i;v=d[k]
    o=[f"{lvl} T{i:02d} · {v['title']} {{#{k}}}",'',f"*{', '.join(v['topics'])}*",'']
    if v['text']:o+=[v['text'],'']
    o+=[f"![T{i:02d}](img/tasks/{k}.svg)",'']
    return o+['??? note "3D view"','    ',f"    ![T{i:02d} 3D](img/tasks/{k}-3d.svg)",'',f'<div class="cl-sub" data-task="{k}"></div>','']
def table(ids):
    o=['| # | Part | Topics |','|---|---|---|']
    for i in ids:
        k='t%02d'%i;v=d[k]
        o.append(f"| [{k.upper()}](#{k}) | {v['title']} | {', '.join(v['topics'])} |")
    return o+['']
P=[25,26,27,29,30,31,32,33,34,35,36,37,38,39]
o=['# Practice','',
'Parts from drawings. Most of them are **one sketch, one Extrude**: the work is in the sketch.','',
'- One Onshape document per part: `Lastname - T26 - Rocker arm`.',
'- Try to guess how you would build the part *before* opening the 3D view.',
'- Submit a screenshot in the box under each task. Sign in with the name and password from the coach.','']+table(P)
for i in P:o+=block(i,'##')
open('docs/practice.md','w').write('\n'.join(o))
H=[25,26,29,32,33,34]
o=['# Homework 1','',
'Model each part from its drawing, one Onshape document per part: `Lastname - T25 - Grid plate`. When it is done, check it against the drawing and submit a screenshot in the box under the task (sign in with the name and password from the coach).','']+table(H)
for i in H:o+=block(i,'##')
open('docs/homework-1.md','w').write('\n'.join(o))
