import pygame as pg
from settings import *
from random import randint

SIDEBAR_SIZE = (250, 768)
BACKGROUND_COLOR = (30, 40, 50)
SIDEBAR_COMMENT_SIZE = (250, 40)


# to do properly, and also when done move me to new module like tools or sumnt
class Roll(object):
    def __init__():
        pass

    def has_won_roll(range=100, chance=50):
        if isinstance(range, list):
            range = len(range) -1
        roll = randint(1, range)
        if roll > chance:
            return(False)
        else:
            return(True)


class SideBar(object):
    """ class for the HUD which is displayed on the right of the screen """
    def __init__(self, game):
        self.game = game
        # self.image = game.test_sidebar_img
        self.image = pg.Surface((250, 768))
        self.rect = self.image.get_rect(x=WIDTH - SIDEBAR_SIZE[0]) # width minus the width of the actual sidebar size (not the img so its squished?)
        self.pos = vec(self.rect.x, self.rect.y)
        self.centerpos = vec(self.rect.centerx, self.rect.centery) # self.rect.x = 774, self.rect.centerx = 899

    def update(self): # player
        """ update and redraw all elements to the image """
        self.image.fill(WHITE)

    def draw(self, surface, offset=0):
        """ standard draw """
        surface.blit(self.image, (self.rect.x+offset, self.rect.y))
        #self.update()
        self.image.fill(WHITE)


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
        

class SideBar_Top(object):
    """ temp af """
    def __init__(self, game, sidebar):
        self.game = game
        self.image = game.sidebar_top_img
        self.rect = self.image.get_rect() # width minus the width of the actual sidebar size (not the img so its squished?)
        self.pos = sidebar.pos # vec(self.rect.x, self.rect.y)
        self.sidebar = sidebar
        # self.centerpos = vec(self.rect.centerx, self.rect.centery) # self.rect.x = 774, self.rect.centerx = 899
    
    def draw(self, surface):
        """ standard draw """
        surface.blit(self.image, (0, 0))
        

class Comment_Handler(object):
    """ temp test """
    is_chat_maxed_out = False
    
    def __init__(self, game, sidebar, offset=0): # probs dont need all these btw but had to take all for initial refactor 
        self.game = game
        self.sidebar = sidebar
        self.offset = offset
        self.is_spawn_on_cooldown = False
        self.max_comments = 15 # on screen at one time, which is the amount we allow in the all_comments list (dict!)

    def create_new_comment(self):
        new_comment = Comment(self.game, self.sidebar, self.offset)

    def update_all_comments(self, surf):
        # for i, comment in enumerate(Comment_Handler.all_comments):
        #     comment.draw(surf, i)        
        Comment.draw(Comment, surf)
        if not Comment_Handler.is_chat_maxed_out:   # dont check if true, and most of the time it will be true so is an improvement this way ?         
            if len(Comment.all_comments) >= self.max_comments:
                Comment_Handler.is_chat_maxed_out = True


        # # check we even have a dictionary first, might not be any comments to check
        # if Comment_Handler.all_comments:
        #     # for the very first item in the list (we need to handle a max amount now we're adding this btw)
        #     current_comment = list(Comment_Handler.all_comments.keys())[-1] # get the most recent item in the dictionary # len(Comment_Handler.all_comments) - 1
        #     #print(f"Check is my {current_comment.myid} myYpos: {current_comment.pos.y:.0f} Greater Than whereIshouldBe: {50 * len(Comment_Handler.all_comments)}")
        #     if current_comment.pos.y > 55 * len(Comment_Handler.all_comments): # hard code this to be the height of the most recent comment plus a small margin like + 5
        #         self.is_spawn_on_cooldown = True # if the toppest one is not at the top, spawn comment is still on cooldown
        #     else: # else if it has reached the top the cooldown is now off and we need to remove this object from the list (dict) for tracking
        #         self.is_spawn_on_cooldown = False
        #         # but we only want to remove it from the top if the list is greater than a max size
        #         if len(Comment_Handler.all_comments) >= self.max_comments: # note if the list isnt max size we'll be using the list length as a multiplier to that 55 value (most recent comment height + 5 border)
        #             print(f"TWITCH CHAT IS FULL!\nDeleting Comment {current_comment.myid}")
        #             Comment_Handler.is_chat_maxed_out = True
        #             # del Comment_Handler.all_comments[current_comment] # stop tracking this comment now that is it at the top
        #             # if we dont do the del here it stops at max, which we want, as we want it to scroll through now
        #     for comment in Comment_Handler.all_comments.keys():
        #         comment.draw(surf) # move dem all on dis surface
        #         self.update_comments_list(comment) # update the list of their y positions if they're all not moving


