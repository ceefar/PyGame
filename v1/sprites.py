import pstats
from re import X
import pygame as pg
from settings import *
from tilemap import collide_hit_rect
# start using vectors instead of individual xypos vars
vec = pg.math.Vector2
# for calculating distance between 2 objects and ceiling (and floor) div
from math import hypot, ceil
# for random numbers, uniform is real numbers between given range
from random import randint, uniform

def return_font_size(font="silk", weight="regular", size=32):
    if font == "silk":
        if weight == "regular":
            return pg.font.Font("Silkscreen-Regular.ttf", size)
    

# make wall collisions func global as is useful for more stuff now
# should also do the same with get dinstance tbf lol
# need to refactor this so it actually works just with group lol
def collide_with_walls(sprite, group=False, dir=False, collision_type="standard"): # making group False as we dont need to pass it for bwalls, again tho pls just refactor, as like dir had to be False due to the default before it and now its just a silly mess lmao
    # if checking an x collision, note were using a custom hitbox hit_rect now
    if dir == "x":
        # simple switch for wall/collision type as all have slightly different conditions, this could be further refactored and improved but just rushing out a working version for now
        if collision_type == "standard":
            # then check if we the player have collied with a wall
            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect) # so big note btw, we are passing in the group if using standard so u can use that for other stuff in future - this is why i mean could easily refactor more, as for bwalls we dont actually need the group
            if hits:
                # check if the walls center is greater than the players center
                # if the players center is greater than the walls center 
                # im on the right hand side of the wall
                if hits[0].rect.centerx > sprite.hit_rect.centerx: 
                    # our x should be what ever it was that we hit(s) minus however wide we are
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
                # else if its less than its to the left
                if hits[0].rect.centerx < sprite.hit_rect.centerx:
                    # put ourselves to the right of the thing we hit(s)[0]
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
                # regardless of where we hit we are going to stop ourselves moving on this axis (x), because we've hit a wall to either side of us
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x   
        if collision_type == "breakable":              
            bhits = pg.sprite.spritecollide(sprite, sprite.game.breakablewalls, False, collide_hit_rect)
            if bhits:
                # if i have hit something, check which side is it left or right using our velocity (which direction and where are we moving to)
                # if we were moving to the right when we collided with the wall, so put ourselves on that side of the wall
                if bhits[0].get_hp() <= 0:
                    # bhits[0].try_repair_wall()
                    pass # through freely                
                else:
                    if bhits[0].rect.centerx > sprite.hit_rect.centerx:
                        # our x should be what ever it was that we hit(s) minus however wide we are
                        sprite.pos.x = bhits[0].rect.left - sprite.hit_rect.width / 2
                    # if the speed is the opposite direction then we were moving to the left so
                    if bhits[0].rect.centerx < sprite.hit_rect.centerx:
                        # put ourselves to the right of the thing we hit(s)[0]
                        sprite.pos.x = bhits[0].rect.right + sprite.hit_rect.width / 2
                    # regardless of where we hit we are going to stop ourselves moving on this axis (x), because we've hit a wall to either side of us
                    sprite.vel.x = 0
                    sprite.hit_rect.centerx = sprite.pos.x    
    if dir == "y":
        if collision_type == "breakable":
            bhits = pg.sprite.spritecollide(sprite, sprite.game.breakablewalls, False, collide_hit_rect)
            # breakable wall
            if bhits:
                # print(f"Collided Wall Hp : {bhits[0].get_hp()}")
                if bhits[0].get_hp() <= 0:
                    # bhits[0].try_repair_wall()
                    pass # through freely
                else:
                    if bhits[0].rect.centery > sprite.hit_rect.centery:
                        sprite.pos.y = bhits[0].rect.top - sprite.hit_rect.height / 2
                    if bhits[0].rect.centery < sprite.hit_rect.centery:
                        sprite.pos.y = bhits[0].rect.bottom + sprite.hit_rect.height / 2
                    sprite.vel.y = 0
                    sprite.hit_rect.centery = sprite.pos.y             
        if collision_type == "standard": # normal wall  
            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if hits:
                if hits[0].rect.centery > sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
                if hits[0].rect.centery < sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y  

def get_distance(self, x, y, want_distance=True, want_int=False, next_to=15): 
        """ use hypotenus of the xy vectors to find out how close we are to the given vector pos, note is for 64 tilesize """
        pythag_dist = hypot(self.pos.x-x, self.pos.y-y)
        # by default return the actually distance (as a float btw)
        if want_distance:
            return int(pythag_dist) if want_int else pythag_dist # if want returned as int
        # else if want_distance is false, will return true or false if is within the given next_to distance (defaults to 15, which is v small btw)
        else:
            return True if pythag_dist < next_to else False

# ---- COMPANION NOTES ----
# - if you then add the timer version you can use the new look at to have it update all if not looking at zombie, else every other frame

# ---- COMPANION TOD0 ----
# - add basic stateness text thing like the zombies but based on looking at for now

