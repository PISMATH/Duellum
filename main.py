import pygame
import time
import random
from settings import *
from player import Player
from bullet import Bullet
from enemies import Enemy

def bullet_in_enemy(bullet, enemy):
    if enemy.pos.y - enemy.img_height < bullet.pos.y < enemy.pos.y + enemy.img_height / 2 and \
            enemy.pos.x - enemy.img_width / 2 < bullet.pos.x < enemy.pos.x + enemy.img_width / 2:
        return True
    return False

class Game:
    def __init__(self, game_mode='single player'):
        pygame.init()
        self.game_mode = game_mode
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.players = [Player((screen_width / 2, screen_height / 2), self)]
        self.font = pygame.font.Font('fonts/ARCADECLASSIC.TTF', 32)
        pygame.display.set_caption('Shoot')
        self.images = {
            'play title screen': pygame.image.load('img/play title screen.png')
        }
        self.bullets = []
        self.enemies = []
        self.upgrades = []
        self.enemy_bullets = []
        self.last_enemy_spawn_time = time.time()
        self.enemy_spawn_rate = base_enemy_spawn_speed

        self.background_sound = pygame.mixer.Sound('sound/backgroundmusic.wav')
        self.boom_sound = pygame.mixer.Sound('sound/PlaneExplodes.wav')
        self.heart_gain_sound = pygame.mixer.Sound('sound/GainHeart.wav')
        self.background_sound.play(-1)

    def render_game_single_player(self):
        for bullet in self.bullets:
            bullet.render()

        for enemy in self.enemies:
            enemy.render()

        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.render()

        for upgrade in self.upgrades:
            upgrade.render()
        for player in self.players:
            player.render()

    def update_single_player(self, dt):
        self.handle_item_creation_single_player()
        for bullet in self.bullets:
            if not bullet.update(dt):
                self.bullets.remove(bullet)

        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.update(dt)
            if enemy_bullet.pos.x < 0:
                self.enemy_bullets.remove(enemy_bullet)
            for player in self.players:
                if bullet_in_enemy(enemy_bullet, player):
                    player.handle_life_loss()
                    if enemy_bullet in self.enemy_bullets:
                        self.enemy_bullets.remove(enemy_bullet)
        # enemies
        for enemy in self.enemies:
            for player in self.players:
                if not enemy.update(dt, player.pos):
                    self.enemies.remove(enemy)
                    player.handle_life_loss()
            if enemy.shooting and time.time() - enemy.last_shoot_time > 1 / enemy_shoot_speed:
                nearest_player = self.players[0]
                nearest_distance = float('inf')
                for player in self.players:
                    dist = (player.pos.x - enemy.pos.x) ** 2 + (player.pos.y - enemy.pos.y) ** 2
                    if dist < nearest_distance:
                        nearest_player = player
                        nearest_distance = dist
                bullet = Bullet(enemy.pos, self.screen)
                bullet.direction = pygame.math.Vector2(nearest_player.pos.x - enemy.pos.x + random.randint(-enemy_aim, enemy_aim),
                                                       nearest_player.pos.y - enemy.pos.y + random.randint(-enemy_aim, enemy_aim)).normalize()
                bullet.img = pygame.Surface((4, 4))
                bullet.img.fill('white')
                self.enemy_bullets.append(bullet)
                enemy.last_shoot_time = time.time()

        for upgrade in self.upgrades:
            upgrade.update(dt)
        for player in self.players:
            player.update(dt)

    def handle_item_creation_single_player(self):
        if time.time() - self.last_enemy_spawn_time > 1 / self.enemy_spawn_rate:
            self.enemies.append(
                Enemy((screen_width + enemy_x_offscreen_dist, random.randint(enemy_y_boarders, screen_height - enemy_y_boarders)), self.screen))
            self.last_enemy_spawn_time = time.time()
     
    def title_screen_single_player(self, final_score):
        title = True
        while title:
            self.screen.fill('white')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Check if the user is closing the window
                    pygame.quit()
                    quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:  # Check if the user clicked
                    return True
            
            if final_score is not None:
                # Render final score text
                score_text = self.font.render(f"Final Score: {final_score}", False, "black")  
                score_width = score_text.get_width()
                score_x = (screen_width - score_width) / 2
                score_y = screen_height - 50
                self.screen.blit(score_text, (score_x, score_y))

            # Render play button
            self.screen.blit(
                self.images['play title screen'],
                (screen_width / 2 - self.images['play title screen'].get_width() / 2,
                 screen_height / 2 - self.images['play title screen'].get_height() / 2)
            )
            pygame.display.flip()

    def game(self):
        if self.game_mode == 'single player':
            running = self.title_screen_single_player(None)
            while running:
                self.screen.fill('black')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                dt = self.clock.tick()
                if self.players[0].lives > 0:
                    self.render_game_single_player()
                    self.update_single_player(dt)
                pygame.display.flip()
        elif self.game_mode == 'multiplayer':
            pass

if __name__ == '__main__':
    game = Game()
    game.game()
