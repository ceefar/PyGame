import pygame as pg
from settings import *
from random import randint
from math import floor



# og update with target radius and distance for in a bit
# ------------------------------------------------------
# # requires - self.target_radius = 10
# def update(self):
#     # A vector pointing from self to the target.
#     heading = self.target - self.pos
#     distance = heading.length()  # Distance to the target.
#     heading.normalize_ip()
#     if distance <= self.target_radius:
#         # If we're approaching the target, we slow down.
#         self.vel = heading * (distance / self.target_radius * self.max_speed)
#     else:  # Otherwise move with max_speed.
#         self.vel = heading * self.max_speed
#     self.pos += self.vel
#     self.rect.center = self.pos



MENU_SIZE = (1000, 500) # 1408 x 768
# REEL_SIZE = (MENU_SIZE[0]/8, MENU_SIZE[1])# (MENU_SIZE[0]/6, MENU_SIZE[1]/2)
BACKGROUND_COLOR = (30, 40, 50)
CARDS_LIST = ["G", "G+", "G++"] # player or total as different to do, so only total will be global but is fine for now

             

class Casino_Roller(pg.sprite.Sprite): # (object) ?
    """ basic first test implementation of random one eyed bandit roller """

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface(MENU_SIZE)
        self.rect = self.image.get_rect(x=WIDTH - MENU_SIZE[0]) # width minus the width of the actual sidebar size (not the img so its squished?)
        self.pos = vec(self.rect.x, self.rect.y)
        self.centerpos = vec(self.rect.centerx, self.rect.centery) # self.rect.x = 774, self.rect.centerx = 899
        #
        self.random_number = randint(1,10) # awesome, it persists now
        # icon 1 - gold+
        self.gold_image = self.game.casino_gold_img_1.copy() 
        self.gold_image_rect = self.gold_image.get_rect()
        # icon 2 - gold++
        self.gold_p_image = self.game.casino_gold_img_2.copy() 
        self.gold_p_image_rect = self.gold_p_image.get_rect()
        #
        self.card_buffer = 20 # buffer around the images 
        self.card_gutter = 30 # gutter to space them out
        # 
        self.roll_timer = 0 # randomly stops the random roll

    def draw(self, surface):
        """ standard draw """
        surface.blit(self.image, ((WIDTH / 2) - (self.rect.width / 2),  (HEIGHT / 2) - (self.rect.height / 2)))  
        self.image.fill(WHITE) 
        self.draw_cards()
    
    def update(self):
        pass
        #self.reel_update()

    def draw_cards(self):
        #self.reel_pos = vec(self.reel_rect.x, self.reel_rect.y)
        increment = self.gold_image_rect.width + self.card_gutter # width + buffer
        width_cards = int(MENU_SIZE[0] / increment) # for buffer
        # probably dont need this but saving them now just incase, should be all as a list not sides, just do strip first tho
        top_positions = []

        # own funct maybe ?
        roll_tracker =  self.random_number - 1 # roll_tracker = randint(0,8)

        #
        full_rotation_time = 2000 # how long it takes to flash them all in one go
        rotation_increment = (full_rotation_time / width_cards)

        roll_check_timer = pg.time.get_ticks()

        if self.roll_timer:
            true_roll_time = (roll_check_timer - self.roll_timer) % 2000
            print(f"{true_roll_time = }")
            
        else:
            self.roll_timer = pg.time.get_ticks()


        
        true_roll_time = roll_check_timer - self.roll_timer
        print(f"{true_roll_time = }")
        print(f"{width_cards = }")
        
        if self.roll_timer:
            print(f"{self.roll_timer = }")
            for i in range(1, width_cards):   
                print(f"{i = }")
                print(f"{width_cards = }")
                # get the position we want it at add also add it to our positions list 
                temp_rect = self.gold_image_rect.copy()   
                temp_rect.width += self.card_buffer
                temp_rect.height += self.card_buffer
                temp_rect.x, temp_rect.y,  = increment*i, self.card_gutter
                top_positions.append((temp_rect.x, temp_rect.y))
                if true_roll_time <= rotation_increment * i and true_roll_time > rotation_increment * (i - 1):
                    print(f"print_highlight {i = }")
                    self.draw_single_card(increment, temp_rect, i, True)
                else:
                    print(f"no highlight {i = }")
                    self.draw_single_card(increment, temp_rect, i, False)
        #
        print(f"{self.roll_timer = }")
        if true_roll_time > 2000:
            roll_check_timer = 0
            self.roll_timer = 0
        
        # 
        # print(f"{top_positions = }, {len(top_positions) = }")


    def draw_single_card(self, increment, temp_rect, i, want_highlight=False):
        """ as a function so we can do highlighting in a loop """
        self.image.blit(self.gold_image, ((increment*i) + (self.card_buffer / 2), self.card_gutter + (self.card_buffer / 2))) 
        if want_highlight:
            pg.draw.rect(self.image, ORANGE, temp_rect, 8) # HIGHLIGHTER
        else:
            pg.draw.rect(self.image, BLUEMIDNIGHT, temp_rect, 5)

    # then loop this with the timer ting, if it can stop on the right ting then its golden
    # then
    # obvs want them to be random
    # and in an actual box too
    # then
    # i reckon then actually start slowly styling it for tonight then tomo we start fresh :D




    # self.image.blit(self.gold_p_image, ((100 - self.gold_p_image_rect.width) / 2, 80))  
    



    # def icon_update(self, icon_target, icon_pos, icon_max_speed, icon_vel, icon_rect):
    #     # A vector pointing from self to the target.
    #     heading = icon_target - icon_pos
    #     distance = heading.length()  # Distance to the target.
    #     if distance <= 5:  
    #         icon_pos.y = -50
    #         heading = icon_target - icon_pos
    #         heading.normalize_ip() 
    #     else:
    #         heading.normalize_ip()  
    #     icon_vel = heading * icon_max_speed
    #     icon_pos += icon_vel
    #     icon_rect.center = icon_pos
        

     




    # uh yah, its because these aren't sprites
    # imo just try this again from scratch for a few hours
    # if it doesnt flow after the first hour and a bit
    # do the fork tut to end idea then restart it cleanly imo, starting at ui 

    # custom border, custom card, custom reel, custom bg - all imgs btw
    # also please shortly do other ui things too, damage numbers, subscribers bar, bottom right charge like persona, top right more custom too, card for companion/items, etc

    # do showing dmg numbers too btw

    # should do pick up gold, requires items tut, and likely requires tiled tut...
    # - so dont do now, do after full refactor idea after finishing that base tut from new fork






    # start with ig double shot, uzi, gold, companion sumnt
    # grab these images and then get them on the strip
    # when on the strip get it spinning
    # when spinning get it randomly choosing based on odds
    # when odds get it stopping on the correct image
    # then do the overlay
    # then wire it all up for the logic
    # then make it a tad fancy maybe - or better, fully plan it tbf
    # then refactor
