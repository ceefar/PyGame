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
        # random numbers
        self.random_number = randint(1000, 3000) # for slowing down, basically how long it should take to stop tho not entirely accurate as its sets the rate that we slow at
        self.big_random_number = randint(15_000, 30_000) # the speed we want to get to so we appear as tho we aren't moving, randomised to we get a really good random roll each time 
        self.chicken_dinner_roll = randint(1000, 5000) # left = amount it will defo last for, e.g. 2000 ms, then how long it could last, ideally this should be min 2x the length of 1 rotation for variety 
        print(f"{self.random_number, self.big_random_number, self.chicken_dinner_roll}")
        
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
        # rotation here means of the length of the cards, i.e. how long it takes to flash them all in one go,
        self.roll_timer = 0 # randomly stops the random roll
        self.count_full_rotations = 0 # count of full rotations of a reel, used to count a set amount before slowing down
        self.full_rotation_time = 480 # dynamic af so changing this changes the speed
        self.roll_winner = 0 # ig probs temp while testing how best to do this
        self.winner_winner = False # flag that tells us when the reel roll has completely stopped and a random winner has been selected, winner winner chicken dinner random spinner
        self.roll_stop_timer = False

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
        top_positions = [] # probably dont need this but saving them now just incase, should be all as a list not sides, just do strip first tho
        # how many ticks for each segment based on the time we want to flash for and the amount of cards to flash in one rotation
        rotation_increment = (self.full_rotation_time / width_cards)
        roll_check_timer = pg.time.get_ticks()
    	
        # if more than 5 full rotations, start to decrementally slow
        if self.count_full_rotations >= 5:
            self.slow_rotate_picker_and_choose_a_winner()        

        if self.roll_timer:
            true_roll_time = (roll_check_timer - self.roll_timer) % self.full_rotation_time
            #print(f"{true_roll_time = }")
        else:
            self.roll_timer = pg.time.get_ticks()

        true_roll_time = roll_check_timer - self.roll_timer
        #print(f"{true_roll_time = }")

        if self.winner_winner: # if you've won 
            print(f"CONGRATULATIONS! => {self.roll_winner}!!!")
            # draw again but at fix highlight where winner is and flash
            for i in range(1, width_cards): 
                temp_rect = self.gold_image_rect.copy()   
                temp_rect.width += self.card_buffer
                temp_rect.height += self.card_buffer
                temp_rect.x, temp_rect.y,  = increment*i, self.card_gutter
                top_positions.append((temp_rect.x, temp_rect.y))
                if i == self.roll_winner:
                    flashme2 = pg.time.get_ticks() # start flashing
                    flashme2 = int(f"{flashme2}"[2])
                    if flashme2 % 2 != 0: # if the highest digit number is even on if not off, for flash   
                        self.draw_single_card(increment, temp_rect, i, True)
                        flashme2 = False
                else:
                    self.draw_single_card(increment, temp_rect, i, False)
                    
        else:
            # do this stuff until a winner has been selected 
            if self.roll_timer:
                #print(f"{self.roll_timer = }")
                for i in range(1, width_cards):   
                    # get the position we want it at add also add it to our positions list 
                    temp_rect = self.gold_image_rect.copy()   
                    temp_rect.width += self.card_buffer
                    temp_rect.height += self.card_buffer
                    temp_rect.x, temp_rect.y,  = increment*i, self.card_gutter
                    top_positions.append((temp_rect.x, temp_rect.y))
                    if true_roll_time <= rotation_increment * i and true_roll_time > rotation_increment * (i - 1):
                        self.draw_single_card(increment, temp_rect, i, True) # print highlight
                        self.roll_winner = i # the current highlighted cards index in width cards
                    else:
                        self.draw_single_card(increment, temp_rect, i, False) # no higlight
            if true_roll_time > self.full_rotation_time: # reset the timers if they've hit the full rotation time
                roll_check_timer = 0
                self.roll_timer = 0
                self.count_full_rotations += 1
                #print(f"{self.count_full_rotations = }")
        
    def slow_rotate_picker_and_choose_a_winner(self): # for the dramaz of stopping slowly 
        # X seconds after this triggers the roller will start slowing incrementally until its so slow it seems like it stopped
        # then we'll move them to where they are closest!  

        max_rotation_speed = self.big_random_number  # for slowing down, 1 rotation max speed, in milliseconds
        time_until_stop = self.random_number # how long it should take from triggering stop to hit the max rotation speed, idea being that max rotation speed is so slow you look stopped, then you can actually stop too obvs
        taper_increments = max_rotation_speed / time_until_stop  # how many to add to get to our max rotation speed in the amount of time given, in ticks
        # slow down
        if self.full_rotation_time < max_rotation_speed: # if you've not slowed to a halt, keep slowing
            self.full_rotation_time += taper_increments
            self.roll_stop_timer = pg.time.get_ticks()
            #print(f"{self.full_rotation_time = }")
        # at this speed (now add ms too), pick a winner
        just_stop = False
        check_timer = pg.time.get_ticks()
        print(f"{check_timer - self.roll_stop_timer = }")
        if check_timer - self.roll_stop_timer > 5000: # if its been more than 5 seconds since you started slowing down, then stop
            self.roll_stop_timer = 0 # turn off these timers
            check_timer = 0
            just_stop = True
            print("STOPPED BY TIMER")
        if self.full_rotation_time > self.chicken_dinner_roll or just_stop: # this is actually a certain speed it wants us to get to before stopping, so adding another timer condition just incase
            # if you wanna do bonus stuff it can be changed by altering max_rotation_speed, the randint range of time_until_stop_ and this var here too
            self.winner_winner = True # use this flag to toggle when to stop the roll, we will have saved the winning index from the loop already so is fine if we just reprint the win!
            self.full_rotation_time = 1_000_000 # make it so ridiculous it wont move
            print("IF NOT STOPPED BY TIMER THEN I WAS STOPPED BY SPEED")
            print(f"{self.chicken_dinner_roll = }")

    def draw_single_card(self, increment, temp_rect, i, want_highlight=False):
        """ as a function so we can do highlighting in a loop """
        # get random card ()
        # - want to return name also so can display that and know what it is duh! 
        # - likely also want odds as part of that too so just return a tuple with odds anyway even if u dont use them!
        self.image.blit(self.gold_image, ((increment*i) + (self.card_buffer / 2), self.card_gutter + (self.card_buffer / 2))) 
        if want_highlight:
            pg.draw.rect(self.image, ORANGE, temp_rect, 8) # HIGHLIGHTER
        else:
            pg.draw.rect(self.image, BLUEMIDNIGHT, temp_rect, 5)










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
