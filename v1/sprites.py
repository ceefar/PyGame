import pstats
import pygame as pg
from settings import *
from tilemap import collide_hit_rect
# start using vectors instead of individual xypos vars
vec = pg.math.Vector2
# for calculating distance between 2 objects
from math import hypot
# for random numbers, uniform is real numbers between given range
from random import randint, uniform
# for fake names
from faker import Faker

# make wall collisions func global as is useful for more stuff now
# should also do the same with get dinstance tbf lol
# need to refactor this so it actually works just with group lol
def collide_with_walls(sprite, group, dir):
    # if checking an x collision, note were using a custom hitbox hit_rect now
    if dir == "x":
        # then check if we the player have collied with a wall
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # if i have hit something, check which side is it left or right using our velocity (which direction and where are we moving to)
            # if we were moving to the right when we collided with the wall, so put ourselves on that side of the wall
            if sprite.vel.x > 0:
                # our x should be what ever it was that we hit(s) minus however wide we are
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            # if the speed is the opposite direction then we were moving to the left so
            if sprite.vel.x < 0:
                # put ourselves to the right of the thing we hit(s)[0]
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            # regardless of where we hit we are going to stop ourselves moving on this axis (x), because we've hit a wall to either side of us
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x        
        bhits = pg.sprite.spritecollide(sprite, sprite.game.breakablewalls, False, collide_hit_rect)
        if bhits:
            # if i have hit something, check which side is it left or right using our velocity (which direction and where are we moving to)
            # if we were moving to the right when we collided with the wall, so put ourselves on that side of the wall
            if bhits[0].get_hp() <= 0:
                # bhits[0].try_repair_wall()
                pass # through freely                
            else:
                if sprite.vel.x > 0:
                    # our x should be what ever it was that we hit(s) minus however wide we are
                    sprite.pos.x = bhits[0].rect.left - sprite.hit_rect.width / 2
                # if the speed is the opposite direction then we were moving to the left so
                if sprite.vel.x < 0:
                    # put ourselves to the right of the thing we hit(s)[0]
                    sprite.pos.x = bhits[0].rect.right + sprite.hit_rect.width / 2
                # regardless of where we hit we are going to stop ourselves moving on this axis (x), because we've hit a wall to either side of us
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x    
    if dir == "y":
        bhits = pg.sprite.spritecollide(sprite, sprite.game.breakablewalls, False, collide_hit_rect)
        # breakable wall
        if bhits:
            # print(f"Collided Wall Hp : {bhits[0].get_hp()}")
            if bhits[0].get_hp() <= 0:
                # bhits[0].try_repair_wall()
                pass # through freely
            else:
                if sprite.vel.y > 0:
                    sprite.pos.y = bhits[0].rect.top - sprite.hit_rect.height / 2
                if sprite.vel.y < 0:
                    sprite.pos.y = bhits[0].rect.bottom + sprite.hit_rect.height / 2
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y             
        # normal wall    
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y  


