import pygame as pg
from settings import *
# start using vectors instead of individual xypos vars
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        # new - velocity for speeding up and slowing down the player
        self.vc, self.vy = 0, 0
        

        # to start at the correct position on the map multiply initial position by the tilesize
        self.x = x * TILESIZE 
        self.y = y * TILESIZE
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
        self.waiting = False

    def get_keys(self):
        # define what our keys are going to do
        self.vx, self.vy, = 0, 0 
        # see which keys are currently held down
        keys = pg.key.get_pressed()
        # temp af test
        if keys[pg.K_g]: 
            # g = gold, figure out how to use game current time (from recent viewed stackoverflow) to tempoarily stop for stuff like this!
            self.player_gold = self.player_gold + 10
        if keys[pg.K_p]: # p == print 
            print(f"{self.player_gold = }")
        if keys[pg.K_u]:     
        # test unlock walls < use U for unlock plis
            for a_wall in self.game.unlockwalls:
                # for every wall, if you are near that wall
                if a_wall.is_near(self.x, self.y): # if you've pushed this button delete, and it checks if you are near (and can buy it) first
                    a_wall.unlock()
        if keys[pg.K_e]:
            # test breakable walls
            for a_wall in self.game.breakablewalls:
                print(a_wall.x)
                if a_wall.is_near(self.x, self.y):
                    print("reparing wall")
                    a_wall.try_repair_wall()
            # if e key set is_interacting to true else false
            self.is_interacting = True
        else:
            self.is_interacting = False
        # if were pressing left on the keyboard or a            
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            # we're going to the left, so use negative
            self.vx = -PLAYER_SPEED  
            # set our state based on what keys we are pressing
            # when adding 'recovering' functionality, only set these states if not recovering, that takes precedence
            self.state_moving = "walking"        
        # use if to allow diagonal movements 
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
            self.state_moving = "walking"
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
            self.state_moving = "walking"
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
            self.state_moving = "walking"      
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            # [ todo ] - own function, is sprinting /  handle sprinting
            # new sprint implementation, only called when holding sprint
            # so any sprint meter stuff needs to be done outside here duh
            self.vy *= self.get_sprint_multiplier() 
            self.vx *= self.get_sprint_multiplier() 
            self.state_moving = "sprinting"
            # [ todo ] - new function - handle sprint meter
            # decrease our sprint meter, make this a function too pls, pass a parameter as maybe we wanna reuse this for other reasons to decrease meter 
            # and legit have it recover less if you are in tiring zones
            # and defo do recover more if standing still btw duh!
            # maybe have sprint go down a bit faster btw
            self.sprint_meter -= self.sprint_meter / 100
        # DUHHHHHH if we are defo not sprinting things here
        else:
            # [ todo ] - own function, is not sprinting / handle walking
            # if the sprint meter is not full, start to refill it
            if self.sprint_meter < 10_000:
                # [ todo ] - new function - handle sprint meter
                # if we are defo not sprinting the refill the bar, by 0.5 percent each frame
                # CHECK IF WE ARE STANDING STILL FIRST, IF WE ARE RECOVER BY MORE
                self.sprint_meter += self.sprint_meter / 200
            # remove any small offsets
            if self.sprint_meter > 10_000:
                self.sprint_meter = 10_000
        # if not moving in any direction, even if ur holding sprint, ur not moving
        if self.vx == 0 and self.vy == 0:
            self.state_moving = "chilling"
        # if two directions at the same time we dont want to do double speed     
        # dont need to reset state here dw       
        if self.vx != 0 and self.vy != 0:
            # because its multiplying by 2, get the square root of 2 to slow us back to down to where we should be (by multiplying under 1)
            self.vx *= 0.7071
            self.vy *= 0.7071
        # if you are not sprinting but are also fatigued because ur sprint meter is exhausted
        # then reduce ur speed also, with rudimentary af ramping 
        # obvs very very unsure of the numbers and ranges yet but this implementation is fine for this mvp testing stage
        if self.state_moving == "walking" and self.sprint_meter < 1_000:
             self.vx *= 0.7
             self.vy *= 0.7
        if self.state_moving == "walking" and self.sprint_meter < 2_000:
             self.vx *= 0.8
             self.vy *= 0.8
        if self.state_moving == "walking" and self.sprint_meter < 3_000:
             self.vx *= 0.9
             self.vy *= 0.9    
        # [ todo! ] - if you are walking you should still gain some fatigue meter / lose sprint meter 
        # [ todo! ] - yeah actual call fatigue meter for now but anyway, walking still lose a lil bit 
        # [ todo! ] - as we wanna show this too, and note other actions like building should cost fatigue 
        # [ todo! ] - and have the shit just regen slowly, but leaving all this for now tbf :D 
        
        # [ consider! ] - if sprinting into a wall disable sprint, shouldnt be taxing you, & u shouldnt be in a sprint state

    # [ note! ] - really need to figure out ramping 

    def get_sprint_multiplier(self) -> int:
        # should probably refector into get player speed but its fine for now
        # default player speed is 400, x1
        # once have ranges, hardcode the values and the increment differences for hella easy updates
        # if over 30% full sprint meter, there is no impact on your sprint speed, ur quick af boii
        if self.sprint_meter > 3_000: 
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
            return(1.15) # hastened
        else:
            # for now, if ur not spent, but not over 30% then still quick but not sprint, its like a jog
            return(1.25) # quick

    def collide_with_walls(self, dir):
        # if checking an x collision
        if dir == "x":
            # then check if we the player have collied with a wall
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                # if i have hit something, check which side is it left or right using our velocity (which direction and where are we moving to)
                # if we were moving to the right when we collided with the wall, so put ourselves on that side of the wall
                if self.vx > 0:
                    # our x should be what ever it was that we hit(s) minus however wide we are
                    self.x = hits[0].rect.left - self.rect.width
                # if the speed is the opposite direction then we were moving to the left so
                if self.vx < 0:
                    # put ourselves to the right of the thing we hit(s)[0]
                    self.x = hits[0].rect.right
                # regardless of where we hit we are going to stop ourselves moving on this axis (x), because we've hit a wall to either side of us
                self.vx = 0
                self.rect.x = self.x
        
        if dir == "y":
            uhits = pg.sprite.spritecollide(self, self.game.unlockwalls, False)
            # unlock walls
            if uhits:
                # print(f"Collided Wall Hp : {bhits[0].get_hp()}")
                if not uhits[0].is_locked:
                    # bhits[0].try_repair_wall()
                    pass # through freely
                else:
                    if self.vy > 0:
                        self.y = uhits[0].rect.top - self.rect.height
                    if self.vy < 0:
                        self.y = uhits[0].rect.bottom
                    self.vy = 0
                    self.rect.y = self.y             
                    

            bhits = pg.sprite.spritecollide(self, self.game.breakablewalls, False)
            # breakable wall
            if bhits:
                # print(f"Collided Wall Hp : {bhits[0].get_hp()}")
                if bhits[0].get_hp() <= 0:
                    # bhits[0].try_repair_wall()
                    pass # through freely
                else:
                    if self.vy > 0:
                        self.y = bhits[0].rect.top - self.rect.height
                    if self.vy < 0:
                        self.y = bhits[0].rect.bottom
                    self.vy = 0
                    self.rect.y = self.y             
                    
            # normal wall    
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y             

    # [ todo ]
    def colour_sprite(self):
        # new function handle state, set our colour to red if were fatigued
        if self.state_state == "fatigued":
            self.image.fill(RED)
        elif self.state_state == "struggling":
            self.image.fill(ORANGE)
        elif self.state_state == "tiring":
            self.image.fill(YELLOW)    
        else:
            self.image.fill(WHITE)           

    def update(self):
        self.get_keys()
        # [ todo-asap! ] - new function
        # need sumnt like set state, unsure if best after or before keys but assumed after for obvs reasons
        # again forget actual ranges for now but if we are under 30% we are fatigued
        if self.sprint_meter < 1_000:
            self.state_state = "fatigued"
        elif self.sprint_meter < 2_000:
            # note yeah ranges and stuff still defo off af but the functionality is actually pretty good tbf i like it
            self.state_state = "struggling"            
        elif self.sprint_meter < 3_000:
            self.state_state = "tiring"     
        elif self.sprint_meter > 3_000:
            self.state_state = "fresh"
        # log our state and sprint meter
        # print(f"{(self.sprint_meter):.1f}% - {self.state_moving = }, {self.state_state = }, {self.vx = }")
        self.colour_sprite()
        # update the position of the player based on keys pressed using speed multiplied by time, dt = the current timestamp of the game, so we move at a consistent speed independent of our framerate 
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # set our rectangles x & y to the speed/post to check for collisions 
        self.rect.x = self.x
        self.collide_with_walls('x')
        # basically were doing 2 collision check, 1 for each axis
        self.rect.y = self.y
        self.collide_with_walls('y')
        # new test
        if self.waiting:
            space_end = pg.time.get_ticks() 
            if space_end - self.waiting >= 2000:
                print("Buying Reactivated")
                self.waiting = False
        


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
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.hp_current = hp
        self.hp_max = 4
        self.build_bar = 0
        self.player = player
        self.update_colour()
        # if the class variable wall_ids is not an empty list 
        if BreakableWall.wall_ids:
            # then add the most recent id + 1 
            BreakableWall.wall_ids.append(BreakableWall.wall_ids[-1] + 1) 
        # else if there is no ids in the wall_ids
        else:
            BreakableWall.wall_ids.append(1)
        self.myid = self.wall_ids[-1]
        print(f"Breakable Wall '{self.myid}' was born", x, y, f"{self.hp_current = }", self)

    # is broken, i.e. is 0 hp is what i want now
    def get_hp(self):
        return(self.hp_current)

    def try_repair_wall(self):
        # keys = pg.key.get_pressed()
        # if were pressing left on the keyboard or a
        # if keys[pg.K_q]:
        #     self.build_bar -= 1
        # if keys[pg.K_e]:
        self.build_bar += 1
        if self.hp_current < self.hp_max:
            if self.build_bar == 30:
                self.hp_current += 1
                self.build_bar = 0
        # print(f"Ouch {self.build_bar = }, {self.hp_current = }")
        self.update_colour()
    
    def update_colour(self):
        """ every time something interacts with me, run this (?) """
        if self.hp_current == 0:
            self.image.fill(BLACK)
        elif self.hp_current == 1:
            self.image.fill(MAGENTA)
        elif self.hp_current == 2:
            self.image.fill(GREY)
        elif self.hp_current == 3:
            self.image.fill(BLUEGREEN) # BLUEGREEN    
        elif self.hp_current == 4:
            self.image.fill(GREEN) # BLUEGREEN  

    def is_near(self, player_x, player_y):
        dist = pg.math.Vector2(self.x*TILESIZE, self.y*TILESIZE).distance_to((player_x, player_y))  
        # print(f"{dist = }")
        # print(f"{self.x*TILESIZE = }, {self.y*TILESIZE = }, {player_x = }, {player_y = }")
        return True if dist < 30 else False

    def update(self):
        # if we (this iinstance of breakable wall) are near the player
        if self.is_near(self.player.x, self.player.y):  
            # debug log the walls id          
            # print(f"Player is near Breakable Wall [ {self.myid} ] {self.hp_current = }")
            # if the wall can be rebuilt more still
            if self.hp_current < 4:
                # and the player isn't interacting with anything
                # currently only the 'e' aka 'build' key but will be others for sure, sprint too surely duhhh!
                if self.player.is_interacting == False:
                    self.image.fill(NAVYBLUE)
        else:
            self.update_colour()

    # [ todo-asap! ] - wall max hp broken again
    # [ todo-asap! ] - then continue tuts pls!
                    





























