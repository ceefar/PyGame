import pygame as pg
from random import uniform, randint
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2

###########################################
# ---- stuff for its own module asap ---- #
###########################################

def round_to_base(x, base=5):
    """ defaults to 5 """
    return base * round(x/base)



###########################################

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

class Mob(pg.sprite.Sprite):
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
        self.max_hp_amount = 250 # self.current_health = MOB_HEALTH
        self.min_hp_amount = 100
        self.max_health = round_to_base(self.set_initial_health())
        self.current_health = self.max_health # should rename to 'current health' asap btw to avoid confusion
        self.myname = self.get_first_name()

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

    def get_first_name(self): # [CUSTOM]
        list_of_names = ["Zob", "Zenjamin", "Zames", "Zohn", "Zichard", "Zhomas", "Zhristopher", "Zaniel", "Znthony"]
        return(list_of_names[randint(0, 8)])

    def set_initial_health(self): # [CUSTOM]
        # sets the health to a random int from the min and max health variables
        random_hp = randint(self.min_hp_amount, self.max_hp_amount)
        return random_hp if random_hp >= self.min_hp_amount * 1.2 else self.min_hp_amount # if not more than a 50% increase, set it to the min/floor value to give game difficuly more consistency 

    # HUD functions
    def draw_unit_health(self): # [CUSTOM]
        # basic bar setup for mob character
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        # for strips between bars, serves to indicate a block/chunk of hp and ** not ** relative to the bar length
        BAR_HP_SEGMENT = 50
        BAR_SEGMENT_COUNT = self.max_health / BAR_HP_SEGMENT
        SEGMENT_LENGTH = BAR_LENGTH / BAR_SEGMENT_COUNT # set the x segments even based on the BAR_SEGMENT_HP e.g. 50, 100, 150 for 175 hp
        # positions in relation to the surface
        x, y = self.pos.x + 10, self.pos.y + 10 
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
        # debuggy
        print(f"{self.myname.title()} : hp blocks = {BAR_SEGMENT_COUNT}, {self.current_health}hp of {self.max_health = }hp remaining [ {health_remaining_percent} ]")
        # then draw it on the surface we said, in the colour we said, using the fill_rect we've passed
        pg.draw.rect(self.game.screen, col, fill_rect)
        pg.draw.rect(self.game.screen, DARKGREY, outline_rect, 2)

        # loop to draw the segments, which are stubby split indicator bars between to show blocks/chunks of hp 
        for i in range(BAR_SEGMENT_COUNT):
            print(f"{i = }, {i * SEGMENT_LENGTH = }")
            segment_rect = pg.Rect(x + (SEGMENT_LENGTH * i), y, 4, (BAR_HEIGHT / 2))
            pg.draw.rect(self.game.screen, DARKGREY, segment_rect, 2)
        
        
class Bullet(pg.sprite.Sprite):
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

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

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
