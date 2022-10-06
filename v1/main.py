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
        self.clout_streak = 0
 
    def load_data(self):
        # location of where our game is running from, main.py
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.map = Map(path.join(game_folder, 'map2.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        # scale up our new loaded wall image to the tilesize, if need to reuse functionality then make this a function or a class
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        # new zombie img
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        # new bullet img
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        # new custom test myturret img
        self.my_turret_img = pg.image.load(path.join(img_folder, MY_TURRET_IMG)).convert_alpha()
        # scale up our new loaded wall image to the tilesize, if need to reuse functionality then make this a function or a class
        self.paywall_img = pg.image.load(path.join(img_folder, PAY_WALL_IMG)).convert_alpha()
        self.paywall_img = pg.transform.scale(self.paywall_img, (TILESIZE, TILESIZE))        
        
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
        
        # self.player_blur3_img = pg.image.load(path.join(img_folder, PLAYER_BLUR3_IMG)).convert_alpha()
        # self.player_injury_img = pg.image.load(path.join(img_folder, PLAYER_INJURY1_IMG)).convert_alpha()

    def new(self):              
        # initialize groups for stuff in game and do all the rest of the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.breakablewalls = pg.sprite.Group() # should be called barricades huh
        self.paywalls = pg.sprite.Group()    
            
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
                            if tile == "B":
                                # place a breakablewall test
                                BreakableWall(self, col, row, self.player)  
                            if tile == "M":
                                # place a paywall
                                PayWall(self, col, row, self.player)  
                        if run == 3:    
                            if tile == "Z":
                                # place a breakablewall test
                                Mob(self, col, row, self.breakablewalls)                       
                        if run == 1:
                            # if the tile is a P, this is the player
                            if tile == "P":
                                # spawn them at the col, row position on the map 
                                self.player = Player(self, col, row)
        spawn_stuff_on_map()                          
        self.camera = Camera(self.map.width, self.map.height)

    def run(self): 
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
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

        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE # we can have base damage and subclasses of mobs to get around this, plus then also stuff like armor so chill lol
            # have the mob stop again
            if self.player.health <= 0:
                # game over man, game over
                Comment.all_comments = [] # for now, wipe the comments if u die
                self.playing = False 
        if hits:
            print(f"[ {self.player.health}hp ] Player got Bitchslapped by {hits[0].myname}")
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
            # new clout stuff
            if self.player.clout_rating_base_timer: # if the clout rating timer is running / active and we just got hit by a zombie
                self.player.is_clout_bonus_active = False
                self.player.clout_rating_base_timer = False # the player got hit so turn off our timer
                # some way to print this on screen to the player, or flag it or sumnt idk
                # we now also need a clout cooldown timer for the player thats started here too 

        # to add to player if you we're hit so you've now lost any streak u had by us turning off the active bonus timer, also activate the cooldown timer here too

        # k so big note, already know how to add bullets going thru say 5 zombies then dying functionality
        # for bulletstreaks n shit, but problem is it counts every time again, would be an easy enough solution but diminishing returns rn so leaving for now

        # bullets hit mobs <= this type of implementation here is likely a good starting point for handling ui stuff like killstreaks i reckon
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True) # zombie stay, bullets go
        for hit in hits:
            # was previously constant global from settings as player_damage, now we need to set it for crits hence this, temp for now anywayas
            hit.health -= self.player.player_damage
            
            # tho do need to do collisions properly seems so far that the way ive set it up, it is still only crit for the bullet that is crit, not for any others flying around
            # i think so anyway but unsure, either way need to do collisions properly anyway so dw for now
            if self.player.player_damage >= 100: 
                print("CRIT BAYBAYYYYY!")
                self.player.player_damage = 10
                # just some quick extra rotation for randomness during this heavier crit pushback
                hit.look_at(vec(hit.pos.x - 10, hit.pos.y - 10)) 
                # make this bullet temporarily push the zombie back if its a crit
                hit.vel = vec(-150,0)
            else:
                hit.vel = vec(0,0)
                # make this bullet temporarily slow the zombie a normal amount
                hit.vel = vec(0,0)                
            print(f"UPDATE - zombie {hit.myid} on {hit.health}hp, {self.player.player_damage = }")                
            if hit.health <= 0:
                if not self.player.clout_rating_base_timer and not self.player.clout_cooldown_timer:  # or is_clout_bonus_active ?
                    # you've killed a zombie, so if this is not on, and also not on cooldown, then activate the clout bonus, else it is just running
                    self.player.is_clout_bonus_active = True 
                print(f"{hit.myname} has Died [ hp: {hit.health} ]")
                self.clout_streak += 1
            else:
                print(f"[ {hit.health} to {hit.health - self.player.player_damage}hp ] - zombie {hit.myid} 'OOF' - player dealt [ {self.player.player_damage}hp ] damage ")
        # test and temp af
        # test_timer = pg.time.get_ticks() 
        # if test_timer - self.player.clout_rating_base_timer > 5000: # if ur 5 second timer has ran out

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self): # go through all the sprites and draw them on the screen
        # temp
        if Bullet.bullet_hit:
            accuracy = (Bullet.bullet_hit / Bullet.bullet_count) * 100
        else:
            accuracy = 0
        # temp, set the caption of the window to be any core debug things, framerate etc
        pg.display.set_caption(f"FPS: {self.clock.get_fps():.2f}, ShotsHit: {Bullet.bullet_hit}, ShotsFired: {Bullet.bullet_count}, ShotAccuracy: {accuracy:.0f}%, RoundEarnings:{self.player.player_gold}, AutoShoot: {self.player.autoshoot}, Energy: {self.player.sprint_meter:.0f}, State: {self.player.state_state}-{self.player.state_moving}, Interacting: {self.player.is_interacting}, Player: {self.player.pos} / {self.player.vel} / {self.player.rot:.0f}, Gold: {self.player.player_gold}") # pos, vel, rot, sprint_meter, state_moving, state_state, is_interacting, player_gold
        # -- actual main draw stuff --
        # actual draw stuff
        self.screen.fill(BGCOLOR)
        # self.screen.blit(self.test_bg_img, (0,0)) # the fake twitch bg test
        want_grid = False
        # for debugging -> draw the players rectangle, and hitbox
        draw_rect = True
        # -- draws player collider --
        if draw_rect:
            # pg.draw.rect(self.screen, WHITE, self.camera.apply(self.player), 2)
            # wont draw hit rect which is weird af
            pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 5) 
        # -- draw grid --
        if want_grid:
            self.draw_grid()
        # -- the main draw sprites loop --
        for sprite in self.all_sprites:
            # only do this draw for instances of the zombie mob
            if isinstance(sprite, Mob):
                # personal custom zombie name display, note this isn't a sprite or part of the sprint (cause img size = bounds) but drawn ontop during the render so has layering considerations which is why the name is drawn on first, then the hp bar (?)
                destination = self.camera.apply(sprite).copy()
                destination.move_ip(-10, TILESIZE/2)
                self.screen.blit(sprite.draw_name(), destination) #self.camera.apply(sprite)) #.move(0, -TILESIZE / 2)) # .move moves it back half a tile behind us, depending on our rotation 
                # actually clean draw health
                sprite.draw_health()
            # take the camera and apply it to that sprite 
            self.screen.blit(sprite.image, self.camera.apply(sprite))  
        # -- nested func for rendering basic text which guna move to ui functs shortly --
        # literally is just here cause its used regularly while figuring things out so pointless moving it            
        def render_to_basic_ui(text, x, y, color=None, font_size=12, want_font="silk_bold", alignment="center"):
            # personal basic af test ui stuff
            if want_font == "silk_bold":
                font = pg.font.Font("Silkscreen-Bold.ttf", font_size) # font = pg.font.SysFont("arial", 16) # create the font object
            elif want_font == "silk_regular":
                font = pg.font.Font("Silkscreen-Regular.ttf", font_size)
            if color == "rating": # the colours here do change based on things which should keep tbf but dont over kill it tho
                text = font.render(f'{text}', True, RED if self.player.clout_rating_base_timer else YELLOW, BLUEMIDNIGHT) # use the font object to render ur text
            elif color == "earnings":
                text = font.render(f'{text}', True, GREEN if self.player.won_clout else YELLOW, BLUEMIDNIGHT) # use the font object to render ur text  
            elif color == "zombies": # the colours here do change based on things which should keep tbf but dont over kill it tho
                text = font.render(f'{text}', True, GREEN if Mob.get_my_hps() < 9 else RED, BLUEMIDNIGHT) # use the font object to render ur text   
            elif color == "weapons": # the colours here do change based on things which should keep tbf but dont over kill it tho
                text = font.render(f'{text}', True, MAGENTA if self.player.autoshoot else YELLOW, BLUEMIDNIGHT) # use the font object to render ur text                                 
            elif color == "green": # temp, for has_won clout multiplier stuff, so need to proper implementation, as will everything here tbf
                text = font.render(f'{text}', True, GREEN, BLUEMIDNIGHT)
            else:
                text = font.render(f'{text}', True, HIGHLIGHTER, BLUEMIDNIGHT) # use the font object to render ur text             
            textRect = text.get_rect() # then create a surface for the rect 
            textRect.x = x # put the center of that rect where we want it
            if alignment == "right":
                textRect.midright = (x, 28) # fyi this y is surely rect.centery or rect.width / 2 or sumnt but not 28 pls duhh
            textRect.y = y # put the center of that rect where we want it        
            # copy the text surface object to the screen and render at the given center pos
            self.screen.blit(text, textRect)
        player_clip_size = self.player.return_clip_size()
        bullets_remaining = self.player.return_clip_size() - self.player.clip_counter
        # -- ui text renders --
        # temp to do proper
        render_to_basic_ui(f"Rating: {self.player.get_display_clout_rating()} [{self.player.clout_rating_detail}]", x = 20, y = 50, color = "rating") 
        render_to_basic_ui(f"Weapon: {self.player.current_weapon.title()}", x = 20, y = 70, color = "weapon") 
        render_to_basic_ui(f"Episode Earnings: ${self.player.player_gold}", x = 20, y = 90, color = "earnings") 
        render_to_basic_ui(f"Zombies Remaining: {Mob.get_my_hps()}", x = 20, y = 110, color = "zombies") 
        render_to_basic_ui(f"Bullets Remaining: {bullets_remaining}", x = 20, y = 130, color = "weapon") 
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

        # ---- draw player clout multiplier bar stuff ----
        # -- the large clout rating letter + title --
        render_to_basic_ui(f"Clout Rating: ", x = 950, y = 530, want_font="silk_regular", font_size=14) 
        render_to_basic_ui(f"{self.player.get_display_clout_rating()}", x = 1085, y = 530, font_size=44)
        # if atleast 1 zombie is still alive 
        if Mob.get_my_hps():
            if self.player.is_clout_bonus_active:
                # -- the small potential winnings pot during clout level activation --
                render_to_basic_ui(f"$100,000", x = 1078, y = 555, color="green", want_font="silk_regular", font_size=24, alignment="right") # viewer boost / subscriber boost
                # -- for flashing going viral text -- ... >> make own function or decorator! <<   :o
                flash_viral = pg.time.get_ticks() 
                flash_viral = int(f"{flash_viral}"[1])
                if flash_viral % 5 != 0: # if the highest digit number is even on if not off, for flash   
                    render_to_basic_ui(f"Going Viral? ", x = 900, y = 600, want_font="silk_regular", font_size=20) # viewer boost / subscriber boost
                    flash_viral = False
                # -- semi large clout multiplier number  --
                render_to_basic_ui(f"x{self.player.clout_sub_level}", x = 1080, y = 600, font_size=24)
                # -- clout level multiplier charge bar --
                draw_a_chargebar(self.screen, 905, 635, self.player.sub_clout_time, bar_width=220, bar_height=25)
        else:
            # want_celebrate => stop the player, ideally make him spin around shooting, temp implementation anyways
            want_celebrate = False
            if want_celebrate:
                self.player.rot += 5
                self.player.vel = vec(1,0)
                # pos = self.player.pos # + BARREL_OFFSET.rotate(-self.player.rot) # was for shooting bullets idea but didnt get there in the end and forget it for now anyways

        # -- new test ui stuff --
        # handle (temp test) comment cooldown timer
        cd_check = pg.time.get_ticks()
        if self.twitch_chat.is_spawn_on_cooldown: # if the timer is running
            if self.twitch_chat.is_chat_maxed_out:
                self.twitch_chat.is_spawn_on_cooldown = True # dont draw if its maxed out (for now anyway, as we can handle a different way ooo)
            elif cd_check - self.twitch_chat.is_spawn_on_cooldown > 2000: # every 2 sec, # elif so if above is true we can skip this
                self.twitch_chat.is_spawn_on_cooldown = False

        # draw the sidebar
        if self.want_twitch:
                
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
            
        # -- finally done, flip the display and render complete --
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()


