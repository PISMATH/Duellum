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

def ai_v2(player, enemies_shot_at=[]):
    farthest_enemy_dist = float('inf')
    farthest_enemy = None # The enemy farthest into our territory 
    player_x, player_y = player.pos

    for enemy in player.game.enemies:
        enemy_x, _ = enemy.pos
        
        if enemy in enemies_shot_at and enemy_x > enemy_sight_radius + (enemy_speed * enemy_sight_radius / bullet_speed):
            continue

        if enemy_x < farthest_enemy_dist:
            farthest_enemy_dist = enemy_x
            farthest_enemy = enemy

    up = None
    shooting = False
    if farthest_enemy is not None:
        enemy_x, enemy_y = farthest_enemy.pos
        if abs(enemy_y - player_y) < farthest_enemy.img_height / 2:
            shooting = True
            enemies_shot_at.append(farthest_enemy)

        if enemy_y < player_y:
            up = True
        else:
            up = False

    going_up = up if up is not None else False
    going_down = not up if up is not None else False

    return going_up, going_down, True, False, shooting

controllers = {
    'user': user_controls,
    'random': random_controls,
    'ai_v1': ai_v1,
    'ai_v2': ai_v2
}