#Classes for loading map data and setting up the scrolling camera that follows the player
import pygame as pg
from settings import *


class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)

        #limites scrolling to map size
        x = min(0, x) # left side
        x = max(-(self.width - WIDTH), x) #right side
        y = min(0, y) # top side
        y = max(-(self.height - HEIGHT), y) #right side

        self.camera = pg.Rect(x, y, self.width, self.height)
