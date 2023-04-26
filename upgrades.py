import random

import pygame
from settings import *
from images import player_heart_image
"""
               Class hierarchy

                   Upgrade
                 /   |   \
               /     |    \
 +1 Life Upgrade    |      \
           Speed Shoot      \
                        Clear Screen

Probability:
Every enemy killed by the player will be a chance for a upgrade to spawn
If we do chose to spawn an upgrade it will be a few hundred pixels off screen
If the player collides with an upgrade the it will become the player's current upgrade

"""

class Upgrade:
    def __init__(self):
        self.pos = pygame.math.Vector2(screen_width + upgrade_offscreen_dist, random.randint(upgrade_y_borders, screen_height - upgrade_y_borders))
        self.speed = upgrade_move_speed
        self.img = player_heart_image
        self.img_height = self.img.get_height()
        self.img_width = self.img.get_width()
        self.screen = pygame.display.get_surface()

    def move(self, dt):
        self.pos.x -= dt * self.speed

    def render(self):
        self.screen.blit(self.img, (self.pos.x - self.img_height / 2, self.pos.y - self.img_width / 2))

    def update(self, dt):
        self.move(dt)
        if self.pos.x < - self.img_height:
            return False
        self.render()
        return True
