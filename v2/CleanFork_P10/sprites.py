import pygame as pg
from random import uniform, randint
from settings import *
from tilemap import collide_hit_rect
# New
from math import hypot 
vec = pg.math.Vector2

###########################################
# ---- stuff for its own module asap ---- #
###########################################

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


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.current_health = PLAYER_HEALTH

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)
                self.vel = vec(-KICKBACK, 0).rotate(-self.rot)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


class Mob(pg.sprite.Sprite): # heremob herezombie
    zombie_counter = 1 # class var for ids

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
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
        # new for boolean on hit idea, rn testing for chargebar tho
        self.attack_timer = 0
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

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
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
        # kinda just as temp af rn so can randomise the status just to see how the display will look at certain char widths, not intended to be planned implementation of statuses
        list_of_statuses = ["Roaming", "Hunting"]
        roll = randint(0,2)
        if roll == 2:
            return list_of_statuses
        else:
            return list_of_statuses[roll]

    def get_first_name(self): # [CUSTOM]
        list_of_names = ["Zob", "Zenjamin", "Zames", "Zohn", "Zichard", "Zhomas", "Zhristopher", "Zaniel", "Znthony"]
        return(list_of_names[randint(0, 8)])

    def set_initial_health(self): # [CUSTOM]
        # sets the health to a random int from the min and max health variables
        random_hp = randint(self.min_hp_amount, self.max_hp_amount)
        return random_hp if random_hp >= self.min_hp_amount * 1.2 else self.min_hp_amount # if not more than a 50% increase, set it to the min/floor value to give game difficuly more consistency 

    # HUD functions
    def draw_unit_level(self): # [CUSTOM]
        BOX_SIZE = 28 # current box size = 20, note this should be slightly bigger than the unit health bar size btw so when hardcoding do this properly, aka dynamic from it
        x, y = (self.pos.x + int(TILESIZE/2) - 30) + int(TILESIZE/2), self.pos.y - int(TILESIZE/2) - 6 - 10 # scoot back and up a tad from the unit health display to be centralised
        level_box_fill = pg.Rect(x, y, BOX_SIZE, BOX_SIZE)
        level_box_outline_rect = pg.Rect(x, y, BOX_SIZE, BOX_SIZE)
        # before we draw it apply the camera to it, the move ip does nothing but left incase in future we wanna reposition the bars, use move ip instead
        level_box_fill = self.game.camera.apply_to_rect(level_box_fill).copy()
        level_box_fill.move_ip(0, 0) # (-10, TILESIZE/2) # better way to handle moving things btw donkey!, also btw, ip = in place
        level_box_outline_rect = self.game.camera.apply_to_rect(level_box_outline_rect).copy()
        level_box_outline_rect.move_ip(0, 0) # better way to handle moving things btw donkey!, also btw, ip = in place
        pg.draw.rect(self.game.screen, BLUEMIDNIGHT, level_box_fill)
        pg.draw.rect(self.game.screen, DARKGREY, level_box_outline_rect, 3)
        # finally draw the actual number representing this unit/zombies level in that box
        self.level_textsurface = self.game.FONT_SILK_REGULAR_18.render(f"{self.power_level}", True, WHITE) # "text", antialias, color
        temp_rect = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.game.camera.apply_to_rect(temp_rect).copy()
        destination.move_ip(BOX_SIZE/2 - 7, 1)
        self.game.screen.blit(self.level_textsurface, destination)

    # add a char limit to this once implementing statuses
    def draw_unit_status(self): # [CUSTOM]
        status = self.my_status if isinstance(self.my_status, str) else ", ".join(self.my_status)
        self.name_textsurface = self.game.FONT_SILK_REGULAR_10.render(f"{status}", True, RED) # "text", antialias, color
        x, y = self.pos.x + int(TILESIZE/2) + int(TILESIZE/2), self.pos.y - int(TILESIZE/2) - 10
        test_rect = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.game.camera.apply_to_rect(test_rect).copy()
        destination.move_ip(2, -30) # better way to handle moving things btw donkey!, also btw, ip = in place
        self.game.screen.blit(self.name_textsurface, destination)

    def draw_unit_action_chargebar(self, pct=97):
        BAR_LENGTH = 97
        BAR_HEIGHT = 4 # 20
        x, y = self.pos.x + int(TILESIZE/2) + int(TILESIZE/2), self.pos.y - int(TILESIZE/2) - 10 
        if pct > BAR_LENGTH: # just incase we get a number that is bigger
            pct = BAR_LENGTH
        chargebar = pg.Rect(x, y, pct, BAR_HEIGHT)
        chargebar = self.game.camera.apply_to_rect(chargebar).copy()
        chargebar.move_ip(2,17) # (-10, TILESIZE/2) # better way to handle moving things btw donkey!, also btw, ip = in place
        chargebar_background = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        chargebar_background = self.game.camera.apply_to_rect(chargebar_background).copy()
        chargebar_background.move_ip(2,17) # (-10, TILESIZE/2) # better way to handle moving things btw donkey!, also btw, ip = in place
        pg.draw.rect(self.game.screen, GREY, chargebar_background)
        pg.draw.rect(self.game.screen, ORANGE, chargebar)

    def draw_unit_name(self): # [CUSTOM]
        self.name_textsurface = self.game.FONT_SILK_REGULAR_14.render(f"{self.myname}", True, WHITE) # "text", antialias, color
        x, y = self.pos.x + int(TILESIZE/2) + int(TILESIZE/2), self.pos.y - int(TILESIZE/2) - 10
        test_rect = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.game.camera.apply_to_rect(test_rect).copy()
        destination.move_ip(2, -20) # better way to handle moving things btw donkey!, also btw, ip = in place
        self.game.screen.blit(self.name_textsurface, destination)

    def draw_unit_health(self): # [CUSTOM]
        # basic bar setup for mob character
        BAR_LENGTH = 100
        BAR_HEIGHT = 16 # 20
        # for strips between bars, serves to indicate a block/chunk of hp and ** not ** relative to the bar length
        BAR_HP_SEGMENT = 50
        BAR_SEGMENT_COUNT = self.max_health / BAR_HP_SEGMENT
        SEGMENT_LENGTH = BAR_LENGTH / BAR_SEGMENT_COUNT # set the x segments even based on the BAR_SEGMENT_HP e.g. 50, 100, 150 for 175 hp
        # positions in relation to the surface
        x, y = self.pos.x + int(TILESIZE/2) + int(TILESIZE/2), self.pos.y - int(TILESIZE/2) - 10 # half a tile to the right, and up by a tad
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
        # first draw the outline and inner rect on the surface we said, in the colour we said, using the fill_rect we've passed
        pg.draw.rect(self.game.screen, col, fill_rect)
        pg.draw.rect(self.game.screen, DARKGREY, outline_rect, 2)
        # then loop to draw the segments, which are stubby split indicator bars between to show blocks/chunks of hp 
        for i in range(int(BAR_SEGMENT_COUNT)):
            if not int(SEGMENT_LENGTH * (i+1)) >= ((BAR_LENGTH / 100) * 95): # if the segment would be placed at the very end of the bar (5% buffer to the end), due to border and small width placing it outside the outline rect, either move it down slightly, or just dont place it (latter for now)
                # ------------ THIS DOESNT WORK AND IDK WHY BUT JUST MOVING ON FOR NOW :( ------------ #
                # for segment bar height have longer/shorter for 50s and 100s
                if i+1 % 2 == 0:
                    segment_height = 4
                else:
                    segment_height = 2
                # it is even, so make it longer
                segment_rect = pg.Rect(x + (SEGMENT_LENGTH * (i+1)), y, 2, (BAR_HEIGHT / segment_height)) # for width -> 2 = thin, 1 = waffer thin, 4 = pretty chunky 
                # again before drawing, ensure we move these bars based on the cameras position too
                segment_rect = self.game.camera.apply_to_rect(segment_rect).copy()                    
                pg.draw.rect(self.game.screen, DARKGREY, segment_rect, 2)                   
        # for debuggy
        want_debuggy = False
        if want_debuggy:
            print(f"{self.myname.title()} : hp blocks = {BAR_SEGMENT_COUNT}, {self.current_health}hp of {self.max_health = }hp remaining")
            print(f"{i+1 = }, {(i+1) * SEGMENT_LENGTH = }, {BAR_SEGMENT_COUNT = }, {int(BAR_SEGMENT_COUNT) = }")
       
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
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
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


class Wall(pg.sprite.Sprite): # herewall
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