class UnlockWall(pg.sprite.Sprite): # should be called barricades huh
    unlock_wall_objects = []
        
    def __init__(self, game, x, y, player, is_wide=True):
        self.groups = game.all_sprites, game.unlockwalls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        want_more_cube = 2 if is_wide else 1
        self.image = pg.Surface((TILESIZE*want_more_cube, TILESIZE))
        self.image.fill(RUST)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * (TILESIZE) # see this is where we could just make it a long boi tbf
        self.rect.y = y * TILESIZE
        self.unlock_cost = 100 # need a programmatice or dynamic way to implement this
        self.player = player
        self.is_locked = True
        # append this object to this list for deleting as pairs
        UnlockWall.unlock_wall_objects.append(self)
        self.id = len(self.unlock_wall_objects)
        print(f"Unlock Wall '{self.id}' was born", x, y, f"{self.player.player_gold = }", f"{self.unlock_cost = }", f"{self.unlock_wall_objects}")

    def check_is_buyable(self):
        if self.player.player_gold >= self.unlock_cost:
            return True
        else:
            return False

    def update_colour(self):
        """ needs to be run after relevant updates """
        if not self.is_locked:
            self.image.fill(BLACK)
        elif self.check_is_buyable():
            self.image.fill(YELLOW)
        else:
            self.image.fill(COFFEE)

    def is_near(self, player_x, player_y):
        dist = pg.math.Vector2(self.x*TILESIZE, self.y*TILESIZE).distance_to((player_x, player_y))  
        print(f"{self.id = }, {self.x*TILESIZE = }, {self.y*TILESIZE = },{dist = }, {player_x = }, {player_y = }")
        print(f"{self.id =} near af boiiii") if dist < 30 else 0 
        return True if dist < 30 else False
            
    def update(self):
        # if we (this iinstance of breakable wall) are near the player
        if self.is_near(self.player.x, self.player.y):
            self.update_colour()
        else:
            if self.is_locked:
                self.image.fill(RUST)
            else:
                self.image.fill(BLACK)

    def unlock(self):
        # if you can buy (you've already pressed the button btw)      
        if not self.player.waiting:
            if self.check_is_buyable():
                # take the gold, and unlock the wall, start the timer so this can only happen one every x seconds
                self.player.player_gold = self.player.player_gold - self.unlock_cost
                self.is_locked = False 
                self.player.waiting = pg.time.get_ticks() 
                print("Buying Disabled For 2 Seconds")


        # OK SO COMPLETELY SCRAP THIS WAY AND DO THE 2 WIDEWAY
        # AND ITS JUST U CAN OR CANT PASS THRU FOR GET DELETE

        # then just try if press whatever key delete and delete the one of same group from the list
        # #(probably just a smart pop -X would work idk tho?)
        # and obvs then do the passing through walls
        # then this is actually done yanno nice

        # sometimes the unlock isnt working but im cool with it for now really like it apart from that tbf lol
        # minor thing tho as just got working anyway so big bosh!
        # to fix more strictness with the group

        # WHEN COME BACK THO ONLY DO THE 2 WIDTH THING, ONLY THAT RN!
        # then cont to sumnt else
        # i think maybe a map, base gold, and then basic implementation for breaking down 1 object and building another (which dies after x time?)