class Companion(pg.sprite.Sprite): # herecompanion new af test - for soliders / units
    def __init__(self, game, x, y):
        # standard basic setup
        self.groups = game.all_sprites, game.companions
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.my_turret_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        # new - moved over, for collisions
        self.hit_rect = COMPANION_HIT_RECT.copy() # NEED TO DO THIS COMPANION DIFFERENTLY! they all need their own unique hit rect so copy is needed
        self.hit_rect.center = self.rect.center
        # rotation
        self.rot = self.game.player.rot # starts looking at the player
        # give the companion movement
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        # make me a constant when done - temporary var for now
        self.companion_move_speed = 85 # zombies 80, player 320, 200 is 120 off each
        # -- custom stuff --
        # for checking and potential stateness too ig
        self.is_looking_at = "bff"
        # closest zombie
        self.closest_zombie_pos = (0,0) # starts looking at the player awww
        self.closest_zombie = 0 # will be an object
        self.closest_zombie_timer = 0
        # companion sight 
        self.companion_sight_range = 500 # 300 temporary start value changed to 1000 for debuging, make me a constant when done but still playing with it so is fine for now
        # test concept - for being tethered to a position
        self.move_here_distance = 1000
        # shooting
        self.last_shot = 0
        self.clip_counter = 0
        self.bullet_damage = 5
        # need to do this properly with weapons remember, see player class - note cards/items too coming shortly too
        self.companion_fire_rate = 900
        # health
        self.hp_max = 2000
        self.hp_current = self.hp_max
        # very very super temp for testing knockback zombies on companion
        self.companion_level = 2
        # temp test for chit chat
        self.companion_chit_chat_counter = 0

    def update(self): # herecompanionupdate - updates every frame
        # -- look at, every frame (likely needs refactor as assumed expensive) --
        self.update_companion_look_at() # looking at where player looks (or player if you want) if no zombies in sight range, else look at closest zombie
        # -- use updated rotation to update the image, rect, and center rect  --
        self.image = pg.transform.rotate(self.game.my_turret_img, self.rot) # rotate the image 
        self.rect = self.image.get_rect() # update rect to be at this position 
        #self.rect.center = self.pos # make sure we update our center rect also
        # -- for moving to a position --
        if self.is_looking_at == "zombie":
            # so we are basically just checking to see if we are in a range of the closest zombie too us, if that range is XYZ or further we dont move else we move (tethered)
            if self.move_here_distance > 250: # if you are move than 250 units away from where you are currently looking, move there (200 feels a biiit too close)
                # -- update where we are, first do acceleration based on rotation, so we are moving in the direction we are looking --
                self.acc = vec(self.companion_move_speed, 0).rotate(-self.rot) # accelerate in the right direction
                self.acc += self.vel * -1
                self.vel += self.acc * self.game.dt
                self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
                self.rect.center = self.pos
            elif self.move_here_distance < 100: # if the zombie is less than 100 units from the companion, it will move away from where it looking
                # -- update where we are, first do acceleration based on rotation, so we are moving in the direction we are looking --
                self.acc = vec(self.companion_move_speed, 0).rotate(-self.rot) # accelerate in the right direction
                self.acc += self.vel * -1
                self.vel += self.acc * self.game.dt
                self.pos -= self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2 # -= so in the opposite direction as the closest zombie is now too close
                self.rect.center = self.pos
                #################################################################
                # will likely need sumnt like if surrounded btw else may crash? #
                #################################################################   
            # -- shoot --
            self.fire_shot() # if ur looking at a zombie always shoot regardless of the rangle           
        # else if looking at the player
        elif self.is_looking_at == "bff":
            # instead of checking our distance to the zombie check our distance to the player
            self.move_here_distance = self.get_distance(self.game.player.pos.x, self.game.player.pos.y) 
            if self.move_here_distance > 300: # if you are move than 300 units away from where you are currently looking, move there
                # -- update where we are, first do acceleration based on rotation, so we are moving in the direction we are looking --
                self.acc = vec(self.companion_move_speed, 0).rotate(-self.rot) # accelerate in the right direction
                self.acc += self.vel * -1
                self.vel += self.acc * self.game.dt
                self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
                self.rect.center = self.pos
        # -- wall collision  --
        # take that rectangle at set it to where our previous rectangle was at
        self.rect.center = self.pos
        # use our rectangles x & y to the speed/pos to check for collisions 
        self.hit_rect.centerx = self.pos.x
        # now we know where the sprite should be set its rect center
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(sprite=self, group=self.game.walls, dir="x")
        collide_with_walls(sprite=self, dir="x", collision_type="breakable")
        collide_with_walls(sprite=self, group=self.game.paywalls, dir="x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(sprite=self, group=self.game.walls, dir="y")
        collide_with_walls(sprite=self, dir="y", collision_type="breakable")
        collide_with_walls(sprite=self, group=self.game.paywalls, dir="y")
        # then set our regular rect to our hit rect, remember we primarily use the hit rect then set it to the regular rect at the end (the visual doesnt match the pixel precision)
        self.rect.center = self.hit_rect.center  
        # ---- temp test for collision issue ----
        # if i hit a y wall so i have zero velocity in y direction, dont let me move back so the collision doesnt fuck itself
        # - do this in collide walls with new collision_type
        # -- then finally --
        if self.hp_current <= 0: # if less than or equal to dead, kill me
            print(f"OOF! Press F for Companion")
            self.kill()

    def draw_status(self, status="D:", color=BLUEMIDNIGHT, small=False):        
        # then before we draw the name rotate it to where we want it to be, since we're doing it with blit in relation to the camera
        if small:
            self.name_textsurface = return_font_size(size=16).render(f"{status}", True, color) # (f"{self.myname} {self.health}", True, BLACK)  # "text", antialias, color
        else:
            self.name_textsurface = return_font_size().render(f"{status}", True, color) # (f"{self.myname} {self.health}", True, BLACK)  # "text", antialias, color
        # e.g. this will rotate to face the player => pg.transform.rotate(textsurface, self.game.player.rot)
        #if self.rot > -135 and self.rot < -45: # only do our rotation at certain angles based on the zombie
        self.name_textsurface = pg.transform.rotate(self.name_textsurface, self.rot + 90) # if at this angle rotate my name
        return self.name_textsurface 

    def draw_health(self):
        # if self.hp_max >= self.hp_current: # simple hp bar
        #     col = GREEN
        # elif self.hp_max >= self.hp_current: # greater than 30%
        #     col = YELLOW
        # else: # else is 30% or less
        col = RED        
        width = int(self.rect.width * self.hp_max / self.hp_current) # width of bar is just the width of this zombies rect time the percent of hp remaining  
        print(f"DEBUG!: {width = } {self.rect.width = } {self.hp_max = } {self.hp_current = }")     
        self.health_bar = pg.Rect(0, 0, width, 7)  # the location on the sprite image not on the screen, 7 is thickness        
        pg.draw.rect(self.game.screen, col, self.health_bar) # draw that self.health_bar on top of our zombies rectangle in the given colour        

    def companion_chit_chat(self):
        # shouldnt happen when D: i.e. when companion is looking at a zombie (and low hp)
        if self.companion_chit_chat_counter == 0:
            self.companion_chit_chat_counter = pg.time.get_ticks()
        check_timer = pg.time.get_ticks()
        true_timer = check_timer - self.companion_chit_chat_counter
        if true_timer > 0 and true_timer < 1500:
            return(self.draw_status("This place...", BLACK, True))
        elif true_timer >= 1_500 and true_timer < 4_000:
            return(self.draw_status("it creeps me out", BLACK, True))
        elif true_timer >= 4_000 and true_timer < 7_000:
            return(self.draw_status("bro... seriously!", BLACK, True))
        elif true_timer >= 7_000 and true_timer < 9_000:
            return(self.draw_status("urghhh", BLACK, True))
        elif true_timer >= 9_000 and true_timer < 11_000:
            return(self.draw_status("fuck this man!", BLACK, True))
        else:
            return(self.draw_status("i hate it here", BLACK, True))

    def companion_chit_chat_end_level(self, perc):
        # shouldnt happen when D: i.e. when companion is looking at a zombie (and low hp)
        perc = perc * 100
        if perc < 50:
            return(self.draw_status("I wanna go home", BLACK, True))      
        else:      
            return(self.draw_status("...Pfff, too easy", BLACK, True))   

    # -- for shooting --
    def fire_shot(self):
        now = pg.time.get_ticks() # track the last time we shot 
        # need to add bullet rate stuff here based on weapons for companion too now
        # - these (the wepaons) should defo be classes
        # - just make for the player
        # - then the companions can just be like 20% or 50% of what the player does bosh
        if now - self.last_shot > self.companion_fire_rate: # if now - self.last_shot > self.return_bullet_rate():
            self.last_shot = now 
            dir = vec(1,0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot) # rotated to match the players direction
            Bullet(self.game, pos, dir, "companion")
            self.clip_counter += 1 # add one to the clip counter which tracks which bullet in the clip we have just fired
            # self.vel = vec(-20,0).rotate(-self.rot)        

        # print(f"COMPANION: is looking at {self.is_looking_at}, DEBUG: move_here_dist = {self.move_here_distance}")

        # heretodo # herenotes
        # what are we actually doing tho, doing that to a point near the player - will be easy enough dw
        # - so we want to...
        #   [DONE] be tethered to the zombies 
        #   [DONE] or be tethered to the player
        #   [DONE] be able to shoot
        #   [DONE] also see if you can easily change the companions size
        #   [DONE] companion collide with walls
        #   [DONE] make zombies go for companion too
        #   [DONE] test companion level 2 knockback
        #   [DONE] basic concept of companion chit chat
        #
        #   - DO. gamble ui > [NEED EVENT TUT!]
        #   - DO. dropping gold
        #           - could try and find a quick tut for it tho actually
        #           - tho do think this probably requires tiled tbf
        #           - for hacky approach when one dies just print a random coin to the map in camera range bosh
        #   - DO. zombie spawn >>> [NEW TUT!]
        #           - try dis quickly anyways, bug if long move on 100
        #   - FIX. the problem with the clout bonus wallet thing is that it just dies if you should have won it but all the zombies are dead
        #           - should be an easy enough fix tbf
        #   - DO. companion respawn (idk how yet), and upgrading
        #   - DO. items / cards
        #   - DO. weapons
        #   - DO. game levels
        #   - DO. levelling up and menus
        #   - DO. tiled
        #   - DO. companion improvements
        #           - improve and have hit scream out help (idea being ur the general their rookies, they're scared bitches dont lose them - can make this more of the game in future, like state = scared, fleeing, running, routing, etc)
        #           - if hes offscreen bigger warning and arrow based on the colour of his hp bar
        #
        #   tomo 
        #   - PERSONAL. various see phone, jobs
        #   - DO. change companion bullet size, but no rush tho skip this for now 
        #   - DO. make companion turn abit if hes being chased! <<<<<<<<<<<<<<<<<<< DIS
        #   - FIX. if the zombie loses sight of me its roaming, that shouldnt happen it is locked on the companion
        #   - FIX. zombies changing between companion and player needs work 
        #   - THEN. i reckon just levels, items, random roll, etc (see phone)
        #       - but consider below too
        #
        #   CONSIDER 
        #   - MAYBE DO. be tethered to a point near the player, on button press (ideally the player circle tho a pos, i.e. in front, would be fine for now)
        #   - MAYBE DO. then maybe call to "form up", or maybe automatically do that if a zombie dies and ur not in range
        # - ahhhhh looking_at is guna be huge here btw, nice if it is
        # - once that stuff is done really should try to get to item stuff asap
        # - really love the idea of like scared and fearless companion states btw, to do this easily could be about say its hp and zombies near it or sumnt
        

        # please have them talk to each other in bff mode if they're idleing
        # - if player not moving
        # - and companion is looking at player
        # - have_a_chat()
        # - where they just pass status style messages back and forth 
        # - hehehe so cute 
        # - this will basically trigger at the start too so have a sliiiight delay?

        # also please give the companion a status too

        # with the staggered update thing so its not instant?
        # and also consider what to do in the initial state when is looking where the player is, maybe move with them? or just dont move (for now anyways)
        # then to improve
        # nice quick and easy way would be to
        # only move when companion is looking at zombie
        # and only move if the zombie is x range away, that will tether them to the nearest zombie (which may have some strange effects)
        # but what i actually want is for them to be tethered to the player
        # in a circle around the player
        # where they then move in that ring based on the position of the closest zombie bosh
        # - probably should have that they focus a zombie until it dies (updating this first now dw)

    def update_companion_look_at(self):
        """ functionality : companion will look at where the player is looking until it sees a zombie within its companion_sight_range """
        if self.game.mobs: # if all the zombies are dead dont do this, else do it
            # get closest zombie and its position, note - probably should improve on my version still but is fine for now tbf
            self.closest_zombie, closest_zombie_distance = self.get_closest_zombie(want_instance=True) # also returns the actual distance in a tuple
            self.closest_zombie_pos = self.closest_zombie.pos
            # if the closest zombie is within ur sight range look at it, else look at the player
            if self.companion_sight_range >= closest_zombie_distance:
                self.move_here_distance = self.get_distance(self.closest_zombie_pos.x, self.closest_zombie_pos.y) # print(f"COMPANION: is {self.move_here_distance} meters away from tracking position")
                self.rot = (self.closest_zombie_pos - self.pos).angle_to(vec(1, 0)) # look at player, like zombies do
                self.is_looking_at = "zombie" # set new looking at var
            elif closest_zombie_distance - self.companion_sight_range > 1000: # if the closest zombie is far away, look at ur bff the player
                self.is_looking_at = "bff"
                self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0)) # look at player, like zombies do
            else:
                # else here changed from look where player is, to look at the player for now (its just temp)
                # tho ig what you want is when hes at the player (based on distance)
                # to be looking at where the player is
                # this would be a basic form up mechanic
                self.is_looking_at = "bff"
                self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0)) # look at player, like zombies do
            # elif self.companion_sight_range < closest_zombie_distance: # else look at where player is
            #     self.rot = self.game.player.rot # look at where actual player is looking, you have the same rotation as the player
            #     self.is_looking_at = "with_player" # set new looking at var
        else: # else, if there are no mobs left alive, look at ur bff the player, ig only should happen if all dead, may be some other edge cases tho idk yet so leaving for now
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0)) # look at player, like zombies do
            self.is_looking_at = "with_player"
        
    def get_closest_zombie(self, want_instance=False, want_pos=True):
        zombie_distances = {} # distance key as int, mob object as value
        smallest_distance = 5000
        closest_zombie_instance = 0 # will be an object
        for zombie in self.game.mobs:
            distance_away = (self.get_distance(zombie.pos.x, zombie.pos.y, want_distance=True))
            zombie_distances[distance_away] = zombie
        for distance, zombie in zombie_distances.items():
            if distance < smallest_distance:
                smallest_distance = distance
                closest_zombie_instance = zombie
        distance_away = (self.get_distance(closest_zombie_instance.pos.x, closest_zombie_instance.pos.y, want_distance=True)) # write over this at loop end to get the return instances actual distance
        if want_instance:
            return(closest_zombie_instance, distance_away)
        elif want_pos:
            return(closest_zombie_instance.pos, distance_away)

    def get_distance(self, x, y, want_distance=True, want_int=False, next_to=15): 
        """ use hypotenus of the xy vectors to find out how close we are to the given vector pos, note is for 64 tilesize """
        pythag_dist = hypot(self.pos.x-x, self.pos.y-y)
        # by default return the actually distance (as a float btw)
        if want_distance:
            return int(pythag_dist) if want_int else pythag_dist # if want returned as int
        # else if want_distance is false, will return true or false if is within the given next_to distance (defaults to 15, which is v small btw)
        else:
            return True if pythag_dist < next_to else False



    #############################################################
    # GOOD OLD UPDATE WITH TIMER BUT JUST CBA TO COMPLETE IT RN #
    #############################################################
    # def update(self):
    #     # -- look at, on timer --
    #     if self.closest_zombie_timer: # if it is running
    #         closest_check_timer = pg.time.get_ticks() # start a check timer 
    #         if closest_check_timer - self.closest_zombie_timer > 35: # do this alot but just not every frame, 1000 / 60 (@ 60fps) is approx 16
    #             self.closest_zombie_timer = 0 # reset the main timer 
    #             closest_check_timer = 0 # (and the check timer ?)
    #             self.update_companion_look_at() # set the look at
    #             # very very very temp
    #             self.companion_update_closest_zombie_checks_counter += 1
    #             print(f"Check for closest zombie: [ {self.companion_update_closest_zombie_checks_counter} ]")
    #     else: # if the timer is not running, start it    
    #         self.closest_zombie_timer = pg.time.get_ticks()
    #     # -- look at, for initial first set  --
    #     if not self.closest_zombie: # if the timer means we cant run look at, but we havent run it yet (so we have no target), then run it one time 
    #         self.update_companion_look_at() # looking at where player looks (or player if you want) if no zombies in sight range, else look at closest zombie
    #     # -- update the image --
    #     self.image = pg.transform.rotate(self.game.my_turret_img, self.rot)
    #     self.rect = self.image.get_rect()
    #     self.rect.center = self.pos


    # def __init__(self, game, x, y): #  hp = 0
    #     self.groups = game.all_sprites, game.companions
    #     pg.sprite.Sprite.__init__(self, self.groups)
    #     self.game = game
    #     self.image = game.my_turret_img
    #     self.rect = self.image.get_rect()
    #     self.x = x
    #     self.y = y
    #     self.rect.x = x * TILESIZE
    #     self.rect.y = y * TILESIZE
    #     self.pos = vec(x, y) * TILESIZE
    #     self.rect.center = self.pos
    #     self.rot = 0
    #     self.vel = vec(1,1)
    #     self.acc = vec(0,0) 
    #     # # in testing
        # self.closest_zombie = 0 # will be an object
        # self.closest_zombie_timer = 0

    # def find_closest_zombie(self): # only do every second
    #     # player probably has this btw
    #     zombie_distances = {} # distance key as int, mob object as value
    #     smallest_distance = 5000
    #     for zombie in self.game.mobs:
    #         distance_away = (self.is_near(zombie.pos.x, zombie.pos.y, return_distance=True))
    #         zombie_distances[distance_away] = zombie
    #     for distance, zombie in zombie_distances.items():
    #         if distance < smallest_distance:
    #             smallest_distance = distance
    #             self.closest_zombie = zombie 

    # def update(self):
    #     self.find_closest_zombie()
    #     self.look_at(self.closest_zombie.pos)
    #     self.rot = (self.rot + self.game.player.rot_speed * self.game.dt) % 360 
    #     self.image = pg.transform.rotate(self.game.my_turret_img, self.rot)

    # def look_at(self, look_at_me):        
    #     self.rot = (look_at_me - self.pos).angle_to(vec(1,0))
    #     self.image = pg.transform.rotate(self.game.my_turret_img, self.rot)

    # def is_near(self, x, y, next_to=15, return_distance=False): # use hypotenus of the xy vectors to find out how close we are to the given vector pos, note is for 64 tilesize
    #     pythag_dist = hypot(self.pos.x-x, self.pos.y-y)
    #     if return_distance:
    #         return pythag_dist
    #     else:
    #         return True if pythag_dist < next_to else False

    # get moving near you
    # - guna need to go thru old mob tut again me thin
    # get working on button press
    # get shooting
    # get colliding and being hit and hp
    # get proper moving 
    
    # then either 
    # levels 
    # or 
    # random roll
    # or
    # units menu (init menu tho - meh could be end of level tbf so do that - note both are defo different)
 


