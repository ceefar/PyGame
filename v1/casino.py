import pygame as pg
from settings import *
from random import randint

MENU_SIZE = (1000, 500) # 1408 x 768
# REEL_SIZE = (MENU_SIZE[0]/8, MENU_SIZE[1])# (MENU_SIZE[0]/6, MENU_SIZE[1]/2)
BACKGROUND_COLOR = (30, 40, 50)
CARDS_LIST = ["G", "G+", "G++"] # player or total as different to do, so only total will be global but is fine for now



# rename da ting
# implement update and acc vel pos to get it infinitely scrolling from top to bottom
# get it to stop on a timer
# then decide if wanna do flashing light cube or roller idea
# then do it while styling at the same time

class Testy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.casino
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        

class Casino_Roller(pg.sprite.Sprite): # (object) ?
    """ basic first test implementation of random one eyed bandit roller """
    def __init__(self, game):
        self.game = game
        self.image = pg.Surface(MENU_SIZE)
        self.rect = self.image.get_rect(x=WIDTH - MENU_SIZE[0]) # width minus the width of the actual sidebar size (not the img so its squished?)
        self.pos = vec(self.rect.x, self.rect.y)
        self.centerpos = vec(self.rect.centerx, self.rect.centery) # self.rect.x = 774, self.rect.centerx = 899

    def draw(self, surface):
        """ standard draw """
        surface.blit(self.image, ((WIDTH / 2) - (self.rect.width / 2),  (HEIGHT / 2) - (self.rect.height / 2)))  
        self.image.fill(WHITE)
        testy = Testy(self.game, 1, 1)
        print(f"{testy.rect = }")
        print(f"{self.rect = }")
        self.image.blit(testy.image, testy.rect)                  


        # for sprite in self.all_sprites:
        #     # only do this draw for instances of the zombie mob
        #     if isinstance(sprite, Mob):
        #         # personal custom zombie name display, note this isn't a sprite or part of the sprint (cause img size = bounds) but drawn ontop during the render so has layering considerations which is why the name is drawn on first, then the hp bar (?)
        #         destination = self.camera.apply(sprite).copy()
        #         destination_status = self.camera.apply(sprite).copy()
        #         destination_attack_bar = self.camera.apply(sprite).copy()
        #         destination.move_ip(-10, TILESIZE/2) # in place btw
        #         destination_status.move_ip(-20, -TILESIZE/2)
        #         destination_attack_bar.move_ip(20, -TILESIZE/2)
        #         if self.want_zombie_names:
        #             self.screen.blit(sprite.draw_name(), destination) #self.camera.apply(sprite)) #.move(0, -TILESIZE / 2)) # .move moves it back half a tile behind us, depending on our rotation 
        #             self.screen.blit(sprite.draw_status(), destination_status) 
        #         # actually clean draw health
        #         sprite.draw_health()




    # uh yah, its because these aren't sprites
    # imo just try this again from scratch for a few hours
    # if it doesnt flow after the first hour and a bit
    # do the fork tut to end idea then restart it cleanly imo, starting at ui 

    # custom border, custom card, custom reel, custom bg - all imgs btw
    # also please shortly do other ui things too, damage numbers, subscribers bar, bottom right charge like persona, top right more custom too, card for companion/items, etc

    # do showing dmg numbers too btw

    # should do pick up gold, requires items tut, and likely requires tiled tut...
    # - so dont do now, do after full refactor idea after finishing that base tut from new fork






    # start with ig double shot, uzi, gold, companion sumnt
    # grab these images and then get them on the strip
    # when on the strip get it spinning
    # when spinning get it randomly choosing based on odds
    # when odds get it stopping on the correct image
    # then do the overlay
    # then wire it all up for the logic
    # then make it a tad fancy maybe - or better, fully plan it tbf
    # then refactor
