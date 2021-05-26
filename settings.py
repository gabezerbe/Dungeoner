# Game Settings File that contains Options so as not to clutter the main

#Window Settings and Constants
TITLE = "Dungeoner!"
GLOBAL_SCALE = 5
TILESIZE = 16 * GLOBAL_SCALE
TILES_W = 16
TILES_H = 9
WIDTH = TILESIZE * TILES_W
HEIGHT = TILESIZE * TILES_H

#INGAME SETTINGS
LEVEL_SIZE = (5,5)
SCROLL_SPEED = 0.5 * GLOBAL_SCALE
PLAYER_SPEED = 1 * GLOBAL_SCALE
SCORE = 0
LIFE = 100

#ROOMS TO CHOOSE FROM
ROOMS = {
    'N': ['NS', 'S', 'WS', 'ES', 'SWE', 'NSW', 'NSE'],
    'W': ['WE', 'E', 'ES', 'EN', 'SWE', 'NSE', 'NWE'],
    'E': ['WE', 'W', 'WS', 'WN', 'SWE', 'NSW', 'NWE'],
    'S': ['NS', 'N', 'WN', 'EN', 'NSE', 'NSW', 'NEW']
}

#Tick rate/ Frame Rate
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)

#FILE PATHS
#SPRITES
CHAR_SHEET = "assets/characters.png"
COIN_SHEET = "assets/coin_gold.png"
#SOUND
BG_MUSIC = "assets/BG_MUSIC.wav"
COIN_NOISE = "assets/COIN_COLLECT.wav"