import pygame
from os import path
from config import display_height

image_path = path.join(path.dirname(path.abspath(__file__)), 'image_sources')
i_platform = pygame.image.load(path.join(image_path, 'platform.png'))
i_bplatform = pygame.image.load(path.join(image_path, 'bouncy-platform.png'))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = i_platform
        self.rect = self.image.get_rect()
        self.id = id
        self.rect.x = x
        self.rect.y = y
        self.b_vel = -20
        self.alive = True

    def update(self):
        if self.rect.y > display_height:
            self.alive = False

class Bouncy_platform(Platform):
    def __init__(self, x, y, id):
        super().__init__(x, y, id)
        self.image = i_bplatform
        self.rect = self.image.get_rect()
        self.id = id
        self.rect.x = x
        self.rect.y = y
        self.b_vel = 1.5*self.b_vel