class Comment(object): # note have this be rough for now as im an idiot, twitch goes top to bottom, but dw at all for now will be hella refactors
    """ class for the Comments shown in the sidebar """
    all_comments = []
   
    def __init__(self, game, sidebar, offset=0):
        self.game = game
        self.image =  self.select_bg()
        self.rect = self.image.get_rect() # 250
        start_pos = 760 - self.rect.height + offset # guna need to increase this so that it is actually hidden when theres an img infront, and have it scroll from under that, but is fine for now
        self.pos = vec(0, start_pos) # always want to start at the bottom of the sidebar # SIDEBAR_SIZE[1] - self.rect.y
        self.sidebar = sidebar
        self.comment_positions = () # fixed positions, should be a constant class var but this is temp af so dw
        # testing potential to add
        self.rect.center = self.pos
        self.vel = vec(0,0)
        self.myid = len(Comment.all_comments)
        self.comment_move_speed = 330 # the velocity which we move the comments
        self.commenter_username = self.get_commenter_username()
        self.commenter_color = self.get_a_random_colour()
        self.commenter_comment = self.get_commenter_comment()
        # test  
        self.username_textsurface = self.write_commenter_username()
        self.comment_body_textsurface = self.write_commenter_comment()
        self.all_comments.append(self)

    def get_commenter_username(self): # to do 
        commenter_usernames = [f"{self.game.username} Da Bes!", f"{self.game.username}'s #1 Fan", f"{self.game.username} Is LIFE", f"PogChamp69", "YoMommaDoucheCanoe", f"xXx_69_zOmBiEkIlLA_69_xXx", "OnlyClaps", "McSlappington"]
        roll = randint(1, len(commenter_usernames)-1)
        name_attempt = commenter_usernames[roll]
        # some validation pls, actually note, sometimes we maybe even want two messages in a row ngl that would be kewl but excessive af so allow for now lol
        return(name_attempt)

    def get_commenter_comment(self): # to do 
        # comment type, sentiment and ting, etc etc dw for now tho
        commenter_comment = [f"Wtf 10 v 1 lol", f"{self.game.username} EZ Clap!", f"Pog", f"Oof", "Wait did u guys see that wtffff", f"yo i swear he was in my class" f"Looooooooooooooool", "Dub", "Big Dub", "Pogggggggg","Nice stream bro", "Dope", "Bruh this guy sucks hes guna die this season", "Season 12 Baybayyyyyyyy"]
        roll = randint(1, len(commenter_comment)-1)
        comment_attempt = commenter_comment[roll]
        return(comment_attempt)

    def get_a_random_colour(self):
        color_picker = [LIME, PRINT, ORANGE, BLUE, RED, PURPLE]
        roll = randint(1, len(color_picker)-1)
        return(color_picker[roll])

    def write_commenter_comment(self):
        font = pg.font.Font("Kappa_Regular.otf", 11) # Kappa_Regular KappaDisplay_ExtraBold.otf Kappa_Black.otf KappaDisplay_Regular.otf KappaDisplay_Bold.otf
        # so far colour options are lime pink orange red blue purple
        textsurface = font.render(self.commenter_comment, False, DARKGREY) # "text", antialias, color
        textsurface = pg.transform.rotate(textsurface, 0) # if at this angle rotate my name
        return(textsurface)

    def write_commenter_username(self):
        font = pg.font.Font("KappaDisplay_ExtraBold.otf", 12) # Kappa_Regular KappaDisplay_ExtraBold.otf Kappa_Black.otf KappaDisplay_Regular.otf KappaDisplay_Bold.otf
        # so far colour options are lime pink orange red blue purple
        textsurface = font.render(self.commenter_username, False, self.commenter_color) # "text", antialias, color
        textsurface = pg.transform.rotate(textsurface, 0) # if at this angle rotate my name
        print(f"write_commenter_username: {self.myid} {self.commenter_username}, {self.commenter_color}")
        return(textsurface) 

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

    def draw(self, surface): # index
        # before we draw, run update, remember this isnt a sprite so update isnt running by itself
        for comment in self.all_comments:
            comment.update()
            surface.blit(comment.username_textsurface, (comment.pos.x + 50, comment.pos.y))  
            surface.blit(comment.comment_body_textsurface, (comment.pos.x + 30, comment.pos.y + 20))  
            surface.blit(comment.image, comment.pos)
            
    def update(self):
        if Comment_Handler.is_chat_maxed_out == False: # if the chat is not full move individually, else you move all as a whole
            if self.pos.y >= 50 * len(self.all_comments): # set our move speed but this wont move us yet but what were saying is move us, at this speed upwards if we are not at the top yet
                self.vel = vec(0, -self.comment_move_speed)
            else: # else stop dead lol
                self.vel = vec(0, 0) 
            self.pos += self.vel * self.game.dt
        # update the list stuff should go here


# big note here, i think a part of the issue may be initialising everything for ui during the game
# is it possible to like initialise everything except the actual writing first as templates complete and ready in memory
# then just write then stuff and blit on init


# real quick, if ur the bg with only 1 img on it, move the x pos over a bit (so minus from the existing number)
# buyable and subscribers (basic af ui for it)
# consider try moving the screen, could google it too tbf
# then just pure leetcode
# note, obvs have foobar open tomo init


# (actually do leetcode first pls)
# rn pls just do some bwalls then...
# - find the question and solution i just did on that test in leetcode and write it up
# - find the EXACT problems the Abu mentioned and writing the full solutions in IDE too
 
# then finish the tut

# (subs, viewers | bullet count ui) <<<< done or not worth doing until refactor due to ui issues