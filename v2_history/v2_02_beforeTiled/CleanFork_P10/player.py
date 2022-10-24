import pygame as pg
from random import uniform, randint
from settings import *
from tilemap import collide_hit_rect
# New
from sprites import *
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


class Player(pg.sprite.Sprite): # hereplayer
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
        # new custom variables
        # -- ui / general stuff --
        self.character_name = "PlayerName"
        self.power_level = 1 # randint(1,10) # will need to make this persistent soon, and also dynamically placed as does vary slightly on numbers, but for now this is fine
        self.max_health = PLAYER_HEALTH
        self.current_health = self.max_health
        self.my_status = "Vibin'"
        # -- new reloading stuff --
        # need to do this weapon stuff properly as classes asap, all ur doing is returning vars based on a string
        # legit just need a WeaponsHandler class with all the weapons in it bosh, i mean ideally with weapon classes too or slot classes idk but just simple to start is fine
        self.current_weapon = "pistol"
        self.weapon_clipsize = self.get_gun_clipsize()
        self.weapon_reload_speed = self.get_gun_reload_speed()
        self.weapon_bullet_rate = self.get_gun_bullet_rate()
         # you start with a full clip obvs, would be cute if you didnt reload at level end to start at the same tho
        self.bullets_remaining_in_clip = self.weapon_clipsize
        self.reload_chargebar = 0
        self.is_reloading = False
        self.current_weapon_slot = 0
        self.unlocked_weapons_list = ["pistol", "uzi"]
        self.current_weapon_img = self.get_gun_image()
        self.disable_weapon_change = False # if true cant change weapon, gets set to true when zombies are too close to you oooo
        self.change_weapon_cooldown = 0
        # need to add it so that when you change weapon you have the ammo for that clip? (else its always a new clip, which would be fine for now tbf)
        # debuggy
        # print(f"{self.weapon_clipsize = }, {self.weapon_reload_speed = }, {self.weapon_bullet_rate = }")

    def handle_change_weapon(self):
        # only allowed if not reloading, else if ur reloading do nothing 
        # ok also added if the zombies arent too close to you either
        if not self.is_reloading and not self.disable_weapon_change:
            # called when the player releases the weapon change button
            self.current_weapon_slot += 1
            # loop back to the start
            if self.current_weapon_slot >= len(self.unlocked_weapons_list):
                self.current_weapon_slot = 0
            # set the current weapon based on the index of the wanted item in the unlocked weapons list
            self.current_weapon = self.unlocked_weapons_list[self.current_weapon_slot]
            # set the current weapon vars based on the new current weapon
            self.weapon_clipsize = self.get_gun_clipsize()
            self.weapon_reload_speed = self.get_gun_reload_speed()
            self.weapon_bullet_rate = self.get_gun_bullet_rate()
            self.current_weapon_img = self.get_gun_image()
            # resets to a full clip each time u change weapon, is fine as you cant change weapon while reloading 
            # but do actually want each to have its own unique stats 
            # so make parent class gun and then pistol uzi etc etc 
            # initalise them all so they persist and you can have the player attributes update them and shit
            self.bullets_remaining_in_clip = self.weapon_clipsize 
            # start the cooldown timer so you cant spam it
            self.change_weapon_cooldown = pg.time.get_ticks()
            self.weapon_cooldown_timer = 3000 # 3 seconds is a bit long but maybe its more about the tension of that stuff, i.e. lots of weapon jams etc
            # temp debuggy
            print(f"{self.weapon_clipsize = }, {self.weapon_reload_speed = }, {self.weapon_bullet_rate = }")
            print(f"{self.current_weapon_slot = }, {self.current_weapon_slot = }, {self.current_weapon = }")

    # new rushed implementation before doing actual class/es for weapons / weapon handling
    def get_gun_clipsize(self): # [CUSTOM]
        # done like this so we can call to update it but probs not the ideal way to do it tbf
        if self.current_weapon == "pistol":
            return GUN_PISTOL_CLIPSIZE
        elif self.current_weapon == "uzi":
            return GUN_UZI_CLIPSIZE      

    def get_gun_image(self): # [CUSTOM]
        # done like this so we can call to update it but probs not the ideal way to do it tbf
        if self.current_weapon == "pistol":
            return self.game.gun_pistol_img
        elif self.current_weapon == "uzi":
            return self.game.gun_uzi_img          

    def get_gun_bullet_rate(self):
        if self.current_weapon == "pistol":
            return GUN_PISTOL_BULLET_RATE
        elif self.current_weapon == "uzi":
            return GUN_UZI_BULLET_RATE

    def get_gun_reload_speed(self): # [CUSTOM]
        if self.current_weapon == "pistol":
            return GUN_PISTOL_RELOAD_SPEED
        elif self.current_weapon == "uzi":
            return GUN_UZI_RELOAD_SPEED 

    def get_keys(self): # herekeys
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
        # -- trying to fire a shot by pressing space --
        if keys[pg.K_SPACE]: 
            now = pg.time.get_ticks()
            if self.bullets_remaining_in_clip <= 0: # if the clip is empty, reload
                self.is_reloading = True
            if not self.is_reloading:
                if now - self.last_shot > self.weapon_bullet_rate:
                    # we've 100% fired a bullet so reset the timer for the next bullet, fire a bullet were the players barrel is
                    # move the player vs the kickback, and empty the clip by 1 
                    self.last_shot = now
                    dir = vec(1, 0).rotate(-self.rot)
                    pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                    Bullet(self.game, pos, dir)
                    self.vel = vec(-KICKBACK, 0).rotate(-self.rot)
                    self.bullets_remaining_in_clip -= 1 

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

    # -- new custom player functions --
    # need to make a parent unit class for this stuff btw
    def draw_player_name(self): # [CUSTOM]
        self.name_textsurface = self.game.FONT_SILK_REGULAR_14.render(f"{self.character_name}", True, WHITE) # "text", antialias, color
        x, y = self.pos.x, self.pos.y 
        destination = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.game.camera.apply_to_rect(destination).copy()
        destination.move_ip(int(TILESIZE/2) + 20, -int(TILESIZE)) # better way to handle moving things btw donkey!, also btw, ip = in place
        self.game.screen.blit(self.name_textsurface, destination)

    def draw_player_chargebar(self, pct=136, is_refilling=False):
        BAR_LENGTH = 136
        BAR_HEIGHT = 4 # 20
        x, y = self.pos.x + int(TILESIZE/2) + int(TILESIZE/2), self.pos.y - int(TILESIZE/2) - 10 
        if pct > BAR_LENGTH: # just incase we get a number that is bigger
            pct = BAR_LENGTH
        chargebar = pg.Rect(x, y, pct, BAR_HEIGHT)
        chargebar = self.game.camera.apply_to_rect(chargebar).copy()
        chargebar.move_ip(-10,18) # (-10, TILESIZE/2) # better way to handle moving things btw donkey!, also btw, ip = in place
        chargebar_background = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        chargebar_background = self.game.camera.apply_to_rect(chargebar_background).copy()
        chargebar_background.move_ip(-10,18) # (-10, TILESIZE/2) # better way to handle moving things btw donkey!, also btw, ip = in place
        # if you cant change weapon (due to zombie range or coolodwn, ur ammo bar shows as red
        colr = RED if self.disable_weapon_change or self.change_weapon_cooldown > 0 == True else ORANGE
        colr = GREEN if not is_refilling else colr
        pg.draw.rect(self.game.screen, GREY, chargebar_background)
        pg.draw.rect(self.game.screen, colr, chargebar)

    # -- new test for "talking" characters -- 
    def draw_unit_conversation(self, lines): # [CUSTOM]
        BOX_SIZE = 36 # current box size = 20, note this should be slightly bigger than the unit health bar size btw so when hardcoding do this properly, aka dynamic from it
        shift_x, shift_y = 50, -50
        x, y = (self.pos.x, self.pos.y) # scoot back and up a tad from the unit health display to be centralised
        # -- calculate this stuff first so we know the size the main box needs to be based on the text
        speech_text_surf = self.game.FONT_SILK_REGULAR_18.render(f"{lines}", True, WHITE) # "text", antialias, color
        speech_text_surf_width = speech_text_surf.get_width() # as should be different or dynamic for multiple lines but dont have to make fully multiline rn
        SPEECH_BOX_LENGTH, SPEECH_BOX_HEIGHT = speech_text_surf_width + 20, 36 
        # -- icon box --
        icon_box_rect = pg.Rect(x, y, BOX_SIZE, BOX_SIZE)
        icon_box_rect = self.game.camera.apply_to_rect(icon_box_rect).copy() # before we draw it apply the camera to it, the move ip does nothing but left incase in future we wanna reposition the bars, use move ip instead
        icon_box_rect.move_ip(shift_x, shift_y) # (-10, TILESIZE/2) # better way to handle moving things btw donkey!, also btw, ip = in place#
        pg.draw.rect(self.game.screen, BLUEMIDNIGHT, icon_box_rect)
        # -- icon box outline --
        icon_box_outline_rect = pg.Rect(x, y, BOX_SIZE, BOX_SIZE)
        icon_box_outline_rect = self.game.camera.apply_to_rect(icon_box_outline_rect).copy()
        icon_box_outline_rect.move_ip(shift_x, shift_y)
        pg.draw.rect(self.game.screen, DARKGREY, icon_box_outline_rect, 3)
        # -- speech box --
        speech_box_rect = pg.Rect(x, y, SPEECH_BOX_LENGTH, SPEECH_BOX_HEIGHT)
        speech_box_rect = self.game.camera.apply_to_rect(speech_box_rect).copy()
        speech_box_rect.move_ip(shift_x+44, shift_y) 
        pg.draw.rect(self.game.screen, DARKGREY, speech_box_rect)
        # -- icon --
        # draw a scaled down icon which we're using to highlight who's speaking
        icon_rect = pg.Rect(x, y, 32, 32)
        icon_rect = self.game.camera.apply_to_rect(icon_rect).copy()
        icon_rect.move_ip(shift_x+2, shift_y+2) # better way to handle moving things btw donkey!, also btw, ip = in place
        self.game.screen.blit(pg.transform.scale(self.game.lego_img,(32,32)), icon_rect)
        # -- speech box text -- 
        destination = pg.Rect(x, y, SPEECH_BOX_LENGTH, SPEECH_BOX_HEIGHT) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.game.camera.apply_to_rect(destination).copy()
        destination.move_ip(shift_x+50, shift_y+2)
        self.game.screen.blit(speech_text_surf, destination)

