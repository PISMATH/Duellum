import pygame
from settings import *
from math import atan, degrees
import time


class Enemy:
    def __init__(self, enemy_images, pos, screen):
        self.pos = pygame.math.Vector2(pos)
        self.speed = enemy_speed
        self.screen = screen
        self.enemy_images = enemy_images
        self.img = enemy_images[0]
        self.img_height = self.img.get_height()
        self.img_width = self.img.get_width()
        self.total_time = 0
        self.direction = pygame.math.Vector2(-1, 0)
        self.past_player = False
        self.shooting = False
        self.last_shoot_time = time.time()

    def move(self, dt):
        x_collide = True
        y_collide = True

        if self.pos.x > screen_width - self.img_width / 2:
            self.pos.x = screen_width - self.img_width / 2
        else:
            x_collide = False

        if self.pos.y < self.img_height / 2:
            self.pos.y = self.img_height / 2

        elif self.pos.y > screen_height - self.img_height / 2:
            self.pos.y = screen_height - self.img_height / 2
        else:
            y_collide = False

        if not (x_collide or y_collide):
            if self.direction.magnitude() > 0:
                self.direction = self.direction.normalize()

        self.pos += self.direction * dt * self.speed

    def update_direction(self, player_pos):
        self.direction.x += (player_pos.x - self.pos.x) * \
            enemy_turn_speed / 100000
        self.direction.y += (player_pos.y - self.pos.y) * \
            enemy_turn_speed / 100000

    def render(self):
        self.img = pygame.transform.rotate(
            self.img, degrees(-atan(self.direction.y / self.direction.x)))
        self.img.set_colorkey('white')
        self.img_height = self.img.get_height()
        self.img_width = self.img.get_width()

        self.screen.blit(
            self.img, (self.pos.x - self.img_height / 2, self.pos.y - self.img_width / 2))
        self.img = self.enemy_images[round(self.total_time) % 8]

    def update(self, dt, player_pos):
        if enemy_sight_radius ** 2 > ((self.pos.x - player_pos.x) ** 2 + (self.pos.y - player_pos.y) ** 2):
            self.update_direction(player_pos)
        else:
            self.direction = pygame.math.Vector2(-1, 0)
        self.shooting = enemy_sight_radius ** 2 > (
            (self.pos.x - player_pos.x) ** 2 + (self.pos.y - player_pos.y) ** 2)
        self.move(dt)
        self.total_time += dt
        if self.pos.x < - self.img_height:
            return False
        return True