class Player(pg.sprite.Sprite): #hereplayer
    weapon_list = ["uzi", "pistol"]

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img # pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT # define new hitbox separate to our dynamic due to rotation self.rect
        self.hit_rect.center = self.rect.center # make sure the center of our hitbox rect is the same as our actual center
        # new - velocity vector, for speeding up and slowing down the player
        self.vel = vec(0, 0)
        # new - need position vector now too
        self.pos = vec(x, y) * TILESIZE
        # new - rotation, starting rot=0 is pointing right so in positive x position/axis
        self.rot = 0
        self.last_shot = 0
        # new - player health
        self.health = PLAYER_HEALTH

        # new sprint meter test
        self.sprint_meter = 6_000
        # new implementation is a dictionary storing the info on all states
        # using generic `state` for now until good reason to section out more 
        self.state_moving = "chilling"
        self.state_state = "fresh"
        # new test
        self.is_interacting = False
        # new player gold implementation, could be a class var if ur lazy
        # [ FOR GOLD ] 
        self.player_gold = 0
        self.player_prizemoney = 0 # some kinda idea of banking gold after a set amount of levels, maybe the amount banked also provides bonuses like bonus exp, extra unlocks (for hoarding and not spending etc)
        # note defo have more things that make u get paid for hampering urself
        # maybe even presenting as option at level start
        # new test, pause interactions
        self.waiting_print = False
        self.waiting = False
        # new auto-shooting toggle test
        self.autoshoot = False
        self.toggle_wait = False

        # new player damage stuff, actually altering og code quite substantially for this but will be fine
        self.player_damage = BULLET_DAMAGE

        # new custom clout rating test stuff
        self.clout_rating_base_timer = False # this should *now* be the 5 second timer btw
        self.clout_level = 1 # base level 1- 50 for now me thinks
        # self.clout_cooldown_timer = False # this is the timer that start on kill
        self.sub_clout_time = 0 # also activates on kill, i think this is what ur using to handle the actual temporary score that may or may not be achieved, as so will be the display var

        # new custom dash test stuff
        self.dash_cooldown = False

        # new gun clip
        self.clip_counter = 0
        self.is_reloading = False

        # new player weapon stuff
        self.current_weapon_id = 1
        self.current_weapon = Player.weapon_list[0] # remember may be based on other stuff at the start of level, for sure as classes, i geddit

        # new test player stats stuff
        self.current_accuracy = [0,0] # amount hit, amount missed, then just add them both if u want totals 

        # new for actual levelling, like classic level ups, in game level tho, not like character (overall? / evolution / << similar) level which should persist outside the in game levels (do that soon tho)
        self.character_level = 1

    def set_player_weapon_id(self):
        # if the current weapon id isn't the list len (allow zeros btw)
        if self.current_weapon_id >= len(Player.weapon_list):
            self.current_weapon_id = 1 # loop to start
        else:
            self.current_weapon_id += 1 # go to next

    def return_clip_size(self):
        if self.current_weapon == "uzi":
            return(UZI_CLIP_SIZE)
        if self.current_weapon == "pistol":
            return(PISTOL_CLIP_SIZE)

    def return_bullet_rate(self): # just bullet rate for now
        if self.current_weapon == "pistol":
            return PISTOL_BULLET_RATE
        elif self.current_weapon == "uzi":
            return UZI_BULLET_RATE

    def return_gun_kickback(self): # sep funcs for now
        if self.current_weapon == "pistol":
            return PISTOL_KICKBACK
        elif self.current_weapon == "uzi":
            return UZI_KICKBACK

    def return_gun_reload_speed(self):
        if self.current_weapon == "pistol":
            return PISTOL_RELOAD_SPEED
        elif self.current_weapon == "uzi":
            return UZI_RELOAD_SPEED         

    def return_gun_crit_chance(self):
        if self.current_weapon == "pistol":
            return PISTOL_CRIT_RATE
        elif self.current_weapon == "uzi":
            return UZI_CRIT_RATE            

    def return_gun_spread(self):
        if self.current_weapon == "pistol":
            return PISTOL_SPREAD
        elif self.current_weapon == "uzi":
            return UZI_SPREAD

    def get_display_clout_level(self): # rudimentary for now but is fine just leave how it is, will be doing the average over time thing here shortly...
        # simple af test func to convert the clout rating in to its appropriate string value
        clout_ratings = {1:"U",2:"F",3:"E-",4:"E",5:"E+",6:"D-",7:"D",8:"D+",9:"C-",10:"C",11:"C+",12:"B-",13:"B",14:"B+",15:"A-",16:"A",17:"A+",18:"A++",19:"A+++",20:"A*"}
        closest = min(clout_ratings.keys(), key=lambda x: abs(x - self.clout_level))
        return(clout_ratings[closest])    

    def get_keys(self): # herekeys #hereplayerkeys
        self.rot_speed = 0 # normally will be zero, works the same as velocity, hold it down one way increases that way
        self.vel = vec(0, 0) # define what our keys are going to do
        keys = pg.key.get_pressed() # see which keys are currently held down
        # -------- dev keys stuff - might integrate tho --------
        if keys[pg.K_p]:
            if not self.toggle_wait: # its lazy but its the autoshoot toggle so its not guna get used enough to matter rn chill
                self.set_player_weapon_id()
                self.toggle_wait = pg.time.get_ticks()
        # -------- player interaction keys stuff --------
        # -- bottom clout ui sidebar --
        if keys[pg.K_u]: # for twitch tho also is temp af
            if not self.toggle_wait: # <<<<<<<<<<<<<<<<<<<<<<<<<<< ffs make this a function or better still a class
                # dont let us toggle 1 jillion times per second
                self.game.want_clout_ui = not self.game.want_clout_ui # flip it
                self.toggle_wait = pg.time.get_ticks() 
                print(f"{self.game.want_clout_ui = }")
        # -- zombie names - for debugging mostly --
        if keys[pg.K_y]: # y for your name? nah idk its just in the middle of u for ui and t for twitch chat so made sense
            if not self.toggle_wait:
                # dont let us toggle 1 jillion times per second
                self.game.want_zombie_names = not self.game.want_zombie_names # flip it
                self.toggle_wait = pg.time.get_ticks() 
                print(f"{self.game.want_zombie_names = }")
        # -- twitch chat sidebar --
        if keys[pg.K_t]: # for twitch tho also is temp af
            if not self.toggle_wait:
                # dont let us toggle 1 jillion times per second
                self.game.want_twitch = not self.game.want_twitch # flip it
                self.toggle_wait = pg.time.get_ticks() 
                print(f"{self.game.want_twitch = }")
        # -- shooting --
        # -- toggle auto shooting --
        if keys[pg.K_b]: # for bullets... or beginner but easily could be harder tho so nah
            if not self.toggle_wait:
                # dont let us toggle 1 jillion times per second
                self.autoshoot = False if self.autoshoot else True # flip it
                self.toggle_wait = pg.time.get_ticks() 
        # -- actual shooting --
        if keys[pg.K_SPACE]:
            if not self.autoshoot:
                if not self.is_reloading:
                    # temp af for now but should increase the shooting speed by a factor of 2 if not in auto shoot
                    now = pg.time.get_ticks() # track the last time we shot 
                    if now - self.last_shot > self.return_bullet_rate():
                        self.last_shot = now 
                        dir = vec(1,0).rotate(-self.rot)
                        pos = self.pos + BARREL_OFFSET.rotate(-self.rot) # rotated to match the players direction
                        Bullet(self.game, pos, dir)
                        self.clip_counter += 1 # add one to the clip counter which tracks which bullet in the clip we have just fired
                        self.vel = vec(-self.return_gun_kickback(),0).rotate(-self.rot)
        # pass the game, the player(pos), and the rotation vector we've just figured out (where the player is facing)
        # -- action key --    
        if keys[pg.K_e]: # if E
            # need to fix this so it only takes payment once, and then when that works make it infectious, for now i really dont care enough its a simple af functionality so its fine for now
            # handle paywalls action button press interactions
            for paywall in self.game.paywalls:
                # we dont need to check already unlocked walls
                if not paywall.is_unlocked:
                        # most computationally expensive part so do any break conditions before this 
                        if paywall.is_near(self.pos.x, self.pos.y): # i get this so much now right, like ur for sure doing this twice, once here, and once to highlight them, which is silly, reducing stuff like this is crucial in refactor and moving forwards                            
                            unlock_cost = paywall.get_unlock_cost() # using function assuming that we'll start doing it dynamically shortly
                            if self.player_gold >= unlock_cost:
                                self.player_gold -= unlock_cost
                                print(f"BALLIN' - Splashed ${unlock_cost} To Bypass A PayWall")
                                paywall.is_unlocked = True
                                break # and if one of these break conditions has been met, stop checking to see if were near any other walls
                            else:
                                print("PAYWALLED! - Get more kills and subscribers to earn more CA$H!")
                                break                          
            # handle breakable walls action button press interactions
            for a_wall in self.game.breakablewalls:
                # if player is near a breakable wall
                if a_wall.is_near(None, None):
                    a_wall.try_repair_wall()
                    # new test but assume fine, just a condition to break the loop if we are near a wall, no need to check for more
            # only allow one interaction at a time, 2 sec pause currently should reduce tho
            self.is_interacting = True
        else:
            self.is_interacting = False
        # -------- player main movement keys stuff --------
        # if were pressing left on the keyboard or a            
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED  
            self.state_moving = "walking"        
        # use if to allow diagonal movements 
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
            self.state_moving = "walking"
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot) # move at the player speed in the 1 direction and 0 in the y direction, then rotate that vector by whatever our rotation is, negative and us will take us left, counterclockwise so negaitve degrees
            self.state_moving = "walking"
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED /2, 0).rotate(-self.rot) # now we are rotating this is moving backwards, hence the minus player speed and the negative 2 so we've notably slower backwards
            self.state_moving = "walking"      

        # -- companion --
        if keys[pg.K_c]:
            pass # not yet implemented

        # -- new dash test --
        if keys[pg.K_TAB]:
            if not self.dash_cooldown:
                self.vel *= 4
                print(f"Dash! => {self.vel}")
                self.dash_cooldown = pg.time.get_ticks() 

        # -------- player sprint stuff --------  
        if keys[pg.K_LSHIFT]: # if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:  
            # to make as own function, is sprinting / handle sprinting - new sprint implementation, only called when holding sprint so any sprint meter stuff needs to be done outside here duh
            self.vel *= self.get_sprint_multiplier() 
            self.state_moving = "sprinting"
            self.sprint_meter -= self.sprint_meter / 100
        # duh if we are defo not sprinting things here
        else:
            #self.image = self.game.player_img
            # make own function, is not sprinting / handle walking
            # if the sprint meter is not full, start to refill it
            if self.sprint_meter < 10_000:
                # make new function - handle sprint meter
                # if we are defo not sprinting the refill the bar, by 0.5 percent each frame
                # CHECK IF WE ARE STANDING STILL FIRST, IF WE ARE RECOVER BY MORE
                self.sprint_meter += self.sprint_meter / 200
            # remove any small offsets
            if self.sprint_meter > 6_000:
                self.sprint_meter = 6_000
        # -------- player not moving stuff --------                
        # if not moving in any direction, even if ur holding sprint, ur not moving
        if self.vel == 0 and self.vel.y == 0:
            self.state_moving = "chilling"
        # -------- player if walking and fatigued speed stuff -------- 
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
            #self.image = self.game.player_blur3_img
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
            #self.image = self.game.player_blur1_img
            return(1.15) # hastened
        else:
            # for now, if ur not spent, but not over 30% then still quick but not sprint, its like a jog
            #self.image = self.game.player_blur1_img
            return(1.25) # quick           

    def is_near(self, x, y, how_near=400): # 400 is random af default, is for 64 tile size too btw
        # abstract this properly pls 
        pythag_dist = hypot(self.pos.x-x, self.pos.y-y)
        # if pythag_dist < how_near:
        #     print(f"Dist = {pythag_dist}")
        return True if pythag_dist < how_near else False
                
    def handle_reload(self):
        # if we've hit the limit of our weapons clip size
        if self.clip_counter >= self.return_clip_size():
            print("RELOADING!!!")
            self.clip_counter = 0 # reset the clip counter
            self.is_reloading = pg.time.get_ticks()

    def update(self): # hereplayerupdate
        self.get_keys()
        self.current_weapon = self.weapon_list[self.current_weapon_id - 1]
        # update the rotation based on where we are facing
        # [note!] - if you want to update the player img u need to do it here as the rotation is done here and thats important mkay
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 # modulo 360 so if we hit 361 we just go back to 1
        # transform our image based on our current rotation
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        # calculate what our new rectangle is as we rotate it as it holds our image
        self.rect = self.image.get_rect()
        # take that rectangle at set it to where our previous rectangle was at
        self.rect.center = self.pos
        # use our rectangles x & y to the speed/pos to check for collisions 
        self.hit_rect.centerx = self.pos.x
        # update the position of the player based on keys pressed using velocity vector
        self.pos += self.vel * self.game.dt
        collide_with_walls(sprite=self, group=self.game.walls, dir='x')
        collide_with_walls(sprite=self, dir='x', collision_type="breakable")
        collide_with_walls(sprite=self, group=self.game.paywalls, dir="x")
        # basically were doing 2 collision check, 1 for each axis
        self.hit_rect.centery = self.pos.y
        collide_with_walls(sprite=self, group=self.game.walls, dir='y')
        collide_with_walls(sprite=self, dir='y', collision_type="breakable")
        collide_with_walls(sprite=self, group=self.game.paywalls, dir="y")
        # after collision make sure our regular rect is set to the position of our hit rect, 
        # since we're now updating the hict rects position (not rotation, or velocity, just pos) 
        # if it collides (by moving in the opposite of where we tried to move), so we need to reapply this transformation to the player and not just the hitbox
        self.rect.center = self.hit_rect.center

        # need sumnt like set state, unsure if best after or before keys but assumed after for obvs reasons
        # again forget actual ranges for now but if we are under 30% we are fatigued
        if self.sprint_meter < 3_000 :
            # you need to know if sprinting or not as should still be blurred if sprinting but dw about stuff like that at all for now
            # make me red and decoloured if im fatigued, img
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
        # print(f"{(self.sprint_meter):.1f}% - {self.state_moving = }, {self.state_state = }, {self.vx = }")

        # new test dash cd 
        cd_end = pg.time.get_ticks() 
        if cd_end - self.dash_cooldown >= 10000: # 10 sec
            self.dash_cooldown = False
        
        # new test handle reload
        self.handle_reload()
        reload_end = pg.time.get_ticks() 
        if self.is_reloading: # if this is a timer and not a False bool
            if reload_end - self.is_reloading >= self.return_gun_reload_speed(): # 10 sec
                # if ur done reloading reset this var and its gravy
                self.is_reloading = False

        # new test
        if self.waiting:
            space_end = pg.time.get_ticks() 
            if space_end - self.waiting >= 1000:
                print(f"interactions enabled")
                self.waiting = False
        if self.waiting_print:
            space_end = pg.time.get_ticks() 
            if space_end - self.waiting_print >= 1000:
                self.waiting_print = False 
        if self.toggle_wait:
            space_end = pg.time.get_ticks() 
            if space_end - self.toggle_wait >= 100:
                self.toggle_wait = False 
        # then finish by shooting a bullet
        # but only if a zombie is close
        now = pg.time.get_ticks() # track the last time we shot 
        if self.autoshoot: # if autoshoot is on, currently the b key
            BULLET_RATE = 300 # temp
            for mob in self.game.mobs:
                # temp test -> save all the zombie hps, if they are all dead then stop all timers (well we defo wanna no this too so gg4dat)
                if now - self.last_shot > BULLET_RATE: # fixes double bullets by being inside
                    if self.is_near(mob.pos.x, mob.pos.y, PISTOL_SIGHT): # shortly this will become current weapon sight
                        # now we need not only if the player is in range, but if the player is facing the right direction, no backwards shooting
                        # should also be before / only the mob in mobs that are facing are valid, yeah so here is fine tbf whatever man just go 
                        # if the zombies rotation and our rotation are within 150 degrees? but way less to test first
                        rot_diff = -mob.rot + self.rot # you want this to be perpendicular, 180 degrees, or as close to it as possible for locked line of sight
                        # so we say if you're within the acceptable range and perpendicular to a close zombies line of sight then take the shot else dont
                        # viewing angle now a setting
                        # successfully sets the auto shoot to only occur when in front of the player
                        # and pretty much (tho needs fixing 100%) shoots the closest target
                        if rot_diff > (180 - VIEWING_ANGLE / 2) and rot_diff < (180 + VIEWING_ANGLE / 2):
                            # we're taking a shot now for sure so update our last shot time to now, only do this when 100% sure we're shooting
                            self.last_shot = now 
                            dir = vec(1,0).rotate(-self.rot) # used for normal shooting
                            player_pos = vec(self.pos).copy() # dont update the players actual position 
                            rot_to_mob = (mob.pos - player_pos).angle_to(vec(1,0)) # the angle
                            dir_to_mob = vec(1,0).rotate(-rot_to_mob) # the final direction vector
                            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                            #print(f"PEW!, AUTOSHOT AT {mob.myid}")
                            # should try here -> if the vector between me, the player and my exact facing rot, the unused dir here if the firs thing on the path of that vector, if a wall, dont shoot, else shoot
                            # use the pos for the bullet start, and the direction is now to the closest mob instead of where the player is facing
                            Bullet(self.game, pos, dir_to_mob)
                            # fake way to do kickback in autoshoot for now, but needs to be fixed obvs
                            self.vel = vec(-200,0) # kickback the player slightly in the opposite direction after every shot, rotated to push in the opposite of the direction ur facing


