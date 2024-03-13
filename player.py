import random
import pygame
import time
from settings import *
from bullet import Bullet
from upgrades import Upgrade


def bullet_in_enemy(bullet, enemy):
    if enemy.pos.y - enemy.img_height < bullet.pos.y < enemy.pos.y + enemy.img_height / 2 and \
            enemy.pos.x - enemy.img_width / 2 < bullet.pos.x < enemy.pos.x + enemy.img_width / 2:
        return True
    return False


def collide(R1, R2):
    if (R1[0] >= R2[2]) or (R1[2] <= R2[0]) or (R1[3] <= R2[1]) or (R1[1] >= R2[3]):
        return False
    return True


class Player:
    def __init__(self, player_image, bullet_image, player_heart_image, pos, game):
        self.img = player_image
        self.bullet_image = bullet_image
        self.player_heart_image = player_heart_image
        self.img_height = self.img.get_height()
        self.img_width = self.img.get_width()

        self.game = game
        self.screen = game.screen

        self.lives = player_lives
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(pos)
        self.speed = player_speed

        self.last_shoot_time = time.time()
        self.player_shoot_speed = player_shoot_speed

        self.total_time = 0
        self.enemy_spawn_rate = base_enemy_spawn_speed
        self.last_enemy_spawn_time = time.time()
        self.kill_count = 0
        self.current_upgrade = None

    def handle_life_loss(self):
        self.lives -= 1
        self.game.statistics["Damage Taken"] += 1 
        if self.lives < 1:
            self.handle_dead_screen()

    def handle_dead_screen(self):
        score = self.kill_count
        self.restart()
        self.game.title_screen_single_player(score)

    def restart(self):
        self.game.bullets = []
        self.game.enemies = []
        self.game.gen6 = []
        self.game.upgrades = []
        self.game.enemy_bullets = []
        self.game.gen6_bullets = []
        self.game.last_enemy_spawn_time = time.time()
        self.game.enemy_spawn_rate = base_enemy_spawn_speed
        self.lives = player_lives
        self.kill_count = 0
        self.pos = pygame.math.Vector2(screen_width / 2, screen_height / 2)
        self.last_shoot_time = time.time()
        for stat in self.game.statistics:
            self.game.statistics[stat] = 0

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[up_key]:
            self.direction.y = -1
        elif keys[down_key]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[left_key]:
            self.direction.x = -1
        elif keys[right_key]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        
        if time.time() - self.last_shoot_time > (1 / self.player_shoot_speed) and (keys[shoot_key] or player_machine_gun_mode):
            self.game.bullets.append(
                Bullet(self.bullet_image, (self.pos.x, self.pos.y), self.screen))
            self.last_shoot_time = time.time()

    # Enemy
    def handle_bullet_enemy_collision(self):
        for enemy in self.game.enemies:
            for bullet in self.game.bullets:
                if bullet_in_enemy(bullet, enemy):
                    if enemy in self.game.enemies:
                        self.game.enemies.remove(enemy)
                        self.kill_count += 1
                        self.game.enemy_spawn_rate += enemy_spawn_rate_increment
                        if random.randint(0, upgrade_kill_wait_time) == 0:
                            self.game.upgrades.append(
                                Upgrade(self.player_heart_image))
                        self.game.boom_sound.play()
                    if bullet in self.game.bullets:
                        self.game.bullets.remove(bullet)

    def check_enemy_intersect(self, enemy):
        return collide(
            (self.pos.x - self.img_width / 2, self.pos.y - self.img_height / 2,
             self.pos.x + self.img_width / 2, self.pos.y + self.img_height / 2),
            (enemy.pos.x - enemy.img_width / 2, enemy.pos.y - enemy.img_height / 2, enemy.pos.x + enemy.img_width / 2,
             enemy.pos.y + enemy.img_height / 2))

    def handle_enemy_collide(self):
        for enemy in self.game.enemies:
            if self.check_enemy_intersect(enemy):
                self.game.enemies.remove(enemy)
                self.handle_life_loss()

    # Upgrade section
    def check_upgrade_collide(self, upgrade):
        return collide(
            (self.pos.x - self.img_width / 2, self.pos.y - self.img_height / 2,
             self.pos.x + self.img_width / 2, self.pos.y + self.img_height / 2),
            (upgrade.pos.x - upgrade.img_width / 2, upgrade.pos.y - upgrade.img_height / 2, upgrade.pos.x + upgrade.img_width / 2,
             upgrade.pos.y + upgrade.img_height / 2))

    def handle_upgrades(self):
        if player_heart_cap is None or self.lives < player_heart_cap:
            for upgrade in self.game.upgrades:
                if self.check_upgrade_collide(upgrade):
                    self.current_upgrade = upgrade
                    self.game.upgrades.remove(upgrade)
                    self.game.statistics["Hearts Collected"] += 1

            if self.current_upgrade is not None:
                self.current_upgrade = None
                self.lives += 1
                pygame.mixer.Sound.play(self.game.heart_gain_sound)

    # Big
    def render(self):
        self.screen.blit(
            self.img, (self.pos.x - self.img_width / 2, self.pos.y - self.img_height / 2))

        for i in range(min(self.lives, screen_width // player_heart_spacing)):
            self.screen.blit(self.player_heart_image, (player_heart_pos[0] - self.player_heart_image.get_width() / 2 + i * player_heart_spacing,
                                                       player_heart_pos[1] - self.player_heart_image.get_height() / 2))

        player_kill_count_img = self.game.font.render(
            f'Points: {self.kill_count}', False, 'white')
        self.screen.blit(player_kill_count_img,
                         (screen_width - player_kill_count_img.get_width() - player_kill_count_spacing_x, player_kill_count_spacing_y))

    def move(self, dt):
        x_collide = True
        y_collide = True
        if self.pos.x < self.img_width / 2:
            self.pos.x = self.img_width / 2

        elif self.pos.x > screen_width - self.img_width / 2:
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

    def update(self, dt):
        self.total_time += dt

        self.input()
        self.move(dt)
        self.handle_enemy_collide()
        self.handle_bullet_enemy_collision()
        self.handle_upgrades()
