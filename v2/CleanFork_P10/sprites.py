import pygame as pg
from random import uniform, randint, choice
from settings import *
from tilemap import collide_hit_rect
# New
from math import hypot 
vec = pg.math.Vector2

# some handy fonts
# FONT_DAYDREAM_22, FONT_UPHEAVTT_22, FONT_KA1_22, FONT_KAPPA_BLACK_22, FONT_MEMESBRUH_22

###########################################
# ---- stuff for its own module asap ---- #
###########################################

# -- unit HUD functions --

# 100% want this stuff to be in a unit parent class
def draw_unit_level(self): # [CUSTOM]
    if isinstance(self, Mob):
        # if sprite is zombie mob
        BOX_SIZE = 28  
        x, y = self.pos.x, self.pos.y 
        in_place_move = ((int(TILESIZE/2) - 30) + int(TILESIZE/2), -int(TILESIZE/2) - 6 - 10)
        in_place_move_text = ((BOX_SIZE/2 - 6), 1)
        self.level_textsurface = self.game.FONT_SILK_REGULAR_18.render(f"{self.power_level}", True, WHITE) # "text", antialias, color
    else:
        # else is player sprite
        BOX_SIZE = 34
        x, y = self.pos.x, self.pos.y
        in_place_move = ((int(TILESIZE/2) - 45) + int(TILESIZE/2) - 6, -int(TILESIZE/2) - 11 - 10 - 6)
        in_place_move_text = ((BOX_SIZE/2 - 7), 1)
        # not properly implemented but leaving the skeleton so when its needed, if 2 digit number in level box we need to resize the box and the font and reposition too
        if self.power_level >= 10:
            self.level_textsurface = self.game.FONT_SILK_REGULAR_18.render(f"{self.power_level}", True, WHITE) # "text", antialias, color
        else:
            self.level_textsurface = self.game.FONT_SILK_REGULAR_22.render(f"{self.power_level}", True, WHITE) # "text", antialias, color
    # note this should be slightly bigger than the unit health bar size btw so when hardcoding do this properly, aka dynamic from it
    level_box_fill = pg.Rect(x, y, BOX_SIZE, BOX_SIZE)
    level_box_outline_rect = pg.Rect(x, y, BOX_SIZE, BOX_SIZE)
    # before we draw it apply the camera to it, the move ip does nothing but left incase in future we wanna reposition the bars, use move ip instead
    level_box_fill = self.game.camera.apply_to_rect(level_box_fill).copy()
    level_box_outline_rect = self.game.camera.apply_to_rect(level_box_outline_rect).copy()
    # then move it by anything else
    level_box_fill.move_ip(in_place_move) 
    level_box_outline_rect.move_ip(in_place_move) 
    # then draw to screen
    pg.draw.rect(self.game.screen, BLUEMIDNIGHT, level_box_fill)
    pg.draw.rect(self.game.screen, DARKGREY, level_box_outline_rect, 3)
    # finally draw the actual number representing this unit/zombies level in that box
    destination = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
    destination = self.game.camera.apply_to_rect(destination).copy()
    destination.move_ip(in_place_move) # move the text to the bg box position
    destination.move_ip(in_place_move_text) # then do an additional nudge to centralise the text
    self.game.screen.blit(self.level_textsurface, destination)

# add a char limit to this once implementing statuses
def draw_unit_status(self): # [CUSTOM]
    x, y = self.pos.x, self.pos.y # refactored to take the same x and y and just change the in place move coordinates, note positions are in relation to the surface obvs
    if isinstance(self, Mob):
        # if sprite is zombie mob  
        in_place_move = (int(TILESIZE/2) + int(TILESIZE/2) + 2, -int(TILESIZE/2) - 10 - 30)
    else:
        # else is player sprite
        in_place_move = int(TILESIZE/2) + 20, -int(TILESIZE) - 10 # (int(TILESIZE/2) + int(TILESIZE/2) + 2, -int(TILESIZE/2) - 10 - 30)
    # set the status to be a string with commas if it is a list, else its just the given string
    status = self.my_status if isinstance(self.my_status, str) else ", ".join(self.my_status)
    self.name_textsurface = self.game.FONT_SILK_REGULAR_10.render(f"{status}", True, RED) # "text", antialias, color
    test_rect = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
    destination = self.game.camera.apply_to_rect(test_rect).copy()
    destination.move_ip(in_place_move) # better way to handle moving things btw donkey!, also btw, ip = in place
    self.game.screen.blit(self.name_textsurface, destination)

