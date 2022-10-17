import pygame as pg
from settings import *
import pytmx

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class TiledMap:
    def __init__(self, filename):
        """ load the file """
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tilewidth
        self.tmxdata = tm

    def render(self, surface):
        """ go through the tiled data that theyre listed in the file (ground/0 first, etc etc) until they are rendered """
        # define the image that goes with a set tile id
        ti = self.tmxdata.get_tile_image_by_gid # aliasing the command
        for layer in self.tmxdata.visible_layers: # go through the visible layers only
            if isinstance(layer, pytmx.TiledTileLayer): # if that layer is a tile layer (not object or image)
                for x,y,gid in layer:
                    tile = ti(gid) # get the tiles grid id
                    if tile: # if its a tile
                        surface.blit(tile, (x * self.tmxdata.tilewidth, 
                                            y * self.tmxdata.tilewidth)) # blit the tile where it is supposed to be from the tiled tilemap data
        
    def make_map(self):
        """ run when we load the file > load the file then make map """
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_to_rect(self, rect): # [CUSTOM-TEST]
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
