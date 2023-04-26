import pygame
from settings import *

player_image = pygame.image.load('img/Player.png')
player_image.set_colorkey('white')

player_heart_image = pygame.image.load('img/Player_life.png')
player_heart_image.set_colorkey('white')

bullet_image = pygame.Surface([4, 4])
bullet_image.fill('red')

enemy_images = pygame.image.load('img/Enemy_Frames.png')
enemy_images.set_colorkey('white')
enemy_images = [enemy_images.subsurface((i * enemy_img_width, 0, enemy_img_width, 42)) for i in range(total_enemy_animation_frames_length)]

gen6_images = pygame.image.load('img/Gen6.png')
gen6_images.set_colorkey('white')
gen6_images = [gen6_images.subsurface((i * enemy_img_width, 0, enemy_img_width, 42)) for i in range(total_enemy_animation_frames_length)]
