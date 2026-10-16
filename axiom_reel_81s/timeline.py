# Single timeline shared by visuals (scenes.py) and sound (audio.py). Times are local to each scene, in seconds.
FPS = 30; TOTAL = 81.0
# (name, start, duration)
SCENES = [('A',0,6),('B',6,6),('C',12,3),('D',15,9),('E',24,6),('F',30,12),('G',42,12),('H',54,6),('I',60,21)]
START = {n: s for n, s, d in SCENES}
DUR = {n: d for n, s, d in SCENES}
TRANS = [15, 30, 42, 60]      # 4 soft crossfades (budget: 1 per ~20 s)
TD = 0.25                     # crossfade length
A_ROW=[0.0,0.45,0.9,1.35,1.8]; A_SENT=[1.4,2.6,3.8,5.0]; A_CLK=3.0
B_Z=[0.9,1.7]; B_H=[1.4,2.2]; B_CHAT=[3.3,4.2,4.9,5.5]
C_T=[0.5+0.4*i for i in range(5)]
D_FILL1=[0.4+0.3*k for k in range(8)]; D_FILL2=[3.4+0.3*k for k in range(9)]; D_FLIP=8.0
E_Z=[0.6,0.8]; E_H=[1.1,1.3]; E_ROW=[1.5+0.35*r for r in range(4)]; E_BAR=3.3; E_EASY=4.4; E_WARN=4.9
F_Q=[0.1+0.1*i for i in range(24)]; F_CLK=3.0; F_NUM=[3.5+0.5*k for k in range(5)]
F_LEAVE=[6.4+0.35*i for i in range(5)]; F_TICK=[9.2+0.08*i for i in range(24)]; F_FULL=11.3
G_Z=[0.6,1.1,1.6]; G_H=[1.0,1.5,2.0]; G_PULSE=2.3
G_CHAT=[3.2,3.6,4.1,4.5,5.0,5.4]; G_B=[6.5,7.4]; G_BH=[7.0,7.9]
G_C=[9.6,10.4]; G_CH=[10.1,10.9]
H_N=[0.2+0.4*k for k in range(6)]; H_Q=[3.2,4.2,5.2]
I_BAR=[0.2+0.25*i for i in range(5)]; I_ARC=3.3; I_RING=[4.0,5.4]; I_B=6.7; I_BH=7.2
I_STEP=[9.5+0.45*k for k in range(5)]; I_LINE=13.0; I_FIN=14.3; I_LRN=15.2; I_END=[18.3,19.3,20.3]

def events():
    """(global_time, kind, pan) - one sound per visual event."""
    E = []
    def a(sc, times, kind, pan=0.0):
        for t in times: E.append((START[sc]+t, kind, pan))
    a('A',A_ROW,'tick',-.1); a('A',A_SENT,'tap',.12); a('A',[A_CLK],'tick')
    a('B',B_Z,'zap',-.05); a('B',B_H[:1],'hit'); a('B',[B_H[1]],'glass'); a('B',B_CHAT,'tap',.1)
    a('C',C_T[:4],'num'); a('C',[C_T[4]],'glass')
    a('D',D_FILL1[::2],'tick',-.1); a('D',D_FILL2[::3],'tick',.1); a('D',[D_FLIP],'glass')
    a('E',E_Z,'zap'); a('E',E_H,'hit'); a('E',E_ROW,'tick'); a('E',[E_BAR],'tsk'); a('E',[E_EASY],'tick'); a('E',[E_WARN],'tap')
    a('F',F_Q[::3],'tick',-.12); a('F',[F_CLK],'tick'); a('F',F_NUM,'num'); a('F',F_LEAVE,'tap',.1); a('F',F_TICK[::4],'num'); a('F',[F_FULL],'glass')
    a('G',G_Z,'zap',-.1); a('G',G_H,'hit'); a('G',[G_PULSE],'glass'); a('G',G_CHAT,'tap',.12)
    a('G',G_B,'zap'); a('G',G_BH[:1],'hit'); a('G',[G_BH[1]],'glass'); a('G',G_C,'zap'); a('G',G_CH[:1],'hit'); a('G',[G_CH[1]],'glass')
    a('H',H_N,'hit'); a('H',H_Q[:1],'glass')
    a('I',I_BAR,'glass'); a('I',[I_ARC],'tsk'); a('I',[I_RING[1]],'glass'); a('I',[I_B],'zap'); a('I',[I_BH],'hit')
    a('I',I_STEP,'tick'); a('I',[I_LINE],'tsk'); a('I',[I_FIN],'glass'); a('I',[I_LRN],'tick'); a('I',[I_END[0]],'glass')
    for t in TRANS: E.append((t-0.12,'whoosh',0.0))
    return sorted(E)