def draw_unit_health(self): # [CUSTOM]
    # define the unit type at the start for any changes in ui we may add to player, mob, companion, obstacle, item, npc, etc
    if isinstance(self, Mob):
        # if sprite is zombie mob  
        x, y = self.pos.x + int(TILESIZE/2) + int(TILESIZE/2), self.pos.y - int(TILESIZE/2) - 10 # positions in relation to the surface
        unit_type = "mob"
        BAR_LENGTH = 100
        BAR_HEIGHT = 16 # 20
    else:
        # else is player sprite
        x, y = self.pos.x, self.pos.y + 20 # slightly different, should really be refactored, wouldnt be that long tbf
        unit_type = "player"
        BAR_LENGTH = 140
        BAR_HEIGHT = 18 # 20
    # for strips between bars, serves to indicate a block/chunk of hp and ** not ** relative to the bar length
    BAR_HP_SEGMENT = 50
    BAR_SEGMENT_COUNT = self.max_health / BAR_HP_SEGMENT
    SEGMENT_LENGTH = BAR_LENGTH / BAR_SEGMENT_COUNT # set the x segments even based on the BAR_SEGMENT_HP e.g. 50, 100, 150 for 175 hp
    # in cases when we pass a negative, pin it at 0 so it doesnt go under
    if self.current_health < 0:
        self.current_health = 0
    # calculate the percentage of hp remaining and convert it based on the bar size
    health_remaining_percent = self.current_health / self.max_health
    fill = BAR_LENGTH * health_remaining_percent
    # define the inner and outer rect objects that will be drawn
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    # what colour
    if health_remaining_percent >= 0.6:
        col = GREEN
    elif health_remaining_percent >= 0.3:
        col = YELLOW
    else:
        col = RED
    # again before drawing, ensure we move these bars based on the cameras position too
    fill_rect = self.game.camera.apply_to_rect(fill_rect).copy()
    outline_rect = self.game.camera.apply_to_rect(outline_rect).copy()
    if unit_type == "player":
        fill_rect.move_ip(int(TILESIZE/2) + 20, -int(TILESIZE))
        outline_rect.move_ip(int(TILESIZE/2) + 20, -int(TILESIZE))
    # first draw the outline and inner rect on the surface we said, in the colour we said, using the fill_rect we've passed
    pg.draw.rect(self.game.screen, col, fill_rect)
    pg.draw.rect(self.game.screen, DARKGREY, outline_rect, 2)
    # then loop to draw the segments, which are stubby split indicator bars between to show blocks/chunks of hp 
    for i in range(int(BAR_SEGMENT_COUNT)):
        if not int(SEGMENT_LENGTH * (i+1)) >= ((BAR_LENGTH / 100) * 95): # if the segment would be placed at the very end of the bar (5% buffer to the end), due to border and small width placing it outside the outline rect, either move it down slightly, or just dont place it (latter for now)
            # for segment bar height have longer/shorter for 50s and 100s
            if i % 2 == 0:
                segment_height = 2
            else:
                segment_height = 1.5
            # it is even, so make it longer
            segment_rect = pg.Rect(x + (SEGMENT_LENGTH * (i+1)), y, 2, (BAR_HEIGHT / segment_height)) # for width -> 2 = thin, 1 = waffer thin, 4 = pretty chunky 
            # again before drawing, ensure we move these bars based on the cameras position too
            segment_rect = self.game.camera.apply_to_rect(segment_rect).copy()   
            if unit_type == "player":
                segment_rect.move_ip(int(TILESIZE/2) + 20, -int(TILESIZE))        
            pg.draw.rect(self.game.screen, DARKGREY, segment_rect, 2)                   
    # for debuggy
    want_debuggy = False
    if want_debuggy:
        print(f"{self.myname.title()} : hp blocks = {BAR_SEGMENT_COUNT}, {self.current_health}hp of {self.max_health = }hp remaining")
        print(f"{i+1 = }, {(i+1) * SEGMENT_LENGTH = }, {BAR_SEGMENT_COUNT = }, {int(BAR_SEGMENT_COUNT) = }")

# -- general sprite functions --

def round_to_base(x, base=5): # [CUSTOM]
    """ defaults to 5 """
    return base * round(x/base)

def how_near(self, x, y): # [CUSTOM]
    # use hypotenus of the xy vectors to find out how close we are to the given vector pos
    pythag_dist = hypot(self.pos.x-x, self.pos.y-y)
    return pythag_dist

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


###########################################


