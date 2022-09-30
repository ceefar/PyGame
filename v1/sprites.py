import pygame as pg
from settings import *
# start using vectors instead of individual xypos vars
vec = pg.math.Vector2
# test
from math import hypot



class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img # pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        # new - velocity vector, for speeding up and slowing down the player
        self.vel = vec(0, 0)
        # new - need position vector now too
        self.pos = vec(x, y) * TILESIZE

        # new sprint meter test
        self.sprint_meter = 6_000
        # new implementation is a dictionary storing the info on all states
        # using generic `state` for now until good reason to section out more 
        self.state_moving = "chilling"
        self.state_state = "fresh"
        # new test
        self.is_interacting = False
        # new player gold implementation, could be a class var if ur lazy
        self.player_gold = 0
        # new test, pause interactions
        self.waiting_print = False
        self.waiting = False

    def get_keys(self):
        self.vel = vec(0, 0) # define what our keys are going to do
        keys = pg.key.get_pressed() # see which keys are currently held down
        # -- player interaction keys --
        if keys[pg.K_e]: # if E
            # check any breakable walls interaction
            for a_wall in self.game.breakablewalls:
                # if player is near a breakable wall
                if a_wall.is_near(None, None):
                    a_wall.try_repair_wall()
            # only allow one interaction at a time, 2 sec pause currently should reduce tho
            self.is_interacting = True
        else:
            self.is_interacting = False
        # -- player movement keys --
        # if were pressing left on the keyboard or a            
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            # we're going to the left, so use negative
            self.vel.x = -PLAYER_SPEED  
            # set our state based on what keys we are pressing
            # when adding 'recovering' functionality, only set these states if not recovering, that takes precedence
            self.state_moving = "walking"        
        # use if to allow diagonal movements 
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.state_moving = "walking"
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            self.state_moving = "walking"
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            self.state_moving = "walking"      
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            # [ todo ] - own function, is sprinting /  handle sprinting
            # new sprint implementation, only called when holding sprint
            # so any sprint meter stuff needs to be done outside here duh
            self.vel *= self.get_sprint_multiplier() 
            self.state_moving = "sprinting"
            # [ todo ] - new function - handle sprint meter
            # decrease our sprint meter, make this a function too pls, pass a parameter as maybe we wanna reuse this for other reasons to decrease meter 
            # and legit have it recover less if you are in tiring zones
            # and defo do recover more if standing still btw duh!
            # maybe have sprint go down a bit faster btw
            self.sprint_meter -= self.sprint_meter / 100
        # DUHHHHHH if we are defo not sprinting things here
        else:
            self.image = self.game.player_img
            # [ todo ] - own function, is not sprinting / handle walking
            # if the sprint meter is not full, start to refill it
            if self.sprint_meter < 10_000:
                # [ todo ] - new function - handle sprint meter
                # if we are defo not sprinting the refill the bar, by 0.5 percent each frame
                # CHECK IF WE ARE STANDING STILL FIRST, IF WE ARE RECOVER BY MORE
                self.sprint_meter += self.sprint_meter / 200
            # remove any small offsets
            if self.sprint_meter > 6_000:
                self.sprint_meter = 6_000
        # if not moving in any direction, even if ur holding sprint, ur not moving
        if self.vel == 0 and self.vel.y == 0:
            self.state_moving = "chilling"
        # if two directions at the same time we dont want to do double speed     
        # dont need to reset state here dw       
        if self.vel.x != 0 and self.vel.y != 0:
            # because its multiplying by 2, get the square root of 2 to slow us back to down to where we should be (by multiplying under 1)
            self.vel *= 0.7071
        # if you are not sprinting but are also fatigued because ur sprint meter is exhausted
        # then reduce ur speed also, with rudimentary af ramping 
        # obvs very very unsure of the numbers and ranges yet but this implementation is fine for this mvp testing stage
        if self.state_moving == "walking" and self.sprint_meter < 1_000:
             self.vel *= 0.7
        if self.state_moving == "walking" and self.sprint_meter < 2_000:
             self.vel *= 0.8
        if self.state_moving == "walking" and self.sprint_meter < 3_000:
             self.vel *= 0.9    

    def get_sprint_multiplier(self) -> int:
        # should probably refector into get player speed but its fine for now
        # default player speed is 400, x1
        # once have ranges, hardcode the values and the increment differences for hella easy updates
        # if over 30% full sprint meter, there is no impact on your sprint speed, ur quick af boii
        if self.sprint_meter > 3_000: 
            # make me blurry if im sprinting at nax speed
            self.image = self.game.player_blur3_img
            return(1.5) # fast
        # else if we are basically out of sprint meter, and we're tryna sprint
        if self.sprint_meter < 600:
            return(0.5)
        if self.sprint_meter < 600:
            return(0.65)
        if self.sprint_meter < 700:
            return(0.8) # if you keep maxing it then sprint is actually slower than walking, were force the player to manage this             
        if self.sprint_meter < 800:
            return(0.9) # were force the player to manage this properly or pay the price, just like irl       
        if self.sprint_meter < 900:
            return(1) # no change from normal walking
        if self.sprint_meter < 1_000:
            # remember we *are* sprinting if this is called, or we are trying to anyway, its held down
            # so if you are super low on sprint meter, you should be notably not near sprint speed
            # should defo note this in yanno like pop up screens when explaining game functionality
            # as there is an implicit trade off here, if you are 'fatigued' 
            self.image = self.game.player_blur1_img
            return(1.15) # hastened
        else:
            # for now, if ur not spent, but not over 30% then still quick but not sprint, its like a jog
            self.image = self.game.player_blur1_img
            return(1.25) # quick

    def collide_with_walls(self, dir):
        # if checking an x collision
        if dir == "x":
            # then check if we the player have collied with a wall
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                # if i have hit something, check which side is it left or right using our velocity (which direction and where are we moving to)
                # if we were moving to the right when we collided with the wall, so put ourselves on that side of the wall
                if self.vel.x > 0:
                    # our x should be what ever it was that we hit(s) minus however wide we are
                    self.pos.x = hits[0].rect.left - self.rect.width
                # if the speed is the opposite direction then we were moving to the left so
                if self.vel.x < 0:
                    # put ourselves to the right of the thing we hit(s)[0]
                    self.pos.x = hits[0].rect.right
                # regardless of where we hit we are going to stop ourselves moving on this axis (x), because we've hit a wall to either side of us
                self.vel.x = 0
                self.rect.x = self.pos.x
        
        if dir == "y":
            bhits = pg.sprite.spritecollide(self, self.game.breakablewalls, False)
            # breakable wall
            if bhits:
                # print(f"Collided Wall Hp : {bhits[0].get_hp()}")
                if bhits[0].get_hp() <= 0:
                    # bhits[0].try_repair_wall()
                    pass # through freely
                else:
                    if self.vel.y > 0:
                        self.pos.y = bhits[0].rect.top - self.rect.height
                    if self.vel.y < 0:
                        self.pos.y = bhits[0].rect.bottom
                    self.vel.y = 0
                    self.rect.y = self.pos.y             
                    
            # normal wall    
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y             

    def update(self):
        self.get_keys()
        # update the position of the player based on keys pressed using velocity vector
        self.pos += self.vel * self.game.dt
        # set our rectangles x & y to the speed/post to check for collisions 
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        # basically were doing 2 collision check, 1 for each axis
        self.rect.y = self.pos.y
        self.collide_with_walls('y') 
        # pg.BLENDMODE_NONE
        print(f"{self.sprint_meter=}")
        # [ todo-asap! ] - new function
        # need sumnt like set state, unsure if best after or before keys but assumed after for obvs reasons
        # again forget actual ranges for now but if we are under 30% we are fatigued
        if self.sprint_meter < 3_000 :
            
            # you need to know if sprinting or not as should still be blurred if sprinting but dw about stuff like that at all for now
            # make me red and decoloured if im fatigued
            self.image = self.game.player_injury_img

            if self.sprint_meter < 1_000:
                self.state_state = "fatigued"
            elif self.sprint_meter < 2_000:
                # note yeah ranges and stuff still defo off af but the functionality is actually pretty good tbf i like it
                self.state_state = "struggling"            
            elif self.sprint_meter < 3_000:
                self.state_state = "tiring"     
        #elif self.sprint_meter > 3_000:
        else:
            self.state_state = "fresh"

            # tint img colour            


        # print(f"{(self.sprint_meter):.1f}% - {self.state_moving = }, {self.state_state = }, {self.vx = }")
        # new test
        if self.waiting:
            space_end = pg.time.get_ticks() 
            if space_end - self.waiting >= 2000:
                self.waiting = False
        if self.waiting_print:
            space_end = pg.time.get_ticks() 
            if space_end - self.waiting_print >= 2000:
                self.waiting_print = False                
        

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


