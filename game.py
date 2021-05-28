#Game object class for keeping main clean
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
        self.running = False
        self.menu = True
        self.end_game = False
        self.bg_music = pg.mixer.music.load(st.BG_MUSIC)
        self.coin_collect = pg.mixer.Sound(st.COIN_NOISE)
        self.score = 0
        self.current_level = 0
        self.load_data()

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = [Map(path.join(self.game_folder, 'map.txt')),
                    Map(path.join(self.game_folder, 'map1.txt')),
                    Map(path.join(self.game_folder, 'map2.txt'))]

    def new(self):
        # Start a new Game
        # Sprite Groups

        self.all_sprites = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.all_treasure = pg.sprite.Group()
        self.all_enemies = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.floor_tiles = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.stairs = pg.sprite.Group()

        # Generate rooms and spawn the player
        self.generate_rooms()
        self.camera = Camera(self.map[self.current_level].width, self.map[self.current_level].height)

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
        for row, tiles in enumerate(self.map[self.current_level].data):
            for col, tile in enumerate(tiles):
                if tile == 'w':
                    spr.Wall(self, col, row)
                if tile == 'f':
                    spr.Floor_Tile(self, col, row)
                if tile == 'c':
                    spr.Floor_Tile(self, col, row)
                    spr.Coin(self, col, row)
                if tile == 'p':
                    spr.Floor_Tile(self, col, row)
                    self.player = spr.Player(self, col, row)
                if tile == 's':
                    spr.Stairs(self, col, row)
                if tile == 'd':
                    spr.Door(self, col, row)

    def draw(self):
        # Game Loop Draw
        self.screen.fill(st.DARK_GRAY)
        for sprite in self.walls:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.floor_tiles:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.all_treasure:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.doors:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.player_sprite:
            self.screen.blit(sprite.image, self.camera.apply(sprite))


        self.font = pg.font.Font(None, 64)
        self.text = self.font.render('Score: %d' % self.score, True, st.WHITE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (150, 32)

        self.screen.blit(self.text, self.textRect)
        pg.display.flip()

    def show_splash_screen(self):
        while self.menu:
            self.events()

            self.screen.fill(st.DARK_GRAY)
            self.font = pg.font.Font(None, 152)
            self.font2 = pg.font.Font(None, 86)
            self.text = self.font.render("DUNGEONER", True, st.WHITE)
            self.text2 = self.font2.render("PRESS SPACE TO START", True, st.WHITE)
            self.textRect = self.text.get_rect()
            self.textRect.center = (st.WIDTH/2, st.HEIGHT/2)
            self.text2Rect = self.text2.get_rect()
            self.text2Rect.center = (st.WIDTH/2, (st.HEIGHT/2) + 64)

            self.screen.blit(self.text, self.textRect)
            self.screen.blit(self.text2, self.text2Rect)

            pg.display.flip()

            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                self.running = True
                self.menu = False


    def show_end_screen(self):
        # End Screen
        while self.end_game:
            self.events()
            self.screen.fill(st.DARK_GRAY)

            self.scoreFont = pg.font.Font(None, 128)
            self.font = pg.font.Font(None, 128)

            self.text = self.font.render("You've braved the Dungeon!", True, st.WHITE)
            self.text2 = self.scoreFont.render("Score: %d" % self.score, True, st.WHITE)

            self.textRect = self.text.get_rect()
            self.textRect2 = self.text2.get_rect()

            self.textRect.center = (st.WIDTH / 2, st.HEIGHT / 2 - 64)
            self.textRect2.center = (st.WIDTH / 2, (st.HEIGHT / 2) + 96)

            self.screen.blit(self.text, self.textRect)
            self.screen.blit(self.text2, self.textRect2)

            pg.display.flip()

            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                self.new()
                self.end_game = False
                self.running = True
            if keys[pg.K_ESCAPE]:
                pg.quit()