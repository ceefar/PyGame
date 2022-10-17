import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from player import Player


# HUD functions
def draw_player_health(surf, x, y, pct): # [DEPRECIATED]
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img') # where we are saving our img (png) files
        map_folder = path.join(game_folder, 'Tiled') # where we are saving our tmx files
        self.map = TiledMap(path.join(map_folder, 'level2.tmx')) # load the new tiled map
        self.map_img = self.map.make_map() # make a surface for the Tiled map
        self.map_rect = self.map_img.get_rect() # and grab rect so we can locate on the screen where to draw it
        # self.map = Map(path.join(game_folder, 'map3.txt')) < old map loading code
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha() 
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        # new custom images
        self.gun_pistol_img = pg.image.load(path.join(img_folder, GUN_PISTOL_IMAGE)).convert_alpha()
        self.gun_pistol_img = pg.transform.scale(self.gun_pistol_img, (TILESIZE, TILESIZE)) # (TILESIZE, TILESIZE) # (TILESIZE*2, TILESIZE*2)
        self.gun_uzi_img = pg.image.load(path.join(img_folder, GUN_UZI_IMAGE)).convert_alpha()
        self.gun_uzi_img = pg.transform.scale(self.gun_uzi_img, (84, 40))
        self.gun_pistol_nulled_img = pg.image.load(path.join(img_folder, GUN_PISTOL_NULLED_IMAGE)).convert_alpha()
        self.gun_pistol_nulled_img = pg.transform.scale(self.gun_pistol_nulled_img, (TILESIZE, TILESIZE))
        self.gun_uzi_nulled_img = pg.image.load(path.join(img_folder, GUN_UZI_NULLED_IMAGE)).convert_alpha()
        self.gun_uzi_nulled_img = pg.transform.scale(self.gun_uzi_nulled_img, (84, 40))
        # test images
        self.lego_img = pg.image.load(path.join(img_folder, LEGO_IMG)).convert_alpha()
        # fx images
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()

        # load fonts
        # choices
        # ka1.ttf # Silkscreen-Regular.ttf # upheavtt.ttf # Daydream.ttf # superstar_memesbruh03.ttf # Kappa_ (various)
        # silkscreen
        self.FONT_SILK_REGULAR_10 = pg.font.Font("Silkscreen-Regular.ttf", 10) # more here than needed to test, remove those unused when ui is finalised 
        self.FONT_SILK_REGULAR_12 = pg.font.Font("Silkscreen-Regular.ttf", 12)
        self.FONT_SILK_REGULAR_14 = pg.font.Font("Silkscreen-Regular.ttf", 14)
        self.FONT_SILK_REGULAR_16 = pg.font.Font("Silkscreen-Regular.ttf", 16)
        self.FONT_SILK_REGULAR_18 = pg.font.Font("Silkscreen-Regular.ttf", 18)
        self.FONT_SILK_REGULAR_22 = pg.font.Font("Silkscreen-Regular.ttf", 22)
        self.FONT_SILK_REGULAR_24 = pg.font.Font("Silkscreen-Regular.ttf", 24)
        self.FONT_SILK_REGULAR_32 = pg.font.Font("Silkscreen-Regular.ttf", 32)
        # memesbruh
        self.FONT_MEMESBRUH_22 = pg.font.Font("superstar_memesbruh03.ttf", 22) 
        self.MEMESBRUH_32 = pg.font.Font("superstar_memesbruh03.ttf", 32) # rename these, they need FONT_
        self.MEMESBRUH_36 = pg.font.Font("superstar_memesbruh03.ttf", 36) # rename these, they need FONT_
        self.MEMESBRUH_44 = pg.font.Font("superstar_memesbruh03.ttf", 44) # rename these, they need FONT_
        # kappa
        self.FONT_KAPPA_BLACK_22 = pg.font.Font("Kappa_Black.otf", 22)
        # upheavtt
        self.FONT_UPHEAVTT_22 = pg.font.Font("upheavtt.ttf", 22)
        # ka1
        self.FONT_KA1_22 = pg.font.Font("ka1.ttf", 22)
        # daydream
        self.FONT_DAYDREAM_22 = pg.font.Font("Daydream.ttf", 22)
        # army rust
        self.FONT_ARMYRUST_22 = pg.font.Font("ARMY RUST.ttf", 22)
        # marbella army
        self.FONT_MARBELLA_ARMY_22 = pg.font.Font("Marbella Army.otf", 22)
        # old stamper
        self.FONT_OLDSTAMPER_36 = pg.font.Font("old_stamper.ttf", 28)
        # take cover
        self.FONT_TAKECOVER_22 = pg.font.Font("Take cover.ttf", 22)
        # i pixel u
        self.FONT_IPIXELU_22 = pg.font.Font("I-pixel-u.ttf", 22)
        # new test concept for drawing damage numbers on screen
        self.damage_numbers_positions_list = []
        self.damage_numbers_pos_timers_list = []
        self.random_rotation = 0
        # temp test extension of above for when player damaged
        self.player_damage_display_dict = {}

    def new(self):
        # initialize all variables and do all the setup for a new game
        # self.all_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        # code for new Tiled setup
        # go through the objects we defined in our objects layer in our Tiled map and add in the obstacles
        for tile_object in self.map.tmxdata.objects: # dictionary of properties for each value
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == "player":
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == "zombie":
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ["health"]:
                Item(self, obj_center, tile_object.name)
        # old .txt map loading code
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        # for drawing collisions
        self.draw_debug = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # -- mobs hit player --
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits: # player has been "hit" by this zombie by colliding with it
            # trigger the bool for this zombie that will do all the necessary action during the update
            hit.landed_attack = True    
        # -- for test implementation of damage numbers display, needs to be above bullets hit mobs otherwise the mobs may die before printing the number --
        # -- bullets hit mobs --
        hits = pg.sprite.groupcollide(self.bullets, self.mobs, False, False)
        for hit in hits:
            if hit.pos not in self.damage_numbers_positions_list: # dont add the same position and print loads over each other for no reason
                self.damage_numbers_positions_list.append(hit.pos) # append it then check if its near, if it is too close to one already then remove it
                self.damage_numbers_pos_timers_list.append(pg.time.get_ticks())
        # -- mobs hit bullets --
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            self.randomised_bullet_damage = int((BULLET_DAMAGE / 100) * randint(80, 120))# regardless of what the damage will be give it a 80 - 100% range
            hit.current_health -= self.randomised_bullet_damage
            hit.vel = vec(0, 0)
    
    # idea => maybe a charge attack could slow you or sumnt similar, still fling u back tho obvs
    def zombie_hit_player(self, sprite, hit_type, damage=None):
        """ do all actions required after the player is hit by a zombie
            - hit_type: `str` , 'charge' and 'proximity' """
        # if no damage passed set the damage to the sprites damage
        if not damage:
            damage = sprite.my_damage 
        # deal damage to the player based on the type of hit, notably if you get fully surrounded since collisions between player and zombies arent on, they can kill you super quick in a corner, kinda like tho but can be altered or removed if necessary
        if hit_type == "proximity": # if you deal damage because ur super close do less
            self.player.current_health -= damage
            knockback = sprite.my_knockback
        else: # else charge hit
            self.player.current_health -= damage # temp for now, if you charged up a hit, do a thats a lotta damage
            knockback = sprite.my_knockback * 1.5 # 50% extra the knockback to push player further for a charged hit
            # test => rotate the player a bit, within a random range, after a charge shot, bit of a random test so can be commented out or removed
            randtest = randint(-40, 40) # randtest *= -1 if sprite.rot >= 0 else 0
            self.player.rot += randtest
        # move the player back in the opposite direction rotation of the zombie that just hit him
        self.player.pos += vec(knockback, 0).rotate(-sprite.rot)
        # move back the zombie that landed the hit
        sprite.vel = vec(0, 0)
        # reset the chargebar for the zombie that landed the hit
        sprite.landed_attack = False
        # if the player gets hit and has no hp they end the game
        if self.player.current_health <= 0:
            self.playing = False
        # reset the hit timer
        sprite.attack_timer = 0
    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR) # fill background (before Tiled) 
        self.screen.blit(self.map_img, self.camera.apply_to_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            # -- zombie mob sprites --
            if isinstance(sprite, Mob):
                # draw unit health with hp block segments
                draw_unit_health(sprite) # previously, sprite.draw_unit_health() before that, sprite.draw_health()
                # -- new clumped stuff btw --
                # but not if ur clumped                
                # draw the unit status
                if not sprite.is_clumped:
                    draw_unit_status(sprite)
                # draw level box with level number
                if not sprite.is_clumped:
                    draw_unit_level(sprite)
                # draw the units name stationary within the health and level bounds, note - is different from OG draw_name which drew the name directly underneath with some rotation considerations
                if not sprite.is_clumped:
                    sprite.draw_unit_name()
                # -- for handling charge and proximity hits --
                # -- charge hits are like crits and happen if a zombie stays close for too long and is in 1.5x hit range --
                # -- should put all this stuff in the function btw --
                # draw the unit action chargebar, only activating charging an attack when the player is close (make this a function btw)
                # basically is (without the proximity stuff) => check the zombie distance to the player, if its close start its timer for its hit, if it loses range reset the timer, if it stays in range keep timing, then hit and perform hit actions and reset
                distance_to_player = how_near(sprite, self.player.pos.x, self.player.pos.y)
                # two ways this zombie will attack, either being super close, or being semi close and charging an attack, almost like a swipe
                # we could also make this do different damage too ooo
                # if will hit the player by being super duper close to the player, and reset the 'attack' chargebar
                if distance_to_player < 60:
                    # you're like nearly on top of the sprite so run everything that happens when zombie lands a proximity hit on the player
                    # temporary testing - use these returns to persist the blit
                    damage_number_background_surface, background_destination, \
                    damage_number_text_surface, destination \
                        = self.draw_damage_on_screen(self.player.pos, sprite.my_damage, "player") # sprite.my_damage # "OUCH"
                    # for persisting the damage numbers on screen for a short time
                    self.player_damage_display_dict[sprite.myid] = (damage_number_background_surface, background_destination, \
                                                                    damage_number_text_surface, destination, pg.time.get_ticks())
                    # faster hit charge after a proximity hit
                    sprite.hit_charge_up_time = 800 
                    # do hit at end so we can send different damage
                    self.zombie_hit_player(sprite, "proximity")
                    # debuggy
                    # print(f"{sprite.myid}: 'PROXIMITY' [{sprite.my_damage}] HIT PLAYER, hp remaining = {self.player.current_health}")    
                # show this zombies 'attack' chargebar based on its distance to the player, at a certain range this timer starts, at the end it will hit
                if distance_to_player < 250:
                    # if a zombie is too close the player cant change weapon, feel like its realistic and an interesting constraint but obvs can be removed
                    self.player.disable_weapon_change = True
                    # if zombie is close and theres no timer start the timer
                    if not sprite.attack_timer:
                        sprite.attack_timer = pg.time.get_ticks()
                        
                    # else if the zombie is close and the timer is running      
                    else:
                        check_timer = pg.time.get_ticks()
                        true_timer = check_timer - sprite.attack_timer # print(f"{true_timer = }")
                        # if its on and over 1.5s, hit the player, which does all the stuff and resets the timer
                        if true_timer >= sprite.hit_charge_up_time:
                            # we still want this hit to have a range tho, not at any within 250px
                            if distance_to_player < 80:
                                # temporary implementation of crit damage, need to do this stuff properly and randomise it etc
                                zombie_charge_crit_damage_modifier = sprite.my_damage * float(f"1.{randint(5,9)}") # as decimal, 1.5x to 1.9x / +50% to +90%
                                # temporary testing - use these returns to persist the blit
                                # randomly either send crit or the amount of damage dealt
                                crit_display_roll = randint(1,10)
                                # 10 percent chance to roll a crit charge attack
                                # - should add this to normal attacks but at a drastically reduced rate
                                crit_damage_display = int(zombie_charge_crit_damage_modifier*2) if crit_display_roll >= 8 else int(zombie_charge_crit_damage_modifier)
                                if crit_damage_display == zombie_charge_crit_damage_modifier*2:
                                    # if you hit the 3 in 10 chance to roll a crit on this charge attack, double the 50 - 90% extra damage you already do (due to charge)
                                    modifier = 2
                                else:
                                    modifier = 1 # no extra, extra damage, just the 50 - 90% extra due to charging the hit
                                # see comment next to funct call for sending crit as text if it was a crit vs just sending crit_damage_display
                                damage_number_background_surface, background_destination, \
                                damage_number_text_surface, destination \
                                    = self.draw_damage_on_screen(self.player.pos, crit_damage_display, type="player", is_crit = True if modifier == 2 else False) # self.draw_damage_on_screen(self.player.pos, "CRIT" if crit_damage_display == zombie_charge_crit_damage_modifier*2 else crit_damage_display, type="player") # 100
                                # for persisting the damage numbers on screen for a short time
                                self.player_damage_display_dict[sprite.myid] = (damage_number_background_surface, background_destination, \
                                                                                damage_number_text_surface, destination, pg.time.get_ticks())
                                # do hit at end so we can send different damage
                                self.zombie_hit_player(sprite=sprite, hit_type="charge", damage=crit_damage_display * modifier)
                                # debuggy
                                # print(f">>> {crit_damage_display = }, {zombie_charge_crit_damage_modifier = }")
                                # print(f"{sprite.myid}: 'CHARGE ATTACK' HIT PLAYER, hp remaining = {self.player.current_health}")
                        # print the charge attack chargebar as we are in range and the timer is running
                        # - note there is no cooldown yet but do want to add that too 
                        # - maybe hack it by doing if zombie is over a certain speed lol, would work tho imo
                        if not sprite.is_clumped:
                            sprite.draw_unit_action_chargebar((true_timer / sprite.hit_charge_up_time) * 97)
                # else ur further than 250 away
                else:
                    # so ur not close enough to show a charging chargebar, hence the 0
                    sprite.draw_unit_action_chargebar(0)
                    self.player.disable_weapon_change = False
                    # -- player sprite --
            if isinstance(sprite, Player):  
                if self.mobs:      
                    sprite.draw_player_name()  
                    draw_unit_health(sprite)                                   
                    draw_unit_status(sprite)
                    draw_unit_level(sprite)
                    # new reload (& soon to be, super) chargebar mvp implementation
                    if self.player.is_reloading:
                        if not sprite.reload_chargebar:
                            sprite.reload_chargebar = pg.time.get_ticks()
                        # else if the zombie is close and the timer is running      
                        else:
                            check_timer = pg.time.get_ticks()
                            true_timer = check_timer - sprite.reload_chargebar
                            # if its on and over 2000 reset it                        
                            if true_timer >= sprite.weapon_reload_speed:
                                sprite.reload_chargebar = 0
                                sprite.is_reloading = False
                                sprite.bullets_remaining_in_clip = sprite.weapon_clipsize
                            sprite.draw_player_chargebar((true_timer / sprite.weapon_reload_speed) * 136) # multiplied by bar length
                        # new test reloading text - needs to be printed on top of the bars behind it
                        self.draw_player_reloading()
                    else:
                        # you are not reloading show show the reload bar but its empty
                        # what you actually wanna do tho is show the clip emptying
                        sprite.draw_player_chargebar((sprite.bullets_remaining_in_clip / sprite.weapon_clipsize) * 136, is_refilling=True)
                # -- new test for conversations --
                else: # else if not self.mobs:
                    if sprite.current_health > sprite.max_health / 2:
                        sprite.draw_unit_conversation('"pfff... too easy"') 
                    else:
                        sprite.draw_unit_conversation('"i wanna go home"') 
            # blit the sprite to the screen
            self.screen.blit(sprite.image, self.camera.apply(sprite)) 
            # -- debug for collisions n tings --
            if not isinstance(sprite, Mob): # want to draw the mobs debug rect based on their clumping state 
                if self.draw_debug:
                    pg.draw.rect(self.screen, MAGENTA, self.camera.apply_to_rect(sprite.hit_rect), 1)
            else:
                if self.draw_debug:
                    if sprite.is_clumped:
                        pg.draw.rect(self.screen, YELLOW, self.camera.apply_to_rect(sprite.hit_rect), 3)
                    else:
                        pg.draw.rect(self.screen, MAGENTA, self.camera.apply_to_rect(sprite.hit_rect), 1)
        # -- debug for collisions n tings --
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, SKYBLUE, self.camera.apply_to_rect(wall.rect), 1)
        # -- for test implementation of displaying damage numbers --
        if self.damage_numbers_positions_list:
            for position in self.damage_numbers_positions_list:
                self.draw_damage_on_screen(position, self.randomised_bullet_damage)
                # print(f"{position = }")
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.current_health / PLAYER_HEALTH)
        # to only have damage numbers be on screen for a short amount of time
        for i, position in enumerate(self.damage_numbers_positions_list): # everything except the one u just added
            check_timer = pg.time.get_ticks()
            on_screen_time = check_timer - self.damage_numbers_pos_timers_list[i]
            if on_screen_time > 200:
                self.damage_numbers_positions_list.pop(i)
                self.damage_numbers_pos_timers_list.pop(i)
        # temp test for player being damaged numbers
        dictionary_items_to_delete = []
        for zombie_id_key, tupled_value in self.player_damage_display_dict.items():
            check_timer = pg.time.get_ticks()
            on_screen_time = check_timer - tupled_value[-1]
            # print(f"{zombie_id_key}: {on_screen_time = }")
            # its if its over time delete the item from the dictionary
            if on_screen_time > 200:
                # so we dont change the size of the dictionary while iterating, delete after we've looped the dict
                dictionary_items_to_delete.append(zombie_id_key)
            # else blit what it stored in the dictionary
            else:
                self.screen.blit(tupled_value[0], tupled_value[1])  
                self.screen.blit(tupled_value[2], tupled_value[3])  
        # delete anything thats over time from the dictionary once the loop ends
        for item in dictionary_items_to_delete:
            del self.player_damage_display_dict[item]
        
        # test for change weapon cooldown 
        check_timer = pg.time.get_ticks()
        if check_timer - self.player.change_weapon_cooldown >= 3000:
            # if the cooldown timer has passed, reset the timer
            self.player.change_weapon_cooldown = 0
        # draw the current weapon icon with some light status stuff
        self.draw_weapon_ui()
        # to draw player hitbox rect
        want_player_hitbox = False
        if want_player_hitbox:
            pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2) 
        # finally, flip the display
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
            if event.type == pg.KEYUP:
                if event.key == pg.K_m:
                    # basic cooldown implementation to change weapons
                    print(self.player.change_weapon_cooldown)
                    if not self.player.change_weapon_cooldown: # if not running its not on cooldown, so you can change weapon 
                        self.player.handle_change_weapon()
                    else:
                        # if player tries to change weapon but its on cooldown, dont allow the change
                        # give the user some visual/audio clarity on this too
                        # - maybe the weapon dulled out and its normally highlighted a semi bright colour maybe like an army green
                        # - obvs sumnt else too, but like stuff for this for like a hardcore more
                        pass
        
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


    # ---- new custom functions ----

    def draw_player_reloading(self): # [CUSTOM] # FONT_SILK_REGULAR_22 # FONT_IPIXELU_22 < cute font tbf
        self.reloading_text_surf = self.FONT_SILK_REGULAR_22.render(f"RELOADING", True, WHITE) # "text", antialias, color # FONT_SILK_REGULAR_14 # FONT_ARMYRUST_22
        self.reloading_text_surf_bg = self.FONT_SILK_REGULAR_22.render(f"RELOADING", True, BLACK)
        x, y = self.player.pos.x, self.player.pos.y
        destination = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.camera.apply_to_rect(destination).copy()
        destination.move_ip(51, -20) 
        bg_destination = destination.copy()
        bg_destination.move_ip(2, 2) 
        # rotate the text a bit before the blit
        self.reloading_text_surf = pg.transform.rotate(self.reloading_text_surf, 4)
        self.reloading_text_surf_bg = pg.transform.rotate(self.reloading_text_surf_bg, 4)
        # flash the reloading text
        flash_timer = pg.time.get_ticks() % 300  # flash_timer = int(f"{pg.time.get_ticks() % 1000}"[0]) # hundreds unit from 1000 milliseconds on a loop 
        if flash_timer > 150: # if flash_timer % 2 == 0:
            self.screen.blit(self.reloading_text_surf_bg, bg_destination) 
            self.screen.blit(self.reloading_text_surf, destination) 

    def draw_weapon_ui(self): # new test
        padding = 10
        # first make a copy incase we want to transform the image
        weapon_ui_img = self.player.current_weapon_img.copy()
        if self.player.current_weapon == "uzi":
            weapon_ui_nulled_img = self.gun_uzi_nulled_img
        else:
            weapon_ui_nulled_img = self.gun_pistol_nulled_img
        box_size = (80, 80) # as much as its kewl to have dynamic size box like dis >>>> box_size = weapon_ui_img.get_size() <<<< it doesnt make sense / isnt necessary
        x, y = WIDTH - TILESIZE - 30, HEIGHT - TILESIZE - 30
        weapon_ui_bg = pg.Rect(x, y, box_size[0] + padding, box_size[1] + padding)
        if self.player.current_weapon == "pistol":
            nudge_x, nudge_y = 2, 11
            colr = DARKGREY
            rot = 30
        elif self.player.current_weapon == "uzi":
            nudge_x, nudge_y = 2, 21
            colr = MIDGREY
            rot = 40
                # draw the bg first so its behind the image
        pg.draw.rect(self.screen, colr, weapon_ui_bg) # PRINT RUST TAN COFFEE DARKGREY FORESTGREEN SKYBLUE PALEGREY
        # >>>>>>>>>> add a border to the background pls <<<<<<<<<<
        # if the timer is running its on cooldown, so show a nulled weapon image
        if self.player.change_weapon_cooldown > 0 or self.player.disable_weapon_change or self.player.is_reloading:
            weapon_ui_nulled_img = pg.transform.rotate(weapon_ui_nulled_img, rot)
            self.screen.blit(weapon_ui_nulled_img, (x + (padding / 2) - nudge_x, y - (padding / 2) - (TILESIZE/6) + nudge_y))
        # else show the normal version
        else:
            weapon_ui_img = pg.transform.rotate(weapon_ui_img, rot) # rotate it a bit first (maybe not for all but looks clean on pistol)
            self.screen.blit(weapon_ui_img, (x + (padding / 2) - nudge_x, y - (padding / 2) - (TILESIZE/6) + nudge_y)) # last addition to x and y here is for nudging to sweet spot

    # needs slight persistance
    # randomise the positions slightly
    # maybe add some transparency
    #
    # [ASAP!]
    # -------
    # NEED TO ADD A TYPE NOW AS IT CAN RETURN AND PRINT AT A POSITION ALSO (for persistance)
    # - rn only checking by the instance object type i.e. string or int, but want to pass ints in both cases
    # - so check for new damage_type parameter instead
    def draw_damage_on_screen(self, position, damage=100, type="mob", is_crit = False): # [CUSTOM]
        self.damage_number_text_surface = self.MEMESBRUH_32.render(f"{damage}", True, WHITE).convert_alpha() # "text", antialias, color
        # different colour border for higher numbers, do this for crits surely, or atleast use the concept
        if isinstance(damage, str): # temp af af dw
            if damage == "OOF" or damage == "CRIT": # temp af dw
                colr = RED
            else:
                colr = BLUE
        # else is an int
        else:
            if is_crit:
                colr = ORANGE # YELLOW 
            elif damage > 15: # minimum current crit/swipe zombie damage, will be changing asap tho, was just for testing
                colr = RED 
            else:
                colr = BLUEMIDNIGHT
        self.damage_number_background_surface = self.MEMESBRUH_32.render(f"{damage}", True, colr).convert_alpha() # MEMESBRUH_44
        x, y = position.x, position.y
        destination_rect = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.camera.apply_to_rect(destination_rect).copy()
        background_destination = self.camera.apply_to_rect(destination_rect).copy()
        # draw the background, i.e. the border when centralised
        # print(f"{self.damage_number_background_surface.get_width() = }, {self.damage_number_background_surface.get_width() * 1.2 = }")
        self.damage_number_background_surface = pg.transform.scale(self.damage_number_background_surface, (self.damage_number_background_surface.get_width() * 1.2, self.damage_number_background_surface.get_height() * 1.3))
        background_destination.move_ip(10, 0) # (0,0) # best way to handle moving things in place => _ip
        self.damage_number_background_surface.set_alpha(200)
        self.screen.blit(self.damage_number_background_surface, background_destination)
        # draw the foreground
        destination.move_ip(14, 4) # (+4, +4) # best way to handle moving things in place => _ip
        self.damage_number_text_surface.set_alpha(200)
        self.screen.blit(self.damage_number_text_surface, destination)  
        # test for persisting the player damage differently
        if type == "player": # return everything that was blitted... blit (?) and keep blitting (?) it on a timer
            return self.damage_number_background_surface, background_destination, self.damage_number_text_surface, destination # background, foreground


# NEW PLAYER SPRITE
# NEW ZOMBIE SPRITE
# NEW ARMORED ZOMBIE SPRITE OR SUMNT SIMILAR WHICH CAN JUST PUT AT LIKE LVL 5 FOR NOW OR SUMNT 
# ADD CLEAN COMPANION
        

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
