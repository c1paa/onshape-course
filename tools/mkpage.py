import json
d=json.load(open('tools/tasks.json'))
def block(i,lvl='###'):
    k='t%02d'%i;v=d[k]
    o=[f"{lvl} T{i:02d} · {v['title']} {{#{k}}}",'',f"*{', '.join(v['topics'])}*",'']
    if v['text']:o+=[v['text'],'']
    o+=[f"![T{i:02d}](img/tasks/{k}.svg)",'']
    return o+['??? note "3D view"','    ',f"    ![T{i:02d} 3D](img/tasks/{k}-3d.svg)",'']
def table(ids):
    o=['| # | Part | Topics |','|---|---|---|']
    for i in ids:
        k='t%02d'%i;v=d[k]
        o.append(f"| [{k.upper()}](#{k}) | {v['title']} | {', '.join(v['topics'])} |")
    return o+['']
P=[25,26,27,29,30,31,32,33,34]
o=['# Practice','',
'Parts from drawings. Most of them are **one sketch, one Extrude**: the work is in the sketch.','',
'- One Onshape document per part: `Lastname - T26 - Rocker arm`.',
'- Try to guess how you would build the part *before* opening the 3D view.','']+table(P)
for i in P:o+=block(i,'##')
open('docs/practice.md','w').write('\n'.join(o))
H=[25,26,29,32,33,34]
o=['# Homework 1','',
'Model each part from its drawing, one Onshape document per part: `Lastname - T25 - Grid plate`. When it is done, check it against the drawing and send a screenshot.','']+table(H)
for i in H:o+=block(i,'##')
open('docs/homework-1.md','w').write('\n'.join(o))
