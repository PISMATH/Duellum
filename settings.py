import pygame.constants

#  Screen parameters
screen_width = 1260
screen_height = 720

#  Player parameters
player_speed = .4
player_shoot_speed = 3
player_lives = 3
player_heart_pos = (32, 32)
player_heart_spacing = 40
player_heart_cap = 5
player_kill_count_spacing_x = 20
player_kill_count_spacing_y = 12
player_machine_gun_mode = False

player_controller = 'user' # user, random, ai_v1

# Bullet parameters
bullet_speed = .5

# Enemy parameters
base_enemy_spawn_speed = .5
enemy_spawn_rate_increment = 0.01
enemy_speed = 0.15
enemy_x_offscreen_dist = 100
enemy_y_boarders = 32
enemy_img_width = 88
total_enemy_animation_frames_length = 8
enemy_sight_radius = 400
enemy_aim = 0
enemy_shoot_speed = 2
enemy_turn_speed = 5

# Upgrade parameters
upgrade_offscreen_dist = 100
upgrade_y_borders = 32
upgrade_move_speed = 0.1
upgrade_kill_wait_time = 10

# Keybinds
pause_key = pygame.constants.K_SPACE
shoot_key = pygame.constants.K_s
up_key = pygame.constants.K_UP
down_key = pygame.constants.K_DOWN
left_key = pygame.constants.K_LEFT
right_key = pygame.constants.K_RIGHT