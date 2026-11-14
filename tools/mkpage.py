import json
d=json.load(open('tools/tasks.json'))
def block(i,lvl='###'):
    k='t%02d'%i;v=d[k]
    o=[f"{lvl} T{i:02d} · {v['title']} {{#{k}}}",'',f"*{', '.join(v['topics'])}*",'']
    if v['text']:o+=[v['text'],'']
    o+=[f"![T{i:02d}](img/tasks/{k}.svg)",'']
    chk=f"**Check:** volume = **{v['v']:,.0f} mm³**".replace(',',' ')
    if 'v7' in v:chk+=f" for N = 5, **{v['v7']:,.0f} mm³** for N = 7".replace(',',' ')
    return o+[chk,'','??? note "3D view"','    ',f"    ![T{i:02d} 3D](img/tasks/{k}-3d.svg)",'']
def table(ids):
    o=['| # | Part | Topics | Volume, mm³ |','|---|---|---|---|']
    for i in ids:
        k='t%02d'%i;v=d[k]
        o.append(f"| [{k.upper()}](#{k}) | {v['title']} | {', '.join(v['topics'])} | "+f"{v['v']:,.0f}".replace(',',' ')+" |")
    return o+['']
P=[25,26,27,29,30,31,32,33,34]
o=['# Practice','',
'Parts from drawings. Most of them are **one sketch, one Extrude**: the work is in the sketch.','',
'- One Onshape document per part: `Lastname - T26 - Rocker arm`.',
'- Check your answer: assign **Aluminum - 6061**, open **Mass properties**, compare the **volume**. Within ±1% counts as correct.',
'- Try to guess how you would build the part *before* opening the 3D view.','']+table(P)
for i in P:o+=block(i,'##')
open('docs/practice.md','w').write('\n'.join(o))
H=[25,26,29,32,33,34]
o=['# Homework 1','',
'Model each part from its drawing, one Onshape document per part: `Lastname - T25 - Grid plate`. Assign **Aluminum - 6061** and check the **volume** in **Mass properties** before you submit (±1% counts as correct). Then [submit](submit.md) the links.','']+table(H)
for i in H:o+=block(i,'##')
open('docs/homework-1.md','w').write('\n'.join(o))
