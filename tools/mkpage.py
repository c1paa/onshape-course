import json
d=json.load(open('tools/tasks.json'))
lv=[('Level 1 · Sketch and extrude',1,6),('Level 2 · Fillet and chamfer',7,10),('Level 3 · Patterns',11,15),('Level 4 · Mirror and Boolean',16,19),('Level 5 · Combined',20,24)]
o=['# Practice: 24 parts','',
'Parts from drawings, from easy to hard. Each one uses a few topics from Lesson 1: **sketch, extrude (New / Add / Remove), parts and Boolean, fillet, chamfer, patterns (sketch / feature / face), mirror**.','',
'- Do them in order. Levels 1–3 are for everyone, 4–5 when you feel confident.',
'- One Onshape document per part: `Lastname - T07 - Rounded block`.',
'- Check your answer: assign **Aluminum - 6061**, open **Mass properties**, compare the **volume**. Within ±1% counts as correct.',
'- Try to guess how you would build the part *before* opening the 3D view.','',
'| # | Part | Topics | Volume, mm³ |','|---|---|---|---|']
for k,v in d.items():
    o.append(f"| [{k.upper()}](#{k}) | {v['title']} | {', '.join(v['topics'])} | "+f"{v['v']:,.0f}".replace(',',' ')+" |")
o.append('')
for name,a,b in lv:
    o+=['## '+name,'']
    for i in range(a,b+1):
        k='t%02d'%i;v=d[k]
        o+=[f"### T{i:02d} · {v['title']} {{#{k}}}",'',f"*{', '.join(v['topics'])}*",'']
        if v['text']:o+=[v['text'],'']
        o+=[f"![T{i:02d}](img/tasks/{k}.svg)",'']
        chk=f"**Check:** volume = **{v['v']:,.0f} mm³**".replace(',',' ')
        if 'v7' in v:chk+=f" for N = 5, **{v['v7']:,.0f} mm³** for N = 7".replace(',',' ')
        o+=[chk,'',f'??? note "3D view"','    ',f"    ![T{i:02d} 3D](img/tasks/{k}-3d.svg)",'']
open('docs/practice.md','w').write('\n'.join(o))
