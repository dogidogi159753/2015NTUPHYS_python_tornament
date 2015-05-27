import numpy as np

# helper function
def point_line_distance(line_s, line_p, point):
    return abs(line_s*point[0]-point[1]+line_p[1]-line_s*line_p[0])/(line_s**2+1)**0.5

def point2Slope(p1, p2):
    angle = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])
    return angle

def eval_collision(p, obj): # collision detection, only consider the center of obj hitting the square box from self center
    l = 0.06
    
    if abs(obj[1]-p[0])<l and abs(obj[2]-p[1])<l: return True
    if abs(obj[1]-p[0] + (obj[3]-p[2]))<l and abs(obj[2]-p[1] + (obj[4]-p[3]))<l: return True

    return False

class player_module:
    parameter = {
        "caution_dist" : 0.2,
    }
        
    # constructor, allocate any private date here
    def __init__(self):
        self.init_x, self.init_y = -1., -1.
        self.gauge_flag = False

    # Please update the banner according to your information
    def banner(self):
        print '-'*40
        print 'Author: dogiJ'
        print 'ID: b01202036'
        print '-'*40
    
    # Decision making function for moving your ship, toward next frame:
    # simply return the speed and the angle
    # ----------------------------------------------
    # The value of "speed" must be between 0 and 1.
    # speed = 1 : full speed, moving 0.01 in terms of space coordination in next frame
    # speed = x : moving 0.01*x in terms of space coordination
    # speed = 0 : just don't move
    #
    # The value of angle must be between 0 and 2*pi.
    #
    # if speed is less than 1, it will store the gauge value by 4*(1-speed).
    # If the gauge value reach 1000, it will perform the "gauge attack" and destory
    # any enemy within a circle of 0.6 radius
    #
    def decision(self,player_data, enemy_data):
        
        speed, angle = 0., 0.

        # parameters
        caution_dist = self.parameter["caution_dist"]

        # flags
        release_gauge = False

        # your data
        player1_x     = player_data[0][0]
        player1_y     = player_data[0][1]
        player1_hp    = player_data[0][2]
        player1_score = player_data[0][3]
        player1_gauge = player_data[0][4]
        
        # data for another player
        player2_x     = player_data[1][0]
        player2_y     = player_data[1][1]
        player2_hp    = player_data[1][2]
        player2_score = player_data[1][3]
        player2_gauge = player_data[1][4]
        
        # save the initial x position
        if self.init_x==-1. and self.init_y==-1.:
            self.init_x, self.init_y = 0.5, 0.2
        
        # let's try to move back to the initial position by default
        speed = ((self.init_x-player1_x)**2 + (self.init_y-player1_y)**2)**0.5
        speed /= 0.01 # since the maximum speed is 0.01 unit per frame
        if speed>1.: speed = 1.
        angle = np.arctan2(self.init_y-player1_y,self.init_x-player1_x)
        if not enemy_data: return speed, angle

        # loop over the enemies and bullets
        gauge_range_enemy_num = 0
        nearest_enemy = []
        bullets = []
        for data in enemy_data:
            type = data[0] # 0 - bullet, 1..4 - different types of invaders, 5 - ufo
            x    = data[1]
            y    = data[2]
            dx   = data[3] # expected movement in x direction for the next frame
            dy   = data[4] # expected movement in y direction for the next frame
            dist = ((x-player1_x)**2+(y-player1_y)**2)**0.5

            if dist <= 0.5:
                gauge_range_enemy_num += 1

            if not nearest_enemy:
                nearest_enemy = [dist, data]
            if dist <= nearest_enemy[0]:
                if dist**2 >= ((x+dx-player1_x)**2+(y+dy-player1_y)**2):
                    nearest_enemy = [dist, data]
            if type == 0 and dist < caution_dist:
                bullets.append(data)

        # take action    
        if nearest_enemy and nearest_enemy[0] < caution_dist:
            type = nearest_enemy[1][0] # 0 - bullet, 1..4 - different types of invaders, 5 - ufo
            x    = nearest_enemy[1][1]
            y    = nearest_enemy[1][2]
            dx   = nearest_enemy[1][3] # expected movement in x direction for the next frame
            dy   = nearest_enemy[1][4] # expected movement in y direction for the next frame

            speed = 1.

            if type == 3 and (dy/dx-(player1_y-y)/(player1_x-x)) < 10**-3:
                angle = point2Slope([x, y], [player1_x, player1_y])
                if x > player1_x and y > player1_y:
                    angle += np.pi/2
                else:
                    angle -= np.pi/2
            else:
                tmp_x = player1_x-dy/dx*(dy/dx*player1_x-player1_y+y-dy/dx*x)/((dy/dx)**2+1)
                tmp_y = player1_y+(dy/dx*player1_x-player1_y+y-dy/dx*x)/((dy/dx)**2+1)
                angle = point2Slope([tmp_x, tmp_y], [player1_x, player1_y])

        # if going to hit the enemy, release gauge
        for data in enemy_data:
            if eval_collision([player1_x, player1_y, speed*0.01*np.cos(angle), speed*0.01*np.sin(angle)], data)\
                and player1_gauge >= 995:
                release_gauge = True
                speed = 0.

        # shake to not release gauge
        if player1_gauge >= 995 and speed != 1. and not release_gauge and gauge_range_enemy_num < 10:
            speed = 1.
            if self.gauge_flag:
                angle = 0.
                self.gauge_flag = False
            else:
                angle = np.pi
                self.gauge_flag = True

        return speed, angle