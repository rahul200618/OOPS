import pygame
import os
from settings import ASSETS_PATH

class AssetManager:
    def __init__(self):
        self.images = {}
        self._load_assets()

    def _load_assets(self):
        try:
            idle_path = os.path.join(ASSETS_PATH, 'Idle.png')
            if os.path.exists(idle_path):
                self.images['idle'] = pygame.image.load(idle_path).convert_alpha()

            run_path = os.path.join(ASSETS_PATH, 'Run.png')
            if os.path.exists(run_path):
                self.images['run'] = pygame.image.load(run_path).convert_alpha()

            jump_path = os.path.join(ASSETS_PATH, 'Jump.png')
            if os.path.exists(jump_path):
                self.images['jump'] = pygame.image.load(jump_path).convert_alpha()

            bg_path = os.path.join(ASSETS_PATH, 'background', 'background.png')
            if os.path.exists(bg_path):
                self.images['background'] = pygame.image.load(bg_path).convert()

        except pygame.error as e:
            print(f"Error loading player assets: {e}")
            self.images.setdefault('idle', pygame.Surface((32, 32)))
            self.images.setdefault('run', pygame.Surface((32, 32)))
            self.images.setdefault('jump', pygame.Surface((32, 32)))
            self.images.setdefault('background', None)


    def extract_frames(self, image, frame_w, frame_h):
        frames = []
        sheet_w, sheet_h = image.get_size()
        for y in range(0, sheet_h, frame_h):
            for x in range(0, sheet_w, frame_w):
                frame = image.subsurface(pygame.Rect(x, y, frame_w, frame_h))
                frames.append(frame)
        return frames
