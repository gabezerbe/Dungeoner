import pygame
import random
from spritesheet import *
from settings import *

class Game:
    def __init__(self):
        # Initialize game window and variables
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.last_tick = 0
        self.running = True
        self.bg_music = pygame.mixer.music.load(BG_MUSIC)
        self.coin_collect = pygame.mixer.Sound(COIN_NOISE)
        self.score = SCORE

    def new(self):
        # Start a new Game
        self.all_coins = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_thieves = pygame.sprite.Group()
        self.player = Player()
        self.new_thief()
        self.new_coins()
        self.all_coins.add(self.coin)
        self.all_sprites.add(self.coin)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.thief)

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
        self.all_sprites.update()
        if len(self.all_thieves) == 0:
            self.new_thief

    def events(self):
        # Game Loop Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False

                self.running = False

        #janky way to do mask collisions on the coins for better hit detection
        for self.coins in self.all_coins:
            self.coin_collision = pygame.sprite.collide_mask(self.player, self.coins)
            self.coin_stolen = pygame.sprite.collide_mask(self.thief, self.coins)
            if self.coin_collision:
                self.coin_collect.play()
                self.score += 100
                self.coins.kill()
            if self.coin_stolen:
                self.coins.kill()
            if len(self.all_coins) == 0:
                self.new_coins()

    def new_thief(self):
        print("All Thieves have escaped! A new one arrives")
        self.thief = Thief()
        self.all_thieves.add(self.thief)
        self.all_sprites.add(self.thief)


    def new_coins(self):
        for i in range(10):
            self.coin = Coin()
            self.all_coins.add(self.coin)
            self.all_sprites.add(self.coin)

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