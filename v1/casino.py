import pygame as pg
from settings import *
from random import randint

MENU_SIZE = (1000, 500) # 1408 x 768
REEL_SIZE = (MENU_SIZE[0]/4, MENU_SIZE[1])# (MENU_SIZE[0]/6, MENU_SIZE[1]/2)
BACKGROUND_COLOR = (30, 40, 50)

# just guna do 3 wheel roller with no extras to start
# then when working actually refactor it for what you want
# and maybe do the art for it
# and maybe some extra art too

class Casino_Roller(object):
    """ basic first test implementation of random one eyed bandit roller """
    def __init__(self, game):
        self.game = game
        self.image = pg.Surface(MENU_SIZE)
        self.rect = self.image.get_rect(x=WIDTH - MENU_SIZE[0]) # width minus the width of the actual sidebar size (not the img so its squished?)
        self.pos = vec(self.rect.x, self.rect.y)
        self.centerpos = vec(self.rect.centerx, self.rect.centery) # self.rect.x = 774, self.rect.centerx = 899

    # def update(self): # player
    #     """ update and redraw all elements to the image """
    #     roll = randint(1,2)
    #     if roll > 1:
    #         self.image.fill(GREEN)
    #     else:
    #         self.image.fill(RED)

    def draw(self, surface):
        """ standard draw """
        surface.blit(self.image, ((WIDTH / 2) - (self.rect.width / 2),  (HEIGHT / 2) - (self.rect.height / 2)))  
        self.image.fill(WHITE)
        reel_1 = Roller_Reel(self.game, colr=BLUE)
        reel_2 = Roller_Reel(self.game, colr=GREEN)
        reel_3 = Roller_Reel(self.game, colr=RED)
        reel_1.draw_reel(self.image, x=0)
        reel_2.draw_reel(self.image, x=REEL_SIZE[0] + REEL_SIZE[0] / 2)
        reel_3.draw_reel(self.image, x=(REEL_SIZE[0] * 2) + REEL_SIZE[0])
        # self.update()

class Roller_Reel(object): 
    """ gutters for each lane/reel """
    def __init__(self, game, colr):   
        self.game = game
        self.image = pg.Surface(REEL_SIZE)
        self.rect = self.image.get_rect(x=WIDTH - MENU_SIZE[0]) # width minus the width of the actual sidebar size (not the img so its squished?)
        self.pos = vec(self.rect.x, self.rect.y)
        self.centerpos = vec(self.rect.centerx, self.rect.centery)
        self.image.fill(colr)

    def draw_reel(self, surf, x=0, y=0):
        """ """
        surf.blit(self.image, (x, y))  

    # do showing dmg numbers too btw
    # should do pick up gold, requires items tut, and likely requires tiled tut, so dont do now - do after full refactor idea after finishing that base tut from new fork

    # so ig how this works is actually just the cards selected are on each reel, the display doesnt matter at all
    # you just need to know where in the reel it is, as list and index should be fine
    # and then you just pick one from random based on the odds
    # and stop the reel at that image

    # so ig since guna refactor anyway basically straight after
    # do fixed images n stuff first
    # ig just a list of images or whatever
    # and then you randomly place each one on the strip
    # and then spin the strip with an overlay img which you could totally do custom reel (lol) quick

    # start with ig double shot, uzi, gold, companion sumnt
    # grab these images and then get them on the strip
    # when on the strip get it spinning
    # when spinning get it randomly choosing based on odds
    # when odds get it stopping on the correct image
    # then do the overlay
    # then wire it all up for the logic
    # then make it a tad fancy maybe - or better, fully plan it tbf
    # then refactor
