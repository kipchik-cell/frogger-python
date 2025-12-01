# game/obstacles.py
import pygame
from .config import GameConfig


class Obstacle:
    def __init__(self, config, lane, direction, is_log=False):
        self.config = config
        self.lane = lane
        self.direction = direction  # True = right, False = left
        self.is_log = is_log
        self.speed = 2 if is_log else 3

        # Set size based on type
        if is_log:
            self.width = config.LOG_WIDTH
            self.height = config.LOG_HEIGHT
            self.color = config.COLORS["LOG_BROWN"]
        else:
            self.width = config.CAR_WIDTH
            self.height = config.CAR_HEIGHT
            self.color = config.COLORS["CAR_RED"]

        # Initial position
        self.x = 0 if direction else config.SCREEN_WIDTH
        self.y = lane * config.CELL_SIZE + (config.CELL_SIZE - self.height) // 2

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        """Update obstacle position"""
        if self.direction:  # Moving right
            self.x += self.speed
            if self.x > self.config.SCREEN_WIDTH:
                self.x = -self.width
        else:  # Moving left
            self.x -= self.speed
            if self.x < -self.width:
                self.x = self.config.SCREEN_WIDTH

        self.rect.x = self.x

    def draw(self, screen):
        """Draw obstacle on screen"""
        pygame.draw.rect(screen, self.color, self.rect)
        # Rounded corners
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)

    def collides_with(self, player_rect):
        """Check collision with player"""
        return self.rect.colliderect(player_rect)


class ObstacleManager:
    def __init__(self, config):
        self.config = config
        self.obstacles = []
        self.logs = []

    def create_car(self, lane, direction, is_right=True):
        """Create a car obstacle"""
        car = Obstacle(self.config, lane, is_right, is_log=False)
        self.obstacles.append(car)

    def create_log(self, lane, direction, is_right=True):
        """Create a log obstacle"""
        log = Obstacle(self.config, lane, is_right, is_log=True)
        self.logs.append(log)

    def clear(self):
        """Clear all obstacles"""
        self.obstacles.clear()
        self.logs.clear()

    def update(self):
        """Update all obstacles"""
        for obstacle in self.obstacles + self.logs:
            obstacle.update()

    def draw(self, screen):
        """Draw all obstacles"""
        for obstacle in self.obstacles + self.logs:
            obstacle.draw(screen)

    def is_hit_by_car(self, player_rect):
        """Check if player is hit by any car"""
        for car in self.obstacles:
            if car.collides_with(player_rect):
                return True
        return False

    def is_on_log(self, player_rect):
        """Check if player is on any log"""
        for log in self.logs:
            if log.collides_with(player_rect):
                # Move player with log
                player_rect.x += log.speed if log.direction else -log.speed
                return True
        return False