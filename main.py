# main.py
import pygame
import sys
from game.game import Game
from game.ui import UI


def main():
    # Initialize Pygame
    pygame.init()

    # Create game instance
    game = Game()

    # Create UI instance
    ui = UI(game)

    # Set up screen
    screen_width = game.config.SCREEN_WIDTH
    screen_height = game.config.SCREEN_HEIGHT + 50  # Extra space for info panel
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Frogger - Python Edition")

    # Set up clock
    clock = pygame.time.Clock()

    # Initialize UI
    ui.initialize(screen, clock)

    # Main game loop
    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Game state transitions
                if game.state["current"] == game.config.STATE_START:
                    if event.key == pygame.K_RETURN and ui.text_input:
                        game.start_game(ui.text_input)
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                elif game.state["current"] == game.config.STATE_PLAYING:
                    # Player movement
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        game.move_player("up")
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        game.move_player("down")
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        game.move_player("left")
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        game.move_player("right")
                    elif event.key == pygame.K_p:
                        game.toggle_pause()
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                elif game.state["current"] == game.config.STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        game.reset()
                    elif event.key == pygame.K_m:
                        game.state["current"] = game.config.STATE_START
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                elif game.state["current"] == game.config.STATE_LEVEL_COMPLETE:
                    if event.key == pygame.K_RETURN:
                        game.next_level()
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                game_state = game.get_game_state()

                # Handle button clicks based on current state
                if game.state["current"] == game.config.STATE_START:
                    start_button = pygame.Rect(
                        screen_width // 2 - 100,
                        280,
                        200,
                        50
                    )
                    if start_button.collidepoint(mouse_pos) and ui.text_input:
                        game.start_game(ui.text_input)

                elif game.state["current"] == game.config.STATE_GAME_OVER:
                    restart_button = pygame.Rect(
                        screen_width // 2 - 220,
                        350,
                        200,
                        50
                    )
                    menu_button = pygame.Rect(
                        screen_width // 2 + 20,
                        350,
                        200,
                        50
                    )

                    if restart_button.collidepoint(mouse_pos):
                        game.reset()
                    elif menu_button.collidepoint(mouse_pos):
                        game.state["current"] = game.config.STATE_START

                elif game.state["current"] == game.config.STATE_LEVEL_COMPLETE:
                    continue_button = pygame.Rect(
                        screen_width // 2 - 100,
                        350,
                        200,
                        50
                    )
                    if continue_button.collidepoint(mouse_pos):
                        game.next_level()

            # Handle UI events
            ui.handle_events(event)

        # Update game
        game.update(current_time)

        # Draw everything
        screen.fill(game.config.COLORS["BLACK"])

        if game.state["current"] == game.config.STATE_START:
            ui.draw_start_screen()

        elif game.state["current"] in [game.config.STATE_PLAYING,
                                       game.config.STATE_LEVEL_COMPLETE,
                                       game.config.STATE_GAME_OVER]:
            # Draw game background
            ui.draw_background()

            # Draw game elements
            game.level_manager.draw_homes(screen)
            game.obstacle_manager.draw(screen)
            game.player.draw(screen)

            # Draw game info
            ui.draw_game_info(game.get_game_state())

            # Draw overlay screens
            if game.state["current"] == game.config.STATE_GAME_OVER:
                ui.draw_game_over_screen(game.get_game_state())
            elif game.state["current"] == game.config.STATE_LEVEL_COMPLETE:
                ui.draw_level_complete_screen()
            elif game.state["is_paused"]:
                ui.draw_pause_screen()

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(game.config.FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()