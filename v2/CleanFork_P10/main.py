import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from player import Player


# HUD functions
def draw_player_health(surf, x, y, pct):
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
        img_folder = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'map3.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha() 
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        # test images
        self.lego_img = pg.image.load(path.join(img_folder, LEGO_IMG)).convert_alpha()
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
        # new test concept for drawing damage numbers on screen
        self.damage_numbers_positions_list = []
        self.damage_numbers_pos_timers_list = []
        self.random_rotation = 0

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

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
            
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
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

    def zombie_hit_player(self, sprite):
        # deal damage to the player
        self.player.current_health -= MOB_DAMAGE
        # move back the zombie that landed the hit
        sprite.vel = vec(0, 0)
        # reset the chargebar for the zombie that landed the hit
        sprite.landed_attack = False
        # if the player gets hit and has no hp they end the game
        if self.player.current_health <= 0:
            self.playing = False
    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        for sprite in self.all_sprites:
            # -- zombie mob sprites --
            if isinstance(sprite, Mob):
                # draw unit health with hp block segments
                draw_unit_health(sprite) # previously, sprite.draw_unit_health() before that, sprite.draw_health()
                # draw the unit status
                draw_unit_status(sprite)
                # draw level box with level number
                draw_unit_level(sprite)
                # draw the units name stationary within the health and level bounds, note - is different from OG draw_name which drew the name directly underneath with some rotation considerations
                sprite.draw_unit_name()
                # draw the unit action chargebar, only activating charging an attack when the player is close (make this a function btw)
                # - check the zombie distance to the player
                # - if its close start its timer for its hit,
                # - if it loses range reset the timer, 
                # - if it stays in range keep timing
                # - then hit and perform hit actions and reset
                distance_to_player = how_near(sprite, self.player.pos.x, self.player.pos.y)
                if distance_to_player < 150:
                    # if zombie is close and theres no timer start the timer
                    if not sprite.attack_timer:
                        sprite.attack_timer = pg.time.get_ticks()
                    # else if the zombie is close and the timer is running      
                    else:
                        check_timer = pg.time.get_ticks()
                        true_timer = check_timer - sprite.attack_timer
                        # if its on and over 1.5s reset it
                        if true_timer >= 2500:
                            self.zombie_hit_player(sprite)
                            sprite.attack_timer = 0
                        sprite.draw_unit_action_chargebar((true_timer / 1500) * 97)
                else:
                    sprite.draw_unit_action_chargebar(0)
                    # -- player sprite --
            if isinstance(sprite, Player):  
                if self.mobs:      
                    sprite.draw_player_name()  
                    draw_unit_health(sprite)                                   
                    draw_unit_status(sprite)
                    draw_unit_level(sprite)
                    # new reload & super chargebar test implementation
                    if not sprite.reload_chargebar:
                        sprite.reload_chargebar = pg.time.get_ticks()
                    # else if the zombie is close and the timer is running      
                    else:
                        check_timer = pg.time.get_ticks()
                        true_timer = check_timer - sprite.reload_chargebar
                        # if its on and over 2000 reset it
                        if true_timer >= 1500:
                            sprite.reload_chargebar = 0
                        sprite.draw_player_chargebar((true_timer / 1500) * 136) # multiplied by bar length
                # -- new test for conversations --
                else: # else if not self.mobs:
                    sprite.draw_unit_conversation('"pfff... too easy"') 
            # blit the sprite to the screen
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # -- for test implementation of displaying damage numbers --
        if self.damage_numbers_positions_list:
            for position in self.damage_numbers_positions_list:
                self.draw_damage_numbers(position, self.randomised_bullet_damage)
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
        
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


    # ---- new custom functions ----

    # needs slight persistance
    # randomise the positions slightly
    # maybe add some transparency
    def draw_damage_numbers(self, position, damage=100): # [CUSTOM]
        self.damage_number_text_surface = self.MEMESBRUH_32.render(f"{damage}", True, WHITE).convert_alpha() # "text", antialias, color
        # different colour border for higher numbers, do this for crits surely, or atleast use the concept
        if damage > 50:
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

        # THEN YOU JUST STORE ANOTHER LIST WITH EACH DICTS TIMER
        # AND WHEN EACH TIMER HITS ITS MAX
        # YOU REMOVE THE ITEM FROM THE LIST
        # CHEFSKISS.PNG
        # THEN
        # FINISH ZOMBIE BAR UI STUFF (status/statuses, chargebar below hit for hits activate when close and stops at full fine for now, blue bar below that that can be toggled dull/grey)
        # THEN
        # NEW PLAYER SPRITE
        # NEW ZOMBIE SPRITE
        # NEW ARMORED ZOMBIE SPRITE OR SUMNT SIMILAR WHICH CAN JUST PUT AT LIKE LVL 5 FOR NOW OR SUMNT 
        # PUT BAR ON PLAYER

        # THEN FOR TOMO IG MAYBE
        # START WITH ADDING CLEAN COMPANION?
        # TBF SEE PHONE NOTES 
        
        
        
    # for numbers display idea
    # store a list of numbers that you want to display with their positions
    # display them
    # this would be good as would allow for timing too so they could persist past the bullets death / kill
    # you just empty them at a certain rate, doesnt even have to be a timer a simple countdown will work too tbf, quickest way to test too
        

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
