import pygame
import random
import math
from abc import ABC, abstractmethod
from settings import *

class Trap(ABC):
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.active = True

    @abstractmethod
    def update(self, dt, player): pass
    @abstractmethod
    def draw(self, screen, camera_x): pass
    @abstractmethod
    def reset(self): pass
    def check_collision(self, player):
        return self.active and self.rect.colliderect(player.get_rect())

class InvisibleSpike(Trap):
    def __init__(self, x, y, reveal_dist=60):
        super().__init__(x, y, 16, 16); self.visible = False; self.reveal_dist = reveal_dist
    def update(self, dt, player):
        if abs(player.x - self.rect.x) < self.reveal_dist: self.visible = True
    def draw(self, screen, camera_x):
        if self.visible:
            x = self.rect.x - camera_x
            p = [(x+self.rect.w//2,self.rect.y),(x,self.rect.bottom),(x+self.rect.w,self.rect.bottom)]
            pygame.draw.polygon(screen, RED, p)
    def reset(self): self.visible = False

class FakePlatform(Trap):
    def __init__(self, x, y, width, delay=0.4):
        super().__init__(x, y, width, 20); self.delay = delay; self.timer = 0; self.touched = False
    def update(self, dt, player):
        if self.active and self.rect.colliderect(player.get_rect()):
            self.touched = True
            self.timer += dt
            if self.timer >= self.delay: self.active = False
    def draw(self, screen, camera_x):
        if self.active:
            x = self.rect.x - camera_x
            alpha = max(0, 1.0-(self.timer/self.delay)) if self.touched else 1.0
            color = tuple(int(c * alpha) for c in LIGHT_GRAY)
            shake = random.randint(-2, 2) if self.touched else 0
            pygame.draw.rect(screen, color, (x + shake, self.rect.y, self.rect.w, self.rect.h))
            pygame.draw.rect(screen, GRAY, (x + shake, self.rect.y, self.rect.w, self.rect.h), 2)
    def get_platform_rect(self): return self.rect if self.active else pygame.Rect(0,0,0,0)
    def reset(self): self.active = True; self.touched = False; self.timer = 0

class TrollSaw(Trap):
    def __init__(self, x, y, end_x, speed=150):
        super().__init__(x, y, 38, 38)
        self.start_x = x; self.end_x = end_x; self.speed = speed; self.direction = 1
        self.rotation = 0; self.speed_mult = 1.0
    def update(self, dt, player):
        if random.random() < 0.02: self.speed_mult = random.uniform(0.7, 1.8)
        self.rect.x += int(self.speed * self.direction * self.speed_mult * dt)
        if self.rect.x >= self.end_x or self.rect.x <= self.start_x: self.direction *= -1
        self.rotation += 300 * dt
    def draw(self, screen, camera_x):
        x, y = self.rect.centerx - camera_x, self.rect.centery
        pygame.draw.circle(screen, GRAY, (x, y), 19)
        for i in range(8):
            angle = math.radians(self.rotation + i * 45)
            ex, ey = x + math.cos(angle) * 19, y + math.sin(angle) * 19
            pygame.draw.circle(screen, RED, (int(ex), int(ey)), 4)
    def reset(self): self.rect.x = self.start_x; self.direction = 1

class FakeGoal(Trap):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 50)
        self.pulse = 0
    def update(self, dt, player):
        self.pulse += dt * 3
    def draw(self, screen, camera_x):
        x = self.rect.x - camera_x
        p = abs(math.sin(self.pulse))
        color = (int(50 + 155 * p), int(205 + 50 * p), int(50 + 155 * p))
        pygame.draw.rect(screen, color, (x, self.rect.y, self.rect.w, self.rect.h))
        pygame.draw.line(screen, BLACK, (x + 10, self.rect.y + 25), (x + 18, self.rect.y + 35), 3)
        pygame.draw.line(screen, BLACK, (x + 18, self.rect.y + 35), (x + 32, self.rect.y + 15), 3)
    def reset(self): self.pulse = 0

class NarrowGap(Trap):
    def __init__(self, x, y, gap_h=32):
        super().__init__(x, 0, 20, GAME_HEIGHT); self.gap_y = y; self.gap_h = gap_h
    def update(self, dt, player): pass
    def check_collision(self, player):
        pr = player.get_rect()
        top_rect = pygame.Rect(self.rect.x, 0, self.rect.w, self.gap_y)
        bottom_rect = pygame.Rect(self.rect.x, self.gap_y + self.gap_h, self.rect.w, self.rect.h)
        return top_rect.colliderect(pr) or bottom_rect.colliderect(pr)
    def draw(self, screen, camera_x):
        x = self.rect.x - camera_x
        for i in range(0, self.gap_y, 15):
            p = [(x + 10, i), (x, i + 10), (x + 20, i + 10)]
            pygame.draw.polygon(screen, GRAY, p)
        for i in range(self.gap_y + self.gap_h, GAME_HEIGHT, 15):
            p = [(x + 10, i + 10), (x, i), (x + 20, i)]
            pygame.draw.polygon(screen, GRAY, p)
    def reset(self): pass
