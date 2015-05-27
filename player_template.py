import numpy as np

class player_module:
        
    # constructor, allocate any private date here
    def __init__(self):
        self.init_x, self.init_y = -1., -1.

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
        
        # let's try to move back to the initial position by default
        speed = ((self.init_x-player1_x)**2 + (self.init_y-player1_y)**2)**0.5
        speed /= 0.01 # since the maximum speed is 0.01 unit per frame
        if speed>1.: speed = 1.
        angle = np.arctan2(self.init_y-player1_y,self.init_x-player1_x)
        
        # loop over the enemies and bullets
        for data in enemy_data:
            type = data[0] # 0 - bullet, 1..4 - different types of invaders, 5 - ufo
            x    = data[1]
            y    = data[2]
            dx   = data[3] # expected movement in x direction for the next frame
            dy   = data[4] # expected movement in y direction for the next frame
            if dx == 0: print "0"
            # calculate the distance toward player1
            dist = ((x-player1_x)**2+(y-player1_y)**2)**0.5
            
            # if the enemy is too close
            if dist < 0.2:
                speed = 1.0
                if x<player1_x: angle = 0.    # escape to right
                if x>player1_x: angle = np.pi # escape to left
                break

        return speed, angle