class Player(pg.sprite.Sprite):

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
        self.player_prizemoney = 0 # some kinda idea of banking gold after a set amount of levels, maybe the amount banked also provides bonuses like bonus exp, extra unlocks (for hoarding and not spending etc)
        # note defo have more things that make u get paid for hampering urself
        # maybe even presenting as option at level start
        # new test, pause interactions
        self.waiting_print = False
        self.waiting = False
        # new auto-shooting toggle test
        self.autoshoot = False
        self.toggle_wait = False

        # new player rating test stuff - clout rating boom
        self.clout_rating = 10 # work in integers for now, but want this to represent the float 1, so its 1.0, 11 would be 1.1, so double clout_rating from base is 20
        # obvs need to handle and update clout, and zombies will be affected by ur clout too 

        # new player damage stuff, actually altering og code quite substantially for this but will be fine
        self.player_damage = BULLET_DAMAGE

    def get_keys(self):
        self.rot_speed = 0 # normally will be zero, works the same as velocity, hold it down one way increases that way
        self.vel = vec(0, 0) # define what our keys are going to do
        keys = pg.key.get_pressed() # see which keys are currently held down
        # -------- dev keys stuff - might integrate tho --------
        if keys[pg.K_p]:
            if not self.toggle_wait: # its lazy but its the autoshoot toggle so its not guna get used enough to matter rn chill
                print(f"Episode Earnings = {self.player_gold} gold, Take Home PrizeMoney = {self.player_gold} gold")
                self.toggle_wait = pg.time.get_ticks()
        # -------- player interaction keys stuff --------
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
                # temp af for now but should increase the shooting speed by a factor of 2 if not in auto shoot
                now = pg.time.get_ticks() # track the last time we shot 
                if now - self.last_shot > BULLET_RATE:
                    self.last_shot = now 
                    dir = vec(1,0).rotate(-self.rot)
                    pos = self.pos + BARREL_OFFSET.rotate(-self.rot) # rotated to match the players direction
                    Bullet(self.game, pos, dir)
                    self.vel = vec(-GUN_KICKBACK,0).rotate(-self.rot)
        # pass the game, the player(pos), and the rotation vector we've just figured out (where the player is facing)
        # -- action key --    
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
        # -------- player sprint stuff --------    
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            # [ todo ] - own function, is sprinting / handle sprinting - new sprint implementation, only called when holding sprint so any sprint meter stuff needs to be done outside here duh
            self.vel *= self.get_sprint_multiplier() 
            self.state_moving = "sprinting"
            self.sprint_meter -= self.sprint_meter / 100
        # [ duh! ] - if we are defo not sprinting things here
        else:
            #self.image = self.game.player_img
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
                
    def update(self):
        self.get_keys()
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
        collide_with_walls(self, self.game.walls, 'x')
        # basically were doing 2 collision check, 1 for each axis
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y') 
        # after collision make sure our regular rect is set to the position of our hit rect, 
        # since we're now updating the hict rects position (not rotation, or velocity, just pos) 
        # if it collides (by moving in the opposite of where we tried to move), so we need to reapply this transformation to the player and not just the hitbox
        self.rect.center = self.hit_rect.center

        # [ todo-asap! ] - new function
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
                    
                    # still big issue with shooting order, need to be checking whos closest? idk need to confirm tbf
                    # just do collisions quickly ffs

                    # use faker to give the zombies fake names, 
                    # have their names be part of their class so can use it obvs 
                       
        
