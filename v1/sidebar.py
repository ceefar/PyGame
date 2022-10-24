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


class SubsBar(object):
    """ bottom bar """
    def __init__(self, game):
        self.game = game
        self.image = pg.Surface((WIDTH, 70))
        self.rect = self.image.get_rect() # width minus the width of the actual sidebar size (not the img so its squished?)
        self.pos = vec(self.rect.x, self.rect.y)
        self.centerpos = vec(self.rect.centerx, self.rect.centery) # self.rect.x = 774, self.rect.centerx = 899

    def update(self): # player
        """ update and redraw all elements to the image """
        self.image.fill(WHITE)

    def draw(self, surface):
        """ standard draw """
        surface.blit(self.image, (0, HEIGHT-SUBSBAR_HEIGHT))
        #self.update()
        self.image.fill(WHITE)
        self.draw_right_img(surface)
        self.draw_left_img(surface)

    def draw_right_img(self, surface):  # both wrong way round btw lmao
        self.right_image = self.game.sidebar_bottom_right_img
        self.right_image_rect = self.right_image.get_rect()
        self.right_image_pos = vec(0, HEIGHT - SUBSBAR_HEIGHT) # 250 SIDEBAR_WIDTH hard code as constant pls
        surface.blit(self.right_image, self.right_image_pos)

    def draw_left_img(self, surface):
        self.left_image = self.game.sidebar_bottom_left_img
        self.left_image_rect = self.right_image.get_rect()
        self.left_image_pos = vec(WIDTH - SIDEBAR_SIZE[0] - self.left_image_rect.width + 20, HEIGHT - SUBSBAR_HEIGHT) # 250 SIDEBAR_WIDTH hard code as constant pls
        surface.blit(self.left_image, self.left_image_pos)


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
        Comment.draw(Comment, surf)
        if not Comment_Handler.is_chat_maxed_out:   # dont check if true, and most of the time it will be true so is an improvement this way ?         
            if len(Comment.all_comments) >= self.max_comments:
                Comment_Handler.is_chat_maxed_out = True


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
        # so far colour options are lime pink orange red blue purple
        textsurface = self.game.FONT_KAPPA_REGULAR_11.render(self.commenter_comment, False, DARKGREY) # "text", antialias, color
        textsurface = pg.transform.rotate(textsurface, 0) # if at this angle rotate my name
        return(textsurface)

    def write_commenter_username(self):
        # so far colour options are lime pink orange red blue purple
        textsurface = self.game.FONT_KAPPADISPLAY_EXTRABOLD_12.render(self.commenter_username, False, self.commenter_color) # "text", antialias, color
        textsurface = pg.transform.rotate(textsurface, 0) # if at this angle rotate my name
        # print(f"write_commenter_username: {self.myid} {self.commenter_username}, {self.commenter_color}")
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