class Mob(pg.sprite.Sprite): # heremob herezombies
    zombie_id_counter = 0
        
    def __init__(self, game, x, y, bwalls): #  hp = 0
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy() # they all need their own unique hit rect so copy is needed
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.rot = 0
        self.vel = vec(1,1)
        self.acc = vec(0,0) 
        
        # new test font constants
        self.FONT_SILK_REGULAR_12 = pg.font.Font("Silkscreen-Regular.ttf", 12)
        self.FONT_SILK_REGULAR_32 = pg.font.Font("Silkscreen-Regular.ttf", 32)

        self.max_health = self.set_init_hp() # 150  # get a random number for our initial max health, else its 100
        # then set the starting health to that max health
        self.health = self.max_health 

        # my own super test af stuff
        # this is literally the entire class object, not a class instance
        self.bwalls = bwalls
        # if has collided with a bwall, do climb in stuff, then hunt the player 
        self.climbed_in = False
        # add zombie to the class variable list and assign it an id too
        # could do stuff here too for different value zombies, difficulty, etc, all off random
        self.waiting = False # give them their own waiting too, for breaking stuff and hiting the player
        self.waiting_speed = 1000 # seconds so this is half a second, can say thats quick/avg for now

        # generate ids
        Mob.zombie_id_counter += 1
        self.myid = Mob.zombie_id_counter
        
        # - currently unused - new stalled fixer test
        self.stalled = False

        # name stuff
        self.myname = f"{self.get_first_name()}" # need to fix this stuff btw, just remove recursion, was nice to implement but nah g that aint it
        print(f"{self.myname} {'is roaming' if self.health <= 150 else 'is looking for blood' if self.health > 150 and self.health < 250 else 'is enraged'}... [ {self.health}hp ]")

        # [NEW!] rework/refactor
        self.is_looking_at = "roaming"
        self.closest_bwall = [0,0]
        self.last_target = 0 # for super basic roaming
    
        if self.game.player.pos.y < self.pos.y: # you are above the player, so only look below you (not the full height of the screen)
            # self.random_place_to_look = (randint(1,WIDTH)*TILESIZE, randint(1,HEIGHT)*TILESIZE) # very very very temporary test
            self.random_place_to_look = (randint(1,WIDTH)*TILESIZE, randint(1,int(self.pos.x))*TILESIZE)
            ############################################################################################
            #                                                                                          #
            # FIX THIS ITS WRONG, WANT TO ONLY LOOK UP OR DOWN BASED ON THE PLAYER AND UR OWN POSITION #
            #                                                                                          #
            ############################################################################################
        else:
            self.random_place_to_look = (randint(1,WIDTH)*TILESIZE, randint(HEIGHT, int(self.pos.x),)*TILESIZE) # if you are below the player, dont look below yourself
        self.zombie_sight_range = randint(500,700)
        self.is_looking_at_bwall = 0 # this will be a bwall object
        self.charging_attack = 0 # is a counter
        self.broken_in = False
        self.hit_by_bullet = 0
        self.is_frenzied = False
        self.low_hp = 0 # so we dont set it twice we init to zero, then if its zero we set it, else we dont set it
        # self.check_and_update_looking_at_status()
        # ---- end init ----

    def get_first_name(self):
        list_of_names = ["Zob", "Zenjamin", "Zames", "Zohn", "Zichard", "Zhomas", "Zhristopher", "Zaniel", "Znthony"]
        return(list_of_names[randint(0, 8)])

    def set_init_hp(self):
        roll_chance = randint(1, 10)
        if roll_chance <= 5:        
            maxhp = (randint(1, 10) * 10) + MOB_BASE_HEALTH # if the zombie won a 50/50 head or tails, then give it up to 100 more hp based on its second roll 1 - 10 
        else:
            maxhp = MOB_BASE_HEALTH       
        return(maxhp)  # should make this more dynamic by giving each zombie traits like luck too

    def draw_health(self):
        if self.health >= (self.max_health / 10) * 6: # simple hp bar
            col = GREEN
        elif self.health >= (self.max_health / 10) * 3: # greater than 30%
            col = YELLOW
        else: # else is 30% or less
            col = RED        
        width = int(self.rect.width * self.health / self.max_health) # width of bar is just the width of this zombies rect time the percent of hp remaining       
        self.health_bar = pg.Rect(0, 0, width, 7)  # the location on the sprite image not on the screen, 7 is thickness        
        if self.health < self.max_health:  # only draw the bar if the zombie is not full hp            
            pg.draw.rect(self.image, col, self.health_bar) # draw that self.health_bar on top of our zombies rectangle in the given colour

    def get_display_status(self): # considered things like [tanky boi] but the spacing is too much, clogs up the screen like mad
        if self.hit_by_bullet > 0: # if you got hit by a bullet in the last 2 seconds ur a sadge boi
            status = ":("
            color = NAVYBLUE
        elif self.is_looking_at == "bwall":
            if self.charging_attack: # if charging attack bit different status display than just looking for wall
                if self.charging_attack < 0:
                    status = ":/"
                    color = NAVYBLUE
                else:
                    status = "?!"
                    color = RED
            # and elif knockback which is just on cooldown with sadge face lol, not sadge when they die confused when they get hit back! :/
            else:
                status = "?"
                color = ORANGE
        elif self.is_looking_at == "player":
            if self.is_frenzied:
                status = "!!!"
                color = RED
            else:
                status = "!"
                color = RED
        elif self.is_looking_at == "roaming":
            status = ":)"
            color = NAVYBLUE
        return status, color

    def draw_status(self):
        status, color = self.get_display_status()
        # then before we draw the name rotate it to where we want it to be, since we're doing it with blit in relation to the camera
        self.name_textsurface = self.FONT_SILK_REGULAR_32.render(f"{status}", True, color) # (f"{self.myname} {self.health}", True, BLACK)  # "text", antialias, color
        # e.g. this will rotate to face the player => pg.transform.rotate(textsurface, self.game.player.rot)
        #if self.rot > -135 and self.rot < -45: # only do our rotation at certain angles based on the zombie
        self.name_textsurface = pg.transform.rotate(self.name_textsurface, self.rot + 90) # if at this angle rotate my name
        return self.name_textsurface 

    def draw_name(self):
        # then before we draw the name rotate it to where we want it to be, since we're doing it with blit in relation to the camera
        self.name_textsurface = self.FONT_SILK_REGULAR_12.render(f"{self.myname}", True, BLACK) # (f"{self.myname} {self.health}", True, BLACK)  # "text", antialias, color
        # e.g. this will rotate to face the player => pg.transform.rotate(textsurface, self.game.player.rot)
        #if self.rot > -135 and self.rot < -45: # only do our rotation at certain angles based on the zombie
        self.name_textsurface = pg.transform.rotate(self.name_textsurface, self.rot + 90) # if at this angle rotate my name
        return self.name_textsurface 

    def look_at(self, look_at_me):        
        # minus the players pos from this zombies pos to get the vector zombie -> to -> player
        # to get the angle, stick the given vector into to angle with the axis vector e.g. (1, 0) or forward in x, 0 in y i.e to the right, which is positive in the x axis
        self.rot = (look_at_me - self.pos).angle_to(vec(1,0))
        # then rotate our zombies img by the rotation vector
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        # then update our zombies new rectangle centre too
        self.rect = self.image.get_rect()

    def can_climb_in(self):
        """ if you have collided with a"""
        bhits = pg.sprite.spritecollide(self, self.game.breakablewalls, False, collide_hit_rect)
        if bhits:  
            # so here is ur warning stuff nice
            # should do like, if ur nearest bwall is broken then set urself to climbed in so u start going for the player bosh and pretty easy too
            print(f"{self.myname} Broke In @ {self.pos.x}, {self.pos.y} [Collided With B Wall]")
            self.climbed_in = True

    def is_near(self, x, y, next_to=15, return_distance=False): # for 64 tilesize
            # use hypotenus of the xy vectors to find out how close we are to the given vector pos
            pythag_dist = hypot(self.pos.x-x, self.pos.y-y)
            if return_distance:
                # print(f"{pythag_dist=}")
                return pythag_dist
            else:
                return True if pythag_dist < next_to else False

    def check_wall_distance_every_second(self): # completely unused
        if not self.check_dist_timer: # dont start it again if its already on (unsure how get_ticks works tbf, it may do this inherently idk)
            self.check_dist_timer = pg.time.get_ticks() 
        else: # if the timer is running
            check_timer = pg.time.get_ticks() 
            if check_timer - self.check_dist_timer > 200: # check to see if the timer has passed 1 second
                self.check_dist_timer = 0 # if it has reset the timer and do what you want to happen each second here

    def set_closest_bwall_position(self): # now using the constant position for the wall created as a .game variable when the walls are placed
        bwall_distances = []
        for a_bwall in self.game.all_bwall_positions: # loop the list of tuples of positions, but only do this once we need to know where to look at, and only do it once overall, not per frame
            current_bwall_distance = self.is_near(a_bwall[0], a_bwall[1], return_distance=True)
            bwall_distances.append(current_bwall_distance)
        # set our closest bwall to the closest bwall, thank you for coming to my TEDtalk 
        closest_bwall_index = bwall_distances.index(min(bwall_distances))
        # then here check if its index is even as its on the left, so we want to change it to look at the right one instead (since its looking at the left most point and not the center) - note to tell if the bwall selected is on the left or right just check if its index is odd or even since they are always inserted right to left and always in pairs (will work for y walls anyway)
        if closest_bwall_index % 2 == 0:
            closest_bwall_index += 1 # change it to the right one, as these are printed left right pairs its always just +1 for now anyways
        closest_bwall_position = self.game.all_bwall_positions[closest_bwall_index]
        # if this zombie is above the wall or below it set the one tile up difference to be positive or negative
        if closest_bwall_position[1] > self.pos.y: # the zombie y position
            self.closest_bwall = closest_bwall_position[0], closest_bwall_position[1] + (TILESIZE * 2) # look two tiles down for y collision where wall is above you
        else:
            self.closest_bwall = closest_bwall_position[0], closest_bwall_position[1] - (TILESIZE * 2) # else look two tiles up as the wall collided beneath you
        
        # so since we only do this once, HERE, is where we will add the check left or right side code and return it for where the zombie should be exactly looking at
        # you just minus or add half a tile size depending on left or right
        # obvs need to add left and right too
        
    def check_and_update_looking_at_status(self):
        """
        - if you are 400+ away from player you are roaming
        - if you are not roaming you are looking at the player
        - if you were looking at the player and you collided with this wall, you are now finding the closest way in
        """
        # kinda hacky cope for now, saying if its player inside its like its own special new condition to kick you out of the loop, need to fix
        if self.is_looking_at == "companion":
            # provides a break condition for companion so that the zombies dont stop hunting the companion if you are out of the zombies sight range (as its not looking at you duh)
            if self.game.companion.current_health < 0:
                # they will actually go for you if you get closer too which is kewl
                self.is_looking_at == "player"
        elif self.is_looking_at == "bwall":
            self.breaking_and_entering() # print(f"{self.myid = }, {self.vel = }")
            # 
            #
            # until some condition like broken wall in front of me...  
            # if the the wall in front of me is no hp? # optional, would reduce checks but meh 
            #   if right_next_to_pos_infront_of_me: # which will just happen if we've broken the wall as we're looking at it
            #       self.is_looking_at = "player": # this then being the only condition that flips the zombie out of the bwall chasing/breaking in state
            #   else:
            #       self.is_looking_at = "bwall":
            #
            # after running the breaking and entering function,
            # if you've `broken_in`
            if self.broken_in == True:
                self.is_looking_at = "player" # then you should be looking at the player
                self.broken_in == False # also reset broken in as you may need to break in again, this only flags during looking at bwall so this is fine 
            else: # if you've not broken in yet (self flag boolean `broken_in` is not yet true) then ur still looking at bwall, 
                self.is_looking_at = "bwall" 
            #if self.pos.y > self.game.player.pos.y:
                #print(f"{self.myid} I've hit a wall - at pos {self.pos}, at {self.vel}kph, going to wall at {self.rot}. [NOTE] PLAYER Y POS = {self.game.player.pos.y}")
            # i.e. if you've hit a wall after you were looking at the player, keep looking at the place past that wall (until we then destroy it >>>> and then implement that bosh)
        else:
            #print(f"{self.game.zombies_distances_to_player[self.myid] = }")
            # WHEN YOU DIE HERE HAVE A TRY EXCEPT FOR TEMP FIX, THEN ACTUAL FIX
            # LIKELY HAVE TO DO IT FOR LOTS OF ZOMBIES DISTANCES THINGS SO ACTUALLY JUST FIX THAT INSTEAD
            # YOU IDIOT! :D
            if self.game.zombies_distances_to_player[self.myid] > self.zombie_sight_range:                
                self.is_looking_at = "roaming"                
            else:# should 100% be looking at the player btw, so below if is pointless, however if the conditions deepen then will be necessary so leave it for now
                self.is_looking_at = "player"
                if self.is_looking_at == "player": # if we were looking at the player
                    # when you initially collide with a horizontal (x axis) wall, you're y will hit 0 for a frame, use that frame to set us to now finding a way in
                    #print(f"{self.myid} is looking at player, at position {self.pos}, speed = {self.vel}, tile = {ceil(self.pos.y/TILESIZE)}, player at {self.game.player.pos}")
                    if self.vel.y <= 0.5: # to decide if we should be finding a wall to break into, use this vel collision, and then checking if ur by a wall - as if could have been a bullet that changed ur velocity (or another zombie when removed grouping)
                        # again note, sure its not ideal i bet, but its optimised atleast slightly doing it this way
                        # as we're only doing the more complex check against wall collision, if we've slowed down to the point that we might be on a wall
                        if self.am_i_by_a_wall(): # then if we have hit a wall, set us to looking at bwall, else keep looking at what we were looking at, as we probably just got hit by a bullet to slow down
                            print(f"ZOMBIE {self.myid}: was looking at player, collided with a wall, now looking at bwall")
                            self.is_looking_at = "bwall" # set what we are looking at to the bwall'

    def breaking_and_entering(self):
        # some way to find the looking at bwall object but efficiently'
        # if this variable isnt set, then set it, this triggers when the zombie hits a wall, it wants to know if it has a target yet (so we dont loop every update, just once, as if its the closest it wont change anyway)
        if self.is_looking_at_bwall == 0:
            bwall_distances_from_zombie = {}
            closest_distance_tracker = 5000
            # loop the walls to find the closest instance to the zombie
            for a_bwall in self.game.breakablewalls:
                zombie_distance_to_wall = int(self.is_near(a_bwall.pos.x, a_bwall.pos.y, return_distance=True))
                bwall_distances_from_zombie[zombie_distance_to_wall] = a_bwall # distance is the key
                if zombie_distance_to_wall < closest_distance_tracker: # figure out which is the closest during the loop
                    closest_distance_tracker = zombie_distance_to_wall # by setting it during each iteration
            self.is_looking_at_bwall = bwall_distances_from_zombie[closest_distance_tracker] # get the closest object back based on the closest distance
            
            bwall_distances_from_zombie = {} # wipe the dictionary
        # else there is already a variable storing the bwall object that we are closest to, so...
        else:
            # print(f"Zombie [{self.myid}] - looking at bwall {self.is_looking_at_bwall.myid} at position {self.is_looking_at_bwall.pos.x/TILESIZE:.0f},{self.is_looking_at_bwall.pos.y/TILESIZE:.0f} / {self.is_looking_at_bwall.pos.x:.0f}, {self.is_looking_at_bwall.pos.y:.0f}") # first check if the wall has hp, as this decides if we need to attack and destroy its hp first before we can break in 
            if self.is_looking_at_bwall.hp_current > 0: # print(f"Wall I'm Targetting Has {self.is_looking_at_bwall.hp_current} of {self.is_looking_at_bwall.hp_max} hitpoints remaining")
                # if in range of the wall start a charge bar
                bwall_current_distance = self.is_near(self.is_looking_at_bwall.pos.x, self.is_looking_at_bwall.pos.y, return_distance=True) # print(f"{self.myid} zombie is {bwall_current_distance} meters away from bwall {self.is_looking_at_bwall.myid}")
                if bwall_current_distance < 90:
                    self.charging_attack += 1
                    if self.charging_attack > 100: # if greater than a short charge up count # its actually a 200 charge up, the extra 50 that overruns is for cooldown
                        self.charging_attack = -50 # reset the bar to under, for cooldown, the bar wont be displayed if its under 50
                        # and pop back a bit, want to add some weight to this properly with acceleration, below acc implementation is trash as only 1 frame (or maybe even gets overwritten before moving tbf)
                        self.acc.x -= (self.acc.x / 100) * 80
                        self.acc.y -= (self.acc.y / 100) * 80
                        self.vel = vec(-60,0).rotate(-self.rot) # confirm isnt dependent on x or y collision specifically btw
                        self.is_looking_at_bwall.hp_current -= 1
                        self.is_looking_at_bwall.infect_walls()
            # else you have successfully destroy the wall in front
            # now check to see if you are "inside", then when you are hunt the player
            else: # hp is 0 (shouldnt ever be less, confirm dis)
                climbed_in_distance = (self.is_near(self.closest_bwall[0], self.closest_bwall[1], return_distance=True)) # use the actual look at position, not just the wall position as we want to be fully in before we chase the player previouly self.is_looking_at_bwall.pos.x and y
                if climbed_in_distance < 30:
                    print(f"{self.myid}. {self.myname} has broken in and is hunting the player [{self.vel = }]")
                    self.broken_in = True # only condition that will force you out of looking at bwall, for now anyways
                    self.zombie_sight_range += 100 # increase its sight range, as the player may have run 

    # to properly do this parameter for checking x or y btw
    def am_i_by_a_wall(self, x_or_y="y"):
        if x_or_y == "y":
            if self.pos.y < self.game.player.pos.y: # the collision is slightly different if ur hitting a wall above or below or take this into consideration
                true_grid_position = (ceil(self.pos.y/TILESIZE))  # the y position you are on the 48 x 64 tilemap i.e. 15 (removing the idea of 1/2 or 1/4 tiles due to which side judging the collision of a rectangle)      
                # if the true grid y position ur at is also a walls y position (because its in the y_walls_unique list)
                return True if true_grid_position in self.game.y_walls_unique else False
            elif self.pos.y > self.game.player.pos.y:
                true_grid_position = (ceil(self.pos.y/TILESIZE)) - 2
                return True if true_grid_position in self.game.y_walls_unique else False
    # you need to do this as you could be 0 vel for many reasons, and once we confirm ur by a wall...

    def update(self): # run every frame
        if not self.game.zombies_distances_to_player:
            self.game.set_zombies_distances_to_player()
            print(f"{self.game.zombies_distances_to_player = }")

        self.check_and_update_looking_at_status()
        if self.is_looking_at == "roaming":
            self.acc = vec(int(MOB_SPEED/4), 0).rotate(-self.rot) # make the zombos slower if roaming
            # super basic roaming 
            self.look_at(self.random_place_to_look)
        # roaming has break priority, else...
        else:
            self.acc = vec(MOB_SPEED, 0).rotate(-self.rot) # else if thiss zombo is not roaming, make it normal speed

            if self.is_looking_at == "player": # if we're looking at the player
                # simple test check here to see if ur closer to the player or the companion, the look at the one ur closest too
                companion_distance = get_distance(self, self.game.companion.pos.x, self.game.companion.pos.y)
                player_distance = get_distance(self, self.game.player.pos.x, self.game.player.pos.y)
                if player_distance <= companion_distance: # if player closer look at player
                    self.look_at(self.game.player.rect.center)
                else: # else if companion alive, look at companion
                    if self.game.companion.hp_current > 0:  
                        self.is_looking_at == "companion"
                        self.look_at(self.game.companion.rect.center)
                    else: # else look at the player, the companion is dead
                        self.look_at(self.game.player.rect.center)
                self.closest_bwall = [0,0] # ensure this isnt a true type value if we are looking at the player             
                # until some condition like broken wall in front of me that is
                
            if self.is_looking_at == "bwall":
                # if we havent found the closest bwall to you yet, then do that
                if self.closest_bwall == [0,0]: # if the var closest wall var isn't already set, or has been turned off because we'd broken a wall but now have hit another one 
                    self.set_closest_bwall_position() # <= this actually does the set tho
                self.look_at(self.closest_bwall)


            # set the closest bwall if it is not already set
            # if it is already set, look at this position,
            # then when thats working
            # when you are x close to b wall, hit it and bounce back slightly,
            # then go again,
            # include the left or right hand thing at this point too    
            # and dont check every frame for every zombie, even half second probs fine, could even have them all share the same class timer variable

        # ---- actual code ----  
        # once we got the direction, quickly reduce the amount he accelerates by
        # self.acc = vec(MOB_SPEED, 0).rotate(-self.rot) < moved up to create if else roaming slow
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        # eq of motion, velocity times time times half the acceleration, times the time squared
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        # now we know where the sprite should be set its rect center
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(sprite=self, group=self.game.walls, dir="x")
        collide_with_walls(sprite=self, dir="x", collision_type="breakable")
        collide_with_walls(sprite=self, group=self.game.paywalls, dir="x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(sprite=self, group=self.game.walls, dir="y")
        collide_with_walls(sprite=self, dir="y", collision_type="breakable")
        collide_with_walls(sprite=self, group=self.game.paywalls, dir="y")
        # then set our regular rect to our hit rect, remember we primarily use the hit rect then set it to the regular rect at the end (the visual doesnt match the pixel precision)
        self.rect.center = self.hit_rect.center

        # new test for sadge face
        if self.hit_by_bullet > 0: # if this timer is not zero, so its running...
            check_hit_timer = pg.time.get_ticks()
            if check_hit_timer - self.hit_by_bullet > 400: # if its gone over 0.4 seconds reset it 
                self.hit_by_bullet = 0 

        # new frenzied state
        if self.low_hp == 0:
            self.low_hp = (self.max_health / 100) * 50 # 50% hp
        if self.health < self.low_hp: # if less than 20% hp
            self.is_frenzied = True
        if self.is_frenzied:
            self.vel *= 1.005 # this is good for now
            # note instead of stopping them on shot you should just drastically reduce the acc or vel !!!!! <<<<<<< 

            # self.vel *= 1.02 # ok move speed difficulty because they're not weighty, so they just float off
            # so for now just increase damage? (kinda complicated)
            # or figure this out
            # or just sumnt different

        # if the zombie health ever less than zero, kill it, idk why this isnt first in update tho? <= test it defo 
        # note-tho! => tbf for things like waiting i get that but surely not last last atleast mid is best but idk (nah waiting doesnt matter as its self.waiting not player but confirm tbf)
        if self.health <= 0:
            # self.game.screen.blit(self.game.splat_img, self.pos - vec(32, 32)) # half tile size, TILESIZE / 2
            self.kill()
        # end by updating waiting, bloc/cooldown main interactions for 1 second if true, e.g. reloading
        if self.waiting:
            space_end = pg.time.get_ticks() 
            if space_end - self.waiting >= self.waiting_speed: # 1 second waiter rn
                print(f"{self.myname} - interactions enabled")
                self.waiting = False
        # stalled stuff here when reworking it, for now is removed


class Bullet(pg.sprite.Sprite): # herebullet
    def __init__(self, game, pos, dir, bullet_owner = "player"):
        if bullet_owner == "player":
            self.groups = game.all_sprites, game.bullets
            pg.sprite.Sprite.__init__(self, self.groups)
        elif bullet_owner == "companion":
            self.groups = game.all_sprites, game.companion_bullets # game.bullets
            pg.sprite.Sprite.__init__(self, self.groups)
        # self.count_hits = [] # list of ids of zombies ive passed through, and therefore counted as gold/damage/stats, for not counting gold or hits for every split second a bullet has collided
        # here, in above, could really be starting implementation of extra gold, e.g. if multi hit x2 gold, x3 = x3 etc!
        self.game = game
        self.bullet_owner = bullet_owner
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos).copy() # position is the one we pass in, pass a copy so we dont update the players position with the bullet... which is fucking hilarious btw
        self.rect.center = pos # put our rectangle there at the center
        self.live_gun_spread = self.game.player.return_gun_spread()
        if game.player.autoshoot:
            spread = uniform(-self.live_gun_spread*2, self.live_gun_spread*2) # autoshoot is more inaccurate so its not giga free, easily changed and is temp anyway tbf
        else:
            spread = uniform(-self.live_gun_spread, self.live_gun_spread) # bullet will come out at a random angle based on the spread, this should really update or be different for autoshoot but is fine for now
        self.vel = dir.rotate(spread) * BULLET_SPEED # our velocity is the direction vector (len 1 vector pointing in one direction) times by the bullet speed
        self.spawn_time = pg.time.get_ticks() # get our time when we spawn so we know when to delete ourself
        # self.myid = self.bullet_count
        self.is_crit = self.check_crit()
        # more new custom test stuff
        # self.hp = 30 # say going thru each zombie costs 10

    # new custom functionality testing
    def check_crit(self):
        # first check the players clout, if ur mad clouted then ur crit change increases (just keep it giga simple for now) 
        # crit_chance = ((self.game.player.clout_rating / 10) * 5) + PISTOL_CRIT_RATE # div 10 so base would become 1, or double clout would become 2, then * 5, so 1 = 5 and 2 = 25, 95% chance normally, to 75% chance at double crit, its fine its just supposed to be sumnt for now lol
        # then you add the pistol crit rate to that floor value, i.e. 5, 10, 20, and you've got a floor value maybe thats like 30, so 30 - 100 = 70% chance
        crit_chance = PISTOL_CRIT_RATE
        # the default will be 10 / 10 = 1, * 5 = 5, + 10 = 15, 15% crit chance by default 
        actual_chance = randint(1, 100)
        #print(f"wantCrit? => {crit_chance = }, {actual_chance = }, {actual_chance >= crit_chance = }")
        # if our number range / numbers (our crit chance) is greater than or equal to our random chance 1 to 100 roll 
        if actual_chance <= crit_chance:
            # print(f"[ACTION] => Bullet [ {self.myid} ] Gained Critical Hit")
            return True
        else:
            #print(f"Bullet [ {self.myid} ] - nocrit")
            return False
        # remember with this mechanic we also wanna reset timers or speed ups n shit

    def update(self):
        # could calc bullet gold for debugging btw, how much gold this bullet racked up before it died
        base_gold = 10 # make this a constant once you figure out how it works to basic af mvp level
        self.pos += self.vel * self.game.dt # update our position vs our velocity
        self.rect.center = self.pos # update the rectangle to that new position too
        hit_zombie = pg.sprite.spritecollideany(self, self.game.mobs)
        if hit_zombie:
            if self.is_crit: # if this is a crit bullet, and you've hit a zombie, set the player damage to 100, # new crit test, not ideal as the way were doing collision rn i cant check the bullet just the zombie but its fine for now just playing around anyways, will do proper collisions soon 
                self.game.player.player_damage = 100 # but remember this is a temporary af hacky way so this will stay like that forever unless we put it back, we do that after the hit has been logged, if a 100 hit is logged, player_damage = 10, plus also if this bullet times out player damage = 10 # this will break af btw, e.g. bullets could get set to 200 or 300 etc is easy to fix but just saying dont forget lol   
                
                # [ FOR GOLD ] self.game.paused = not self.game.paused
                self.game.player.player_gold += base_gold

                self.game.player.current_accuracy[0] += 1 # current_accuracy = [bullets_hit, bullets_missed]
        # -- important --> this should contain bwalls and paywalls duh
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill() #  bullet is added to missed if it ran out of time or hit a wall
            self.game.player.current_accuracy[1] += 1
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME: # do a meeseeks
            self.kill() # delete the bullet
            self.game.player.current_accuracy[1] += 1 # bullet is added to missed if it ran out of time or hit a wall, current_accuracy = [bullets_hit, bullets_missed]
        

