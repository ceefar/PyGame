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
    is_chat_maxed_out = False
    
    def __init__(self, game, sidebar, offset=0): # probs dont need all these btw but had to take all for initial refactor 
        self.game = game
        self.sidebar = sidebar
        self.offset = offset
        self.is_spawn_on_cooldown = False
        self.max_comments = 15 # on screen at one time, which is the amount we allow in the all_comments list (dict!)

    def create_new_comment(self):
        new_comment = Comment(self.game, self.sidebar, self.offset)

    def update_comments_list(self, comment): # its not actually a list but whatever
        comment.update_comment_handler_list()

    def update_all_comments(self, surf):
        # check we even have a dictionary first, might not be any comments to check
        if Comment_Handler.all_comments:
            # for the very first item in the list (we need to handle a max amount now we're adding this btw)
            current_comment = list(Comment_Handler.all_comments.keys())[-1] # get the most recent item in the dictionary # len(Comment_Handler.all_comments) - 1
            #print(f"Check is my {current_comment.myid} myYpos: {current_comment.pos.y:.0f} Greater Than whereIshouldBe: {50 * len(Comment_Handler.all_comments)}")
            if current_comment.pos.y > 55 * len(Comment_Handler.all_comments): # hard code this to be the height of the most recent comment plus a small margin like + 5
                self.is_spawn_on_cooldown = True # if the toppest one is not at the top, spawn comment is still on cooldown
            else: # else if it has reached the top the cooldown is now off and we need to remove this object from the list (dict) for tracking
                self.is_spawn_on_cooldown = False
                # but we only want to remove it from the top if the list is greater than a max size
                if len(Comment_Handler.all_comments) >= self.max_comments: # note if the list isnt max size we'll be using the list length as a multiplier to that 55 value (most recent comment height + 5 border)
                    print(f"TWITCH CHAT IS FULL!\nDeleting Comment {current_comment.myid}")
                    Comment_Handler.is_chat_maxed_out = True
                    # del Comment_Handler.all_comments[current_comment] # stop tracking this comment now that is it at the top
                    # if we dont do the del here it stops at max, which we want, as we want it to scroll through now
            for comment in Comment_Handler.all_comments.keys():
                comment.draw(surf) # move dem all on dis surface
                self.update_comments_list(comment) # update the list of their y positions if they're all not moving


class Comment(object): # note have this be rough for now as im an idiot, twitch goes top to bottom, but dw at all for now will be hella refactors
    """ class for the Comments shown in the sidebar """
   
    def __init__(self, game, sidebar, offset=0):
        self.game = game
        self.image =  self.select_bg()
        self.rect = self.image.get_rect()
        start_pos = 760 - self.rect.height + offset # guna need to increase this so that it is actually hidden when theres an img infront, and have it scroll from under that, but is fine for now
        self.pos = vec(0, start_pos) # always want to start at the bottom of the sidebar # SIDEBAR_SIZE[1] - self.rect.y
        self.sidebar = sidebar
        self.comment_positions = () # fixed positions, should be a constant class var but this is temp af so dw
        # for refactor
        Comment_Handler.all_comments[self] = self.pos.y # now add it here too
        # testing potential to add
        self.rect.center = self.pos
        self.vel = vec(0,0)
        self.myid = len(Comment_Handler.all_comments)
        self.comment_move_speed = 120 # the velocity which we move the comments

    def update_comment_handler_list(self):
        for comment in Comment_Handler.all_comments.keys(): # for every comment which is the key in this dict
            if Comment_Handler.all_comments[comment] == self: # if dis is you
                if Comment_Handler.all_comments[comment] != self.pos.y: # dont do a write for no reason 
                    Comment_Handler.all_comments[comment] = self.pos.y # update ur y pos

    def write_comment(self, player):
        """ write a basic comment based on some context """
        ...
    
    def select_bg(self):
        roll = randint(1,3)
        if roll == 1:
            return(self.game.comment_img_1)
        elif roll == 2:
            return(self.game.comment_img_2)
        elif roll == 3:
            return(self.game.comment_img_3)
        else:
            return(self.game.comment_img_4) # blank one nearly fucked me up lol    
    
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
        # but what were saying is move us, at this speed upwards if we are not at the top yet
        if Comment_Handler.is_chat_maxed_out == False: # if the chat is not full
            if self.pos.y >= 50 * len(Comment_Handler.all_comments): # increase velocity up to this point
                self.vel = vec(0, -self.comment_move_speed)
            else: # else stop dead lol
                self.vel = vec(0, 0) 
            self.pos += self.vel * self.game.dt
        # if it is maxed out then move everyone by the same velocity - then in handler dont update until the last item is at the top then remove that item 
        else:
            # doesnt work as expected just due to it printing loads under these conditions, leaving for now so disabling on full
            # then
            # finally
            # move us to the top position gradually
            # self.vel = vec(0, -self.comment_move_speed)
            # self.pos += self.vel * self.game.dt
            pass
        # print(f"Comment [ {self.myid} ] - position:{self.pos}, sidebar:{self.sidebar.pos}")



# record this, maybe with commentary but idk, actually yh why not
# put the names in the comments
# put some basic semi contextual randomised comments in 
# then just continue (subs, viewers | bullet count ui | buyable walls and couple more zeds)

# then record this
# and continue to...
# buyable walls
# and then just finish the tut bosh