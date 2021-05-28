#SpriteSheet Class and Object classes file
import pygame
from settings import *
import random
import game
vec = pygame.math.Vector2


class SpriteSheet:

    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, rectangle, colorkey = None):
        # grabs an image from specific position on a larger image
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.spritesheet, (0,0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def get_images(self, rects, colorkey = None):
        return [self.get_image(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        tups = [(rect[0]+rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.get_images(tups, colorkey)

class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.filename = TILE_SHEET
        self.sprite = SpriteSheet(self.filename)
        self.load_frames()
        self.image = self.standing_frames[0]
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def load_frames(self):
        self.standing_frames = [self.sprite.get_image((140, 212, 16, 16), BLACK)]

class Stairs(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.stairs, game.floor_tiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.filename = TILE_SHEET
        self.sprite = SpriteSheet(self.filename)
        self.load_frames()
        self.image = self.standing_frames[0]
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def load_frames(self):
        self.standing_frames = [self.sprite.get_image((216, 64, 16, 16), BLACK)]

class Floor_Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.floor_tiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.filename = TILE_SHEET
        self.sprite = SpriteSheet(self.filename)
        self.load_frames()
        self.image = self.standing_frames[random.randrange(0, 3)]
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def load_frames(self):
        self.standing_frames = [self.sprite.get_image((44, 64, 16, 16), BLACK),
                                self.sprite.get_image((82, 50, 16, 16), BLACK),
                                self.sprite.get_image((38, 79, 16, 16), BLACK),
                                self.sprite.get_image((60, 80, 16, 16), BLACK)]


class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_treasure
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.filename = COIN_SHEET
        self.sprite = SpriteSheet(self.filename)
        self.load_frames()
        self.current_frame = 0
        self.last_update = 0
        self.image = self.standing_frames[0]
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.width = TILESIZE
        self.rect.height = TILESIZE
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        self.animate()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

    def load_frames(self):
        self.standing_frames = [self.sprite.get_image((0, 0, 32, 32), BLACK),
                                self.sprite.get_image((32, 0, 32, 32), BLACK),
                                self.sprite.get_image((32 * 2, 0, 32, 32), BLACK),
                                self.sprite.get_image((32 * 3, 0, 32, 32), BLACK),
                                self.sprite.get_image((32 * 4, 0, 32, 32), BLACK),
                                self.sprite.get_image((32 * 5, 0, 32, 32), BLACK),
                                self.sprite.get_image((32 * 6, 0, 32, 32), BLACK),
                                self.sprite.get_image((32 * 7, 0, 32, 32), BLACK)]

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            self.image = self.standing_frames[self.current_frame]
            self.mask = pygame.mask.from_surface(self.image)


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.filename = TILE_SHEET
        self.sprite = SpriteSheet(self.filename)
        self.load_frames()
        self.image = self.standing_frames[0]
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.width = TILESIZE
        self.rect.height = TILESIZE
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def load_frames(self):
        self.standing_frames = [self.sprite.get_image((32, 228, 16, 16), BLACK)]


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.player_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #keeping track of if we're walking or not and what frame we're on
        self.walking_r = False
        self.walking_l = False
        self.current_frame = 0
        self.standing_on_stairs = False
        self.loading_level = False

        #Sets an internal frame rate to animate at
        self.last_update = 0

        #Loads the sprite sheet and sets the images
        self.filename = CHAR_SHEET
        self.sprite = SpriteSheet(self.filename)
        self.load_frames()
        self.image = self.standing_frames[0]
        self.image = pygame.transform.scale(self.image, (18 * 5, 24 * 5))

        #Sets image and positions
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = vec(x * TILESIZE, y * TILESIZE)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_frames(self):
        self.standing_frames = [self.sprite.get_image((8, 40, 18, 24), WHITE)]

        self.walk_frames_r = [self.sprite.get_image((456, 40, 18, 24), WHITE),
                              self.sprite.get_image((456 + 32, 40, 18, 24), WHITE),
                              self.sprite.get_image((456 + 64, 40, 18, 24), WHITE),
                              self.sprite.get_image((456 + 96, 40, 18, 24), WHITE)]
        #Sets an empty array for the left facing walking frames, then takes the right facing walking
        #frames, flips them, and adds them to the new array
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))

    def collide_with_door(self):
        self.hits = pygame.sprite.spritecollide(self, self.game.doors, False)

        if self.hits:
            print('Congratulatoins, you\'ve made it to the end of the dungeon!')
            self.game.end_game = True
            self.game.running = False
            self.game.show_end_screen()

    def collide_with_stairs(self):
        self.hits = pygame.sprite.spritecollide(self, self.game.stairs, False)

        if not self.loading_level:
            if self.hits:
                self.standing_on_stairs = True

    def collide_with_coins(self):
        self.hits = pygame.sprite.spritecollide(self, self.game.all_treasure, True)
        if self.hits:
            self.game.score += 100
            self.game.coin_collect.play()
            print(self.game.score)

    def collide_with_walls(self, dir):
        if dir == 'x':
            self.hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if self.hits:
                if self.acc.x > 0:
                    self.pos.x = self.hits[0].rect.left - self.rect.width
                if self.acc.x < 0:
                    self.pos.x = self.hits[0].rect.right
                self.acc.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            self.hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if self.hits:
                if self.acc.y > 0:
                    self.pos.y = self.hits[0].rect.top - self.rect.height
                if self.acc.y < 0:
                    self.pos.y = self.hits[0].rect.bottom
                self.acc.y = 0
                self.rect.y = self.pos.y


    def get_keys(self):

        self.acc = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -6
        if keys[pygame.K_RIGHT]:
            self.acc.x = 6
        if keys[pygame.K_UP]:
            self.acc.y = -6
        if keys[pygame.K_DOWN]:
            self.acc.y = 6

        if self.acc.x != 0 and self.acc.y != 0:
            self.acc.x *= 0.7071
            self.acc.y *= 0.7071

        if self.acc.x > 0:
            self.walking_r = True
            self.walking_l = False
        if self.acc.x < 0:
            self.walking_l = True
            self.walking_r = False
        if self.acc.x == 0:
            self.walking_l = False
            self.walking_r = False

        self.pos += self.acc

        if self.standing_on_stairs:
            if not self.loading_level:
                self.game.current_level += 1
                self.loading_level = True
                self.game.new()
            print(self.game.current_level)

    def update(self):
        self.animate()
        self.get_keys()

        self.image = pygame.transform.scale(self.image, (18 * 5, 24 * 5))

        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        self.collide_with_coins()
        self.collide_with_stairs()
        self.collide_with_door()


    def animate(self):
        now = pygame.time.get_ticks()
        if not self.walking_l and not self.walking_r:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]
                self.mask = pygame.mask.from_surface(self.image)

        if self.walking_l:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                self.image = self.walk_frames_l[self.current_frame]
                self.mask = pygame.mask.from_surface(self.image)

        if self.walking_r:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                self.image = self.walk_frames_r[self.current_frame]
                self.mask = pygame.mask.from_surface(self.image)