class Wall(pg.sprite.Sprite): # herewall
    # should do an InteractWall Class with even just is_near yanno (and then else valid for that)
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Coin(pg.sprite.Sprite): # herecoin
    # test af
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.gold_coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
    def update(self):
        self.x = self.x
        self.y = self.y


class BreakableWall(pg.sprite.Sprite): # herebwall should be called barricades huh
    wall_ids = []
    
    def __init__(self, game, x, y, player, hp=2):
        self.groups = game.all_sprites, game.breakablewalls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.hp_current = hp
        # sets the image, tho mayb should set to a default first incase sumnt weird happens and need a fallback idk
        self.update_image()
        self.rect = self.image.get_rect()
        # new - need position vector now too
        self.pos = vec(x, y) * TILESIZE
        
        self.hp_max = 4
        self.build_bar = 0
        self.player = player
        
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

    def try_repair_wall(self):
        # we're using delta time now for 1 second, see historical_backups v1_6 for the percent meter version (which is kinda better tbf but added complexity at this stage has diminishing returns)
        self.do_one_repair()
        # for infectious buildling, repairing a tile will repairing any that are touching it
        for a_wall in self.wall_ids:
            # check if we this wall is near any other walls
            if a_wall.is_near(self.pos.x, self.pos.y):
                # if we both tiles dont have the same hp, update them so they are
                if a_wall.hp_current != self.hp_current:
                    self.print_once(f"Shared Our HP Commrade -> {a_wall.hp_current}, {self.hp_current}")
                    a_wall.hp_current = self.hp_current
        # print(f"repairing wall [ {self.myid} - {self.hp_current}hp ] -> {self.build_bar = }")
        self.update_image()
        
    def infect_walls(self):
        # for infectious buildling, repairing a tile will repairing any that are touching it
        for a_wall in self.wall_ids:
            # check if we this wall is near any other wall out of all the walls (which we are)
            if a_wall.pos.x == self.pos.x or a_wall.pos.y == self.pos.y:
                # when we find a wall on the same axis, check if it is actually the wall next to you using its id and which side it should be on (2 wall pairs only) 
                if self.myid % 2 != 0: # if im odd im on the left, so get the id to the right
                    if a_wall.myid == self.myid + 1:
                        # if we both tiles dont have the same hp, update them so they are
                        if a_wall.hp_current != self.hp_current:
                            self.print_once(f"Shared Our HP Commrade [ ids = {self.myid} & {a_wall.myid}, hp = {self.hp_current} ]")
                            a_wall.hp_current = self.hp_current
                        if a_wall.hp_current < 0:
                            a_wall.hp_current = 0 # but never less than 0
                        if self.hp_current < 0:
                            self.hp_current = 0 # but never less than 0
                        
                else:
                    if a_wall.myid == self.myid - 1: # even so right hand side
                        # if we both tiles dont have the same hp, update them so they are
                        if a_wall.hp_current != self.hp_current:
                            self.print_once(f"Shared Our HP Commrade [ ids = {self.myid} & {a_wall.myid}, hp = {self.hp_current} ]")
                            a_wall.hp_current = self.hp_current
                        if a_wall.hp_current < 0:
                            a_wall.hp_current = 0 # but never less than 0
                        if self.hp_current < 0:
                            self.hp_current = 0 # but never less than 0

            
                
                

    def update_image(self, is_near=False):
        """ every time something interacts with me, run this (?) """
        # if box has 0 hp
        if self.hp_current == 0:
            # then in here you want the hp x is interacting check from update
            #if self.hp_current < self.hp_max: # if this wall is full hp
            if is_near:
                self.image = self.game.break_wall_hl_0_img
            else:
                self.image = self.game.break_wall_0_img
            #self.image.fill(BLACK)
        # if box has 1 hp
        elif self.hp_current == 1:
            if is_near:
                self.image = self.game.break_wall_hl_1_img # if near use the highlighted version
            else:
                self.image = self.game.break_wall_1_img
        # if box has 2 hp
        elif self.hp_current == 2:
            if is_near:
                self.image = self.game.break_wall_hl_2_img # if near use the highlighted version
            else:
                self.image = self.game.break_wall_2_img
        # if box has 3 hp
        elif self.hp_current == 3:
            if is_near:
                self.image = self.game.break_wall_hl_3_img # if near use the highlighted version
            else:
                self.image = self.game.break_wall_3_img
        # if box has 1 hp
        elif self.hp_current == 4:
            if is_near:
                if self.player.is_interacting:
                    # render slightly reddened version
                    self.image = self.game.break_wall_hl_4b_img
                else:
                    # else normal yellow highlight
                    self.image = self.game.break_wall_hl_4_img # if near use the highlighted version
            else:
                self.image = self.game.break_wall_4_img           

    def is_near(self, x, y):
        close = 180 # for 64 tilesize # close = 80 #, 50, 30 < for 32x32 pixel tilessize 
        if not x:
            x = self.player.pos.x
        if not y:
            y = self.player.pos.y
        # use hypotenus of the xy vectors to find out how close we are to the player
        pythag_dist = hypot(self.pos.x-x, self.pos.y-y)
        if pythag_dist < close:
            # print if we're close to a bwall
            pass
            # self.print_once(f"Player is {pythag_dist}ft away from {self.myid}") #  x:{self.pos.x}, y:{self.pos.y}, x:{x}, y:{y}
        # if we are right next to the sprite our pythag_dist will be the size of the tile e.g. 32 
        return True if pythag_dist < close else False

    def print_once(self,print_me): # temp test for debugging only   
        # abusing the players waiting variable to only do an action 1 once every x seconds (2s currently)
        if not self.player.waiting_print:
            print(print_me)
            self.player.waiting_print = pg.time.get_ticks()

    def do_one_repair(self): # temp test for now
        # use waiting var to only do 1 interaction per x, tho should use is_interacting thing instead < do this asap as stateness duh
        if not self.player.waiting:
            if self.hp_current < self.hp_max:
                self.hp_current = self.hp_current + 1
                print(f"DONE REPAIR {self.myid=} {self.hp_current=} - interactions disabled")
            # pressing when you cant buy will still take an action ??
            self.player.waiting = pg.time.get_ticks()

    def update(self):
        # if we (this iinstance of breakable wall) are near the player
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.is_near(None, None):  
            self.update_image(True)
        else:
            self.update_image()


