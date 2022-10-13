# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 1
# Project setup
# Video link: https://youtu.be/3UxnelT9aCo
import pygame as pg
import sys
# to get the map.txt ?
from os import path
from settings import *
from sprites import *
from tilemap import *
# temp test
from sidebar import *
# temp test
from casino import *
# for profiling
# from profilehooks import profile
import cProfile as profile

from v1.casino import Casino_Roller

# HUD functions
def draw_player_health(surf, x, y, pct): # surface, pos, pos, percentage of health
    # incase we pass a negative, pin it at 0
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    # what colour
    if pct >= 0.6:
        col = GREEN
    elif pct >= 0.3:
        col = YELLOW
    else:
        col = RED
    # then draw it on the surface we said, in the colour we said, using the fill_rect we've passed
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, DARKGREY, outline_rect, 2)

def draw_companion_health(surf, x, y, pct): # surface, pos, pos, percentage of health
    # incase we pass a negative, pin it at 0
    if pct < 0:
        pct = 0
    BAR_LENGTH = 80
    BAR_HEIGHT = 10
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    # what colour
    if pct >= 0.6:
        col = GREEN
    elif pct >= 0.3:
        col = YELLOW
    else:
        col = RED
    # then draw it on the surface we said, in the colour we said, using the fill_rect we've passed
    pg.draw.rect(surf, col, fill_rect)
    # pg.draw.rect(surf, DARKGREY, outline_rect, 1)

