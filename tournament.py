import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.animation as animation

import player_Yi as P1
import player_ver3 as P2

print 'Imported Player 1:'
player1 = P1.player_module()
player1.banner()

print 'Imported Player 2:'
player2 = P2.player_module()
player2.banner()

# initial all graphical objects
fig = plt.figure(figsize=(6,7), dpi=100)
ax = plt.axes(xlim=(-0.1,+1.1), ylim=(-0.2,+1.2))

# tool for converting the 2d bitmaps to matplotlib paths
def create_path_from_array(bitmap):
    verts = []
    codes = []
    dx = 2./bitmap.shape[1]
    dy = 2./bitmap.shape[0]
    
    for j in range(bitmap.shape[0]):
        for i in range(bitmap.shape[1]):
            
            if bitmap[bitmap.shape[0]-j-1,i]==1: # full square
                verts += [(dx*(i+0)-1., dy*(j+0)-1.), # left, bottom
                          (dx*(i+0)-1., dy*(j+1)-1.), # left, top
                          (dx*(i+1)-1., dy*(j+1)-1.), # right, top
                          (dx*(i+1)-1., dy*(j+0)-1.), # right, bottom
                          (dx*(i+0)-1., dy*(j+0)-1.)]
                codes += [mpath.Path.MOVETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.CLOSEPOLY]
    
            if bitmap[bitmap.shape[0]-j-1,i]==2: # triangle toward left-bottom
                verts += [(dx*(i+0)-1., dy*(j+0)-1.), # left, bottom
                          (dx*(i+0)-1., dy*(j+1)-1.), # left, top
                          (dx*(i+1)-1., dy*(j+0)-1.), # right, bottom
                          (dx*(i+0)-1., dy*(j+0)-1.)]
                codes += [mpath.Path.MOVETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.CLOSEPOLY]

            if bitmap[bitmap.shape[0]-j-1,i]==3: # triangle toward right-bottom
                verts += [(dx*(i+0)-1., dy*(j+0)-1.), # left, bottom
                          (dx*(i+1)-1., dy*(j+1)-1.), # right, top
                          (dx*(i+1)-1., dy*(j+0)-1.), # right, bottom
                          (dx*(i+0)-1., dy*(j+0)-1.)]
                codes += [mpath.Path.MOVETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.CLOSEPOLY]

            if bitmap[bitmap.shape[0]-j-1,i]==4: # triangle toward right-top
                verts += [(dx*(i+0)-1., dy*(j+1)-1.), # left, top
                          (dx*(i+1)-1., dy*(j+1)-1.), # right, top
                          (dx*(i+1)-1., dy*(j+0)-1.), # right, bottom
                          (dx*(i+0)-1., dy*(j+1)-1.)]
                codes += [mpath.Path.MOVETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.CLOSEPOLY]

            if bitmap[bitmap.shape[0]-j-1,i]==5: # triangle toward left-top
                verts += [(dx*(i+0)-1., dy*(j+0)-1.), # left, bottom
                          (dx*(i+0)-1., dy*(j+1)-1.), # left, top
                          (dx*(i+1)-1., dy*(j+1)-1.), # right, top
                          (dx*(i+0)-1., dy*(j+0)-1.)]
                codes += [mpath.Path.MOVETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.CLOSEPOLY]

    return mpath.Path(verts, codes)

# bitmaps for invaders, ufo, and the players
bitmap_invader1 = np.array([[0,4,2,0,0,0,0,0,3,5,0],
                            [0,0,4,2,0,0,0,3,5,0,0],
                            [0,3,1,1,1,1,1,1,1,2,0],
                            [3,1,1,0,1,1,1,0,1,1,2],
                            [1,1,1,1,1,1,1,1,1,1,1],
                            [1,0,1,1,1,1,1,1,1,0,1],
                            [1,0,1,0,0,0,0,0,1,0,1],
                            [0,0,4,1,1,0,1,1,5,0,0]])

bitmap_invader2 = np.array([[0,0,1,2,0,0,0,3,1,0,0],
                            [1,0,0,1,0,0,0,1,0,0,1],
                            [1,3,1,1,1,1,1,1,1,2,1],
                            [1,1,1,0,1,1,1,0,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1,1],
                            [4,1,1,1,1,1,1,1,1,1,5],
                            [0,0,3,1,5,0,4,1,2,0,0],
                            [3,1,5,0,0,0,0,0,4,1,2]])

