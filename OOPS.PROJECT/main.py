import pygame
import random
from settings import *
from assets import AssetManager
from utils import SaveManager, Camera
from player import Player
from levels import LevelFactory
from ui import UIManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.is_fullscreen = True
        self.state = 'menu'

        self.asset_manager = AssetManager()
        self.save_manager = SaveManager()
        self.levels = LevelFactory.create_all_levels()
        self.ui_manager = UIManager(self.save_manager, len(self.levels))

        self.game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.player = None
        self.camera = None
        self.current_level = None
        self.current_death_message = ""

    def run(self):
        while self.is_running:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()
        pygame.quit()

    def _handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11: self._toggle_fullscreen()
                if event.key == pygame.K_ESCAPE: self.state = 'menu'

            if self.state == 'menu':
                for btn in self.ui_manager.menu_buttons:
                    btn.update(mouse_pos)
                    if btn.is_clicked(event):
                        if btn.text == "PLAY": self.state = 'level_select'
                        elif btn.text == "EXIT": self.is_running = False

            if self.state == 'level_select':
                unlocked = self.save_manager.data["unlocked_level"]
                for i, btn in enumerate(self.ui_manager.level_buttons):
                    btn.update(mouse_pos)
                    if i + 1 <= unlocked and btn.is_clicked(event):
                        self._start_level(i + 1)

            if self.state == 'death' and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._reset_level()
            
            if self.state == 'victory' and (event.type == pygame.KEYDOWN and 
                 event.key in [pygame.K_RETURN, pygame.K_SPACE]):
                next_level_num = self.current_level.num + 1
                if next_level_num <= len(self.levels):
                    self.save_manager.unlock_level(next_level_num)
                    self._start_level(next_level_num)
                else:
                    self.state = 'menu'

    def _update(self, dt):
        if self.state == 'playing':
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                self.player.jump()

            self.player.update(dt, keys, self.current_level.get_all_platforms())
            self.current_level.update(dt, self.player)
            self.camera.update(self.player.x, dt)

            for trap in self.current_level.traps:
                if trap.check_collision(self.player):
                    self._player_die(); return
            
            if self.player.y > GAME_HEIGHT + 100:
                self._player_die(); return

            if self.current_level.goal.check_collision(self.player):
                self.state = 'victory'

    def _draw(self):
        if self.state == 'menu':
            self.ui_manager.draw_menu(self.screen)
        elif self.state == 'level_select':
            self.ui_manager.draw_level_select(self.screen)
        elif self.state in ['playing', 'death', 'victory']:
            self.game_surface.fill(DARK_BLUE)

            bg_image = self.asset_manager.images.get('background')
            if bg_image:
                bg_width = bg_image.get_width()
                camera_x_offset = self.camera.get_x() % bg_width
                for i in range(-1, (GAME_WIDTH // bg_width) + 2):
                    self.game_surface.blit(bg_image, (i * bg_width - camera_x_offset, 0))

            camera_x = self.camera.get_x()
            self.current_level.draw(self.game_surface, camera_x)
            self.player.draw(self.game_surface, camera_x)
            self.ui_manager.draw_hud(self.game_surface, self.current_level)
            scaled_surface = pygame.transform.scale(self.game_surface, self.screen.get_size())
            self.screen.blit(scaled_surface, (0, 0))
            if self.state == 'death':
                self.ui_manager.draw_death_screen(self.screen, self.current_death_message)
            elif self.state == 'victory':
                self.ui_manager.draw_victory_screen(self.screen, self.current_level.death_count)
        pygame.display.flip()

    def _start_level(self, level_num):
        if 1 <= level_num <= len(self.levels):
            self.current_level = self.levels[level_num - 1]
            self.current_level.death_count = 0
            self.current_level.reset()
            spawn_x, spawn_y = self.current_level.spawn
            self.player = Player(spawn_x, spawn_y, self.asset_manager)
            self.camera = Camera(self.current_level.width)
            self.state = 'playing'

    def _reset_level(self):
        if self.current_level:
            spawn_x, spawn_y = self.current_level.spawn
            self.player.reset(spawn_x, spawn_y)
            self.current_level.reset()
            self.state = 'playing'

    def _player_die(self):
        self.player.die()
        self.camera.shake()
        self.current_death_message = random.choice(DEATH_MESSAGES)
        self.current_level.death_count += 1
        self.save_manager.add_death()
        self.state = 'death'

    def _toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

if __name__ == "__main__":
    game = Game()
    game.run()