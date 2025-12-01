# game/ui.py
import pygame
from .config import GameConfig


class UI:
    def __init__(self, game):
        self.game = game
        self.config = game.config
        self.screen = None
        self.clock = None
        self.fonts = {}

        # UI elements
        self.text_input = ""
        self.active_input = True

    def initialize(self, screen, clock):
        """Initialize UI with screen and clock"""
        self.screen = screen
        self.clock = clock
        self.load_fonts()

    def load_fonts(self):
        """Load game fonts"""
        try:
            self.fonts["large"] = pygame.font.Font(None, 74)
            self.fonts["medium"] = pygame.font.Font(None, 48)
            self.fonts["small"] = pygame.font.Font(None, 36)
            self.fonts["tiny"] = pygame.font.Font(None, 24)
        except:
            # Fallback to default font if custom font fails
            self.fonts["large"] = pygame.font.Font(None, 74)
            self.fonts["medium"] = pygame.font.Font(None, 48)
            self.fonts["small"] = pygame.font.Font(None, 36)
            self.fonts["tiny"] = pygame.font.Font(None, 24)

    def draw_background(self):
        """Draw game background areas"""
        colors = self.config.COLORS

        # Goal area (top)
        pygame.draw.rect(
            self.screen,
            colors["GOAL_GREEN"],
            (0, 0, self.config.SCREEN_WIDTH, 60)
        )

        # River area
        pygame.draw.rect(
            self.screen,
            colors["RIVER_BLUE"],
            (0, 60, self.config.SCREEN_WIDTH, 180)
        )

        # Road area
        pygame.draw.rect(
            self.screen,
            colors["ROAD_GRAY"],
            (0, 240, self.config.SCREEN_WIDTH, 240)
        )

        # Safe area (bottom)
        pygame.draw.rect(
            self.screen,
            colors["GREEN"],
            (0, 480, self.config.SCREEN_WIDTH, 60)
        )

        # Lane lines
        for i in range(self.config.LANES):
            y = i * self.config.CELL_SIZE
            pygame.draw.line(
                self.screen,
                colors["BLACK"],
                (0, y),
                (self.config.SCREEN_WIDTH, y),
                1
            )

    def draw_game_info(self, game_state):
        """Draw game information (score, lives, etc.)"""
        # Draw background for info panel
        pygame.draw.rect(
            self.screen,
            self.config.COLORS["BLACK"],
            (0, self.config.SCREEN_HEIGHT, self.config.SCREEN_WIDTH, 50)
        )

        # Draw info text
        info_y = self.config.SCREEN_HEIGHT + 10
        info_texts = [
            f"Player: {game_state['player_name']}",
            f"Level: {game_state['level']}",
            f"Lives: {game_state['lives']}",
            f"Score: {game_state['score']}"
        ]

        for i, text in enumerate(info_texts):
            text_surface = self.fonts["tiny"].render(text, True, self.config.COLORS["WHITE"])
            self.screen.blit(text_surface, (10 + i * 140, info_y))

    def draw_start_screen(self):
        """Draw start screen"""
        self.screen.fill(self.config.COLORS["DARK_GREEN"])

        # Title
        title = self.fonts["large"].render("FROGGER", True, self.config.COLORS["GOLD"])
        title_rect = title.get_rect(center=(self.config.SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Input field
        input_bg = pygame.Rect(
            self.config.SCREEN_WIDTH // 2 - 125,
            200,
            250,
            40
        )
        pygame.draw.rect(self.screen, self.config.COLORS["WHITE"], input_bg)
        pygame.draw.rect(self.screen, self.config.COLORS["BLACK"], input_bg, 2)

        # Input text
        input_text = self.text_input if self.text_input else "Enter your name"
        text_color = self.config.COLORS["BLACK"] if self.text_input else self.config.COLORS["GRAY"]
        text_surface = self.fonts["small"].render(input_text, True, text_color)
        self.screen.blit(text_surface, (input_bg.x + 10, input_bg.y + 8))

        # Cursor
        if self.active_input:
            cursor_pos = text_surface.get_width() + input_bg.x + 10
            pygame.draw.line(
                self.screen,
                self.config.COLORS["BLACK"],
                (cursor_pos, input_bg.y + 5),
                (cursor_pos, input_bg.y + 35),
                2
            )

        # Start button
        start_button = pygame.Rect(
            self.config.SCREEN_WIDTH // 2 - 100,
            280,
            200,
            50
        )
        pygame.draw.rect(self.screen, self.config.COLORS["FROG_GREEN"], start_button, border_radius=10)
        pygame.draw.rect(self.screen, self.config.COLORS["BLACK"], start_button, 2, border_radius=10)

        start_text = self.fonts["medium"].render("START GAME", True, self.config.COLORS["WHITE"])
        start_rect = start_text.get_rect(center=start_button.center)
        self.screen.blit(start_text, start_rect)

        # Controls info
        controls = [
            "Use ARROW KEYS to move the frog",
            "Avoid cars and don't fall in the river!",
            "Press P to pause"
        ]

        for i, control in enumerate(controls):
            control_text = self.fonts["tiny"].render(control, True, self.config.COLORS["WHITE"])
            control_rect = control_text.get_rect(center=(self.config.SCREEN_WIDTH // 2, 380 + i * 30))
            self.screen.blit(control_text, control_rect)

        return start_button

    def draw_game_over_screen(self, game_state):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(self.config.COLORS["BLACK"])
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        game_over = self.fonts["large"].render("GAME OVER", True, self.config.COLORS["RED"])
        game_over_rect = game_over.get_rect(center=(self.config.SCREEN_WIDTH // 2, 150))
        self.screen.blit(game_over, game_over_rect)

        # Score
        score_text = self.fonts["medium"].render(
            f"Your score: {game_state['score']}",
            True,
            self.config.COLORS["WHITE"]
        )
        score_rect = score_text.get_rect(center=(self.config.SCREEN_WIDTH // 2, 250))
        self.screen.blit(score_text, score_rect)

        # Buttons
        restart_button = pygame.Rect(
            self.config.SCREEN_WIDTH // 2 - 220,
            350,
            200,
            50
        )
        menu_button = pygame.Rect(
            self.config.SCREEN_WIDTH // 2 + 20,
            350,
            200,
            50
        )

        # Draw buttons
        for button, text in [(restart_button, "PLAY AGAIN"), (menu_button, "MAIN MENU")]:
            pygame.draw.rect(self.screen, self.config.COLORS["FROG_GREEN"], button, border_radius=10)
            pygame.draw.rect(self.screen, self.config.COLORS["BLACK"], button, 2, border_radius=10)

            button_text = self.fonts["small"].render(text, True, self.config.COLORS["WHITE"])
            button_rect = button_text.get_rect(center=button.center)
            self.screen.blit(button_text, button_rect)

        return restart_button, menu_button

    def draw_level_complete_screen(self):
        """Draw level complete screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(self.config.COLORS["BLACK"])
        self.screen.blit(overlay, (0, 0))

        # Level Complete text
        complete_text = self.fonts["large"].render("LEVEL COMPLETE!", True, self.config.COLORS["GOLD"])
        complete_rect = complete_text.get_rect(center=(self.config.SCREEN_WIDTH // 2, 150))
        self.screen.blit(complete_text, complete_rect)

        # Message
        message = self.fonts["medium"].render("You reached the next level!", True, self.config.COLORS["WHITE"])
        message_rect = message.get_rect(center=(self.config.SCREEN_WIDTH // 2, 250))
        self.screen.blit(message, message_rect)

        # Continue button
        continue_button = pygame.Rect(
            self.config.SCREEN_WIDTH // 2 - 100,
            350,
            200,
            50
        )
        pygame.draw.rect(self.screen, self.config.COLORS["FROG_GREEN"], continue_button, border_radius=10)
        pygame.draw.rect(self.screen, self.config.COLORS["BLACK"], continue_button, 2, border_radius=10)

        continue_text = self.fonts["medium"].render("CONTINUE", True, self.config.COLORS["WHITE"])
        continue_rect = continue_text.get_rect(center=continue_button.center)
        self.screen.blit(continue_text, continue_rect)

        return continue_button

    def draw_pause_screen(self):
        """Draw pause screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(self.config.COLORS["BLACK"])
        self.screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.fonts["large"].render("PAUSED", True, self.config.COLORS["YELLOW"])
        pause_rect = pause_text.get_rect(center=(self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)

    def handle_events(self, event):
        """Handle UI events"""
        if event.type == pygame.KEYDOWN:
            if self.game.state["current"] == self.config.STATE_START and self.active_input:
                if event.key == pygame.K_RETURN:
                    if self.text_input:
                        self.game.start_game(self.text_input)
                        return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]
                elif len(self.text_input) < 15:
                    self.text_input += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.game.state["current"] == self.config.STATE_START:
                # Check if clicking on input field
                input_rect = pygame.Rect(
                    self.config.SCREEN_WIDTH // 2 - 125,
                    200,
                    250,
                    40
                )
                self.active_input = input_rect.collidepoint(mouse_pos)

        return False