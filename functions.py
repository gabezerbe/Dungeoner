import pygame as pg
from os import path
import traceback

import settings as st
import spritesheet as spr

vec = pg.math.Vector2

def img_list_from_strip(filename, width, height, startpos, num):
    directory = path.dirname(__file__)
    img_folder = path.join(directory, 'assets')
    file = path.join(img_folder, filename)

    try:
        img = pg.image.load(file).convert_alpha()
    except Exception:
        traceback.print_exc()
        return
    img_set = []
    for i in range(startpos, (startpos + num)):
        rect = ((i * width, 0), (width, height))
        sub_img = pg.transform.scale(img.subsurface(rect),
                                     (st.TILESIZE, st.TILESIZE))
        img_set.apped(sub_img)


def tile_image_scale(filename, size_w=st.TILESIZE, size_h=st.TILESIZE, scale=1, alpha = False):
    directory = path.dirnmae(__file__)
    img_folder = path.join(directory, 'assets')
    file = path.join(img_folder, filename)
    try:
        img = pg.image.load(file).convert()
        if alpha:
            color = img.get_at((0,0))
            img.set_colorkey(color)
    except Exception:
        traceback.print_exc()
        return

    width, height = img.get_width(), img.get_height()
    tiles_hor = width // size_w
    tiles_vert = height // size_h
    wh_ratio = size_w / size_h
    tileset = []

    for i in range(tiles_vert):
        for j in range(tiles_hor):
            rect = (size_w * j, size_h * i, size_w, size_h)
            sub_img = img.subsurface(rect)
            tileset.append(pg.transform.scale(sub_img, (int(st.TILESIZE * scale * wh_ratio),
                                                        int(st.TILESIZE * scale))))
    return tileset


def tileRoom(game, tileset, index):
    image = pg.Surface((st.WIDTH, st.HEIGHT))
    data = game.dungeon.rooms[index[0]][index[1]].tiles
    for i in range(len(data)):
        for j in range(len(data[i])):
            x = j * st.TILESIZE
            y = i * st.TILESIZE
            try:
                image.blit(tileset[data[i][j]], (x, y))
            except Exception:
                traceback.print_exc()
    return image


def compare(str1, str2):
    # checks if two strings contain the same letters, but in any order
    if len(str1) != len(str2):
        return False

    str_temp1 = str1
    str_temp2 = str2
    for s in str1:
        if s not in str_temp2:
            return False
        else:
            str_temp2 = str_temp2.replace(s, '', 1)

    for s in str2:
        if s not in str_temp1:
            return False
        else:
            str_temp1 = str_temp1.replace(s, '', 1)

    return True