# test af, needs a better name too
def draw_a_chargebar(surf, x, y, pct, bar_width=100, bar_height=20): # surface, pos, pos, percentage of health
    # incase we pass a negative, pin it at 0
    if pct < 0:
        pct = 0
    BAR_LENGTH = bar_width
    BAR_HEIGHT = bar_height
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    # what colour
    if pct >= 0.6:
        col = GREEN
    elif pct >= 0.3:
        col = YELLOW
    else:
        col = RED
    # then draw it on the surface we said, in the colour we said, using the fill_rect we've passed
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, DARKGREY, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.sidebar = SideBar(self) # create the new sidebar ui object
        self.subsbar = SubsBar(self) # create the new subsbar ui object
        self.sidebar_bottom = SideBar_Bottom(self, self.sidebar) # temp af
        self.sidebar_top = SideBar_Top(self, self.sidebar) # temp af 
        self.twitch_chat = Comment_Handler(self, self.sidebar) # note in an object not a sprite
        self.username = "PlayerMan" # to add this in a menu, will have in twitch chat fans with ur name lol
        self.want_twitch = True
        self.want_clout_ui = True
        # guna make the below stuff into its own class that we'll initialise here ig, but leaving here for now...
        self.clout_streak = 0
        self.clout_streak_timer = 0
        self.clout_cooldown_timer = 0
        self.clout_wallet = 0
        # really just temp var for debugging tho might turn into like a setting tbf idk
        self.want_zombie_names = True
        # test to avoid loading fonts in update functions
        # SILK BOLD
        self.FONT_SILK_BOLD_10 = pg.font.Font("Silkscreen-Bold.ttf", 10) 
        self.FONT_SILK_BOLD_12 = pg.font.Font("Silkscreen-Bold.ttf", 12) 
        self.FONT_SILK_BOLD_14 = pg.font.Font("Silkscreen-Bold.ttf", 14) 
        self.FONT_SILK_BOLD_18 = pg.font.Font("Silkscreen-Bold.ttf", 18) 
        self.FONT_SILK_BOLD_20 = pg.font.Font("Silkscreen-Bold.ttf", 20) 
        self.FONT_SILK_BOLD_24 = pg.font.Font("Silkscreen-Bold.ttf", 24) 
        self.FONT_SILK_BOLD_44 = pg.font.Font("Silkscreen-Bold.ttf", 44) 
        # SILK REGULAR
        self.FONT_SILK_REGULAR_10 = pg.font.Font("Silkscreen-Regular.ttf", 10) 
        self.FONT_SILK_REGULAR_12 = pg.font.Font("Silkscreen-Regular.ttf", 12) 
        self.FONT_SILK_REGULAR_14 = pg.font.Font("Silkscreen-Regular.ttf", 14) 
        self.FONT_SILK_REGULAR_18 = pg.font.Font("Silkscreen-Regular.ttf", 18) 
        self.FONT_SILK_REGULAR_20 = pg.font.Font("Silkscreen-Regular.ttf", 20) 
        self.FONT_SILK_REGULAR_24 = pg.font.Font("Silkscreen-Regular.ttf", 24) 
        self.FONT_SILK_REGULAR_44 = pg.font.Font("Silkscreen-Regular.ttf", 44)  
        # KAPPA
        self.FONT_KAPPA_REGULAR_11 = pg.font.Font("Kappa_Regular.otf", 11) # Kappa_Regular KappaDisplay_ExtraBold.otf Kappa_Black.otf KappaDisplay_Regular.otf KappaDisplay_Bold.otf
        self.FONT_KAPPADISPLAY_EXTRABOLD_12 = pg.font.Font("KappaDisplay_ExtraBold.otf", 12)
        # [NEW!] rework/refactor 
        self.all_bwall_positions = [] # all bwall x and y positions
        self.all_bwall_objects = [] # unused, should remove
        self.zombies_distances_to_player = {}
        self.zombies_distances_to_player_timer = 0
        # [NEW!] casino roller initial test
        self.casino_roller = Casino_Roller(self) # create the new casino roller ui object       
        self.chicken_dinner_timer = 0
        self.chicken_dinner_roll = randint(2000,3000)
        self.chicken_dinner_reel_result = []

    def update_zombies_distances_to_player(self): # every 10 seconds
        if not self.zombies_distances_to_player_timer: # if not started the timer, start the timer
            self.zombies_distances_to_player_timer = pg.time.get_ticks()
        else: # if the timer IS running
            check_timer = pg.time.get_ticks()
            time_running = check_timer - self.zombies_distances_to_player_timer
            # print(f"time running = {time_running}")
            if time_running > 1000: # check if it is over 500 milliseconds
                self.zombies_distances_to_player_timer = 0 # if it is, reset it
                self.set_zombies_distances_to_player() # update the zombie distances
                
    def set_zombies_distances_to_player(self):
        updated_distances = {}
        for a_zombie in self.mobs:
            updated_distances[a_zombie.myid] = (a_zombie.is_near(self.player.pos.x, self.player.pos.y, return_distance=True)) # get distance
        self.zombies_distances_to_player = updated_distances

    def load_data(self):
        # location of where our game is running from, main.py
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.map = Map(path.join(game_folder, 'map.txt')) # map2_zombielag
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        # scale up our new loaded wall image to the tilesize, if need to reuse functionality then make this a function or a class
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        # new zombie img
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        # new bullet img
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        # new - image for the Companion class
        self.my_turret_img = pg.image.load(path.join(img_folder, MY_TURRET_IMG)).convert_alpha()
        self.my_turret_img = pg.transform.scale(self.my_turret_img, (int((TILESIZE / 10) * 5.5), int((TILESIZE / 10) * 5.5))) # reduced size
        # scale up our new loaded wall image to the tilesize, if need to reuse functionality then make this a function or a class
        self.paywall_img = pg.image.load(path.join(img_folder, PAY_WALL_IMG)).convert_alpha()
        self.paywall_img = pg.transform.scale(self.paywall_img, (TILESIZE, TILESIZE))    
        # splat image (/ body outline test)    
        self.splat_img = pg.image.load(path.join(img_folder, PAY_WALL_IMG)).convert_alpha()
        self.splat_img = pg.transform.scale(self.splat_img, (TILESIZE, TILESIZE)) 
        # gold coin test
        self.gold_coin_img = pg.image.load(path.join(img_folder, GOLD_COIN_IMG)).convert_alpha()
        self.gold_coin_img = pg.transform.scale(self.gold_coin_img, (TILESIZE, TILESIZE)) 
         
        # test img stuff
        self.break_wall_0_img = pg.image.load(path.join(img_folder, BREAK_WALL_0_IMG)).convert_alpha()
        self.break_wall_0_img = pg.transform.scale(self.break_wall_0_img, (TILESIZE, TILESIZE))
        self.break_wall_1_img = pg.image.load(path.join(img_folder, BREAK_WALL_1_IMG)).convert_alpha()  
        self.break_wall_1_img = pg.transform.scale(self.break_wall_1_img, (TILESIZE, TILESIZE)) 
        self.break_wall_2_img = pg.image.load(path.join(img_folder, BREAK_WALL_2_IMG)).convert_alpha()
        self.break_wall_2_img = pg.transform.scale(self.break_wall_2_img, (TILESIZE, TILESIZE))
        self.break_wall_3_img = pg.image.load(path.join(img_folder, BREAK_WALL_3_IMG)).convert_alpha()  
        self.break_wall_3_img = pg.transform.scale(self.break_wall_3_img, (TILESIZE, TILESIZE)) 
        self.break_wall_4_img = pg.image.load(path.join(img_folder, BREAK_WALL_4_IMG)).convert_alpha()
        self.break_wall_4_img = pg.transform.scale(self.break_wall_4_img, (TILESIZE, TILESIZE))                
        self.break_wall_hl_0_img = pg.image.load(path.join(img_folder, BREAK_WALL_HL_0_IMG)).convert_alpha()  
        self.break_wall_hl_0_img = pg.transform.scale(self.break_wall_hl_0_img, (TILESIZE, TILESIZE))         
        self.break_wall_hl_1_img = pg.image.load(path.join(img_folder, BREAK_WALL_HL_1_IMG)).convert_alpha()  
        self.break_wall_hl_1_img = pg.transform.scale(self.break_wall_hl_1_img, (TILESIZE, TILESIZE))            
        self.break_wall_hl_2_img = pg.image.load(path.join(img_folder, BREAK_WALL_HL_2_IMG)).convert_alpha()  
        self.break_wall_hl_2_img = pg.transform.scale(self.break_wall_hl_2_img, (TILESIZE, TILESIZE))         
        self.break_wall_hl_3_img = pg.image.load(path.join(img_folder, BREAK_WALL_HL_3_IMG)).convert_alpha()  
        self.break_wall_hl_3_img = pg.transform.scale(self.break_wall_hl_3_img, (TILESIZE, TILESIZE))     
        self.break_wall_hl_4_img = pg.image.load(path.join(img_folder, BREAK_WALL_HL_4_IMG)).convert_alpha()  
        self.break_wall_hl_4_img = pg.transform.scale(self.break_wall_hl_4_img, (TILESIZE, TILESIZE))         
        self.break_wall_hl_4b_img = pg.image.load(path.join(img_folder, BREAK_WALL_HL_4B_IMG)).convert_alpha()  
        self.break_wall_hl_4b_img = pg.transform.scale(self.break_wall_hl_4b_img, (TILESIZE, TILESIZE))  

        self.test_bg_img = pg.image.load(path.join(img_folder, TEST_BG_IMG)).convert_alpha() 
        self.test_bg_img = pg.transform.scale(self.test_bg_img, (WIDTH, HEIGHT))  
        self.test_sidebar_img = pg.image.load(path.join(img_folder, TEST_SIDEBAR_IMG)).convert_alpha() 
        self.sidebar_bottom_img = pg.image.load(path.join(img_folder, SIDEBAR_BOTTOM_IMG)).convert_alpha() 
        self.sidebar_bottom_right_img = pg.image.load(path.join(img_folder, SIDEBAR_BOTTOM_RIGHT_IMG)).convert_alpha() 
        self.sidebar_bottom_left_img = pg.image.load(path.join(img_folder, SIDEBAR_BOTTOM_LEFT_IMG)).convert_alpha() 
        self.sidebar_top_img = pg.image.load(path.join(img_folder, SIDEBAR_TOP_IMG)).convert_alpha()
        self.comment_img_1 = pg.image.load(path.join(img_folder, SIDEBAR_COMMENT_1_BG_IMG)).convert_alpha() 
        self.comment_img_2 = pg.image.load(path.join(img_folder, SIDEBAR_COMMENT_2_BG_IMG)).convert_alpha() 
        self.comment_img_3 = pg.image.load(path.join(img_folder, SIDEBAR_COMMENT_3_BG_IMG)).convert_alpha() 
        self.comment_img_4 = pg.image.load(path.join(img_folder, SIDEBAR_COMMENT_4_BG_IMG)).convert_alpha() 

        # casino
        self.casino_gold_img_1 = pg.image.load(path.join(img_folder, CASINO_GOLD_INGOTS_IMG)).convert_alpha()
        self.casino_gold_img_2 = pg.image.load(path.join(img_folder, CASINO_GOLD_IMG)).convert_alpha()
        self.casino_gold_img_3 = pg.image.load(path.join(img_folder, CASINO_GOLD_TREASURE_IMG)).convert_alpha()
        
        # self.player_blur3_img = pg.image.load(path.join(img_folder, PLAYER_BLUR3_IMG)).convert_alpha()
        # self.player_injury_img = pg.image.load(path.join(img_folder, PLAYER_INJURY1_IMG)).convert_alpha()

    def new(self):              
        # initialize groups for stuff in game and do all the rest of the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.companion_bullets = pg.sprite.Group()
        self.breakablewalls = pg.sprite.Group() # should be called barricades huh
        self.paywalls = pg.sprite.Group() 
        self.companions = pg.sprite.Group()
        # very very temp test
        self.casino = pg.sprite.Group()
        # flags we can toggle
        # self.paused = False
        self.chicken_dinner = False # winner winner, random spinner
        # was temporary, should refactor tbf
        self.walls_pos_collides = []
        self.walls_y_collides = [] 
            
        def spawn_stuff_on_map():
            # first run = run only player first 
            # why? = because we need to pass the player object to instances of other interactive things on the map like walls
            # otherwise we have to place the player above any interactive elements, now we can place the player anywhere
            # enumerate over the map data as   each line is a row on the map from top to bottom
            for i in range(0, 3):
                run = i+1
                for row, tiles in enumerate(self.map.data):
                    # for each tile, which is the actual string for each row `1....1`
                    # enumerate as tiles here becomes the actual character in that position in the string,
                    # and the col becomes the index/x_position of that character in the string/on the map
                    for col, tile in enumerate(tiles):
                        if run == 2:
                            # if the tile is a 1, this is a wall tile
                            if tile == "1":
                                # place a wall at this column and row on the actual map, from the col and row on the tilemap
                                Wall(self, col, row)
                                # if not the edge walls, so...
                                not_cols = [0, 63, 62, 61, 60, 59] # smh, dynamically pls
                                not_rows = [0, 46, 45, 44, 43, 42, 41] # smh, dynamically pls
                                if row not in not_rows: # top and bottom
                                    if col not in not_cols:
                                        self.walls_pos_collides.append((col, row)) if row not in self.walls_y_collides else 0
                            if tile == "B":
                                # place a breakablewall test
                                BreakableWall(self, col, row, self.player)  # this_wall = 
                                self.all_bwall_positions.append((col*TILESIZE, row*TILESIZE)) # append a tuple of the bwall x and y pos to this game object variable on initialisation only (as only needed once, they're static positions)
                                # self.all_bwall_objects.append(this_wall) # unused, should remove
                            if tile == "M":
                                # place a paywall
                                PayWall(self, col, row, self.player)  
                        if run == 3:    
                            if tile == "Z":
                                # place a breakablewall test
                                Mob(self, col, row, self.breakablewalls)
                            if tile == "C":
                                self.companion = Companion(self, col, row)                       
                        if run == 1:
                            # if the tile is a P, this is the player
                            if tile == "P":
                                # spawn them at the col, row position on the map 
                                self.player = Player(self, col, row)
        spawn_stuff_on_map()
        y_walls = [y for _, y in self.walls_pos_collides]
        self.y_walls_unique = set([y for y in y_walls if y_walls.count(y) > 1]) # make a unique wall if theres more than one at this pos, then make this a set so its just the unique ones
        print(f"{self.all_bwall_positions = }")
        print(f"Just the Y position collisions = {self.y_walls_unique = }")
        self.map_mob_count = len(self.mobs) # how many are spawned at the start of the round                       
        self.camera = Camera(self.map.width, self.map.height)

    def run(self): 
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.chicken_dinner: # or not self.chicken_dinner:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        # update the camera based on the position of the player
        self.camera.update(self.player) # any sprite you put in here the camera will follow, dope af!

        # [NEW!] - rework/refactor
        self.update_zombies_distances_to_player()

        # FOR CLOUT WALLET - IMPORTANT, SOMETIMES THIS ISNT WORKING?
        # new test for clout rework
        if self.clout_cooldown_timer:
            check_time = pg.time.get_ticks()
            if check_time - self.clout_cooldown_timer > 2000:
                check_time = 0
                self.clout_cooldown_timer = 0
                # so when this gets trigger for the reset, also add the gold but check if the gold was defo won first (which we havent implemented yet but is only 1 case for now so dw)
                self.player.player_gold += self.clout_wallet
                self.clout_wallet = 0

        want_print_update = False

        # -- when mobs hit player --
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE # we can have base damage and subclasses of mobs to get around this, plus then also stuff like armor so chill lol
            # have the mob stop again
            if self.player.health <= 0:
                # game over man, game over
                Comment.all_comments = [] # for now, wipe the comments if u die
                self.playing = False 
        if hits:
            if want_print_update:
                print(f"[ {self.player.health}hp ] Player got Bitchslapped by {hits[0].myname}")
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
            # new clout stuff
            if self.player.clout_rating_base_timer: # if the clout rating timer is running / active and we just got hit by a zombie
                self.player.clout_rating_base_timer = False # the player got hit so turn off our timer

        # -- using companion : when mobs hit the companion --
        hits = pg.sprite.spritecollide(self.companion, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.companion.hp_current -= MOB_DAMAGE # we can have base damage and subclasses of mobs to get around this, plus then also stuff like armor so chill lol   
            break # only get hit by 1 zombie at a time, should remove tho tbf ig? (were doing companion damage differently now tho)
            # if self.companion.hp_current <= 0:
                # game over man, game over
                # pass # regen, probably not here anyways tbf

        # -- using mobs : when companion hits the mobs --
        if self.companion.companion_level > 1: # gives the companion a pushback mechanic, its kinda trash, but would be better if the companion moved tbf
            hits = pg.sprite.groupcollide(self.mobs, self.companions, False, False)
            for hit in hits:
                print(f"SUPER NEAR PUSH BACK LVL 2 COMPANION PUSH BACK: {hit.is_near(self.companion.pos.x, self.companion.pos.y, return_distance=True)}m away")
                if hit.is_near(self.companion.pos.x, self.companion.pos.y, return_distance=True) > 35: # 59 (and speed 85) @ 0,0,64,64 note is very dependent on the size of the companion hit rect and probably companion speed - you can get some very interesting results, this just only adds the zombies getting pushed back when they're in super close range of an attack, so that they do a bit less damage, force a bit less of an extreme turn from both the zombie and the companion, and means the companion can get away if closed in on but is then instantly surrounded which actually looks really kewl and very natural                    
                    hit.vel += vec(10, 0).rotate(-self.companion.rot)
                    self.companion.vel += vec(20,0).rotate(self.companion.rot)
        # add mobs bounce back when hitting companion
            
        # -- temp test - do companion bullets first --
        bullet_hits = pg.sprite.groupcollide(self.companion_bullets, self.mobs, True, False) # zombie stay, bullets go
        for bullet_hit in bullet_hits:
            # check if the bullet came from the player or the companion
            print(f"HIT BULLET! FROM {bullet_hit.bullet_owner.title()} => [ {self.companion.bullet_damage} ] damage delt") 
            for mob in self.mobs: # gtry a generator maybe?
                if mob.rect.colliderect(bullet_hit.rect): # must be a better way to do this?!
                    mob.health -= self.companion.bullet_damage
                    mob.hit_by_bullet = pg.time.get_ticks()
                    if mob.vel.x >= mob.vel.y:
                        mob.vel.x /= 2 # slow by half if ur fastest direction
                    else:
                        mob.vel.y /= 2

        # -- bullets hit mobs -- <= this type of implementation here is likely a good starting point for handling ui stuff like killstreaks i reckon
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True) # zombie stay, bullets go
        for hit in hits:
            # check if the bullet came from the player or the companion
            # if hit.bullet_owner == "player":
            # was previously constant global from settings as player_damage, now we need to set it for crits hence this, temp for now anywayas
            hit.health -= self.player.player_damage
            # elif hit.bullet_owner == "companion":
            #     hit.health -= self.companion.bullet_damage 
            for bullet in self.bullets:
                print(f"HIT BULLET! FROM {bullet.bullet_owner.title()} => [ {self.player.player_damage} ] damage delt")
                
            # new test for sadge face status
            # so now its been hit, start the hit by bullet timer, which automatically stops itself when it hits 2000 ms / 2 sec
            hit.hit_by_bullet = pg.time.get_ticks()
            
            if self.player.player_damage >= 100: 
                print("CRIT BAYBAYYYYY!")
                if self.clout_streak_timer:
                    self.clout_wallet += 1
                self.player.player_damage = 10
                # just some quick extra rotation for randomness during this heavier crit pushback
                hit.look_at(vec(hit.pos.x - 10, hit.pos.y - 10)) 
                # make this bullet temporarily push the zombie back if its a crit
                hit.vel = vec(-150,0)
            else:
                hit.vel = vec(0,0) # ehhhh
                # make this bullet temporarily slow the zombie a normal amount
                hit.vel = vec(0,0) # ehhhh
            if want_print_update:
                print(f"UPDATE - zombie {hit.myid} on {hit.health}hp, {self.player.player_damage = }") 
            # <==== zombie has died here ====================================================================================================               
            if hit.health <= 0:
                # <==== zombie has died here ====================================================================================================
                print(f"{hit.myname} has Died [ hp: {hit.health} ]")
                
                # only count towards the cloutstreak if its not on cooldown (a few seconds after weve just had a clout streak)
                if self.clout_cooldown_timer == 0:
                    self.clout_streak += 1

                # drop a coin test
                # self.screen.blit()
                
                # temp test for player in game levelling 
                self.level_handler()

                # temp
                BASE_KILL_GOLD = 100
                # increase the clout wallet by the gold won for this kill, plus 10% of the increment var... also me this stuff its own function / class pls
                self.clout_wallet += BASE_KILL_GOLD + (BASE_KILL_GOLD * (self.clout_streak / 10)) # ARBITRARY NUMBER TO HARD CODE FOR GOLD ASAP PLS!

                if self.clout_streak_timer > 0: # if the timer is on, you have an active streak, and if you do and you've got another kill, we reset the timer
                    self.clout_streak_timer = pg.time.get_ticks()
                    print(f"Hot Streak Baybayyyy {self.clout_streak}")
                else:
                    # this is the initial one, incase we want to handle them differently
                    self.clout_streak_timer = pg.time.get_ticks()
                    print(self.clout_streak_timer)
            else:
                if want_print_update:
                    print(f"[ {hit.health} to {hit.health - self.player.player_damage}hp ] - zombie {hit.myid} 'OOF' - player dealt [ {self.player.player_damage}hp ] damage ")

    def level_handler(self): # herelevelhandler #herelvlhandler
        """ very very temporary initial test implementation of mechanic that handles the players current level, 
        for now will just be based off gold since its easier, also ig should do companion too btw,
        purely just learning the events mechanic rn, will improve this drastically in future
        """
        # currently it only runs this check when a zombie dies, actually isnt a bad idea tbf but should actually comfirm if that would work consistently lol
        self.level_up = False # even used? idk  
        # level 1 > 2 ... obvs not a good implementation but is fine for now, idea have a class ig
        if self.player.player_gold >= 0:
            print(f"{self.player.player_gold}")
            self.player.character_level = 2
            self.chicken_dinner = pg.USEREVENT+1
        # level 2 > 3
        elif self.player.player_gold >= 30:
            print(f"{self.player.player_gold}")
            self.player.character_level = 3
            self.chicken_dinner = pg.USEREVENT+1
        # level 3 > 4
        elif self.player.player_gold >= 100:
            print(f"{self.player.player_gold}")
            self.player.character_level = 4
            self.chicken_dinner = pg.USEREVENT+1            
        # timer to check for chicken dinner is necessary, but still should confirm other ways it can be done first before commiting to it tbf
        if self.chicken_dinner: 
            pg.time.set_timer(self.chicken_dinner, 100)
            

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self): # go through all the sprites and draw them on the screen'
        # if self.chicken_dinner:
        #         self.casino_roller.draw(self.screen)
        # else:
        # set the caption of the window to be any core debug things, framerate etc
        pg.display.set_caption(f"FPS: {self.clock.get_fps():.2f}, RoundEarnings:{self.player.player_gold}, AutoShoot: {self.player.autoshoot}, Energy: {self.player.sprint_meter:.0f}, State: {self.player.state_state}-{self.player.state_moving}, Interacting: {self.player.is_interacting}, Player: {self.player.pos} / {self.player.vel} / {self.player.rot:.0f}, Gold: {self.player.player_gold}") # pos, vel, rot, sprint_meter, state_moving, state_state, is_interacting, player_gold
        # -- actual main draw stuff --
        self.screen.fill(BGCOLOR)         # self.screen.blit(self.test_bg_img, (0,0)) # the fake twitch bg test
        # -- the main draw sprites loop --
        for sprite in self.all_sprites:
            # only do this draw for instances of the zombie mob
            if isinstance(sprite, Mob):
                # personal custom zombie name display, note this isn't a sprite or part of the sprint (cause img size = bounds) but drawn ontop during the render so has layering considerations which is why the name is drawn on first, then the hp bar (?)
                destination = self.camera.apply(sprite).copy()
                destination_status = self.camera.apply(sprite).copy()
                destination_attack_bar = self.camera.apply(sprite).copy()
                destination.move_ip(-10, TILESIZE/2) # in place btw
                destination_status.move_ip(-20, -TILESIZE/2)
                destination_attack_bar.move_ip(20, -TILESIZE/2)
                if self.want_zombie_names:
                    self.screen.blit(sprite.draw_name(), destination) #self.camera.apply(sprite)) #.move(0, -TILESIZE / 2)) # .move moves it back half a tile behind us, depending on our rotation 
                    self.screen.blit(sprite.draw_status(), destination_status) 
                # actually clean draw health
                sprite.draw_health()
                # if the mob is firin mah lazer (charging an attack) then show the chargebar, this number can go under 50 as part of a cooldown, so we dont show that either, or when its not charging bosh
                if sprite.charging_attack > 0 and sprite.is_looking_at == "bwall":
                    draw_a_chargebar(self.screen, destination_attack_bar.x, destination_attack_bar.y, sprite.charging_attack / 200, bar_width = 50, bar_height = 14)
                # gold coin test
                # couldnt get it to work, shows up kinda on the blit but then disappears idk, will figure it out another time
            # take the camera and apply it to that sprite 
            self.screen.blit(sprite.image, self.camera.apply(sprite))  
                
            # draw the companion
            if isinstance(sprite, Companion):
                self.screen.blit(sprite.image, self.camera.apply(sprite)) 
                # test for companion hp bar
                destination = self.camera.apply(sprite).copy()
                destination.move_ip(TILESIZE/2, -20) # in place btw
                draw_companion_health(self.screen, destination.x, destination.y, self.companion.hp_current / self.companion.hp_max) # 20, 45
                destination_status = self.camera.apply(sprite).copy()
                destination_status.move_ip(TILESIZE/6, 30) # in place btw
                if sprite.hp_current < sprite.hp_max / 2 and sprite.is_looking_at == "zombie": # only print if looking at zombie but then dont print companion is over 50% hp
                    self.screen.blit(sprite.draw_status(), destination_status) 
                else: # only chit chat if ur defo not already showing something else in status
                    # -- chit chat - if the player hasnt moved and nothing happening, i.e. idleing --
                    chit_chat = True
                    if self.chicken_dinner:
                        chit_chat = False
                    if chit_chat:
                        if sprite.is_looking_at == "with_player":
                            self.screen.blit(sprite.companion_chit_chat_end_level(sprite.hp_max / sprite.hp_current), destination_status) 
                        elif sprite.is_looking_at == "bff":
                            if self.player.vel == vec(0,0): 
                                self.screen.blit(sprite.companion_chit_chat(), destination_status) 
                

        # -- nested func for rendering basic text which guna move to ui functs shortly --
        # literally is just here cause its used regularly while figuring things out so pointless moving it            
        def render_to_basic_ui(text, x, y, color=None, font_size=14, want_font="silk_regular", alignment="center"):
            # personal basic af test ui stuff
            # fonts switch # 14, 24, 44, 20         

            if want_font == "silk_bold": # dictionaries duhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
                if font_size == 12:
                    font = self.FONT_SILK_BOLD_12
                elif font_size == 10:
                    font = self.FONT_SILK_BOLD_10
                elif font_size == 14:
                    font = self.FONT_SILK_BOLD_14 
                elif font_size == 18:
                    font = self.FONT_SILK_BOLD_18                   
                elif font_size == 20:
                    font = self.FONT_SILK_BOLD_20
                elif font_size == 24:
                    font = self.FONT_SILK_BOLD_24
                elif font_size == 44:
                    font = self.FONT_SILK_BOLD_44
                else:
                    font = self.FONT_SILK_BOLD_12
            elif want_font == "silk_regular":
                if font_size == 12:
                    font = self.FONT_SILK_REGULAR_12
                elif font_size == 10:
                    font = self.FONT_SILK_REGULAR_10
                elif font_size == 14:
                    font = self.FONT_SILK_REGULAR_14 
                elif font_size == 18:
                    font = self.FONT_SILK_REGULAR_18                   
                elif font_size == 20:
                    font = self.FONT_SILK_REGULAR_20
                elif font_size == 24:
                    font = self.FONT_SILK_REGULAR_24
                elif font_size == 44:
                    font = self.FONT_SILK_REGULAR_44
                else:
                    font = self.FONT_SILK_REGULAR_12
            # colours switch
            if color == "earnings":
                text = font.render(f'{text}', False, GREEN, BLUEMIDNIGHT) # use the font object to render ur text 
                # text = font.render(f'{text}', True, GREEN if self.player.won_clout else YELLOW, BLUEMIDNIGHT) # use the font object to render ur text  
            elif color == "zombies": # the colours here do change based on things which should keep tbf but dont over kill it tho
                text = font.render(f'{text}', False, GREEN if len(self.mobs) < int(self.map_mob_count / 2) else RED, BLUEMIDNIGHT) # if less than half mobs text changes colour
            elif color == "weapons": # the colours here do change based on things which should keep tbf but dont over kill it tho
                text = font.render(f'{text}', False, MAGENTA if self.player.autoshoot else YELLOW, BLUEMIDNIGHT) # use the font object to render ur text                                 
            elif color == "green": # temp, for has_won clout multiplier stuff, so need to proper implementation, as will everything here tbf
                text = font.render(f'{text}', False, GREEN, BLUEMIDNIGHT)
            else:
                text = font.render(f'{text}', False, HIGHLIGHTER, BLUEMIDNIGHT) # use the font object to render ur text             
            textRect = text.get_rect() # then create a surface for the rect 
            textRect.x = x # put the center of that rect where we want it
            # alignment
            if alignment == "right":
                textRect.midright = (x, 28) # fyi this y is surely rect.centery or rect.width / 2 or sumnt but not 28 pls duhh
            textRect.y = y # put the center of that rect where we want it        
            # copy the text surface object to the screen and render at the given center pos
            self.screen.blit(text, textRect)
        bullets_remaining = self.player.return_clip_size() - self.player.clip_counter
        # -- ui text renders --
        def calculate_accuracy(): # to move obvs
            # take bullets fired and bullets missed, add them together for total bullets fired, then return the accuracy as a 
            total_shots_fired = self.player.current_accuracy[0] + self.player.current_accuracy[1]
            if total_shots_fired: # if theres atleast one shot so this is not zero, else ZeroDivErr
                player_accuracy = (self.player.current_accuracy[0] / total_shots_fired) * 100
                return(player_accuracy)
            else:
                return(0) # no shots fired yet
        
        
        if not self.chicken_dinner:
            # -- top right ui --
            render_to_basic_ui(f"Weapon: {self.player.current_weapon.title()}", x = 20, y = 70, color = "weapon") 
            render_to_basic_ui(f"Episode Earnings: ${self.player.player_gold}", x = 20, y = 90, color = "earnings")
            render_to_basic_ui(f"Zombies Remaining: {len(self.mobs)} of {self.map_mob_count}", x = 20, y = 110, color = "zombies") 
            render_to_basic_ui(f"Bullets Remaining: {bullets_remaining}, Accuracy = {calculate_accuracy():.0f}% [ {self.player.current_accuracy[0]} / {self.player.current_accuracy[1]} ]", x = 20, y = 130, color = "weapon") 
            
            # -- draw player hp bar --
            # before final final flip
            draw_player_health(self.screen, 20, 20, self.player.health / PLAYER_HEALTH)
            
            # -- draw player reloading bar --
            reload_end = pg.time.get_ticks() 
            # if player is reloading
            if self.player.is_reloading:
                flashme = pg.time.get_ticks() 
                flashme = int(f"{flashme}"[1])
                if flashme % 2 != 0: # if the highest digit number is even on if not off, for flash                                                                          
                    render_to_basic_ui(f"Reloading!", (self.screen.get_width()/2) + (TILESIZE/2), (self.screen.get_height()/2) + (TILESIZE/2) - 20, ((reload_end - self.player.is_reloading) / self.player.return_gun_reload_speed())) # flashing?
                    flashme = False
                # isnt actually subclout btw but reload
                draw_a_chargebar(self.screen, (self.screen.get_width()/2) + (TILESIZE/2), (self.screen.get_height()/2) + (TILESIZE/2), (reload_end - self.player.is_reloading) / self.player.return_gun_reload_speed())   # self.screen.get_width() / 2, self.screen.get_height() /2,
            else:
                # if player is not reloading, check if u are low ammo, if so then flash it to player
                if bullets_remaining < 10: # less than 20%
                    flashme2 = pg.time.get_ticks() 
                    flashme2 = int(f"{flashme2}"[1])
                    if flashme2 % 2 != 0: # if the highest digit number is even on if not off, for flash   
                        render_to_basic_ui(f"Danger! Low Ammo", (self.screen.get_width()/2) + (TILESIZE/2), (self.screen.get_height()/2) + (TILESIZE/2) - 20, color = "weapon") 
                        flashme2 = False  
            
        if not self.chicken_dinner:
            if self.want_clout_ui:
                # ---- draw player clout multiplier bar stuff ---- 
                # -- the large clout rating letter + title --
                render_to_basic_ui(f"Clout Rating: ", x = 950, y = 530, want_font="silk_regular", font_size=14) 
                render_to_basic_ui(f"{self.player.get_display_clout_level()}", x = 1085, y = 530, font_size=44)
                # if atleast 1 zombie is still alive 
                if self.mobs: # Mob.get_my_hps():
                    if self.clout_streak >= 1 or self.clout_cooldown_timer > 0: # cooldown allows short the short window to display the results of the streak / bonus if u won it
                        
                        # -- the small potential winnings pot during clout level activation --
                        render_to_basic_ui(f"${self.clout_wallet}", x = 1078, y = 555, color="green", want_font="silk_regular", font_size=24, alignment="right") # viewer boost / subscriber boost
                        
                        # if on cooldown flash you win instead (tho not accurate need both cases am just confirming works fine)
                        if self.clout_cooldown_timer > 0:
                            # will just have some new bool if you've been hit that triggers you lose and then when the cooldown timer is turned off also turn that off too (or on whatever just the opposite)
                            render_to_basic_ui(f"You Win!", x = 900, y = 600, want_font="silk_bold", font_size=20, color="green") # viewer boost / subscriber boost
                        else:
                            # -- for flashing going viral text, removed for now but add back pls, was banging -- ... >> make own function or decorator! <<   :o            
                            render_to_basic_ui(f"Going Viral? ", x = 900, y = 600, want_font="silk_regular", font_size=20) # viewer boost / subscriber boost

                        # -- semi large clout multiplier number  --
                        render_to_basic_ui(f"x{self.clout_streak}", x = 1080, y = 600, font_size=24) 

                        
                        # note - remove all existing main wallet functionality now too!


                        # -- clout level multiplier charge bar --
                        # if self.clout_streak_timer > 0:
                        if self.clout_streak_timer: # dont show what the timer is on if the game is paused,
                            if not self.chicken_dinner: # so it shows empty but it will unpause where it should be dw
                                streak_check = pg.time.get_ticks()
                            else:
                                streak_check = 0
                            streak_timer = (streak_check - self.clout_streak_timer) / 5000 # from 0 - 100% for the 5 second clout streak timer
                            # if the timer has hit 5000
                            if streak_check - self.clout_streak_timer > 5000: # << HARD CODE ME ASAP BAYBAYYYYY
                                # ig wanna check hasn't been hit or sumnt btw? nah as that will just kill the timers!
                                self.clout_streak_timer = 0 # stop the timers
                                streak_check = 0
                                self.clout_streak = 0 # and reset the streak
                                # and also start the cooldown for this entire mechanic also
                                self.clout_cooldown_timer = pg.time.get_ticks()
                            # draw the clout streak / level multiplier bar / meter
                            draw_a_chargebar(self.screen, 905, 635, streak_timer, bar_width=100, bar_height=25)
                            # print(f"{self.clout_wallet = }")
                        
            # else:
            # # want_celebrate => stop the player, ideally make him spin around shooting, temp implementation anyways
            # want_celebrate = False
            # if want_celebrate:
            #     self.player.rot += 5
            #     self.player.vel = vec(1,0)
            #     # pos = self.player.pos # + BARREL_OFFSET.rotate(-self.player.rot) # was for shooting bullets idea but didnt get there in the end and forget it for now anyways

        # -- new test ui stuff --
        # handle (temp test) comment cooldown timer
        if not self.chicken_dinner:
            cd_check = pg.time.get_ticks()
            if self.twitch_chat.is_spawn_on_cooldown: # if the timer is running
                if self.twitch_chat.is_chat_maxed_out:
                    self.twitch_chat.is_spawn_on_cooldown = True # dont draw if its maxed out (for now anyway, as we can handle a different way ooo)
                elif cd_check - self.twitch_chat.is_spawn_on_cooldown > 2000: # every 2 sec, # elif so if above is true we can skip this
                    self.twitch_chat.is_spawn_on_cooldown = False

        # draw the sidebar
        if self.want_twitch:
            # if paused dont render the on screen ui stuff
            if not self.chicken_dinner:
                # twitch chat
                # new subs bar
                self.subsbar.draw(self.screen)
                # want above subs bar behind the side bar so render it first
                if not self.twitch_chat.is_spawn_on_cooldown:
                    # if not self.twitch_chat.is_chat_maxed_out: # temp af so we dont keep printing them when its full for now, since not implementing scrolling all yet 
                        # if not self.player.waiting:
                            roll = randint(1,6) 
                            if roll == 2: # this is effectively spawn rate now, if u make this a funct and just give it a percent chance! bosh
                                self.twitch_chat.create_new_comment() # note we're drawing to the sidebar not the screen, also means we can slide it in and out an no penalty too
                                self.twitch_chat.is_spawn_on_cooldown = pg.time.get_ticks()
                self.twitch_chat.update_all_comments(self.sidebar.image)
                self.sidebar_bottom.draw(self.sidebar.image) # drawn on top of sidebar
                self.sidebar.draw(self.screen)
                self.sidebar_top.draw(self.sidebar.image)
            
        # -- draws player collider and grid -- (player collider doesnt work tho?)
        want_collider_n_grid = False
        if want_collider_n_grid:
            pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 5) # for debugging -> draw the players rectangle, and hitbox
            self.draw_grid()  

        # make this its own function pls ffs
        # -- new winner winner chicken dinner casino spinner --  
        if self.chicken_dinner: # if paused on the chicken dinner event
            #
            #####################################################################################
            #
            #
            # rn this is only scrolling the top 3
            # ultimately i get it
            # but this is such a poor implementation its pointless continuing it
            # imo this should be rewritten
            # then the entire thing should be written ground up by first finishing the tutorials
            #
            # when you come back if you wanna continue
            # imo just rewrite
            # for one strip
            # completely from scratch
            # and imo just a premade strip first
            # as realised the movement is what u need to do first entirely by itself
            # ffs clown, see sidebar 
            # note like whole thing with this at the end was, need to start it with the strip at the top
            # just showing the bottom card
            # then scroll it to the bottom
            # then move it to the top
            # want velocity and acceleration 100%                               
            # that means imo just use sprites! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,,
            #
            #
            ####################################################################################
            #    
            self.casino_roller.update() # update the casino roller         
            self.casino_roller.draw(self.screen) # draw the casino roller
              
            
            

            

        # -- finally done, flip the display and render complete --
        pg.display.flip()

           
    def events(self): # hereevents
        # catch all events here
        for event in pg.event.get():
            # ---- core game button press events ----
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                # if in chicken dinner, end it - but btw, it should first skip, then on second press it should end
                if event.key == pg.K_c:
                    if self.chicken_dinner == True:
                        self.chicken_dinner = False
            # ---- handling custom events ----
            # once we have [ is_started ], it will go here as it may as well 
            if event.type == self.chicken_dinner:
                print(f"WINNER WINNER!\n-------[!! LEVEL [{self.player.character_level}] UP !!]--------\nCHICKEN DINNER!!!!\n")
                self.chicken_dinner = True
                self.chicken_dinner_timer = pg.time.get_ticks()
                Comment.all_comments = [] # temp for now but because the positions of comments jib out after this pause, just wipe them for now
                

            
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# @profile
def main():
    # create the game object
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_go_screen()


if __name__ == "__main__":
    want_stats = False
    if want_stats:
        profile.run('main()', 'restats')
        import pstats
        from pstats import SortKey
        p = pstats.Stats('restats')
        p.strip_dirs().sort_stats(-1).print_stats()
        p.sort_stats(SortKey.TIME)
        p.print_stats()
    else:
        main()
    