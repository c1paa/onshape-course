import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle
R=[('6.2',48,78,110,114,'#9aa3ad'),('7.2',44,76,114,118,'#d64545'),('7.2',44,47.5,108,114,'#d64545'),('7.3',48,81,118,122,'#8e5fb8'),('7.1',48,95,122,126,'#b58fd1'),('7.5',38,42,126,141,'#c9b3e0'),('7.5',42,55,126,129,'#c9b3e0'),('6.1',65,77,60,110,'#9aa3ad')]
fig,ax=plt.subplots(figsize=(11,4.6),dpi=130)
for c,r0,r1,z0,z1,col in R:
    for s in(1,-1):ax.add_patch(Rectangle((s*r0 if s>0 else -r1,z0),r1-r0,z1-z0,fc=col,ec='k',lw=0.6))
ax.add_patch(Circle((0,128),35,fc='none',ec='#2a7',lw=1,ls='--'))
ax.plot([0,0],[60,160],'k-.',lw=0.5)
for t,xy,tx in[('6.2 lower ring (fixed, on posts)',(65,112),(100,100)),('7.2 upper ring + bushing (turns)',(46,110),(60,88)),('7.3 big gear (turns)',(78,120),(100,117)),('7.1 platform (turns)',(90,124),(100,133)),('6.1 post (fixed)',(77,80),(95,75)),('ball Ø70',(-25,128),(-140,140))]:
    ax.annotate(t,xy=xy,xytext=tx,fontsize=9,arrowprops=dict(arrowstyle='->',lw=0.7))
ax.text(-138,84,'bushing goes through the Ø96 hole\nof the fixed ring → turret is centred\non it and turns around it',fontsize=9)
ax.set_xlim(-140,170);ax.set_ylim(70,160);ax.set_aspect('equal');ax.axis('off')
ax.set_title('Turret, cut through the middle',fontsize=11)
plt.savefig('/mnt/user-data/outputs/turret-bushing.png',bbox_inches='tight',facecolor='white')
