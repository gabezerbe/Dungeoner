# Dungeoner animation and AI test project

import game
import pygame
import random
from spritesheet import *
from settings import *

game = game.Game()
pygame.mixer.music.play(-1, 0, 0)
while game.running:
    game.new()
    game.run()
    game.show_end_screen()

pygame.quit()