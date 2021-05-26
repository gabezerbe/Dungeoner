# Dungeoner animation and AI test project

import game
import pygame

game = game.Game()

while game.running:
    game.new()
    game.run()
    game.show_end_screen()

pygame.quit()