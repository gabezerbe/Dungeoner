import pygame as pg
import traceback
import random

import settings as st
import spritesheet as spr
import functions as fn
import rooms

vec = pg.math.Vector2

class Game:
    def __init__(self):
        # Initialize game window and variables
        pg.mixer.init()
        pg.init()

        self.screen = pg.display.set_mode((st.WIDTH, st.HEIGHT))

        self.clock = pg.time.Clock()
        self.running = True

        self.load_data()

    def load_data(self):
        self.room_images = fn.img_list_from_strip('rooms_strip.png', 16, 16, 0, 18)

    def new(self):
        # Start a new Game
        pass

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop Update
        pass

    def events(self):
        # Game Loop Events
        pass

    def draw(self):
        # Game Loop Draw
        self.screen.fill(DARK_GRAY)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def show_splash_screen(self):
        # Splash Screen
        pass

    def show_end_screen(self):
        # End Screen
        pass