# [ todo! ] - so a InteractWall Class with even just is_near yanno (and then else valid for that)

class BreakableWall(pg.sprite.Sprite): # should be called barricades huh
    wall_ids = []
    
    def __init__(self, game, x, y, player, hp=0):
        self.groups = game.all_sprites, game.breakablewalls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # new - need position vector now too
        self.pos = vec(x, y) * TILESIZE

        self.hp_current = hp
        self.hp_max = 4
        self.build_bar = 0
        self.player = player
        self.update_colour()
        # if the class variable wall_ids is not an empty list 
        if BreakableWall.wall_ids:
            # then add the most recent id + 1 
            BreakableWall.wall_ids.append(self) 
        # else if there is no ids in the wall_ids
        else:
            BreakableWall.wall_ids.append(self)
        self.myid = len(self.wall_ids)
        self.print_once(f"Where Player? -> {self.player.pos.x=}, {self.player.pos.y=}")
        print(f"Breakable Wall '{self.myid = }", f"{x=}",f"{y=}",f"{self.pos.x = }", f"{self.pos.y = }", f"{self.hp_current = }")

    # is broken, i.e. is 0 hp is what i want now
    def get_hp(self):
        return(self.hp_current)

    # [ todo ] - we have timed interactions now with is_interacting so implement that duh
    def try_repair_wall(self):
        self.build_bar += 1 # build bar is just the per frame builder, 
        if self.hp_current < self.hp_max: # so if we arent already a max hp wall 
            if self.build_bar == 30: # then if held for half a second at 60 frames, 1 hp will be added
                # self.do_once(x())
                self.hp_current = self.hp_current + 1
                self.build_bar = 0
        # for infectious buildling, repairing a tile will repairing any that are touching it
        for a_wall in self.wall_ids:
            # check if we this wall is near any other walls
            if a_wall.is_near(self.pos.x, self.pos.y):
                # if we both tiles dont have the same hp, update them so they are
                if a_wall.hp_current != self.hp_current:
                    self.print_once(f"Shared Our HP Commrade -> {a_wall.hp_current}, {self.hp_current}")
                    a_wall.hp_current = self.hp_current
        print(f"reparing wall [ {self.myid} - {self.hp_current}hp ] -> {self.build_bar = }")
        self.update_colour()

    def update_colour(self):
        """ every time something interacts with me, run this (?) """
        # DARKGREY, GREY, LIGHTGREY, PRINT, RUST, HIGHLIGHTER, PALEGREY, TAN, COFFEE, MOONGLOW
        if self.hp_current == 0:
            self.image.fill(BLACK)
        elif self.hp_current == 1:
            self.image.fill(GREY) # TOO MUCH LIKE BACKGROUND BUT MAYBE
        elif self.hp_current == 2:
            self.image.fill(BROWNTONE1) # DECENT
        elif self.hp_current == 3:
            self.image.fill(BROWNTONE2) # DECENT    
        elif self.hp_current == 4:
            self.image.fill(BROWNTONE3) # DECENT               

    def is_near(self, x, y):
        # [ todo-asap! ] - the reason it goes up by 2 is if touching 2 
        # [ todo-asap! ] - means same could happen with 3 too 
        # [ todo-asap! ] - so either take the amount touching into consideration 
        # [ todo-asap! ] - or fix a proper way
        # [ todo-asap! ] - actually tbf i think...
        # [ todo-asap! ] - that taking how many are touching into account IS the proper way lol <<<<<< THIS 
        # define vars that mean in future we could have like an action dist, even view dist maybe
        very_very_close = 30 # means in tight spaces only one side or the other but changing the map now anyway so this likely never gets used but nice for reference
        very_close = 50 # might not be agnostic of tilesize btw if changed from 64 that i think im using now
        close = 80
        if not x:
            x = self.player.pos.x
        if not y:
            y = self.player.pos.y
        # use hypotenus of the xy vectors to find out how close we are to the player
        pythag_dist = hypot(self.pos.x-x, self.pos.y-y)
        if pythag_dist < close:
            self.print_once(f"{pythag_dist=}, {self.myid}, {self.pos.x=}, {self.pos.y=}\n{x=}, {y=}")
        # if we are right next to the sprite our pythag_dist will be the size of the tile e.g. 32 
        return True if pythag_dist < close else False

    def print_once(self,print_me): # temp test for debugging only   
        # abusing the players waiting variable to only do an action 1 once every x seconds (2s currently)
        if not self.player.waiting_print:
            print(print_me)
            self.player.waiting_print = pg.time.get_ticks()

    # unused, does work in theory but not properly tested
    def do_once(self, func): # temp test for debugging only   
        # abusing the players waiting variable to only do an action 1 once every x seconds (2s currently)
        if not self.player.waiting:
            func
            self.player.waiting = pg.time.get_ticks()

    def update(self):
        # if we (this iinstance of breakable wall) are near the player
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.is_near(None, None):  
            # if the wall can be rebuilt more still
            if self.hp_current < self.hp_max:
                # and the player isn't interacting with anything
                # currently only the 'e' aka 'build' key but will be others for sure, sprint too surely duhhh!
                if self.player.is_interacting == False:
                    self.image.fill(HIGHLIGHTER)
            else:
                self.image.fill(BROWNTONE4)
        else:
            self.update_colour()

    # [ todo-asap! ] - wall max hp broken again
    # [ todo-asap! ] - then continue tuts pls!


    # unused implementation of is interacting 
    """
    def unlock(self):
        # if you can buy (you've already pressed the button btw)      
        if not self.player.waiting:
            if self.check_is_buyable():
                # take the gold, and unlock the wall, start the timer so this can only happen one every x seconds
                self.player.player_gold = self.player.player_gold - self.unlock_cost
                self.is_locked = False 
                self.player.waiting = pg.time.get_ticks() 
                print("Buying Disabled For 2 Seconds")


        # new test
        if self.waiting:
            space_end = pg.time.get_ticks() 
            if space_end - self.waiting >= 2000:
                print("Buying Reactivated")
                self.waiting = False
    """







