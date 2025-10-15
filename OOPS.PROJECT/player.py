import pygame
from settings import *

class Player:
    def __init__(self, x, y, asset_manager):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = float(x)
        self.y = float(y)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.on_ground = False
        self.alive = True
        self.facing_right = True
        self.asset_manager = asset_manager

        self.state = 'idle'
        self.frame = 0
        self.frame_timer = 0
        self.animations = {}
        self._load_animations()

    def _load_animations(self):
        if 'idle' in self.asset_manager.images:
            self.animations['idle'] = self.asset_manager.extract_frames(self.asset_manager.images['idle'], 32, 32)
        if 'run' in self.asset_manager.images:
            self.animations['run'] = self.asset_manager.extract_frames(self.asset_manager.images['run'], 32, 32)
        if 'jump' in self.asset_manager.images:
            self.animations['jump'] = self.asset_manager.extract_frames(self.asset_manager.images['jump'], 32, 32)

    def update(self, dt, keys, platforms):
        if not self.alive:
            return

        self._handle_movement(dt, keys)
        self._apply_physics(dt)
        self._handle_collisions(platforms)
        self._update_animation(dt)

    def _handle_movement(self, dt, keys):
        move_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        move_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

        if move_left:
            self.vel_x -= ACCELERATION * dt
            self.facing_right = False
        elif move_right:
            self.vel_x += ACCELERATION * dt
            self.facing_right = True
        else:
            if self.vel_x > 0:
                self.vel_x = max(0, self.vel_x - DECELERATION * dt)
            elif self.vel_x < 0:
                self.vel_x = min(0, self.vel_x + DECELERATION * dt)

        self.vel_x = max(-PLAYER_SPEED, min(PLAYER_SPEED, self.vel_x))

    def _apply_physics(self, dt):
        self.vel_y += GRAVITY * dt
        self.vel_y = min(self.vel_y, 1000)
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

    def _handle_collisions(self, platforms):
        self.on_ground = False
        player_rect = self.get_rect()

        for plat in platforms:
            if player_rect.colliderect(plat):
                if self.vel_y > 0 and player_rect.bottom > plat.top and player_rect.bottom < plat.top + 25:
                    self.y = float(plat.top - self.height)
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0 and player_rect.top < plat.bottom:
                    self.y = float(plat.bottom)
                    self.vel_y = 0

                player_rect = self.get_rect()
                if player_rect.colliderect(plat):
                    if self.vel_x > 0:
                        self.x = float(plat.left - self.width)
                    elif self.vel_x < 0:
                        self.x = float(plat.right)
                    self.vel_x = 0

    def _update_animation(self, dt):
        old_state = self.state

        if not self.on_ground:
            self.state = 'jump'
        elif abs(self.vel_x) > 10:
            self.state = 'run'
        else:
            self.state = 'idle'

        if self.state != old_state:
            self.frame = 0

        self.frame_timer += dt
        if self.frame_timer >= 0.1:
            self.frame_timer = 0
            if self.state in self.animations and self.animations[self.state]:
                self.frame = (self.frame + 1) % len(self.animations[self.state])

    def jump(self):
        if self.on_ground and self.alive:
            self.vel_y = JUMP_FORCE

    def die(self):
        self.alive = False

    def reset(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.alive = True
        self.frame = 0
        self.state = 'idle'

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, screen, camera_x):
        if not self.alive:
            return

        screen_x = int(self.x - camera_x)
        screen_y = int(self.y)

        if self.state in self.animations and self.animations[self.state]:
            current_frame = self.animations[self.state][self.frame]
            if not self.facing_right:
                current_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(current_frame, (screen_x, screen_y))
        else:
            pygame.draw.rect(screen, GREEN, (screen_x, screen_y, self.width, self.height))  