bitmap_invader3 = np.array([[0,0,0,3,1,1,1,1,2,0,0,0],
                            [3,1,1,1,1,1,1,1,1,1,1,2],
                            [1,1,1,1,1,1,1,1,1,1,1,1],
                            [1,1,2,0,4,1,1,5,0,3,1,1],
                            [1,1,1,1,1,1,1,1,1,1,1,1],
                            [0,0,3,1,1,0,0,1,1,2,0,0],
                            [0,3,1,5,4,1,1,5,4,1,2,0],
                            [1,1,5,0,0,0,0,0,0,4,1,1]])

bitmap_invader4 = np.array([[0,0,0,3,1,1,2,0,0,0],
                            [0,0,3,1,1,1,1,2,0,0],
                            [0,3,1,1,1,1,1,1,2,0],
                            [3,1,1,0,1,1,0,1,1,2],
                            [4,1,1,1,1,1,1,1,1,5],
                            [0,0,3,1,2,3,1,2,0,0],
                            [0,3,5,0,1,1,0,4,2,0],
                            [3,5,3,1,5,4,1,2,4,2]])

bitmap_ufo      = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,3,1,1,1,1,1,1,2,0,0,0,0],
                            [0,0,3,1,1,1,1,1,1,1,1,1,1,2,0,0],
                            [0,3,1,1,1,1,1,1,1,1,1,1,1,1,2,0],
                            [3,1,1,0,1,1,0,1,1,0,1,1,0,1,1,2],
                            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                            [0,4,1,1,1,5,4,1,1,5,4,1,1,1,5,0],
                            [0,0,4,1,5,0,0,0,0,0,0,4,1,5,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

bitmap_player1  = np.array([[3,5,0,0,3,1,2,0,0,4,2],
                            [1,0,0,0,1,1,1,0,0,0,1],
                            [1,0,0,3,1,1,1,2,0,0,1],
                            [1,0,0,1,1,1,1,1,0,0,1],
                            [1,1,1,1,1,0,1,1,1,1,1],
                            [1,0,0,1,1,0,1,1,0,0,1],
                            [1,1,1,1,1,1,1,1,1,1,1],
                            [1,0,0,4,1,1,1,5,0,0,1],
                            [4,1,2,0,0,0,0,0,3,1,5]])

bitmap_player2  = np.array([[3,5,0,0,3,1,2,0,0,4,2],
                            [1,0,0,0,1,1,1,0,0,0,1],
                            [1,0,0,3,1,1,1,2,0,0,1],
                            [1,0,0,1,1,1,1,1,0,0,1],
                            [1,1,1,1,0,1,0,1,1,1,1],
                            [1,0,0,1,0,1,0,1,0,0,1],
                            [1,1,1,1,1,1,1,1,1,1,1],
                            [1,0,0,4,1,1,1,5,0,0,1],
                            [4,1,2,0,0,0,0,0,3,1,5]])

# now create the paths
path_invader1 = create_path_from_array(bitmap_invader1)
path_invader2 = create_path_from_array(bitmap_invader2)
path_invader3 = create_path_from_array(bitmap_invader3)
path_invader4 = create_path_from_array(bitmap_invader4)
path_ufo      = create_path_from_array(bitmap_ufo)
path_player1  = create_path_from_array(bitmap_player1)
path_player2  = create_path_from_array(bitmap_player2)

# create drawable objects (static)
ax.plot([-0.05,0.35],[-0.15,-0.15],lw=9,color='0.1')
ax.plot([-0.05,0.35],[-0.15,-0.15],lw=7,color='#FFFFF0')
ax.plot([+0.65,+1.05],[-0.15,-0.15],lw=9,color='0.1')
ax.plot([+0.65,+1.05],[-0.15,-0.15],lw=7,color='#FFFFF0')

# create drawable objects (non-static)
plt_invader1, = ax.plot([], [], marker=path_invader1, ms = 7, mec='#900000', mfc='#F00000', ls='None', alpha=0.6)
plt_invader2, = ax.plot([], [], marker=path_invader2, ms = 7, mec='#904000', mfc='#F09000', ls='None', alpha=0.6)
plt_invader3, = ax.plot([], [], marker=path_invader3, ms = 7, mec='#909000', mfc='#F0F000', ls='None', alpha=0.6)
plt_invader4, = ax.plot([], [], marker=path_invader4, ms = 7, mec='#309000', mfc='#60F000', ls='None', alpha=0.6)
plt_ufo,      = ax.plot([], [], marker=path_ufo,      ms =14, mec='#600090', mfc='#9000F0', ls='None', alpha=0.8)
plt_player1,  = ax.plot([], [], marker=path_player1,  ms =14, mec='#002090', mfc='#0040F0', ls='None', alpha=0.8)
plt_player2,  = ax.plot([], [], marker=path_player2,  ms =14, mec='#007080', mfc='#00A0C0', ls='None', alpha=0.8)

plt_explosion,  = ax.plot([], [], marker=(10,1,0), ms = 21, mec='#FF0000', mfc='#FFA000', ls='None', alpha=0.8)
plt_bullet_inv, = ax.plot([], [], marker='o', ms = 3, mec='#FF0000', mfc='#FF0000',  ls='None', alpha=0.6)
plt_bullet_ply, = ax.plot([], [], marker='d', ms = 3, mec='#0000FF', mfc='#0000FF',  ls='None', alpha=0.6)

plt_tx_center = ax.text(0.5,0.5, '', fontsize = 40, color='#60A0C0', ha='center', va='center')
plt_tx_p1 = ax.text(-0.05,1.13, '', fontsize = 14, color='#B06020', ha='left', va='center')
plt_tx_p2 = ax.text(+1.05,1.13, '', fontsize = 14, color='#B06020', ha='right', va='center')
plt_tx_p1_hp = ax.text(-0.05,-.10, '', fontsize = 10, color='#002090', ha='left', va='center')
plt_tx_p2_hp = ax.text(+1.05,-.10, '', fontsize = 10, color='#007080', ha='right', va='center')

plt_gauge_p1, = ax.plot([],[],lw=7,color='#80D070')
plt_gauge_p2, = ax.plot([],[],lw=7,color='#80D070')
plt_gauge_attack_p1, = ax.plot([],[],lw=4,color='#FFAA00')
plt_gauge_attack_p2, = ax.plot([],[],lw=4,color='#FFAA00')

reference_speed = 0.01 # 0.01 per frame

# class for bullets, invaders, players, etc
class sprite:
    def __init__(self, x_init = 0.5, y_init = 1.2):
        
        self.x, self.y = x_init, y_init # current position
        self.speed = reference_speed # speed
        self.angle = np.pi*3./2. # direction
        self.hp = 1 # hit points
        self.charge = 0 # frames before shooting
        self.dx = 0.
        self.dy = 0.
        self.enabled = True
        
        self.type = 1 # 0 - bullet, [1..4] - invader[1..4], 5 - ufo/player1/2
        self.path = 1 # 0 - user controlled, 1 - straight, 2 - curly, 3 - tracing player1, 4 - tracing player2, 5 - random walk
        self.pathpar = 0. # parameter for path moving
    
    def eval_displacement(self): # evaluate the movement toward the next frame
        global sp_player1, sp_player2
        
        if self.path==2:
            self.angle += self.pathpar
        if self.path==3:
            if  sp_player1.enabled:
                self.angle = np.arctan2(sp_player1.y-self.y, sp_player1.x-self.x)
            elif sp_player2.enabled:
                self.angle = np.arctan2(sp_player2.y-self.y, sp_player2.x-self.x)
        if self.path==4:
            if sp_player2.enabled:
                self.angle = np.arctan2(sp_player2.y-self.y, sp_player2.x-self.x)
            elif sp_player1.enabled:
                self.angle = np.arctan2(sp_player1.y-self.y, sp_player1.x-self.x)
        if self.path==5:
            self.angle += (np.random.rand(1)[0]-0.5)*np.pi/6.
        
        self.dx = (self.speed)*np.cos(self.angle)
        self.dy = (self.speed)*np.sin(self.angle)

    def move(self): # actual move the sprite
        self.x += self.dx
        self.y += self.dy

    def eval_collision(self, obj): # collision detection, only consider the center of obj hitting the square box from self center
        l = 0.025
        if self.type==5: l = 0.05
        
        if abs(obj.x-self.x)<l and abs(obj.y-self.y)<l: return True
        if abs(obj.x-self.x + (obj.dx-self.dx))<l and abs(obj.y-self.y + (obj.dy-self.dy))<l: return True

        if obj.dx!=self.dx:
            t = (self.x-obj.x+l)/(obj.dx-self.dx)
            if t>0. and t<1.:
                osy = obj.y-self.y + (obj.dy-self.dy) * t
                if abs(osy)<l: return True
            t = (self.x-obj.x-l)/(obj.dx-self.dx)
            if t>0. and t<1.:
                osy = obj.y-self.y + (obj.dy-self.dy) * t
                if abs(osy)<l: return True

        if obj.dy!=self.dy:
            t = (self.y-obj.y+l)/(obj.dy-self.dy)
            if t>0. and t<1.:
                osx = obj.x-self.x + (obj.dx-self.dx) * t
                if abs(osx)<l: return True
            t = (self.y-obj.y-l)/(obj.dy-self.dy)
            if t>0. and t<1.:
                osx = obj.x-self.x + (obj.dx-self.dx) * t
                if abs(osx)<l: return True

        return False

# sprites for player 1 and 2
sp_player1 = sprite(0.25,0.2)
sp_player1.type = 5
sp_player1.path = 0
sp_player1.hp = 10
sp_player2 = sprite(0.75,0.2)
sp_player2.type = 5
sp_player2.path = 0
sp_player2.hp = 10

# additional information for players
ply_score = [0,0]
ply_gauge = [1.,1.]
ply_gauge_attack = [0,0]
ply_gauge_freeze = [0,0]

# sprite holders
splist_invader = []
splist_bullet_inv = []
splist_bullet_ply1 = []
splist_bullet_ply2 = []
splist_explosion = []

invader_level = 1   # start with level 1
invader_fcount = 0  # counts of frames for adding new invader
center_message = ''
center_message_delay = 0

def init():
    plt_invader1.set_data([], [])
    plt_invader2.set_data([], [])
    plt_invader3.set_data([], [])
    plt_invader4.set_data([], [])
    plt_ufo.set_data([], [])
    plt_player1.set_data([], [])
    plt_player2.set_data([], [])
    plt_explosion.set_data([], [])
    plt_bullet_inv.set_data([], [])
    plt_bullet_ply.set_data([], [])
    
    plt_tx_center.set(text='')
    plt_tx_p1.set(text='P1 ')
    plt_tx_p2.set(text=' P2')
    plt_tx_p1_hp.set(text='HP ')
    plt_tx_p2_hp.set(text=' HP')
    plt_gauge_p1.set_data([], [])
    plt_gauge_p2.set_data([], [])
    plt_gauge_attack_p1.set_data([], [])
    plt_gauge_attack_p2.set_data([], [])
    
    return plt_invader1, plt_invader2, plt_invader3, plt_invader4, plt_ufo, plt_player1, plt_player2, plt_explosion, plt_bullet_inv, plt_bullet_ply, plt_tx_center, plt_tx_p1, plt_tx_p2, plt_tx_p1_hp, plt_tx_p2_hp, plt_gauge_p1, plt_gauge_p2, plt_gauge_attack_p1, plt_gauge_attack_p2

def animate(i):
    global invader_fcount, invader_level
    global center_message, center_message_delay
    
    if i<30: # display the initial message
        plt_tx_center.set(text='Ready?')
        
        plt_player1.set_data([sp_player1.x],[sp_player1.y])
        plt_player2.set_data([sp_player2.x],[sp_player2.y])
        
        return plt_invader1, plt_invader2, plt_invader3, plt_invader4, plt_ufo, plt_player1, plt_player2, plt_explosion, plt_bullet_inv, plt_bullet_ply, plt_tx_center, plt_tx_p1, plt_tx_p2, plt_tx_p1_hp, plt_tx_p2_hp, plt_gauge_p1, plt_gauge_p2, plt_gauge_attack_p1, plt_gauge_attack_p2
    elif i==30:
        center_message = 'Go!'
        center_message_delay = 30
    
    if invader_fcount==0: # add new invaders
        
        sp = sprite()
        
        if np.random.randint(100)==0:
            sp.type = 5
            sp.path = 1
            sp.hp = 5
            if np.random.randint(2)==0:
                sp.x = -0.1
                sp.y = 0.8+np.random.rand(1)[0]*0.2
                sp.angle = 0.
                sp.speed *= 0.25
            else:
                sp.x = +1.1
                sp.y = 0.8+np.random.rand(1)[0]*0.2
                sp.angle = np.pi
                sp.speed *= 0.25
        else:
            sp.type = np.random.randint(1,5)
            if sp.type==1:
                sp.path = 1
            if sp.type==2:
                sp.path = 2
                sp.pathpar = (np.random.rand(1)[0]-0.5)*np.pi/6./10.
            if sp.type==3:
                sp.path = np.random.randint(3,5)
                sp.speed *= (0.4+0.1*invader_level)
            if sp.type==4: sp.path = 5
    
            sp.x = np.random.rand(1)[0]
            if sp.x<0.5: sp.angle = np.pi*3./2. + (np.random.rand(1)[0])*np.pi/4.
            else:        sp.angle = np.pi*3./2. - (np.random.rand(1)[0])*np.pi/4.
        
        splist_invader.append(sp)

    invader_fcount += 1
    if invader_fcount>=11-invader_level: invader_fcount = 0

    # shoot bullets from invader
    for sp in splist_invader:
        if sp.charge>=100-invader_level*10 and sp.x<1. and sp.x>0. and sp.y<1. and sp.y>0. and np.random.randint(2)==1:
            sp.charge = 0
            bullet = sprite(sp.x,sp.y)
            bullet.speed *= 2.
            bullet.type = 0
            bullet.path = 1
            if np.random.randint(2)==0:
                bullet.angle = np.arctan2(sp_player1.y-sp.y, sp_player1.x-sp.x)
            else:
                bullet.angle = np.arctan2(sp_player2.y-sp.y, sp_player2.x-sp.x)
            splist_bullet_inv.append(bullet)
        else:
            if sp.type==5: sp.charge += 2
            elif sp.type!=3: sp.charge += 1

    # shoot bullets from players
    if sp_player1.enabled:
        if sp_player1.charge>=6:
            sp_player1.charge = 0
            bullet = sprite(sp_player1.x,sp_player1.y)
            bullet.speed *= 4.
            bullet.type = 0
            bullet.path = 1
            bullet.angle = np.pi/2.
            splist_bullet_ply1.append(bullet)
        else:
            sp_player1.charge += 1

    if sp_player2.enabled:
        if sp_player2.charge>=6:
            sp_player2.charge = 0
            bullet = sprite(sp_player2.x,sp_player2.y)
            bullet.speed *= 4.
            bullet.type = 0
            bullet.path = 1
            bullet.angle = np.pi/2.
            splist_bullet_ply2.append(bullet)
        else:
            sp_player2.charge += 1

    # evaluate all of the displacements
    enemy_data = []

    for sp in splist_invader:
        sp.eval_displacement()
        enemy_data.append((sp.type,sp.x,sp.y,sp.dx,sp.dy))

    for sp in splist_bullet_inv:
        sp.eval_displacement()
        enemy_data.append((sp.type,sp.x,sp.y,sp.dx,sp.dy))

    for sp in splist_bullet_ply1:
        sp.eval_displacement()

    for sp in splist_bullet_ply2:
        sp.eval_displacement()

    # decision for players

    if sp_player1.enabled:

        player_data = []
        player_data.append((sp_player1.x,sp_player1.y,sp_player1.hp,ply_score[0],ply_gauge[0]))
        player_data.append((sp_player2.x,sp_player2.y,sp_player2.hp,ply_score[1],ply_gauge[1]))
        
        ret = player1.decision(player_data,enemy_data)
        
        sp_player1.speed = ret[0]*reference_speed
        if sp_player1.speed<0.: sp_player1.speed = 0.
        if sp_player1.speed>reference_speed: sp_player1.speed = reference_speed
        sp_player1.angle = ret[1]
        
        if ply_gauge_freeze[0]>0:
            sp_player1.speed = reference_speed
            sp_player1.angle = np.pi*(ply_gauge_freeze[0]%2)
            ply_gauge_freeze[0]-=1
        
        if ply_gauge_attack[0]==0:
            ply_gauge[0] += (reference_speed-sp_player1.speed)/reference_speed*4.
            if ply_gauge[0]>=1000.:
                ply_gauge[0] = 1.
                ply_gauge_attack[0] = 10
        else:
            ply_gauge_attack[0] -= 1
        
        sp_player1.dx = (sp_player1.speed)*np.cos(sp_player1.angle)
        sp_player1.dy = (sp_player1.speed)*np.sin(sp_player1.angle)

    if sp_player2.enabled:
        
        player_data = []
        player_data.append((sp_player2.x,sp_player2.y,sp_player2.hp,ply_score[1],ply_gauge[1]))
        player_data.append((sp_player1.x,sp_player1.y,sp_player1.hp,ply_score[0],ply_gauge[0]))
        
        ret = player2.decision(player_data,enemy_data)
        
        sp_player2.speed = ret[0]*reference_speed
        if sp_player2.speed<0.: sp_player2.speed = 0.
        if sp_player2.speed>reference_speed: sp_player2.speed = reference_speed
        sp_player2.angle = ret[1]

        if ply_gauge_freeze[1]>0:
            sp_player2.speed = reference_speed
            sp_player2.angle = np.pi*(ply_gauge_freeze[1]%2)
            ply_gauge_freeze[1]-=1

        if ply_gauge_attack[1]==0:
            ply_gauge[1] += (reference_speed-sp_player2.speed)/reference_speed*4.
            if ply_gauge[1]>=1000.:
                ply_gauge[1] = 1.
                ply_gauge_attack[1] = 10
        else:
            ply_gauge_attack[1] -= 1

        sp_player2.dx = (sp_player2.speed)*np.cos(sp_player2.angle)
        sp_player2.dy = (sp_player2.speed)*np.sin(sp_player2.angle)
    
    # loop over all bullets from players, check if it hits the invaders
    for sp in splist_bullet_ply1:
        for target in splist_invader:
            if target.eval_collision(sp):
                target.hp -= 1
                sp.hp -= 1
                if target.type==1 or target.type==1: ply_score[0] += 10
                if target.type==2 or target.type==3: ply_score[0] += 20
                if target.type==5: ply_score[0] += 40
    for sp in splist_bullet_ply2:
        for target in splist_invader:
            if target.eval_collision(sp):
                target.hp -= 1
                sp.hp -= 1
                if target.type==1 or target.type==1: ply_score[1] += 10
                if target.type==2 or target.type==3: ply_score[1] += 20
                if target.type==5: ply_score[1] += 40

    # check if the gauge attack hits the invaders & bullets
    if ply_gauge_attack[0]>0:
        rho = (10-ply_gauge_attack[0])*0.06
        for target in splist_invader:
            dist =  ((target.x-sp_player1.x)**2 + (target.y-sp_player1.y)**2)**0.5
            if dist<rho:
                target.hp -= 1
                if target.type==1 or target.type==1: ply_score[0] += 10
                if target.type==2 or target.type==3: ply_score[0] += 20
                if target.type==5: ply_score[0] += 40
        for target in splist_bullet_inv:
            dist =  ((target.x-sp_player1.x)**2 + (target.y-sp_player1.y)**2)**0.5
            if dist<rho:
                target.hp -= 1
                ply_score[0] += 5
        if sp_player2.enabled and ply_gauge_freeze[1]==0:
            dist = ((sp_player1.x-sp_player2.x)**2 + (sp_player1.y-sp_player2.y)**2)**0.5
            if dist<rho: ply_gauge_freeze[1]=50

    if ply_gauge_attack[1]>0:
        rho = (10-ply_gauge_attack[1])*0.06
        for target in splist_invader:
            dist =  ((target.x-sp_player2.x)**2 + (target.y-sp_player2.y)**2)**0.5
            if dist<rho:
                target.hp -= 1
                if target.type==1 or target.type==1: ply_score[1] += 10
                if target.type==2 or target.type==3: ply_score[1] += 20
                if target.type==5: ply_score[1] += 40
        for target in splist_bullet_inv:
            dist =  ((target.x-sp_player2.x)**2 + (target.y-sp_player2.y)**2)**0.5
            if dist<rho:
                target.hp -= 1
                ply_score[1] += 5
        if sp_player1.enabled and ply_gauge_freeze[0]==0:
            dist = ((sp_player1.x-sp_player2.x)**2 + (sp_player1.y-sp_player2.y)**2)**0.5
            if dist<rho: ply_gauge_freeze[0]=50

    # loop over all bullets from the invaders, check if it hits the player
    for sp in splist_bullet_inv:
        if sp_player1.enabled and sp_player1.eval_collision(sp):
            sp_player1.hp -= 1
            sp.hp -= 1
        if sp_player2.enabled and sp_player2.eval_collision(sp):
            sp_player2.hp -= 1
            sp.hp -= 1

    # loop over all invaders, check if it hits the player
    for sp in splist_invader:
        if sp_player1.enabled and sp_player1.eval_collision(sp):
            sp_player1.hp -= 1
            sp.hp -= 1
        if sp_player2.enabled and sp_player2.eval_collision(sp):
            sp_player2.hp -= 1
            sp.hp -= 1

    # move and draw the invaders
    sx1,sy1 = [],[]
    sx2,sy2 = [],[]
    sx3,sy3 = [],[]
    sx4,sy4 = [],[]
    sx5,sy5 = [],[]
    for sp in splist_invader[:]:
        sp.move()
        
        if sp.x<-0.1 or sp.x>1.1 or sp.y<-0.2 or sp.y>1.2:
            splist_invader.remove(sp)
            continue
        if sp.enabled and sp.hp<=0:
            sp.hp = 0
            sp.enabled = False
            splist_invader.remove(sp)
            splist_explosion.append(sp)
            continue
        
        if sp.type==1:
            sx1.append(sp.x)
            sy1.append(sp.y)
        if sp.type==2:
            sx2.append(sp.x)
            sy2.append(sp.y)
        if sp.type==3:
            sx3.append(sp.x)
            sy3.append(sp.y)
        if sp.type==4:
            sx4.append(sp.x)
            sy4.append(sp.y)
        if sp.type==5:
            sx5.append(sp.x)
            sy5.append(sp.y)

    plt_invader1.set_data(sx1,sy1)
    plt_invader2.set_data(sx2,sy2)
    plt_invader3.set_data(sx3,sy3)
    plt_invader4.set_data(sx4,sy4)
    plt_ufo.set_data(sx5,sy5)

    # move and draw the bullets from the invaders
    sx, sy = [], []
    for sp in splist_bullet_inv[:]:
        sp.move()
        if sp.x<-0.1 or sp.x>1.1 or sp.y<-0.2 or sp.y>1.2:
            splist_bullet_inv.remove(sp)
            continue
        if sp.hp<=0:
            splist_bullet_inv.remove(sp)
            continue
        sx.append(sp.x)
        sy.append(sp.y)
    plt_bullet_inv.set_data(sx,sy)

    # move and draw the bullets from the players
    sx, sy = [], []
    for sp in splist_bullet_ply1[:]:
        sp.move()
        if sp.x<-0.1 or sp.x>1.1 or sp.y<-0.2 or sp.y>1.2:
            splist_bullet_ply1.remove(sp)
            continue
        if sp.hp<=0:
            splist_bullet_ply1.remove(sp)
            continue
        sx.append(sp.x)
        sy.append(sp.y)

    for sp in splist_bullet_ply2[:]:
        sp.move()
        if sp.x<-0.1 or sp.x>1.1 or sp.y<-0.2 or sp.y>1.2:
            splist_bullet_ply2.remove(sp)
            continue
        if sp.hp<=0:
            splist_bullet_ply2.remove(sp)
            continue
        sx.append(sp.x)
        sy.append(sp.y)

    plt_bullet_ply.set_data(sx,sy)

    # now move the players, and draw them
    sp_player1.move()
    sp_player2.move()

    if sp_player1.x>1.: sp_player1.x = 1.
    if sp_player1.y>1.: sp_player1.y = 1.
    if sp_player2.x>1.: sp_player2.x = 1.
    if sp_player2.y>1.: sp_player2.y = 1.
    if sp_player1.x<0.: sp_player1.x = 0.
    if sp_player1.y<0.: sp_player1.y = 0.
    if sp_player2.x<0.: sp_player2.x = 0.
    if sp_player2.y<0.: sp_player2.y = 0.

    if sp_player1.enabled and sp_player1.hp<=0:
        sp_player1.hp = 0
        sp_player1.enabled = False
        splist_explosion.append(sp_player1)
    
    if sp_player1.enabled:
        plt_player1.set_data([sp_player1.x],[sp_player1.y])
    else:
        plt_player1.set_data([],[])

    if sp_player2.enabled and sp_player2.hp<=0:
        sp_player2.hp = 0
        sp_player2.enabled = False
        splist_explosion.append(sp_player2)
        
    if sp_player2.enabled:
        plt_player2.set_data([sp_player2.x],[sp_player2.y])
    else:
        plt_player2.set_data([],[])

    # display the explosions
    sx, sy = [], []
    for sp in splist_explosion[:]:
        sx.append(sp.x)
        sy.append(sp.y)
        if sp.type==5:
            for i in range(6):
                sx.append(sp.x+(np.random.rand(1)[0]-0.5)*0.1)
                sy.append(sp.y+(np.random.rand(1)[0]-0.5)*0.1)

        sp.hp -= 1
        if sp.type!=5 and sp.hp<=-3: splist_explosion.remove(sp)
        if sp.type==5 and sp.hp<=-6: splist_explosion.remove(sp)

    plt_explosion.set_data(sx,sy)

    plt_tx_p1.set(text='P1  '+str(ply_score[0]))
    plt_tx_p2.set(text=str(ply_score[1])+'  P2')
    plt_tx_p1_hp.set(text='HP  '+r'$\blacksquare$'*sp_player1.hp)
    plt_tx_p2_hp.set(text=r'$\blacksquare$'*sp_player2.hp+'  HP')

    plt_gauge_p1.set_data([-0.05,-0.05+ply_gauge[0]*0.001*0.4],[-0.15,-0.15])
    plt_gauge_p2.set_data([+1.05-ply_gauge[1]*0.001*0.4,+1.05],[-0.15,-0.15])

    # display the gauge attack
    sx, sy = [], []
    if ply_gauge_attack[0]>0:
        for i in range(91):
            rho = (10-ply_gauge_attack[0])*0.06
            phi = np.pi*2.*i/90.
            sx.append(sp_player1.x + rho*np.cos(phi))
            sy.append(sp_player1.y + rho*np.sin(phi))
    plt_gauge_attack_p1.set_data(sx,sy)

    sx, sy = [], []
    if ply_gauge_attack[1]>0:
        for i in range(91):
            rho = (10-ply_gauge_attack[1])*0.06
            phi = np.pi*2.*i/90.
            sx.append(sp_player2.x + rho*np.cos(phi))
            sy.append(sp_player2.y + rho*np.sin(phi))
    plt_gauge_attack_p2.set_data(sx,sy)

    # level up
    if (ply_score[0]+ply_score[1]>1000  and invader_level<=1) or \
       (ply_score[0]+ply_score[1]>3000  and invader_level<=2) or \
       (ply_score[0]+ply_score[1]>6000  and invader_level<=3) or \
       (ply_score[0]+ply_score[1]>10000 and invader_level<=4) or \
       (ply_score[0]+ply_score[1]>15000 and invader_level<=5):
        invader_level += 1
        center_message = 'Level '+str(invader_level)
        center_message_delay = 30

    # the game over message
    if not sp_player1.enabled and not sp_player2.enabled:
        center_message = 'Game Over'
        center_message_delay = 999
        
    if center_message_delay>0:
        plt_tx_center.set(text=center_message)
        if center_message_delay!=999: center_message_delay -= 1
    else: plt_tx_center.set(text='')

    return plt_invader1, plt_invader2, plt_invader3, plt_invader4, plt_ufo, plt_player1, plt_player2, plt_explosion, plt_bullet_inv, plt_bullet_ply, plt_tx_center, plt_tx_p1, plt_tx_p2, plt_tx_p1_hp, plt_tx_p2_hp, plt_gauge_p1, plt_gauge_p2, plt_gauge_attack_p1, plt_gauge_attack_p2


# main animation function call
anim = animation.FuncAnimation(fig, animate, init_func=init, interval=20)

# plt.tight_layout()
plt.show()
