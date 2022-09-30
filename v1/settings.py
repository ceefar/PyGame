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
BROWNTONE4 = (66, 40, 2)      # HOVERING FULLY BUILT BARRACADE, SHOWS SLIGHTLY DARKER TO INDICATE NULL INTERACTION BETTER THAN NOTHING 

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 32 # default 32, increase the tilesize to zoom in further (i.e. 64 for twice as close), or decrease (by multiples of 2) to zoom out
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings, remember the speeds here are milliseconds, so 1000 per sec (because we're using delta time on the frames)
PLAYER_SPEED = 320
PLAYER_ROT_SPEED = 250 # degrees per second, so just under 1 second to go all the way around (1 rotation)
PLAYER_IMG = "manBlue_gun.png"
# new test stuff
PLAYER_BLUR1_IMG = "manBlue_gun_blur1.png"
PLAYER_BLUR3_IMG = "manBlue_gun_blur3.png"
PLAYER_INJURY1_IMG = "manBlue_gun_injury1.png"