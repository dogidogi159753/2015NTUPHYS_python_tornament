import numpy as np

# helper function
def point_line_distance(line_s, line_p, point):
    return abs(line_s*point[0]-point[1]+line_p[1]-line_s*line_p[0])/(line_s**2+1)**0.5

def point2Slope(p1, p2):
    angle = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])
    if angle < 0: angle += 2*np.pi
    return angle

def eval_collision(p, obj): # collision detection, only consider the center of obj hitting the square box from self center
    l = 0.07
    
    if abs(obj[1]-p[0])<l and abs(obj[2]-p[1])<l: return True
    if abs(obj[1]-p[0] + (obj[3]-p[2]))<l and abs(obj[2]-p[1] + (obj[4]-p[3]))<l: return True

    return False

class player_module:

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
        caution_r = 0.2
        dist_p    = 2.
        bullet_q  = 5.
        line_q    = 1.
        type3_q   = 3.
        curve_q   = 1.3
        wall_p    = 2.
        wall_q    = 1.

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
            self.init_x, self.init_y = player1_x, player1_y
        
        speed, angle = 0.5, point2Slope([player1_x, player1_y], [0.5, 0.2])

        if not enemy_data: return speed, angle

        # loop over the enemies and bullets
        force = []
        gauge_range_enemy_num = 0
        for data in enemy_data:
            type = data[0] # 0 - bullet, 1..4 - different types of invaders, 5 - ufo
            x    = data[1]
            y    = data[2]
            dx   = data[3] # expected movement in x direction for the next frame
            dy   = data[4] # expected movement in y direction for the next frame
            dist = ((x-player1_x)**2+(y-player1_y)**2)**0.5

            if dx == 0: dx += 10**-6
            if dist <= 0.5:
                gauge_range_enemy_num += 1
            
            if type == 0:
                if dist < caution_r:
                    tmp_x = player1_x-dy/dx*(dy/dx*player1_x-player1_y+y-dy/dx*x)/((dy/dx)**2+1)
                    tmp_y = player1_y+(dy/dx*player1_x-player1_y+y-dy/dx*x)/((dy/dx)**2+1)
                    f_angle = point2Slope([tmp_x, tmp_y], [player1_x, player1_y])
                    force.append([bullet_q/dist**dist_p*np.cos(f_angle), bullet_q/dist**dist_p*np.sin(f_angle)])
            if type == 1:
                if dist < caution_r:
                    tmp_x = player1_x-dy/dx*(dy/dx*player1_x-player1_y+y-dy/dx*x)/((dy/dx)**2+1)
                    tmp_y = player1_y+(dy/dx*player1_x-player1_y+y-dy/dx*x)/((dy/dx)**2+1)
                    f_angle = point2Slope([tmp_x, tmp_y], [player1_x, player1_y])
                    force.append([line_q/dist**dist_p*np.cos(f_angle), line_q/dist**dist_p*np.sin(f_angle)])
            if type == 3 and (dy/dx-(player1_y-y)/(player1_x-x)) < 10**-3:
                f_angle = point2Slope([x, y], [player1_x, player1_y])
                if x > player1_x and y > player1_y:
                    f_angle += np.pi/2
                else:
                    f_angle -= np.pi/2
                force.append([type3_q/dist**(dist_p)*np.cos(f_angle), type3_q/dist**(dist_p)*np.sin(f_angle)])
            else:
                if dist < caution_r:
                    f_angle = point2Slope([x, y], [player1_x, player1_y])
                    force.append([curve_q/dist**dist_p*np.cos(f_angle), curve_q/dist**dist_p*np.sin(f_angle)])

        # to avoid stocking at wall
        if player1_x > 0.9 or player1_x < 0.1:
            if player1_x == 0: player1_x += 10**-6
            if player1_x == 1: player1_x -= 10**-6
            force.append([wall_q*(1./player1_x**(wall_p)-1./(1.-player1_x)**(wall_p)), 0.])
        if player1_y > 0.5 or player1_y < 0.1:
            if player1_y == 0: player1_y += 10**-6
            if player1_y == 1: player1_y -= 10**-6
            force.append([0., wall_q/player1_y**(wall_p)-wall_q*2/(1.-player1_y)**(wall_p)])

        # take action
        x_sum, y_sum, count = 0., 0., 0
        for f in force:
            x_sum += f[0]
            y_sum += f[1]
            count += 1
        if count != 0:
            x_sum /= count
            y_sum /= count
            if abs(x_sum)+abs(y_sum) > 10:
                speed = 1.
            else:
                speed = abs(x_sum)+abs(y_sum)/10
            angle = np.arctan2(y_sum, x_sum)
            if angle < 0.: angle += 2*np.pi

        for data in enemy_data:
            if eval_collision([player1_x, player1_y, speed*0.01*np.cos(angle), speed*0.01*np.sin(angle)], data)\
                and player1_gauge >= 995:
                release_gauge = True
                speed = 0.

        if player1_gauge >= 995 and speed != 1. and not release_gauge and gauge_range_enemy_num < 5:
            speed = 1.
            if self.gauge_flag:
                angle = 0.
                self.gauge_flag = False
            else:
                angle = np.pi
                self.gauge_flag = True

        return speed, angle