import pygame as pg
import random
import sys
from os import path
from tilemap import *
import settings as st
import spritesheet as spr
vec = pg.math.Vector2

class Game:
    def __init__(self):
        # Initialize game window and variables
        pg.mixer.init()
        pg.init()
        self.screen = pg.display.set_mode((st.WIDTH, st.HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.bg_music = pg.mixer.music.load(st.BG_MUSIC)
        self.coin_collect = pg.mixer.Sound(st.COIN_NOISE)
        self.load_data()

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, 'map.txt'))

    def new(self):
        # Start a new Game

        # Sprite Groups
        self.all_sprites = pg.sprite.Group()
        self.all_treasure = pg.sprite.Group()
        self.all_enemies = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.floor_tiles = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()

        # Generate rooms and spawn the player
        self.generate_rooms()
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(st.FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def events(self):
        # Game Loop Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False

                self.running = False

    def generate_rooms(self):
        # Generates rooms
        # Small issue when drawing floor tiles where if the tile is drawn after the player it draws it on top of them
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'w':
                    spr.Wall(self, col, row)
                if tile == 'f':
                    #spr.Floor_Tile(self, col, row)
                    pass
                if tile == 'c':
                    #spr.Floor_Tile(self, col, row)
                    spr.Coin(self, col, row)
                if tile == 'p':
                    #spr.Floor_Tile(self, col, row)
                    self.player = spr.Player(self, col, row)
                if tile == 's':
                    spr.Stairs(self, col, row)

    def draw_grid(self):
        for x in range(0, st.WIDTH, st.TILESIZE):
            pg.draw.line(self.screen, st.WHITE, (x, 0), (x, st.HEIGHT))
        for y in range(0, st.HEIGHT, st.TILESIZE):
            pg.draw.line(self.screen, st.WHITE, (0, y), (st.WIDTH, y))

    def draw(self):
        # Game Loop Draw
        self.screen.fill(st.DARK_GRAY)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.flip()

    def show_splash_screen(self):
        # Splash Screen
        pass

    def show_end_screen(self):
        # End Screen
        pass