class Mob(pg.sprite.Sprite):
    showmaker = Faker()
    Zombie_Boys = {} # maybe un-needed, cant remember exactly what is used for rn

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
        self.vel = vec(0,0)
        self.acc = vec(0,0) # use accelerate now so that the zombie doesnt whip around at the same speed when we move past it
        # my own test stuff still but this is placed here as currently setting the hp again here so shouldnt be moving it away from self.health declaration
        # new damage based stuff
        # get a random number for our initial max health, else its 100
        self.max_health = self.set_init_hp()
        # then set the starting health to that max health
        self.health = self.max_health 

        # my own super test af stuff
        # this is literally the entire class object, not a class instance
        self.bwalls = bwalls
        # if has collided with a bwall, do climb in stuff, then hunt the player 
        self.climbed_in = False
        # add zombie to the class variable list and assign it an id too
        # could do stuff here too for different value zombies, difficulty, etc, all off random
        try: # make the zombies id the last id plus 1
            self.myid = list(Mob.Zombie_Boys.keys())[-1] + 1
        except IndexError: # except if the list is empty, then make the id 1
            self.myid = 1
        Mob.Zombie_Boys[self.myid] = self # add myself, the zombie instance, to the class dict
        self.waiting = False # give them their own waiting too, for breaking stuff and hiting the player
        self.waiting_speed = 500 # seconds so this is half a second, can say thats quick/avg for now
        # new stalled fixer test
        self.stalled = False
        # new name
        self.myname = self.showmaker.name()
        print(f"{self.myname} {'is roaming' if self.health <= 100 else 'is looking for blood'}... [ {self.health}hp ]")

    def set_init_hp(self):
        # for now keep this super simple and have the hp just be influenced by a random roll
        # in future pass the zombies class n shit and have that affect the base hp -> other things too like game diff, and character things like items, abilities, traits, etc
        roll_chance = randint(1, 10)
        #print(f"wantCrit? => {crit_chance = }, {actual_chance = }, {actual_chance >= crit_chance = }")
        # if our number range / numbers (our crit chance) is greater than or equal to our random chance 1 to 100 roll 
        if roll_chance <= 5:        
            maxhp = (randint(1, 10) * 10) + 200 # if the zombie won a 50/50 head or tails, then give it up to 100 more hp based on its second roll 1 - 10 
        else:
            maxhp = 200
        # should also include potential punishments this way too
        # also should make this more dynamic by giving each zombie traits like luck too
        return(maxhp)

    def draw_health(self):
        # simple hp bar
        if self.health >= (self.max_health / 10) * 6: # 60%
            col = GREEN
        elif self.health >= (self.max_health / 10) * 3: # greater than 30%
            col = YELLOW
        else: # else is 30% or less
            col = RED
        # width of bar is just the width of this zombies rect time the percent of hp remaining
        width = int(self.rect.width * self.health / self.max_health)
        # the location on the sprite image not on the screen
        self.health_bar = pg.Rect(0, 0, width, 7) # 7 is thickness
        # only draw the bar if the zombie is not full hp
        if self.health < self.max_health: 
            # draw that self.health_bar on top of our zombies rectangle in the given colour
            pg.draw.rect(self.image, col, self.health_bar) 

    def look_at(self, look_at_me):        
        # minus the players pos from this zombies pos to get the vector zombie -> to -> player
        # to get the angle, stick the given vector into to angle with the axis vector e.g. (1, 0) or forward in x, 0 in y i.e to the right, which is positive in the x axis
        self.rot = (look_at_me - self.pos).angle_to(vec(1,0))
        # then rotate our zombies img by the rotation vector
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        # then update our zombies new rectangle centre too
        self.rect = self.image.get_rect()

    def can_climb_in(self):
        bhits = pg.sprite.spritecollide(self, self.game.breakablewalls, False, collide_hit_rect)
        if bhits:
            if not self.climbed_in:
                # so here is ur warning stuff nice
                print(f"{self.myname} Broke In @ {self.pos.x}, {self.pos.y} [Collided With B Wall]")
            self.climbed_in = True
            self.stalled = False # cant be stalled outside, for now anyway

    def is_near(self, x, y):
            # abstract this properly pls 
            next_to = 15 # for 64 tilesize
            literally_next_to = 14
            # use hypotenus of the xy vectors to find out how close we are to the given vector pos
            pythag_dist = hypot(self.pos.x-x, self.pos.y-y)
            # if pythag_dist < next_to:
                # print(f"{self.myid=},{pythag_dist=}\n{x=},{y=},{self.pos.y=},{self.pos.x=}")
                # print(f"{pythag_dist=}, {self.myid}, {self.pos.x=}, {self.pos.y=}\n{x=}, {y=}")
            # if we are right next to the sprite our pythag_dist will be the size of the tile e.g. 32 
            return True if pythag_dist < next_to else False

    def break_barracade(self, bwall):
        if not self.waiting:
            # if the wall has hp and we can attack it then do it, basically dont interact with 0 hp walls at all
            if bwall.hp_current > 0:
                # check here, have i, the zombie, been standing next to a wall with hp
                # and been unable to break it? (im not waiting or sumnt)
                # well then bounce back (will do for now)
                #print(f"Zombie {self.myid} hit wall #{bwall.myid}, going from {bwall.hp_current}hp to {bwall.hp_current - 1}hp\n - zombie {self.myid} interactions temporarily disabled")
                # take down its hp, the action has now been confirmed so anything like animations and updates must happen now
                bwall.hp_current -= 1
                self.stalled = False #if you've done a hit you've stopped stalling, likewise if ur inside uve stopped stalling
                # bounce to the opposite of where u are in relation to the wall
                # when you make contact for this second 
                #print(f"Bounce Me! -> id:{self.myid}, pos:{self.pos}, vel:{self.vel}, acc:{self.acc}, rot:{self.rot}")
                # be sure we have some speed, otherwise the bounce wont be noticeable 
                if self.vel.x < 10 and self.vel.y < 10:  
                    self.vel = vec(-200,0).rotate(-self.rot) # NEW TEST AF
                elif self.vel.x > -10 and self.vel.x < 0 and self.vel.y > -10 and self.vel.y < 0:
                    self.vel = vec(-200,0).rotate(-self.rot)

                #self.vel.y = -self.vel.y
                self.acc.x -= (self.acc.x / 100) * 80
                self.acc.y -= (self.acc.y / 100) * 80
                #print(f"Bounce Me! -> id:{self.myid}, pos:{self.pos}, vel:{self.vel}, acc:{self.acc}, rot:{self.rot}")
                # then infect any touching walls
                bwall.infect_walls()
                # then pause any other interactions for this instance of mob for 1 second
                self.waiting = pg.time.get_ticks()
            # else go attack
            else:
                # really want some validation ur not stuck or sumnt here btw
                pass

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
                        random_rot_angle_adjust = randint(-40,40)
                        self.vel = vec(-100, 0).rotate(-self.rot + random_rot_angle_adjust)
                        self.look_at(bwall.rect.center)
                        self.stalled = False

    # i mean look we got some bouncing issues and many other issues but i 
        
    def update(self):
        list_of_bwall_dists = []
        closest_bwall = "" # not actually a string, becomes the object instance
        # new test stuff
        # if we have collided with a bwall, we have now climbed in, else this will still be false
        self.can_climb_in()
        # if we have climbed in we hunt the player, else we keep trying to climb in
        if self.climbed_in:
            # look at the player, and anything else associated with this toggle state
            self.look_at(self.game.player.rect.center)
        else:
            # else if we have not climbed in yet, loop the walls to find the closest wall etc, important as we can subvert calculating the distance for all walls for this zombie once it has entered (which actually means that this could easily gate us if complexity becomes large, amount of zombies outside walls + lots of bwalls at later levels so calc how many u can handle outside if its insane then dw)
            for bwall in self.bwalls:
                pythag_dist = hypot(self.pos.x-bwall.pos.x, self.pos.y-bwall.pos.y)
                # temp implementation of a warning for when zombie is close (would be like a screen arrow oooo)
                if pythag_dist < 500: # if zombie is close to door
                    pass
                    # some kinda warning arrow or maybe even state change idk
                    # print(f"ZOMBIE CLOSING IN TO DOOR WARNING!\nid:{bwall.myid}, pos:{bwall.pos}, dist:{pythag_dist}")
                list_of_bwall_dists.append(pythag_dist)
                if pythag_dist == min(list_of_bwall_dists):
                    closest_bwall = bwall
            # end loop all breakable walls
            # closest_bwall_dist = min(list_of_bwall_dists) incase we want to check the closest few which we will eventually but is there print(f"{closest_bwall_dist = } - {list_of_bwall_dists = }")
            # ****** need to do for 0 hp stuff here eventually ******
            # look at bwalls
            self.look_at(closest_bwall.pos)
        # ---- end , deciding who to look at)
        # ---- actual code ----
        # our acceleration is going to be mob speed constant, run in the forward direction rotated by whatever this zombies rotation is
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        # once we got the direction, quickly reduce the amount he accelerates by
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        # eq of motion, velocity times time times half the acceleration, times the time squared
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        # now we know where the sprite should be set its rect center
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls,'y')
        # then set our regular rect to our hit rect, remember we primarily use the hit rect then set it to the regular rect at the end (the visual doesnt match the pixel precision)
        self.rect.center = self.hit_rect.center
        # if the zombie health ever less than zero, kill it, idk why this isnt first in update tho? <= test it defo 
        # note-tho! => tbf for things like waiting i get that but surely not last last atleast mid is best but idk (nah waiting doesnt matter as its self.waiting not player but confirm tbf)
        if self.health <= 0:
            self.kill()
        
        # more testing (for breaking it down stuff)
        # check every breakable wall to see if a zombie is near
        for bwall in self.bwalls:
            # if zombie is near a bwall 
            if self.is_near(bwall.pos.x, bwall.pos.y):
                # print(f"ZOMBIE SPEED => {self.myid = }, {self.acc = }, {self.vel = }")
                if self.vel.x < 0.5 and self.vel.y < 0.5:
                    # this is the test for speed if you, the zombie have stalled, want this to pop but testing with pos for now
                    # if the walls x position is less than urs its to the left, else its to the right (?)
                    #if bwall.pos.x < self.pos.x:
                    pass
                # test break it
                self.break_barracade(bwall)
        # end by updating waiting
        if self.waiting:
            space_end = pg.time.get_ticks() 
            if space_end - self.waiting >= self.waiting_speed: # 1 second waiter rn
                print(f"interactions enabled")
                self.waiting = False
        # more new testing, this time for zombies stalled by entrances  
        self.am_i_stalled()


