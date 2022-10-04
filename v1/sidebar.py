import pygame as pg
from settings import *
from random import randint

SIDEBAR_SIZE = (250, 768)
BACKGROUND_COLOR = (30, 40, 50)
SIDEBAR_COMMENT_SIZE = (250, 40)

class SideBar(object):
    """ class for the HUD which is displayed on the right of the screen """
    def __init__(self, game):
        self.game = game
        self.image = game.test_sidebar_img
        self.rect = self.image.get_rect(x=WIDTH - SIDEBAR_SIZE[0]) # width minus the width of the actual sidebar size (not the img so its squished?)
        self.pos = vec(self.rect.x, self.rect.y)
        self.centerpos = vec(self.rect.centerx, self.rect.centery) # self.rect.x = 774, self.rect.centerx = 899

    def update(self, player):
        """ update and redraw all elements to the image """
        self.image.fill(BACKGROUND_COLOR)

    def draw(self, surface, offset=0):
        """ standard draw """
        surface.blit(self.image, (self.rect.x+offset, self.rect.y))


class SideBar_Bottom(object):
    """ temp af """
    def __init__(self, game, sidebar):
        self.game = game
        self.image = game.sidebar_bottom_img
        self.rect = self.image.get_rect() # width minus the width of the actual sidebar size (not the img so its squished?)
        self.pos = sidebar.pos # vec(self.rect.x, self.rect.y)
        self.sidebar = sidebar
        # self.centerpos = vec(self.rect.centerx, self.rect.centery) # self.rect.x = 774, self.rect.centerx = 899
    
    def draw(self, surface):
        """ standard draw """
        surface.blit(self.image, (0, self.sidebar.rect.height - self.rect.height))
        

class Comment_Handler(object):
    """ temp test """
    all_comments = {} # instance of object key : pos/y_pos value
    
    def __init__(self, game, sidebar, offset=0): # probs dont need all these btw but had to take all for initial refactor 
        self.game = game
        self.sidebar = sidebar
        self.offset = offset
        self.is_spawn_on_cooldown = False

    def create_new_comment(self):
        new_comment = Comment(self.game, self.sidebar, self.offset)

    def update_comments_list(self, comment): # its not actually a list but whatever
        comment.update_comment_handler_list()

    def update_all_comments(self, surf):
        # check we even have a dictionary first, might not be any comments to check
        if Comment_Handler.all_comments:
            # for the very first item in the list (we need to handle a max amount now we're adding this btw)
            first_comment = list(Comment_Handler.all_comments.keys())[0] # get the first item in the dictionary
            if first_comment.pos.y > 55: # hard code this to be the height of the most recent comment plus a small margin like + 5
                self.is_spawn_on_cooldown = True # if the toppest one is not at the top, spawn comment is still on cooldown
            else: # else if it has reached the top the cooldown is now off and we need to remove this object from the list (dict) for tracking
                self.is_spawn_on_cooldown = False
                del Comment_Handler.all_comments[first_comment] # stop tracking this comment now that is it at the top
            for comment in Comment_Handler.all_comments.keys():
                comment.draw(surf) # move dem all on dis surface
                self.update_comments_list(comment) # update the list of their y positions if they're all not moving

class Comment(object): # note have this be rough for now as im an idiot, twitch goes top to bottom, but dw at all for now will be hella refactors
    """ class for the Comments shown in the sidebar """
    comment_locations = {} # all instances of comments current y position, when updating just say if its y is greater than we wanna be tracking then remove it from here and or delete / kill (actually del, its not a zombie we dont want to consider reusing it)

    def __init__(self, game, sidebar, offset=0):
        self.game = game
        self.image =  self.select_bg()
        self.rect = self.image.get_rect()
        start_pos = 760 - self.rect.height + offset # guna need to increase this so that it is actually hidden when theres an img infront, and have it scroll from under that, but is fine for now
        self.pos = vec(0, start_pos) # always want to start at the bottom of the sidebar # SIDEBAR_SIZE[1] - self.rect.y
        self.sidebar = sidebar
        self.comment_positions = () # fixed positions, should be a constant class var but this is temp af so dw
        Comment.comment_locations[self] = self.pos.y # self is key (tho maybe id if this object becomes massive tho shouldnt matter as is only like 20 on screen max or whatever)
        # for refactor
        Comment_Handler.all_comments[self] = self.pos.y # now add it here too
        # testing potential to add
        self.rect.center = self.pos
        self.vel = vec(0,0)

    def update_comment_handler_list(self):
        for comment in Comment_Handler.all_comments.keys(): # for every comment which is the key in this dict
            if Comment_Handler.all_comments[comment] == self: # if dis is you
                if Comment_Handler.all_comments[comment] != self.pos.y: # dont do a write for no reason 
                    Comment_Handler.all_comments[comment] = self.pos.y # update ur y pos

    def write_comment(self, player):
        """ write a basic comment based on some context """
        ...
    
    def select_bg(self):
        roll = randint(1,4)
        if roll == 1:
            return(self.game.comment_img_1)
        elif roll == 2:
            return(self.game.comment_img_2)
        elif roll == 3:
            return(self.game.comment_img_3)
        else:
            return(self.game.comment_img_4)            
    
    def write_username():
        ...

    def find_my_position():
        """ find the position of the comment above you """
        # yeah so the big thing about this is obviously they move to a position, then when a new one spawns, everything moves
        # this is then heavily correlated to the amount in the class var with positions as can just use the length of that ig
        # for now im just guna have 20 fixed positions that they move to, then once the list is at a full length, just move up one and delete one and bosh

    def draw(self, surface):
        self.update() # before we draw, run update, remember this isnt a sprite so update isnt running by itself
        surface.blit(self.image, self.pos) # (self.rect.x, self.rect.y)) # draw it on top of the sidebar, not the screen < test this quickly
        
    def update(self):
        # set our move speed but this wont move us yet
        if self.pos.y >= 55: # increase velocity up to this point
            self.vel = vec(0, -100)
        else: # else stop dead lol
            self.vel = vec(0, 0)

        # decide if we can move by checking above us
        if Comment_Handler.all_comments:
            print(f"{Comment_Handler.all_comments = }") # not yet implemented yet tho huh          

        # move us to the top position gradually
        self.pos += self.vel * self.game.dt
        # and ensure we keep the dict storing their positions up to date
        Comment.comment_locations[self] = self.pos.y
        
        print(f"COMMENT - position:{self.pos}, sidebar:{self.sidebar.pos}")




# k so legit learned a lot
# obvs this needs a refactor from scratch due to fact that i want a comment creater and then the comment class like how it is now
# since thats long...

# rn just do font with fake name and fake contextual comment
# make 3 instances of comment at top, comment 1,2,3
# and have the comment start its draw only when x zombies remaining!
# easy af
# then record this
# and continue to...
# buyable walls
# and then just finish the tut bosh