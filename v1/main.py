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

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

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
         
        # self.player_blur3_img = pg.image.load(path.join(img_folder, PLAYER_BLUR3_IMG)).convert_alpha()
        # self.player_injury_img = pg.image.load(path.join(img_folder, PLAYER_INJURY1_IMG)).convert_alpha()

    def new(self):              
        # initialize groups for stuff in game and do all the rest of the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.breakablewalls = pg.sprite.Group() # should be called barricades huh
        self.unlockwalls = pg.sprite.Group()         
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
                self.playing = False 
        if hits:
            print(f"[ {self.player.health}hp ] Player got Bitchslapped by {hits[0].myname}")
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

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
                print(f"{hit.myname} has Died [ hp: {hit.health} ]")
            else:
                print(f"[ {hit.health} to {hit.health - self.player.player_damage}hp ] - zombie {hit.myid} 'OOF' - player dealt [ {self.player.player_damage}hp ] damage ")
        #    
        # yeah for really all stats stuff to be done here duh!

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
        
        # personal new test af draw stuff
        font = pg.font.SysFont("arial", 16) # [ HERE! ] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,

        # actual draw stuff
        self.screen.fill(BGCOLOR)
        want_grid = False
        # for debugging -> draw the players rectangle, and hitbox
        draw_rect = True

        if draw_rect:
            # pg.draw.rect(self.screen, WHITE, self.camera.apply(self.player), 2)
            # wont draw hit rect which is weird af
            pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 5) 

        if want_grid:
            self.draw_grid()
            
        for sprite in self.all_sprites:

            # only do this draw for instances of the zombie mob
            if isinstance(sprite, Mob):
                destination = self.camera.apply(sprite).copy()
                destination.move_ip(-10, TILESIZE/2)
                self.screen.blit(sprite.draw_name(), destination) #self.camera.apply(sprite)) #.move(0, -TILESIZE / 2)) # .move moves it back half a tile behind us, depending on our rotation 
                sprite.draw_health()

            # take the camera and apply it to that sprite 
            self.screen.blit(sprite.image, self.camera.apply(sprite))  

        # before final final flip
        draw_player_health(self.screen, 20, 20, self.player.health / PLAYER_HEALTH)
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



# TUT AND CLOUT RATING! + GOLD SCORE & UNLOCK

# DO FAKER NAMES AND FINISH TUT PLS!

# check out some new art work pls, especially main character

# look into ui and animations and vfx pls 

# zombie logic for getting stuck, if touching wall, go to nearest sumnt ?


# rn do the vids and continue as rapidly as possible
# however
# if u really quickly wanna try destroying walls, say by 3 bumps into them, having them change colour to show hp
# or by button press, with button to build back up too 