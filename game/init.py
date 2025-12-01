# game/__init__.py

# Инициализация пакета game
# Экспортируем основные классы для удобного импорта

from .config import GameConfig
from .game import Game
from .player import Player
from .obstacles import ObstacleManager, Obstacle
from .levels import LevelManager, Home
from .ui import UI

__all__ = [
    'GameConfig',
    'Game',
    'Player',
    'ObstacleManager',
    'Obstacle',
    'LevelManager',
    'Home',
    'UI'
]

__version__ = '1.0.0'