class Bullet(pg.sprite.Sprite):
    bullet_count = 0 # count all bullets shot for stats
    bullet_hit = 0 # track every hit

    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.count_hits = [] # list of ids of zombies ive passed through, and therefore counted as gold/damage/stats, for not counting gold or hits for every split second a bullet has collided
        # here, in above, could really be starting implementation of extra gold, e.g. if multi hit x2 gold, x3 = x3 etc!
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos).copy() # position is the one we pass in, pass a copy so we dont update the players position with the bullet... which is fucking hilarious btw
        self.rect.center = pos # put our rectangle there at the center
        if game.player.autoshoot:
            spread = uniform(-GUN_SPREAD*2, GUN_SPREAD*2) # autoshoot is more inaccurate so its not giga free, easily changed and is temp anyway tbf
        else:
            spread = uniform(-GUN_SPREAD, GUN_SPREAD) # bullet will come out at a random angle based on the spread, this should really update or be different for autoshoot but is fine for now
        self.vel = dir.rotate(spread) * BULLET_SPEED # our velocity is the direction vector (len 1 vector pointing in one direction) times by the bullet speed
        self.spawn_time = pg.time.get_ticks() # get our time when we spawn so we know when to delete ourself
        Bullet.bullet_count += 1
        self.myid = self.bullet_count
        self.is_crit = self.check_crit()
        # more new custom test stuff
        # self.hp = 30 # say going thru each zombie costs 10

    # new custom functionality testing
    def check_crit(self):
        # first check the players clout, if ur mad clouted then ur crit change increases (just keep it giga simple for now) 
        crit_chance = ((self.game.player.clout_rating / 10) * 5) + PISTOL_CRIT_RATE # div 10 so base would become 1, or double clout would become 2, then * 5, so 1 = 5 and 2 = 25, 95% chance normally, to 75% chance at double crit, its fine its just supposed to be sumnt for now lol
        # then you add the pistol crit rate to that floor value, i.e. 5, 10, 20, and you've got a floor value maybe thats like 30, so 30 - 100 = 70% chance
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
            # print(f"[ACTION] => Bullet [ {self.myid} ] hit zombie {hit_zombie.myid}") #myname
            # new crit test, not ideal as the way were doing collision rn i cant check the bullet just the zombie but its fine for now just playing around anyways, will do proper collisions soon 
            if self.is_crit: # if this is a crit bullet, and you've hit a zombie, set the player damage to 100
                # print("PLAYER DAMAGE = 100")
                self.game.player.player_damage = 100
                # but remember this is a temporary af hacky way so this will stay like that forever unless we put it back, we do that after the hit has been logged, if a 100 hit is logged, player_damage = 10, plus also if this bullet times out player damage = 10 # this will break af btw, e.g. bullets could get set to 200 or 300 etc is easy to fix but just saying dont forget lol
            if hit_zombie.myid not in self.count_hits:
                # print(f"Bullet {self.myid}, Zombie {hit_zombie.myid}, {self.count_hits = }")
                # if the zombies id is not already been stored for this bullet, then append the id to the bullet quickly so it knows
                self.count_hits.append(hit_zombie.myid)
                base_gold = base_gold + (base_gold * 0.2) # before doing anything we set the gold, the gold is worth 20% more if its a crit, should be hardcoding btw but was by items n shit so chill 4 now
                # if i passed through 1 person, basic gold
                if len(self.count_hits) == 1: 
                    base_gold *= 1 # temporary buff, difficulty, etc, here btw
                    #print(f"[ +{base_gold} ] -> NICE SHOT")
                    # if was crit etc
                if len(self.count_hits) == 2: 
                    base_gold *= 2
                    # or (as in on random for sure) # DOUBLE PENETRATION, TRIPLE PENETRATION!
                    # tf character voiceline... "ooo kinky... i like kinky"
                    # x = randint(1,10)
                    # print(f"[ +{base_gold} ] [ x2 ] BONUS! -> TWO ZEDS, ONE GUT") if x > 5 else print(f"[ x2 ] BONUS! -> DOUBLE PENETRATION")
                if len(self.count_hits) == 3: 
                    base_gold *= 3   
                    #print(f"[ +{base_gold} ] [ x3 ] BONUS! -> ZOMBIE CENTIPEDE!")                 
                self.game.player.player_gold += base_gold
                Bullet.bullet_hit += 1
                #print(f"[ +{self.game.player.player_gold} ] Gold -> Make It Rain!")
                #print(f"Bullet {self.myid} -> zombie entrants {self.count_hits}")
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME: # do a meeseeks
            self.kill() # delete the bullet
        


