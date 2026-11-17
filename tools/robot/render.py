import sys;sys.path.insert(0,'.')
from model import *
import numpy as np,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
C={'1':'#9aa3ad','2':'#3b6fb6','3':'#555','4':'#e07a2f','5':'#7fbf6a','7':'#b58fd1','8':'#8e5fb8','9':'#d64545','10':'#f0b429','11':'#4a4a4a','12':'#2f9e9e','13':'#222','14':'#2d5fd6','15':'#c0392b'}
MOTS={'2.1','4.5','9.6','7.6'}
def tri(A,only=None,hl=None):
    T=[];K=[];L=np.array([0.4,-0.5,0.8]);L/=np.linalg.norm(L)
    for c,s in A:
        sb=P[c]['sub']
        if only and sb!=only:continue
        col='#333' if 'standard' in P[c]['name'].lower() else C[sb]
        if hl and sb!=hl:col='#dcdcdc'
        v,f=s.val().tessellate(0.4,0.3);v=np.array([x.toTuple() for x in v]);rgb=np.array(matplotlib.colors.to_rgb(col))
        for a,b,d in f:
            t=v[[a,b,d]];n=np.cross(t[1]-t[0],t[2]-t[0]);l=np.linalg.norm(n)
            if l:T.append(t);K.append(np.clip(rgb*(0.45+0.55*abs(n/l@L)),0,1))
    return T,K
def view(T,K,el,az,fn,box=None,sz=(9,7)):
    T=np.array(T)
    if box is None:
        mn=T.reshape(-1,3).min(0);mx=T.reshape(-1,3).max(0)
    else:mn,mx=map(np.array,box)
    c=(mn+mx)/2;r=(mx-mn).max()/2*1.02
    fig=plt.figure(figsize=sz,dpi=120);ax=fig.add_subplot(111,projection='3d')
    ax.add_collection3d(Poly3DCollection(T,facecolors=K,edgecolors='none'))
    ax.set_xlim(c[0]-r,c[0]+r);ax.set_ylim(c[1]-r,c[1]+r);ax.set_zlim(c[2]-r,c[2]+r);ax.set_box_aspect((1,1,1))
    ax.view_init(elev=el,azim=az);ax.set_axis_off();plt.subplots_adjust(0,0,1,1);plt.savefig(fn,facecolor='white',bbox_inches='tight',pad_inches=0.05);plt.close()
if __name__=='__main__':
    A=build();T,K=tri(A);o=sys.argv[1] if len(sys.argv)>1 else '/tmp/rb'
    view(T,K,22,-38,o+'/r0.png');view(22,140,o+'/r1.png') if 0 else view(T,K,22,140,o+'/r1.png');view(T,K,0,-90,o+'/r2.png')
