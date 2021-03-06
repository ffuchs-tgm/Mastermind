# Import the pygame library and initialise the game engine
import pygame as pg
from mastermind import Mastermind
from view import View


class Controller(object):

    def __init__(self):
        self.pygame = pg
        self.mastermind = None
        self.view = None
        self.playing = None
        self.carryOn = None

    def setup(self):
        self.pygame.init()
        self.pygame.font.init()
        self.pygame.display.set_caption("TGMastermind!")
        self.mastermind = Mastermind(self)
        self.view = View(self)
        self.playing = True
        self.carryOn = True

    def run_game(self):
        # The clock will be used to control how fast the screen updates
        clock = self.pygame.time.Clock()
        # -------- Main Program Loop -----------
        while self.carryOn:
            # --- Main event loop
            for event in self.pygame.event.get():  # User did something
                if event.type == self.pygame.QUIT:  # If user clicked close
                    self.carryOn = False  # Flag that we are done so we exit this loop
                #print(self.playing)
                if self.playing:
                    self.view.confirm.handle_event(event)
                    self.view.solve.handle_event(event)
                    if event.type == self.pygame.MOUSEBUTTONUP:
                        pos = self.pygame.mouse.get_pos()
                        # Color selection
                        self.view.color_selected(pos)
                        # entering a colored pin
                        self.view.pin_entered(pos)
                elif not self.view.restart:
                    self.view.give_restart_option()
                    self.view.confirm = None
                    self.view.restart.handle_event(event)
                else:
                    self.view.restart.handle_event(event)
                    # if self.view.confirm.collidepoint(pos):
                    #
                    #if self.view.solve.collidepoint(pos):
                        #colors = self.mastermind.solve_mystery()
                        #self.view.solve_mystery(colors)

                # --- Game logic should go here

                # --- Drawing code should go here
                # First, clear the screen to white.
            if self.view.restart:
                self.view.restart.update()
            else:
                self.view.confirm.update()
            self.view.solve.update()


            # --- Go ahead and update the screen with what we've drawn.
            if self.carryOn:
                self.pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)
        # Once we have exited the main program loop we can stop the game engine:
        self.pygame.quit()

    def confirm_guess(self):
        hints = self.mastermind.check_input(self.view.current_guess)
        if hints != "WIN":
            self.view.add_hints(hints)

    def solve_mystery(self):
        self.playing = False
        colors = self.mastermind.solve_mystery()
        self.view.solve_mystery(colors)

    def guesser_won(self):
        self.playing = False
        self.view.add_hints(['BLACK', 'BLACK', 'BLACK', 'BLACK'])
        self.view.display_guesser_won(self.mastermind.solve_mystery())

    def guesser_lost(self):
        self.playing = False
        self.view.display_guesser_lost(self.mastermind.solve_mystery())

    def restart(self):
        self.carryOn = False
        self.setup()
        self.view.create_ui()
        self.run_game()
