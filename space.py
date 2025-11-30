from screen import Screen
from gameplay import Gameplay
from menu import Menu
from spaceship import Spaceship
import pygame
import enum


class Space(object):
    class GameState(enum.Enum):
        MENU = 0
        PLAYING = 1
        GAME_OVER = 2
        VICTORY = 3

    def __init__(self):
        # Initialization
        pygame.init()
        self.clock = pygame.time.Clock()

        # Screen class holds the actual window and whatever is in the background, like stars and planets
        self.screen = Screen()

        # The Gameplay class holds the main game business logic
        self.game = None

        # Menu system
        self.menu = Menu(self.screen)

        # Caption and icon
        pygame.display.set_caption("Space")
        pic_logo = pygame.image.load("res/spaceship_N_00.png")
        pygame.display.set_icon(pic_logo)

        # Start running :)
        self.running = True

        # Start in menu state
        self.game_state = self.GameState.MENU

    def quit(self):
        """
        Getting here will cause the game loop to end
        """
        self.running = False

    def start_game(self):
        """
        Initialize and start a new game
        """
        Spaceship.reset()
        self.game = Gameplay(self, self.screen)
        self.game.initialize_level()
        self.game_state = self.GameState.PLAYING

    def game_over(self):
        """
        Transition to game over state
        """
        self.game_state = self.GameState.GAME_OVER
        self.menu.reset_animation()

    def victory(self):
        """
        Transition to victory state
        """
        self.game_state = self.GameState.VICTORY
        self.menu.reset_animation()

    def return_to_menu(self):
        """
        Return to main menu
        """
        self.game_state = self.GameState.MENU
        self.menu.selected_option = 0

    def handle_menu_events(self):
        """
        Handle events when in menu state
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                elif event.key == pygame.K_UP:
                    self.menu.move_selection_up()
                elif event.key == pygame.K_DOWN:
                    self.menu.move_selection_down()
                elif event.key == pygame.K_RETURN:
                    selected = self.menu.get_selected_option()
                    if selected == "Start Game":
                        self.start_game()
                    elif selected == "Exit":
                        self.quit()

    def handle_end_screen_events(self):
        """
        Handle events when in game over or victory state
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                elif event.key == pygame.K_RETURN:
                    self.return_to_menu()

    def main(self):
        """
        Main game loop lives here
        """

        while self.running:
            # Make sure the game pace is steady
            self.clock.tick(60)

            # Handle events based on game state
            if self.game_state == self.GameState.MENU:
                self.handle_menu_events()
            elif self.game_state == self.GameState.PLAYING:
                self.game.handle_events()
                self.game.run()
            elif self.game_state in [self.GameState.GAME_OVER, self.GameState.VICTORY]:
                self.handle_end_screen_events()

            # Draw based on game state
            self.screen.draw()
            if self.game_state == self.GameState.MENU:
                self.menu.draw_main_menu()
            elif self.game_state == self.GameState.PLAYING:
                self.game.draw()
            elif self.game_state == self.GameState.GAME_OVER:
                self.menu.draw_game_over(self.game.player.get_score())
            elif self.game_state == self.GameState.VICTORY:
                self.menu.draw_victory(self.game.player.get_score())

            # Update the display
            pygame.display.update()


if __name__ == '__main__':
    space = Space()
    space.main()
