# game/game.py
import pygame
from .config import GameConfig
from .player import Player
from .obstacles import ObstacleManager
from .levels import LevelManager


class Game:
    def __init__(self):
        self.config = GameConfig()
        self.state = {
            "current": self.config.STATE_START,
            "level": 1,
            "lives": self.config.INITIAL_LIVES,
            "score": 0,
            "player_name": "Player",
            "is_paused": False
        }

        # Initialize game objects
        self.player = Player(self.config)
        self.obstacle_manager = ObstacleManager(self.config)
        self.level_manager = LevelManager(self.config)

        # Timing
        self.last_update = 0
        self.game_speed = self.config.LEVEL_SPEEDS[0]

    def reset(self):
        """Reset game to initial state"""
        self.state["level"] = 1
        self.state["lives"] = self.config.INITIAL_LIVES
        self.state["score"] = 0
        self.state["current"] = self.config.STATE_PLAYING
        self.state["is_paused"] = False

        self.player.reset()
        self.obstacle_manager.clear()
        self.level_manager.reset_homes()
        self.level_manager.generate_level(1, self.obstacle_manager)
        self.game_speed = self.config.LEVEL_SPEEDS[0]

    def start_game(self, player_name):
        """Start a new game"""
        self.state["player_name"] = player_name or "Player"
        self.reset()

    def update(self, current_time):
        """Update game state"""
        if self.state["is_paused"] or self.state["current"] != self.config.STATE_PLAYING:
            return

        # Update at game speed interval
        if current_time - self.last_update > self.game_speed:
            self.last_update = current_time

            # Update obstacles
            self.obstacle_manager.update()

            # Check collisions and game logic
            self.check_collisions()

    def check_collisions(self):
        """Check all game collisions"""
        # Update player rectangle
        self.player.update_rect()

        # Check if frog is in river
        if self.player.is_in_river():
            # Check if on log
            if not self.obstacle_manager.is_on_log(self.player.rect):
                self.lose_life()
                return

        # Check if hit by car
        if self.obstacle_manager.is_hit_by_car(self.player.rect):
            self.lose_life()
            return

        # Check if reached home
        if self.level_manager.check_home_reached(self.player.rect):
            self.state["score"] += 100 * self.state["level"]
            self.player.reset()

            if self.level_manager.all_homes_filled():
                self.complete_level()

        # Check if reached top (extra points)
        if self.player.position["y"] < 1:
            self.state["score"] += 50
            self.player.reset()

    def lose_life(self):
        """Handle losing a life"""
        self.state["lives"] -= 1
        self.player.reset()

        if self.state["lives"] <= 0:
            self.state["current"] = self.config.STATE_GAME_OVER

    def complete_level(self):
        """Handle level completion"""
        if self.state["level"] < 2:
            self.state["current"] = self.config.STATE_LEVEL_COMPLETE
        else:
            self.state["score"] += 500
            self.state["current"] = self.config.STATE_GAME_OVER

    def next_level(self):
        """Advance to next level"""
        self.state["level"] += 1
        self.player.reset()
        self.level_manager.reset_homes()
        self.level_manager.generate_level(self.state["level"], self.obstacle_manager)
        self.state["current"] = self.config.STATE_PLAYING

        # Update game speed for level 2
        if self.state["level"] == 2:
            self.game_speed = self.config.LEVEL_SPEEDS[1]

    def move_player(self, direction):
        """Move player in specified direction"""
        if (self.state["current"] == self.config.STATE_PLAYING and
                not self.state["is_paused"]):
            if self.player.move(direction):
                self.player.update_rect()
                self.check_collisions()

    def toggle_pause(self):
        """Toggle pause state"""
        self.state["is_paused"] = not self.state["is_paused"]

    def get_game_state(self):
        """Return current game state"""
        return {
            "player_name": self.state["player_name"],
            "level": self.state["level"],
            "lives": self.state["lives"],
            "score": self.state["score"],
            "state": self.state["current"]
        }