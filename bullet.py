from settings import *
import pygame


class Bullet:
    def __init__(self, bullet_image, pos, screen):
        self.pos = pygame.math.Vector2(pos)
        self.speed = bullet_speed
        self.screen = screen
        self.direction = pygame.math.Vector2(1, 0)
        self.img = bullet_image
        self.img_height = self.img.get_height()
        self.img_width = self.img.get_width()

    def move(self, dt):
        self.pos.x += dt * self.speed * self.direction.x
        self.pos.y += dt * self.speed * self.direction.y

    def render(self):
        self.screen.blit(
            self.img, (self.pos.x - self.img_height / 2, self.pos.y - self.img_height / 2))

    def update(self, dt):
        self.move(dt)
        if self.direction.magnitude() > 0:
            self.direction.normalize()
        if self.pos.x > screen_width + self.img_width:
            return False
        return True