class PayWall(pg.sprite.Sprite): # literally call it this in game too
    all_paywalls = {}
    
    def __init__(self, game, x, y, player):
        self.groups = game.all_sprites, game.paywalls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.paywall_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.player = player
        self.game = game
        self.unlock_cost = 1000 # self.get_unlock_cost()
        self.unlock_condition = 0 # based on subscribers
        self.is_unlocked = False
        self.myid = len(PayWall.all_paywalls)
        PayWall.all_paywalls[self.myid] = self # add urself to the all_paywalls dict as a value, with ur id which is ur index, as the key 

    def update(self):
        # if we (this iinstance of breakable wall) are near the player
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.update_image()

    def get_unlock_cost(self):
        return(self.unlock_cost)
        
    def is_near(self, x, y, how_close = 180): # 180 as default 'close' is for 64 tilesize
        # use hypotenus of the xy vectors to find out how close we are to the player
        pythag_dist = hypot(self.pos.x-x, self.pos.y-y)
        # if we are right next to the sprite our pythag_dist will be the size of the tile e.g. 32 
        return True if pythag_dist < how_close else False # print(f"near paywall? = {pythag_dist < close}")

    def update_image(self):
        if self.is_unlocked:
            self.kill() # self.image.fill(BGCOLOR)
        # no need to do is_near check if ur unlocked
        elif self.is_near(self.player.pos.x, self.player.pos.y):
            self.image = self.game.break_wall_hl_4_img
        else:
            self.image = self.game.paywall_img

    def infect_walls(self):
        # for infectious buildling, repairing a tile will repairing any that are touching it
        for a_wall in self.wall_ids:
            # check if we this wall is near any other walls
            if a_wall.is_near(self.pos.x, self.pos.y):
                # if we both tiles dont have the same hp, update them so they are
                if a_wall.hp_current != self.hp_current:
                    self.print_once(f"Shared Our HP Commrade -> {a_wall.hp_current}, {self.hp_current}")
                    a_wall.hp_current = self.hp_current



