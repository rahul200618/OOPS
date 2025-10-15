import pygame
from settings import *

class Button:
    def __init__(self, x, y, w, h, text, color=BLUE, hover_color=CYAN):
        self.rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 3)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered

class UIManager:
    def __init__(self, save_manager, level_count):
        self.save_manager = save_manager
        self.level_count = level_count
        self.font_huge = pygame.font.Font(None, 100)
        self.font_large = pygame.font.Font(None, 72)
        self.font_med = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self._create_buttons()

    def _create_buttons(self):
        center_x = SCREEN_WIDTH // 2
        
        self.menu_buttons = [
            Button(center_x, SCREEN_HEIGHT // 2 - 100, 250, 70, "PLAY"),
            Button(center_x, SCREEN_HEIGHT // 2, 250, 70, "SETTINGS"),
            Button(center_x, SCREEN_HEIGHT // 2 + 100, 250, 70, "EXIT"),
        ]

        self.level_buttons = []
        rows, cols = 2, 5
        btn_w, btn_h = 160, 110
        spacing_x, spacing_y = 190, 150
        grid_w = (cols - 1) * spacing_x
        start_x = center_x - grid_w // 2
        start_y = SCREEN_HEIGHT // 2 - 100

        for i in range(self.level_count):
            row = i // cols
            col = i % cols
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            self.level_buttons.append(Button(x, y, btn_w, btn_h, f"Level {i + 1}"))

    def draw_menu(self, screen):
        screen.fill(DARK_PURPLE)
        title = self.font_huge.render("DON'T EVEN BOTHER", True, RED)
        subtitle = self.font_small.render("Pure Evil Edition - NO WARNINGS!", True, ORANGE)
        deaths = self.font_small.render(f"Total Deaths: {self.save_manager.data['total_deaths']}", True, RED)
        hint = self.font_small.render("ESC = Menu | F11 = Fullscreen", True, GRAY)

        screen.blit(title, title.get_rect(centerx=screen.get_width() // 2, y=150))
        screen.blit(subtitle, subtitle.get_rect(centerx=screen.get_width() // 2, y=260))
        screen.blit(deaths, deaths.get_rect(centerx=screen.get_width() // 2, bottom=screen.get_height() - 120))
        screen.blit(hint, hint.get_rect(centerx=screen.get_width() // 2, bottom=screen.get_height() - 60))
        
        for btn in self.menu_buttons:
            btn.draw(screen, self.font_med)

    def draw_level_select(self, screen):
        screen.fill(DARK_PURPLE)
        title = self.font_large.render("SELECT LEVEL", True, YELLOW)
        hint = self.font_small.render("ESC to go back", True, WHITE)

        screen.blit(title, title.get_rect(centerx=screen.get_width() // 2, y=100))
        screen.blit(hint, hint.get_rect(centerx=screen.get_width() // 2, bottom=screen.get_height() - 60))

        unlocked = self.save_manager.data["unlocked_level"]
        for i, btn in enumerate(self.level_buttons):
            if i + 1 <= unlocked:
                btn.draw(screen, self.font_med)
            else:
                pygame.draw.rect(screen, GRAY, btn.rect)
                pygame.draw.rect(screen, DARK_PURPLE, btn.rect, 3)
                lock_surf = self.font_med.render("LOCKED", True, DARK_PURPLE)
                screen.blit(lock_surf, lock_surf.get_rect(center=btn.rect.center))

    def draw_hud(self, screen, level):
        deaths_txt = self.font_small.render(f"Deaths: {level.death_count}", True, RED)
        level_txt = self.font_small.render(f"Level {level.num}", True, YELLOW)
        screen.blit(deaths_txt, (20, 20))
        screen.blit(level_txt, (GAME_WIDTH - level_txt.get_width() - 20, 20))

    def draw_death_screen(self, screen, message):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((80, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        msg = self.font_huge.render("YOU DIED", True, RED)
        taunt = self.font_large.render(message, True, ORANGE)
        hint = self.font_med.render("Press R to restart | ESC for menu", True, WHITE)
        
        screen.blit(msg, msg.get_rect(centerx=screen.get_width() // 2, centery=screen.get_height() // 3))
        screen.blit(taunt, taunt.get_rect(centerx=screen.get_width() // 2, centery=screen.get_height() // 2))
        screen.blit(hint, hint.get_rect(centerx=screen.get_width() // 2, centery=screen.get_height() // 2 + 120))

    def draw_victory_screen(self, screen, death_count):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 100, 0, 150))
        screen.blit(overlay, (0, 0))

        win = self.font_huge.render("LEVEL COMPLETE!", True, GREEN)
        deaths = self.font_large.render(f"Deaths: {death_count}", True, YELLOW)
        cont = self.font_med.render("Press SPACE to continue | ESC for menu", True, WHITE)

        screen.blit(win, win.get_rect(centerx=screen.get_width() // 2, centery=screen.get_height() // 3))
        screen.blit(deaths, deaths.get_rect(centerx=screen.get_width() // 2, centery=screen.get_height() // 2))
        screen.blit(cont, cont.get_rect(centerx=screen.get_width() // 2, centery=screen.get_height() // 2 + 120))
