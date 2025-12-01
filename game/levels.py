# game/levels.py
import pygame
from .config import GameConfig


class Home:
    def __init__(self, config, x, y):
        self.config = config
        self.x = x
        self.y = y
        self.width = config.HOME_WIDTH
        self.height = config.HOME_HEIGHT
        self.filled = False
        self.frog_color = config.COLORS["RED"]
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):
        """Draw home on screen"""
        # Draw home area
        pygame.draw.rect(
            screen,
            self.config.COLORS["GOAL_GREEN"],
            self.rect
        )

        # Draw border
        pygame.draw.rect(
            screen,
            self.config.COLORS["BLACK"],
            self.rect,
            2
        )

        # Draw dashed border
        dash_length = 5
        for i in range(0, self.width, dash_length * 2):
            pygame.draw.line(
                screen,
                self.config.COLORS["BLACK"],
                (self.x + i, self.y),
                (self.x + i + dash_length, self.y),
                2
            )
            pygame.draw.line(
                screen,
                self.config.COLORS["BLACK"],
                (self.x + i, self.y + self.height),
                (self.x + i + dash_length, self.y + self.height),
                2
            )

        for i in range(0, self.height, dash_length * 2):
            pygame.draw.line(
                screen,
                self.config.COLORS["BLACK"],
                (self.x, self.y + i),
                (self.x, self.y + i + dash_length),
                2
            )
            pygame.draw.line(
                screen,
                self.config.COLORS["BLACK"],
                (self.x + self.width, self.y + i),
                (self.x + self.width, self.y + i + dash_length),
                2
            )

        # Draw frog if home is filled
        if self.filled:
            frog_rect = pygame.Rect(
                self.x + self.width // 2 - self.config.FROG_SIZE // 2,
                self.y + self.height // 2 - self.config.FROG_SIZE // 2,
                self.config.FROG_SIZE,
                self.config.FROG_SIZE
            )
            pygame.draw.circle(
                screen,
                self.frog_color,
                frog_rect.center,
                self.config.FROG_SIZE // 2
            )


class LevelManager:
    def __init__(self, config):
        self.config = config
        self.homes = []
        self.create_homes()

    def create_homes(self):
        """Create home positions"""
        self.homes.clear()
        for i in range(5):
            x = 40 + i * 120
            y = 10
            home = Home(self.config, x, y)
            self.homes.append(home)

    def generate_level(self, level, obstacle_manager):
        """Generate obstacles for specific level"""
        obstacle_manager.clear()

        if level == 1:
            self.generate_level_1(obstacle_manager)
        elif level == 2:
            self.generate_level_2(obstacle_manager)

    def generate_level_1(self, obstacle_manager):
        """Generate level 1 obstacles"""
        # Cars on road (lanes 4-7)
        obstacle_manager.create_car(4, True)  # Lane 4, moving right
        obstacle_manager.create_car(5, False)  # Lane 5, moving left
        obstacle_manager.create_car(6, True)  # Lane 6, moving right
        obstacle_manager.create_car(7, False)  # Lane 7, moving left

        # Logs on river (lanes 1-3)
        obstacle_manager.create_log(1, True)  # Lane 1, moving right
        obstacle_manager.create_log(2, False)  # Lane 2, moving left
        obstacle_manager.create_log(3, True)  # Lane 3, moving right

    def generate_level_2(self, obstacle_manager):
        """Generate level 2 obstacles (more challenging)"""
        # More cars
        obstacle_manager.create_car(4, True)
        obstacle_manager.create_car(4, False)
        obstacle_manager.create_car(5, False)
        obstacle_manager.create_car(5, True)
        obstacle_manager.create_car(6, True)
        obstacle_manager.create_car(6, False)
        obstacle_manager.create_car(7, False)
        obstacle_manager.create_car(7, True)

        # More logs
        obstacle_manager.create_log(1, True)
        obstacle_manager.create_log(1, False)
        obstacle_manager.create_log(2, False)
        obstacle_manager.create_log(2, True)
        obstacle_manager.create_log(3, True)
        obstacle_manager.create_log(3, False)

    def check_home_reached(self, player_rect):
        """Check if player reached any home"""
        for home in self.homes:
            if not home.filled and home.rect.colliderect(player_rect):
                home.filled = True
                return True
        return False

    def all_homes_filled(self):
        """Check if all homes are filled"""
        return all(home.filled for home in self.homes)

    def reset_homes(self):
        """Reset all homes to unfilled"""
        for home in self.homes:
            home.filled = False

    def draw_homes(self, screen):
        """Draw all homes"""
        for home in self.homes:
            home.draw(screen)