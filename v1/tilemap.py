import pygame as pg
from settings import *

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

class Camera:
    # track the offset for where we draw the camera based on the objects on the map 
    def __init__(self, width, height):
        # track using a rect
        self.camera = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # apply this to an object, entity could end it a mob, a wall, whatever
        # return that entities rectangle, and move it by whatever our camera coordinates are
        # the move command when applied to a rect gives you back a rectanlge that is shifted by the amount sent as a parameter
        return entity.rect.move(self.camera.topleft)
    
    def update(self, target):
        # for update, we want to follow a sprite, which will be the player
        # adjust where the x and y of the camera are needed to shift to
        # we need to move in the oppsite direction of the player to offset the camera
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)
        self.camera = pg.Rect(x, y, self.width, self.height)
        
        # limit scrolling to map size
        # set the offset to either what its got back based on the true position of the camera, or some other offset value, 0 for at the wall, less than zero for further away
        x = min(0, x) # left
        y = min(0, y) # top
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)