class Wall(pg.sprite.Sprite):
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


# [ todo! ] - so a InteractWall Class with even just is_near yanno (and then else valid for that)

class BreakableWall(pg.sprite.Sprite): # should be called barricades huh
    wall_ids = []
    
    def __init__(self, game, x, y, player, hp=4):
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
            # check if we this wall is near any other walls
            if a_wall.is_near(self.pos.x, self.pos.y):
                # if we both tiles dont have the same hp, update them so they are
                if a_wall.hp_current != self.hp_current:
                    self.print_once(f"Shared Our HP Commrade -> {a_wall.hp_current}, {self.hp_current}")
                    a_wall.hp_current = self.hp_current

    def update_image(self, is_near=False):
        """ every time something interacts with me, run this (?) """
        # if box has 0 hp
        if self.hp_current == 0:
            # [ testing! ]
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
        # [ todo-asap! ] - the reason it goes up by 2 is if touching 2 
        # [ todo-asap! ] - means same could happen with 3 too 
        # [ todo-asap! ] - so either take the amount touching into consideration 
        # [ todo-asap! ] - or fix a proper way
        # [ todo-asap! ] - actually tbf i think...
        # [ todo-asap! ] - that taking how many are touching into account IS the proper way lol <<<<<< THIS 
        # define vars that mean in future we could have like an action dist, even view dist maybe
        very_very_close = 30 # means in tight spaces only one side or the other but changing the map now anyway so this likely never gets used but nice for reference
        very_close = 50 # might not be agnostic of tilesize btw if changed from 64 that i think im using now
        # close = 80 #, 50, 30 < for 32x32 pixel tilessize 
        close = 180 # for 64 tilesize
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

    # [ todo-asap! ] - wall max hp broken again
    # [ todo-asap! ] - then continue tuts pls!

    # DARKGREY, GREY, LIGHTGREY, PRINT, RUST, HIGHLIGHTER, PALEGREY, TAN, COFFEE, MOONGLOW

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

# DO FAKER NAMES AND FINISH TUT PLS!



# DO SHOOTING TUT 1ST
# THEN TEST 4 HP WALLS
# THEN THE HP TUT
# THEN DO GOLD AND KILLSTREAKS!

