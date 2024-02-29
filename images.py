import pygame
from settings import *


class ImageUtils:
    def __init__(self) -> None:
        self.player_image = pygame.image.load('img/Player.png')
        self.player_image.set_colorkey('white')

        self.player_heart_image = pygame.image.load('img/Player_life.png')
        self.player_heart_image.set_colorkey('white')

        self.bullet_image = pygame.Surface([4, 4])
        self.bullet_image.fill('red')

        self.enemy_images = pygame.image.load('img/Enemy_Frames.png')
        self.enemy_images.set_colorkey('white')
        self.enemy_images = [self.enemy_images.subsurface(
            (i * enemy_img_width, 0, enemy_img_width, 42)) for i in range(total_enemy_animation_frames_length)]

        self.gen6_images = pygame.image.load('img/Gen6.png')
        self.gen6_images.set_colorkey('white')
        self.gen6_images = [self.gen6_images.subsurface(
            (i * enemy_img_width, 0, enemy_img_width, 42)) for i in range(total_enemy_animation_frames_length)]