class Mob(pg.sprite.Sprite): # heremob herezombie
    zombie_counter = 1 # class var for ids

    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = choice(MOB_SPEEDS)
        # new custom variables
        self.myname = self.get_first_name()
        self.power_level = self.set_power_level()
        # important! => starting health is reliant on power_level
        self.max_hp_amount = self.set_max_hp_amount() # self.current_health = MOB_HEALTH
        self.min_hp_amount = self.set_min_hp_amount()
        self.max_health = round_to_base(self.set_initial_health())
        self.current_health = self.max_health # should rename to 'current health' asap btw to avoid confusion
        # more new custom variables
        self.myid = Mob.zombie_counter
        Mob.zombie_counter += 1
        self.my_status = self.get_status()
        # new for booleans on hit idea
        self.attack_timer = 0
        self.landed_attack = False # so its only 1 hit and not time colliding
        # new damage update for boolean hits and hit types
        self.my_damage = 15 # will be adding this properly shortly
        self.my_knockback = 15 # and this too, smaller knockback if proximity hit, bigger if charged
        self.hit_charge_up_time = 1000 # basically how long it takes to fill the bar, we want to be able to make this faster after a proximity hit but not a swipe
        # new for ui updates based on unit clumping
        self.is_clumped = False
        # debuggy init values
        print(f"{self.myname}: {self.max_hp_amount = }, {self.min_hp_amount = }, {self.max_health = }, LVL={self.power_level}")

    def set_max_hp_amount(self): # [CUSTOM]
        base_max_hp_amount = 200
        level_adjusted_max_hp_amount = base_max_hp_amount + (50 * (self.power_level - 1)) # -1 so at level 1 there is no additional bonus but is so minor it can be changed tbf
        return level_adjusted_max_hp_amount

    def set_min_hp_amount(self): # [CUSTOM]
        base_min_hp_amount = 200
        level_adjusted_min_hp_amount = base_min_hp_amount + (50 * (self.power_level - 1)) # -1 so at level 1 there is no additional bonus but is so minor it can be changed tbf
        return level_adjusted_min_hp_amount

    def set_power_level(self): # [CUSTOM]
        # guna do properly shortly, for now just a random range is fine say 1 - 5
        return randint(1,5) # ideally would be like 1 - 2/3/4 but idk how incremental we are guna get with it and what the max is yet so dw

    def avoid_mobs(self):
        # loop thru all the mobs and get the arrows/vectors for how we push away from any other zombie close to us
        for mob in self.game.mobs:
            # not the current mob we're on tho, ignore that apart from setting its 'is clumped' var
            dist = self.pos - mob.pos # the arrow pointing from mob were on to the one we wanna move away from
            # print(f"{self.myid}. {self.myname}: {dist.length() = } -> avoid? {0 < dist.length() < AVOID_RADIUS} -> [{self.game.mobs}]")
            # use avoid radius to tweek how the mobs group up
            if 0 < dist.length() < AVOID_RADIUS: # if 2 mobs on top of each other theyre dist will be zero so consider this also 
                self.acc += dist.normalize() # add the distance normalised to our acceleration (to make it a length of 1)
                mob.is_clumped = True
            # -- new test --
            # if you are close to another zombie but not clumping, so say double avoid range
            elif 0 < dist.length() < AVOID_RADIUS * 2.5:
                # -- note --
                # for this also use self.game.mobs to check how many are near by, 2 or 3 idm showing slight overlap on this few names, but more it becomes too much
                # -- end note -- 
                # flag this mob so we dont display all of the ui stuff for it, just its hp bar
                mob.is_clumped = True
            # else ur +3x the avoid rad so should be chill for full ui as ur not clumped
            else:
                mob.is_clumped = False
            # -- CRIT FOR FIXING IS CLUMPED --
            # - you really just need to know who ur around as one always has theirs on lol

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc = vec(1, 0).rotate(-self.rot) # now acc just a single unit vector (no mob speed)
        self.avoid_mobs() 
        self.acc.scale_to_length(self.speed) # then scale our final direction acceleration to whatever speed it should be (as the vectors were normalised to 1 before)
        # new - might move tbf
        # check if clumped, if so toggle this so we can update the units ui bar
        print(f"{self.myid}. {self.myname} : {self.is_clumped = }")
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.current_health <= 0:
            self.kill()

    def get_status(self): # [CUSTOM]
        # just as temp af rn so can randomise the status just to see how the display will look at certain char widths, not intended to be planned implementation of statuses
        list_of_statuses = ["Roaming", "Hunting",f"{self.speed}kph", f"{self.speed}mph"]
        return choice(list_of_statuses)

    def get_first_name(self): # [CUSTOM]
        list_of_names = ["Zob", "Zenjamin", "Zames", "Zohn", "Zichard", "Zhomas", "Zhristopher", "Zaniel", "Znthony"]
        return(list_of_names[randint(0, 8)])

    def set_initial_health(self): # [CUSTOM]
        # sets the health to a random int from the min and max health variables
        random_hp = randint(self.min_hp_amount, self.max_hp_amount)
        return random_hp if random_hp >= self.min_hp_amount * 1.2 else self.min_hp_amount # if not more than a 50% increase, set it to the min/floor value to give game difficuly more consistency 

    def draw_unit_action_chargebar(self, pct=97):
        BAR_LENGTH = 97
        BAR_HEIGHT = 4 # 20
        x, y = self.pos.x + int(TILESIZE/2) + int(TILESIZE/2), self.pos.y - int(TILESIZE/2) - 10 
        if pct > BAR_LENGTH: # just incase we get a number that is bigger
            pct = BAR_LENGTH
        chargebar = pg.Rect(x, y, pct, BAR_HEIGHT)
        chargebar = self.game.camera.apply_to_rect(chargebar).copy()
        chargebar.move_ip(1,17) # (-10, TILESIZE/2) # better way to handle moving things btw donkey!, also btw, ip = in place
        chargebar_background = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        chargebar_background = self.game.camera.apply_to_rect(chargebar_background).copy()
        chargebar_background.move_ip(1,17) # (-10, TILESIZE/2) # better way to handle moving things btw donkey!, also btw, ip = in place
        pg.draw.rect(self.game.screen, GREY, chargebar_background)
        pg.draw.rect(self.game.screen, ORANGE, chargebar)

    def draw_unit_name(self): # [CUSTOM] # FONT_MARBELLA_ARMY_22 FONT_OLDSTAMPER_22 FONT_TAKECOVER_22
        self.name_textsurface = self.game.FONT_SILK_REGULAR_14.render(f"{self.myname}", True, WHITE) # "text", antialias, color # FONT_SILK_REGULAR_14 # FONT_ARMYRUST_22
        x, y = self.pos.x + int(TILESIZE/2) + int(TILESIZE/2), self.pos.y - int(TILESIZE/2) - 10
        test_rect = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.game.camera.apply_to_rect(test_rect).copy()
        destination.move_ip(2, -20) # better way to handle moving things btw donkey!, also btw, ip = in place
        self.game.screen.blit(self.name_textsurface, destination)
       
    def draw_name(self): # [DEPRECIATED] [CUSTOM]
        """ og way, draws the image underneath the zombie with some light regard to its rotation """
        # then before we draw the name rotate it to where we want it to be, since we're doing it with blit in relation to the camera
        self.name_textsurface = self.game.FONT_SILK_REGULAR_12.render(f"{self.myname}", True, BLACK) # (f"{self.myname} {self.health}", True, BLACK)  # "text", antialias, color
        # e.g. this will rotate to face the player => pg.transform.rotate(textsurface, self.game.player.rot)
        #if self.rot > -135 and self.rot < -45: # only do our rotation at certain angles based on the zombie
        self.name_textsurface = pg.transform.rotate(self.name_textsurface, self.rot + 90) # if at this angle rotate my name
        return self.name_textsurface


class Bullet(pg.sprite.Sprite): # herebullet
    bullet_counter = 1

    def __init__(self, game, pos, dir):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.hit_rect = self.rect
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        # more new custom variables
        self.myid = Bullet.bullet_counter
        Bullet.bullet_counter += 1

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()           

class MuzzleFlash(pg.sprite.Sprite): # heremuzzleflash # hereflash
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites 
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20,50)
        self.image =pg.transform.scale(choice(game.gun_flashes), (size, size)) # scale it to a random size
        self.rect = self.image.get_rect()
        self.pos = pos 
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        # has it been long enough to despawn
        check_time = pg.time.get_ticks()
        if check_time - self.spawn_time > FLASH_DURATION:
            self.kill()


class Obstacle(pg.sprite.Sprite): # herewalls # hereobstacles
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls # not even in all sprites as its not drawn just invisibly sits on top of obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = pg.Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.rect.x = x 
        self.rect.y = y # we just get the pixel/grid pos back so its fine


# generic parent class for item
class Item(pg.sprite.Sprite): # hereitems
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites 
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos





class Wall(pg.sprite.Sprite): # herewall
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
