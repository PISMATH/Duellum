from math import e
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

def ai_v1(player):
    farthest_enemy_dist = float('inf')
    farthest_enemy = None # The enemy farthest into our territory 
    player_x, player_y = player.pos

    for enemy in player.game.enemies:
        enemy_x, _ = enemy.pos
        if enemy_x < farthest_enemy_dist:
            farthest_enemy_dist = enemy_x
            farthest_enemy = enemy
    up = False
    if farthest_enemy is not None:
        _, enemy_y = farthest_enemy.pos
        if enemy_y < player_y:
            up = True
        else:
            up = False

    return up, not up, True, False, True
controllers = {
    'user': user_controls,
    'random': random_controls,
    'ai_v1': ai_v1
}