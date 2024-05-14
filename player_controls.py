from settings import *
import random
import pygame

def user_controls(player):
    keys = pygame.key.get_pressed()
    return keys[up_key], keys[down_key], keys[left_key], keys[right_key], keys[shoot_key]

def random_controls(player):
    up = random.choice([False, True])
    left = random.choice([False, True])
    shoot = random.choice([False, True])
    return up, not up, left, not left, shoot

controllers = {
    'user': user_controls,
    'random': random_controls
}