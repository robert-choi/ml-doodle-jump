from os import path
import pygame
from config import *

image_path = path.join(path.dirname(path.abspath(__file__)), 'image_sources')
i_left = pygame.image.load(path.join(image_path, 'bunny-left.png'))
i_right = pygame.image.load(path.join(image_path, 'bunny-right.png'))

class Jumper(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = i_right
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_vel = x_velocity
        self.y_vel = -28
        self.left = False
        self.bounce = False
        self.b_cool = 0
        self.max_height = False
        self.score =  0
        self.alive = True
        self.plat_index = 0

    def update(self):
        next_y = self.rect.y + self.y_vel   # Continuous (downward) motion
        self.b_cool -= 1
        if not next_y < display_width//2+100:
            self.rect.y = next_y
            self.max_height = False
        else:
            self.max_height = True  # Check for reaching max height to scroll
            self.score -= self.y_vel
        if self.y_vel < terminal_vel:   # Accelerate to terminal velocity
            self.y_vel += gravity
        elif self.left:     # Image verification
            self.image = i_left
        else:
            self.image = i_right
        #if self.y_vel > 0:  # Check for falling action by character
        #    self.bounce = False
        if self.rect.left > display_width:  # Teleport to oposite side after reaching bounds
            self.rect.right = self.rect.left-display_width
        elif self.rect.right < 0:
            self.rect.left = self.rect.right+display_width
        if self.rect.y > display_height:    # Die if dead
            self.alive = False

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_left()
        elif keys[pygame.K_RIGHT]:
            self.move_right()

    def move_left(self):
        self.rect.x -= self.x_vel
        self.left = True
        self.image = i_left

    def move_right(self):
        self.rect.x += self.x_vel
        self.left = False
        self.image = i_right

    def check_coll_bounce(self, platform):
        b_coll = False
        if not self.bounce and self.b_cool<1 and pygame.sprite.collide_rect(self, platform):
            self.bounce = True
            self.y_vel = platform.b_vel
            self.b_cool = 3
