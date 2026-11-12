import math,sys
sys.path.insert(0,'tools')
from draw import S
pi=math.pi
D='docs/img/'
R={}
def cf(r):return r*r*(1-pi/4)
s=S(760,500,5);s.at(360,250)
s.rrect(-48,-24,96,48,4)
s.circ(0,0,7)
for y in(-16,16):
    for i in range(11):s.circ(-40+8*i,y,2)
s.cl(-54,0,54,0);s.cl(0,-30,0,30)
s.dim(-48,24,48,24,40);s.dim(-48,-24,-48,24,40)
s.dim(-40,-24,-32,-24,-22,'8');s.dim(-48,-24,-40,-24,-22,'8')
s.dim(48,-16,48,16,-30,'32')
s.lead(0,0,40,40,'Ø14',7)
s.lead(40,16,40,30,'Ø4 × 22',2)
s.lead(-48+1.17,24-1.17,135,30,'R4 × 4')
s.at(360,450);s.rrect(-48,0,96,4);s.dim(48,0,48,4,-30,'4')
s.txt(360,480,'SIDE',13,px=True)
s.svg(D+'p0-plate.svg','L1 · Pattern plate')
v=96*48*4-4*cf(4)*4-pi*49*4-22*pi*4*4;R['p0']=v
s=S(640,360,8);s.at(170,190)
s.circ(0,0,7);s.circ(0,0,2);s.cl(-10,0,10,0);s.cl(0,-10,0,10)
s.lead(0,0,45,40,'Ø14',7);s.lead(0,0,-60,60,'Ø4',2)
s.at(330,190);s.rrect(0,-7,24,14);s.hid(0,2,24,2);s.hid(0,-2,24,-2);s.cl(-3,0,27,0)
s.dim(0,7,24,7,30,'24')
s.txt(170,320,'FRONT',13,px=True);s.txt(426,320,'SIDE',13,px=True)
s.svg(D+'hw1-spacer.svg','HW1 · Spacer')
R['hw1']=pi*(49-4)*24
s=S(760,420,5);s.at(90,330)
s.path([(0,0),(40,0),(40,3),(3,3),(3,32),(0,32)])
s.dim(0,0,40,0,-30);s.dim(0,0,0,32,30)
s.dim(3,32,0,32,-22,'3');s.dim(40,0,40,3,-22,'3')
s.hid(22,0,22,3);s.hid(26,0,26,3);s.hid(0,18,3,18);s.hid(0,22,3,22);s.cl(-2,20,5,20);s.dim(3,0,3,20,40,'20')
s.txt(190,380,'FRONT (profile)',13,px=True)
s.at(460,330);s.rrect(0,0,40,24);s.rrect(0,0,3,24);s.circ(24,12,2);s.cl(24,7,24,17);s.cl(19,12,29,12)
s.dim(0,24,40,24,26);s.dim(40,0,40,24,-30,'24')
s.dim(0,0,24,0,-26,'24');s.lead(24,12,50,30,'Ø4 × 2',2)
s.txt(560,380,'TOP',13,px=True)
s.at(460,190-60);s.e.append('')
s.svg(D+'hw2-bracket.svg','HW2 · L-bracket (both legs: hole Ø4 centered on width)')
R['hw2']=(40*3+29*3)*24-2*pi*4*3
s=S(700,490,4.6);s.at(260,240)
s.rrect(-32,-32,64,64,6);s.circ(0,0,12)
for a in range(4):s.circ(16*math.cos(a*pi/2),16*math.sin(a*pi/2),2)
for x in(-24,24):
    for y in(-24,24):s.circ(x,y,2)
s.e.append(f'<circle cx="260" cy="240" r="{16*4.6:.1f}" fill="none" stroke="#c33" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
s.cl(-38,0,38,0);s.cl(0,-38,0,38)
s.dim(-32,32,32,32,36);s.dim(32,-32,32,32,-40)
s.dim(-32,-32,-24,-32,-24,'8');s.dim(-32,-32,-32,-24,24,'8')
s.lead(0,0,150,46,'Ø24',12);s.lead(16,0,-40,60,'Ø4 × 4 on Ø32 circle',2)
s.lead(24,24,45,24,'Ø4 × 4',2);s.lead(32-1.76,-32+1.76,-45,24,'R6 × 4')
s.at(560,240);s.rrect(0,-32,4,64);s.dim(0,32,4,32,24,'4')
s.txt(260,440,'TOP',13,px=True);s.txt(570,440,'SIDE',13,px=True)
s.svg(D+'hw3-motor-plate.svg','HW3 · Motor plate')
R['hw3']=64*64*4-4*cf(6)*4-pi*144*4-8*pi*4*4
s=S(900,380,3.6);s.at(60,200)
s.rrect(0,-24,120,48)
for i in range(15):s.circ(4+8*i,0,2)
s.cl(-4,0,124,0)
s.hid(0,21.5,120,21.5);s.hid(0,-21.5,120,-21.5)
s.dim(0,24,120,24,30);s.dim(0,-24,4,-24,-44,'4');s.dim(4,-24,12,-24,-24,'8')
s.lead(116,0,40,40,'Ø4 × 15',2)
s.txt(276,330,'BOTTOM',13,px=True)
s.at(740,290);s.path([(-24,48),(-24,0),(24,0),(24,48),(21.5,48),(21.5,2.5),(-21.5,2.5),(-21.5,48)])
s.dim(-24,48,24,48,22);s.dim(24,0,24,48,-26,'48');s.dim(21.5,48,24,48,44,'2.5')
s.txt(740,330,'END',13,px=True)
s.svg(D+'hw4-channel.svg','HW4 (bonus) · U-channel (wall 2.5 everywhere, holes in bottom)')
R['hw4']=(48*48-43*45.5)*120-15*pi*4*2.5
s=S(660,380,9);s.at(180,200)
s.circ(0,0,10);s.circ(0,0,4);s.cl(-13,0,13,0);s.cl(0,-13,0,13)
s.hid(-1.65,4,-1.65,10);s.hid(1.65,4,1.65,10)
s.lead(0,0,-30,40,'Ø20',10);s.lead(0,0,-120,40,'Ø8',4)
s.lead(0,10,60,30,'Ø3.3 to bore',0)
s.at(400,200);s.rrect(0,-10,10,20);s.circ(5,10-0.01,0.01);s.hid(0,4,10,4);s.hid(0,-4,10,-4)
s.hid(3.35,4,3.35,10);s.hid(6.65,4,6.65,10);s.cl(5,1,5,13)
s.dim(0,-10,10,-10,-30,'10');s.dim(0,10,5,10,26,'5')
s.txt(180,360,'FRONT',13,px=True);s.txt(445,360,'SIDE',13,px=True)
s.svg(D+'hw5-collar.svg','HW5 (bonus) · Shaft collar (radial hole Ø3.3 for M4 tap)')
n=400000;r=1.65;acc=0
for i in range(2000):
    x=-r+(i+.5)*2*r/2000;h=math.sqrt(max(r*r-x*x,0))
    m=200;dz=2*h/m
    for j in range(m):
        z=-h+(j+.5)*dz;q=math.sqrt(x*x)
        lo=math.sqrt(max(16-x*x,0));hi=math.sqrt(max(100-x*x,0));acc+=(hi-lo)*dz*2*r/2000
R['hw5']=pi*(100-16)*10-acc
for k,v in R.items():print(k,'V=%.0f mm3'%v,'m=%.1f g'%(v*2.7e-3))
