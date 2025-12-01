# game/config.py

class GameConfig:
    def __init__(self):
        # Screen settings
        self.SCREEN_WIDTH = 560
        self.SCREEN_HEIGHT = 600
        self.FPS = 60

        # Game settings
        self.LANES = 10
        self.CELL_SIZE = 60
        self.FROG_START = {"x": 5, "y": 9}
        self.INITIAL_LIVES = 3

        # Colors - УБЕДИТЕСЬ ЧТО GRAY ЕСТЬ
        self.COLORS = {
            "BLACK": (0, 0, 0),
            "WHITE": (255, 255, 255),
            "GRAY": (128, 128, 128),  # <-- ДОБАВЬТЕ
            "LIGHT_GRAY": (200, 200, 200),  # <-- МОЖНО ТАКЖЕ ДОБАВИТЬ
            "GREEN": (144, 238, 144),
            "DARK_GREEN": (0, 100, 0),
            "BLUE": (135, 206, 235),
            "RIVER_BLUE": (30, 144, 255),
            "ROAD_GRAY": (105, 105, 105),
            "CAR_RED": (255, 69, 0),
            "LOG_BROWN": (139, 69, 19),
            "FROG_GREEN": (50, 205, 50),
            "YELLOW": (255, 215, 0),
            "RED": (255, 0, 0),
            "GOLD": (255, 215, 0),
            "GOAL_GREEN": (144, 238, 144)
        }

        # Game speeds
        self.LEVEL_SPEEDS = [300, 200]

        # Obstacle sizes
        self.CAR_WIDTH = 80
        self.CAR_HEIGHT = 40
        self.LOG_WIDTH = 120
        self.LOG_HEIGHT = 40
        self.FROG_SIZE = 40
        self.HOME_WIDTH = 80
        self.HOME_HEIGHT = 40

        # Game states
        self.STATE_START = 0
        self.STATE_PLAYING = 1
        self.STATE_GAME_OVER = 2
        self.STATE_LEVEL_COMPLETE = 3