# do pause menu for three popup things idea




# old mob, am_i_stalled implementation
    """
    def am_i_stalled(self):
        for bwall in self.bwalls:
            # if i, this zombie, am near a bwall 
            if self.is_near(bwall.pos.x, bwall.pos.y):
                if not self.stalled:
                    # if stalled is false, start a timer with it
                    self.stalled = pg.time.get_ticks()
                else:
                    # if i am stalled
                    time_end = pg.time.get_ticks() 
                    if time_end - self.stalled >= 6000:
                        # if i have been touching this wall and not reset yet
                        print(f"[{self.myname}] I'm Stalled, Change My Velocity -> {self.vel}") 
                        random_rot_angle_adjust = randint(-50,50)
                        self.vel = vec(-250, 0).rotate(-self.rot + random_rot_angle_adjust)
                        self.look_at(bwall.rect.center)
                        self.stalled = False
                        """



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
    
    # decorator template to add for pg.time.get_ticks() timings 

    # def perfTimer(self, func): # func:FunctionType
    #     """ new test for performance timer decorator """
    #     def wrapper(*args, **kwargs):
    #         """ the wrapper to do start and end the performance timing around running the entirety of the given function and getting its return value, returns the value at the end """
    #         # define long line for log formatting
    #         longlong = "- - - - - - - - - - - - - - - - - - - - -"
    #         # start timer
    #         start = pg.time.get_ticks()
    #         # run function
    #         rv = func(*args, **kwargs)
    #         # end timer
    #         total = perf_counter() - start
    #         # log timings
    #         funcName = f"{func=}"
    #         print(f"{longlong}\nTimer Result\n- {self.clean_functName(funcName)}: {total:.4f} secs\n{longlong}")
    #         # return the result of the function that ran
    #         return(rv)
    #     # return the entire thing and run it
    #     return(wrapper)
