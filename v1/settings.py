import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)
ORANGE = (255,100,10)
BLUEGREEN = (0,255,170)
MARROON = (115,0,0)
LIME = (180,255,100)
PRINT = (255,100,180)           # PINK AF  
PURPLE = (240,0,255)  
GREY = (127,127,127)
MAGENTA = (255,0,230)
BROWN = (100,40,0)
FORESTGREEN = (0,50,0)
NAVYBLUE = (0,0,100)
RUST = (210,150,75)             # GOLD AF
BRIGHTYELLOW = (255,200,0)
HIGHLIGHTER = (255,255,100)     # YELLOW AF
SKYBLUE = (0,255,255)
PALEGREY = (200,200,200)
TAN = (230,220,170)             # PALE YELLOW, DEFO BE GOOD ME THINKS  
COFFEE =(200,190,140)           # ALSO GOOD PALE YELLOW   
MOONGLOW = (235,245,255)        # KINDA CRISPY BRIGHT GREY WITH HINT OF BLUE, QUITE NICE TBF
BROWNTONE1 = (123, 111, 100)    # (119, 99, 80)
BROWNTONE2 = (114, 88, 61)      # FOR BUILDING BARRACADES
BROWNTONE3 = (101, 66, 22)      # FOR BUILDING BARRACADES
BROWNTONE4 = (66, 40, 2)        # HOVERING FULLY BUILT BARRACADE, SHOWS SLIGHTLY DARKER TO INDICATE NULL INTERACTION BETTER THAN NOTHING 
BROWNPALE =  (215, 195, 163)
BLUEMIDNIGHT = (0, 51, 102)

# game settings
WIDTH = 1408 # 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768 # 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWNPALE

# new own custom test game constants/settings for ui stuff
SUBSBAR_HEIGHT = 70

TILESIZE = 64 # default 32, increase the tilesize to zoom in further (i.e. 64 for twice as close), or decrease (by multiples of 2) to zoom out
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings, remember the speeds here are milliseconds, so 1000 per sec (because we're using delta time on the frames)
PLAYER_SPEED = 320
PLAYER_HEALTH = 100
PLAYER_ROT_SPEED = 250 # degrees per second, so just under 1 second to go all the way around (1 rotation)
PLAYER_IMG = "manBlue_gun.png"
PLAYER_HIT_RECT = pg.Rect(0,0,20,20)
BARREL_OFFSET = vec(30,10)

# Gun settings
BULLET_IMG = "bullet.png"
BULLET_SPEED = 500
BULLET_LIFETIME = 1000 # is in ms, basically range but range is really distance which is speed over time, defo calculate this too  
BULLET_RATE = 150 # how fast we can shoot, slower is faster
GUN_KICKBACK = 200 # -velocity back after each shot
GUN_SPREAD = 4 # the range of how many degrees left or right of straight the bullet can travel

# Damage settings
BULLET_DAMAGE = 10

# NEW Custom Weapon settings
# like bullet but since these are my own custom and not really bullet appropriate we're doing this, tho may v likely change
PISTOL_SIGHT = 300 # the distance from which you will begin to fire on a zombie with this weapon
PISTOL_ACCURACY = 95 # actually want these to be ranges? or something to convert to ranges, with the ranges becoming shorter based on the time in game ooo (or even bullets fired n shit lol)
PISTOL_CRIT_RATE = 15 # the crit number is just an improvement thats added to the 1 - 100 random int check, so adding 10 crit chance literally remove 10 of 100 numbers from the range to check against
PISTOL_KICKBACK = 200
PISTOL_SPREAD = 20
PISTOL_DAMAGE = 25
PISTOL_BULLET_SPEED = 500
PISTOL_BULLET_RATE = 280
PISTOL_BULLET_LIFETIME = 100
PISTOL_CLIP_SIZE = 20
PISTOL_RELOAD_SPEED = 400 # ms

# NEW Custom Multi-Weapon settings 
UZI_SIGHT = 220
UZI_ACCURACY = 70
UZI_CRIT_RATE = 4
UZI_KICKBACK = 250
UZI_SPREAD = 15
UZI_DAMAGE = 10
UZI_BULLET_SPEED = 800
UZI_BULLET_RATE = 140
UZI_BULLET_LIFETIME = 80
UZI_CLIP_SIZE = 50
UZI_RELOAD_SPEED = 900 # ms

# NEW Custom MyTurret settings
MY_TURRET_IMG = "hitman1_gun.png"

# NEW Custom Player settings
# viewing angle to be default 60 degrees each side
VIEWING_ANGLE = 120

# Mob (Zombie) settings
MOB_IMG = "zoimbie1_hold.png"
MOB_SPEED = 80
MOB_HIT_RECT = pg.Rect(0,0,25,25)
MOB_BASE_HEALTH = 150 # literally like the very (not actually tho but practically) lowest hp a zombie can have
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20

# More Image settings
WALL_IMG = "tileBrick_01.png" # tileGreen_39.png note is also 108 x 108 (not right size btw)

# better new test stuff
BREAK_WALL_0_IMG = "wallTest_0.png"
BREAK_WALL_1_IMG = "wallTest_1.png"
BREAK_WALL_2_IMG = "wallTest_2.png"
BREAK_WALL_3_IMG = "wallTest_3.png"
BREAK_WALL_4_IMG = "wallTest_4.png"
BREAK_WALL_HL_0_IMG = "wallTestHL_0.png"
BREAK_WALL_HL_1_IMG = "wallTestHL_1.png"
BREAK_WALL_HL_2_IMG = "wallTestHL_2.png"
BREAK_WALL_HL_3_IMG = "wallTestHL_3.png"
BREAK_WALL_HL_4_IMG = "wallTestHL_4.png"
BREAK_WALL_HL_4B_IMG = "wallTestHL_4b.png"

# pay wall test stuff
PAY_WALL_IMG = "tileGreen_39.png"

# gold test stuff
GOLD_COIN_IMG = "gold_coin.png"

# splat / outline test stuff
SPLAT_IMG = "splat red.png"

# new test stuff
PLAYER_BLUR1_IMG = "manBlue_gun_blur1.png"
PLAYER_BLUR3_IMG = "manBlue_gun_blur3.png"
PLAYER_INJURY1_IMG = "manBlue_gun_injury1.png"

# test af stuff
TEST_BG_IMG = "test_bg.png"
TEST_SIDEBAR_IMG = "empty_sidebar_1.png"
SIDEBAR_BOTTOM_IMG = "sidebar_bottom.png"
SIDEBAR_TOP_IMG = "sidebar_top.png"
SIDEBAR_BOTTOM_RIGHT_IMG = "subsbar_img_left_2.png"
SIDEBAR_BOTTOM_LEFT_IMG = "subsbar_img_left_1.png"
SIDEBAR_COMMENT_1_BG_IMG = "comment_bg_1.png"
SIDEBAR_COMMENT_2_BG_IMG = "comment_bg_2.png"
SIDEBAR_COMMENT_3_BG_IMG = "comment_bg_3.png"
SIDEBAR_COMMENT_4_BG_IMG = "comment_bg_4.png"

# test companion stuff
COMPANION_HIT_RECT = pg.Rect(0,0,40,40) # 64

# casino test suff
CASINO_GOLD_INGOTS_IMG = "ingots.png"
CASINO_GOLD_IMG = "gold.png"
CASINO_GOLD_TREASURE_IMG = "treasure.png"