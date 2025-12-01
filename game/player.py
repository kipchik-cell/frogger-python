# game/player.py
import pygame
from .config import GameConfig


class Player:
    def __init__(self, config):
        self.config = config
        self.position = config.FROG_START.copy()
        self.start_position = config.FROG_START.copy()
        self.rect = None
        self.color = config.COLORS["FROG_GREEN"]
        self.size = config.FROG_SIZE

    def move(self, direction):
        old_position = self.position.copy()

        if direction == "up" and self.position["y"] > 0:
            self.position["y"] -= 1
        elif direction == "down" and self.position["y"] < 9:
            self.position["y"] += 1
        elif direction == "left" and self.position["x"] > 0:
            self.position["x"] -= 1
        elif direction == "right" and self.position["x"] < 8:
            self.position["x"] += 1

        # Return True if position changed
        return old_position != self.position

    def update_rect(self):
        """Update rectangle position based on grid position"""
        cell_size = self.config.CELL_SIZE
        self.rect = pygame.Rect(
            self.position["x"] * cell_size + (cell_size - self.size) // 2,
            self.position["y"] * cell_size + (cell_size - self.size) // 2,
            self.size,
            self.size
        )

    def reset(self):
        """Reset player to starting position"""
        self.position = self.start_position.copy()
        self.update_rect()

    def is_in_river(self):
        """Check if player is in river area (rows 1-3)"""
        return 1 <= self.position["y"] <= 3

    def draw(self, screen):
        """Draw the player on screen"""
        if self.rect:
            pygame.draw.circle(
                screen,
                self.color,
                self.rect.center,
                self.size // 2
            )
            # Draw border
            pygame.draw.circle(
                screen,
                self.config.COLORS["BLACK"],
                self.rect.center,
                self.size // 2,
                2
            )