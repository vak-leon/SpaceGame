import pygame
from const import Const
from time import perf_counter as clock


class Menu:
    """
    Menu system for game start, game over, and victory screens
    """

    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font("res/PixelEmulator-xq08.ttf", 48)
        self.font_menu = pygame.font.Font("res/PixelEmulator-xq08.ttf", 32)
        self.font_subtitle = pygame.font.Font("res/PixelEmulator-xq08.ttf", 24)

        # Menu options
        self.menu_options = ["Start Game", "Exit"]
        self.selected_option = 0

        # Animation for game over / victory
        self.animation_time = 0
        self.animation_y_offset = 0
        self.animation_started = False

    def reset_animation(self):
        """Reset animation for game over/victory screens"""
        self.animation_started = False
        self.animation_time = clock()
        self.animation_y_offset = -200  # Start from above screen

    def move_selection_up(self):
        """Move menu selection up"""
        self.selected_option = (self.selected_option - 1) % len(self.menu_options)

    def move_selection_down(self):
        """Move menu selection down"""
        self.selected_option = (self.selected_option + 1) % len(self.menu_options)

    def get_selected_option(self):
        """Return the currently selected menu option"""
        return self.menu_options[self.selected_option]

    def draw_main_menu(self):
        """Draw the main menu screen"""
        # Draw title
        title = self.font_title.render("SPACE GAME", True, Const.COLOR_WHITE)
        title_width, title_height = title.get_rect().size
        title_x = (Const.SCREEN_WIDTH - title_width) / 2
        title_y = Const.SCREEN_HEIGHT / 4
        self.screen.window.blit(title, (title_x, title_y))

        # Draw menu options
        menu_start_y = Const.SCREEN_HEIGHT / 2
        for i, option in enumerate(self.menu_options):
            # Highlight selected option
            if i == self.selected_option:
                color = Const.COLOR_RED
                prefix = "> "
            else:
                color = Const.COLOR_WHITE
                prefix = "  "

            option_text = self.font_menu.render(prefix + option, True, color)
            option_width, option_height = option_text.get_rect().size
            option_x = (Const.SCREEN_WIDTH - option_width) / 2
            option_y = menu_start_y + i * (option_height + 20)
            self.screen.window.blit(option_text, (option_x, option_y))

    def draw_game_over(self, score):
        """Draw the game over screen with animation"""
        if not self.animation_started:
            self.reset_animation()
            self.animation_started = True

        # Animate the "GAME OVER" text falling down
        elapsed = clock() - self.animation_time
        if elapsed < 2.0:  # Animation duration
            # Ease-out animation
            progress = min(1.0, elapsed / 2.0)
            self.animation_y_offset = -200 + (Const.SCREEN_HEIGHT / 3 + 200) * (progress ** 2)
        else:
            self.animation_y_offset = Const.SCREEN_HEIGHT / 3

        # Draw "GAME OVER" text
        game_over_text = self.font_title.render("GAME OVER", True, Const.COLOR_RED)
        text_width, text_height = game_over_text.get_rect().size
        text_x = (Const.SCREEN_WIDTH - text_width) / 2
        self.screen.window.blit(game_over_text, (text_x, self.animation_y_offset))

        # Draw score below after animation settles
        if elapsed > 1.5:
            score_text = self.font_subtitle.render(f"Final Score: {str(score).zfill(6)}", True, Const.COLOR_WHITE)
            score_width, score_height = score_text.get_rect().size
            score_x = (Const.SCREEN_WIDTH - score_width) / 2
            score_y = self.animation_y_offset + text_height + 40
            self.screen.window.blit(score_text, (score_x, score_y))

        # Draw "Press ENTER to continue" after animation completes
        if elapsed > 2.5:
            continue_text = self.font_subtitle.render("Press ENTER to continue", True, Const.COLOR_WHITE)
            continue_width, continue_height = continue_text.get_rect().size
            continue_x = (Const.SCREEN_WIDTH - continue_width) / 2
            continue_y = Const.SCREEN_HEIGHT - Const.SCREEN_HEIGHT / 4
            self.screen.window.blit(continue_text, (continue_x, continue_y))

    def draw_victory(self, score):
        """Draw the victory screen with animation"""
        if not self.animation_started:
            self.reset_animation()
            self.animation_started = True

        # Animate the "VICTORY!" text falling down
        elapsed = clock() - self.animation_time
        if elapsed < 2.0:  # Animation duration
            # Ease-out animation with a bounce
            progress = min(1.0, elapsed / 2.0)
            target_y = Const.SCREEN_HEIGHT / 3
            self.animation_y_offset = -200 + (target_y + 200) * (progress ** 2)
            # Add a small bounce effect
            if progress > 0.8:
                bounce = 20 * (1 - progress) / 0.2
                self.animation_y_offset += bounce
        else:
            self.animation_y_offset = Const.SCREEN_HEIGHT / 3

        # Draw "VICTORY!" text with a golden color
        victory_color = (255, 215, 0)  # Gold color
        victory_text = self.font_title.render("VICTORY!", True, victory_color)
        text_width, text_height = victory_text.get_rect().size
        text_x = (Const.SCREEN_WIDTH - text_width) / 2
        self.screen.window.blit(victory_text, (text_x, self.animation_y_offset))

        # Draw score below after animation settles
        if elapsed > 1.5:
            score_text = self.font_subtitle.render(f"Final Score: {str(score).zfill(6)}", True, Const.COLOR_WHITE)
            score_width, score_height = score_text.get_rect().size
            score_x = (Const.SCREEN_WIDTH - score_width) / 2
            score_y = self.animation_y_offset + text_height + 40
            self.screen.window.blit(score_text, (score_x, score_y))

            congrats_text = self.font_subtitle.render("You saved the galaxy!", True, Const.COLOR_WHITE)
            congrats_width, congrats_height = congrats_text.get_rect().size
            congrats_x = (Const.SCREEN_WIDTH - congrats_width) / 2
            congrats_y = score_y + score_height + 20
            self.screen.window.blit(congrats_text, (congrats_x, congrats_y))

        # Draw "Press ENTER to continue" after animation completes
        if elapsed > 2.5:
            continue_text = self.font_subtitle.render("Press ENTER to continue", True, Const.COLOR_WHITE)
            continue_width, continue_height = continue_text.get_rect().size
            continue_x = (Const.SCREEN_WIDTH - continue_width) / 2
            continue_y = Const.SCREEN_HEIGHT - Const.SCREEN_HEIGHT / 4
            self.screen.window.blit(continue_text, (continue_x, continue_y))
