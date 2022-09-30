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
        self.map = Map(path.join(game_folder, 'map2.txt'))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.breakablewalls = pg.sprite.Group() # should be called barricades huh
        self.unlockwalls = pg.sprite.Group()
        def spawn_stuff_on_map(first_run=True):
            # first run = run only player first 
            # why? = because we need to pass the player object to instances of other interactive things on the map like walls
            # otherwise we have to place the player above any interactive elements, now we can place the player anywhere
            # enumerate over the map data as each line is a row on the map from top to bottom
            for row, tiles in enumerate(self.map.data):
                # for each tile, which is the actual string for each row `1....1`
                # enumerate as tiles here becomes the actual character in that position in the string,
                # and the col becomes the index/x_position of that character in the string/on the map
                for col, tile in enumerate(tiles):
                    if not first_run:
                        # if the tile is a 1, this is a wall tile
                        if tile == "1":
                            # place a wall at this column and row on the actual map, from the col and row on the tilemap
                            Wall(self, col, row)
                        if tile == "B":
                            # place a breakablewall test
                            BreakableWall(self, col, row, self.player)
                        if tile == "U":
                            UnlockWall(self, col, row, self.player)
                        if tile == "u":
                            UnlockWall(self, col, row, self.player, is_wide=False)                            
                    else:
                        # if the tile is a P, this is the player
                        if tile == "P":
                            # spawn them at the col, row position on the map 
                            self.player = Player(self, col, row)
        spawn_stuff_on_map()
        spawn_stuff_on_map(False)                            
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

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            # take the camera and apply it to that sprite
            self.screen.blit(sprite.image, self.camera.apply(sprite))
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




# rn do the vids and continue as rapidly as possible
# however
# if u really quickly wanna try destroying walls, say by 3 bumps into them, having them change colour to show hp
# or by button press, with button to build back up too 