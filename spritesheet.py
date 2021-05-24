import pygame
from settings import *
import random
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


class Thief(pygame.sprite.Sprite):
    #enemy sprite that will try to steal your coins
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #keeping track of if the sprite is moving left or right
        self.move_right = False
        self.move_left = False
        self.current_frame = 0
        #storing when the last tick an update occured
        self.last_update = 0
        self.filename = CHAR_SHEET
        self.sprite = SpriteSheet(self.filename)
        self.load_frames()
        self.image = self.moving_r_frames[0]

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(random.randrange(-5, 5), 0)

    def load_frames(self):
        self.moving_r_frames = [self.sprite.get_image((416, 64, 32, 32), WHITE),
                              self.sprite.get_image((448, 64, 32, 32), WHITE),
                              self.sprite.get_image((480, 64, 32, 32), WHITE),
                              self.sprite.get_image((512, 64, 32, 32), WHITE)]
        #Sets an empty array for the left facing walking frames, then takes the right facing walking
        #frames, flips them, and adds them to the new array
        self.moving_l_frames = []
        for frame in self.moving_r_frames:
            self.moving_l_frames.append(pygame.transform.flip(frame, True, False))

    def update(self):
        if self.acc.x < 0:
            self.move_right = False
            self.move_left = True
        if self.acc.x > 0:
            self.move_right = True
            self.move_left = False

        self.animate()

        self.pos += self.acc
        self.rect.center = self.pos

    def animate(self):
        now = pygame.time.get_ticks()
        if self.move_left:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_l_frames)
                self.image = self.moving_l_frames[self.current_frame]
                self.image = pygame.transform.scale(self.image, (96, 96))
                self.mask = pygame.mask.from_surface(self.image)

        if self.move_right:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_r_frames)
                self.image = self.moving_r_frames[self.current_frame]
                self.image = pygame.transform.scale(self.image, (96, 96))
                self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #keeping track of if we're walking or not and what frame we're on
        self.walking_r = False
        self.walking_l = False
        self.current_frame = 0

        #Sets an internal frame rate to animate at
        self.last_update = 0

        #Loads the sprite sheet and sets the images
        self.filename = CHAR_SHEET
        self.sprite = SpriteSheet(self.filename)
        self.load_frames()
        self.image = self.standing_frames[0]

        #Sets image and positions
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_frames(self):
        self.standing_frames = [self.sprite.get_image((0, 32, 32, 32), WHITE)]

        self.walk_frames_r = [self.sprite.get_image((416, 32, 32, 32), WHITE),
                              self.sprite.get_image((448, 32, 32, 32), WHITE),
                              self.sprite.get_image((480, 32, 32, 32), WHITE),
                              self.sprite.get_image((512, 32, 32, 32), WHITE)]
        #Sets an empty array for the left facing walking frames, then takes the right facing walking
        #frames, flips them, and adds them to the new array
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))

    def update(self):

        self.animate()
        self.acc = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -3
        if keys[pygame.K_RIGHT]:
            self.acc.x = 3
        if keys[pygame.K_UP]:
            self.acc.y = -3
        if keys[pygame.K_DOWN]:
            self.acc.y = 3

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
        self.rect.center = self.pos

    def animate(self):
        now = pygame.time.get_ticks()
        if not self.walking_l and not self.walking_r:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]
                self.image = pygame.transform.scale(self.image, (96, 96))
                self.mask = pygame.mask.from_surface(self.image)

        if self.walking_l:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                self.image = self.walk_frames_l[self.current_frame]
                self.image = pygame.transform.scale(self.image, (96, 96))
                self.mask = pygame.mask.from_surface(self.image)

        if self.walking_r:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                self.image = self.walk_frames_r[self.current_frame]
                self.image = pygame.transform.scale(self.image, (96, 96))
                self.mask = pygame.mask.from_surface(self.image)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = random.randrange(64, WIDTH - 64)
        self.y_pos = random.randrange(64, HEIGHT - 64)
        self.filename = COIN_SHEET
        self.sprite = SpriteSheet(self.filename)
        self.last_update = 0
        self.current_frame = 0
        self.load_frames()
        self.image = self.frames[0]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos // 1, self.y_pos // 1)

    def update(self):
        self.animate()

    def load_frames(self):
        self.frames = [self.sprite.get_image((0, 0, 32, 32), BLACK),
                       self.sprite.get_image((32, 0, 32, 32), BLACK),
                       self.sprite.get_image((64, 0, 32, 32), BLACK),
                       self.sprite.get_image((96, 0, 32, 32), BLACK),
                       self.sprite.get_image((128, 0, 32, 32), BLACK),
                       self.sprite.get_image((160, 0, 32, 32), BLACK),
                       self.sprite.get_image((192, 0, 32, 32), BLACK),
                       self.sprite.get_image((224, 0, 32, 32), BLACK)]

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.mask = pygame.mask.from_surface(self.image)

