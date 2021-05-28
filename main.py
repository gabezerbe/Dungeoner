# Dungeoner Final Project
import game
import pygame

game = game.Game()
pygame.mixer.music.play(-1, 0, 0)

while game.menu:
    game.show_splash_screen()

while game.running:
    game.new()
    game.run()

while game.end_game:
    game.show_end_screen()