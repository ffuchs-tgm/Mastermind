class View:

    def __init__(self, pygame):
        self.pygame = pygame
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.CYAN = (0, 255, 255)
        self.MAGENTA = (255, 0, 255)
        self.GREY = (128, 128, 128)
        self.DARK_GREY = (96, 96, 96)
        self.SILVER = (192, 192, 192)
        self.colors = {'RED': (255, 0, 0), 'GREEN': (0, 255, 0), 'BLUE': (0, 0, 255), 'CYAN': (0, 255, 255),
                       'MAGENTA': (255, 0, 255), 'YELLOW': (255, 255, 0)}
        self.screen = pygame.display.set_mode((280, 620))
        self.screenWidth = self.screen.get_rect().width
        self.screenHeight = self.screen.get_rect().height
        self.numbers = []
        self.guesses = []
        self.remaining_guesses = 10
        self.current_guess = []
        self.hints = []
        self.selectableColors = {}
        self.confirm = 0
        self.selected_color = ""
        self.temp = []

    def create_ui(self):
        myfont = self.pygame.font.SysFont('Raleway', 50)
        textsurface = myfont.render('MASTERMIND', True, self.WHITE)

        self.screen.fill(self.DARK_GREY)

        # MASTERMIND text
        self.screen.blit(textsurface, (self.screenWidth / 2 - (textsurface.get_rect().width / 2), 10))

        # 4 Mysterious Dots
        for i in range(0, 4):
            self.pygame.draw.circle(self.screen, self.SILVER, ((int(self.screenWidth / 2) - 70) + 50 * i, 70), 20, 0)
        # Background rect
        self.pygame.draw.rect(self.screen, self.GREY, [0, 100, self.screenWidth, self.screenHeight - 100], 0)

        # 10 rows for payling field
        for i in range(0, 11):
            # Number rects
            self.numbers.append(self.pygame.draw.rect(self.screen, self.WHITE, [10, 110 + i * 40, 30, 30], 0))
            # 4 empty color selections for the guessing player
            for j in range(0, 4):
                self.temp.append(self.pygame.draw.circle(self.screen, self.SILVER, (70 + 50 * j, 125 + i * 40), 15, 0))
                # print(temp)
            # Border for the hints
            self.guesses.append(self.temp.copy())
            # print(guesses)
            self.temp.clear()
            self.pygame.draw.rect(self.screen, self.WHITE, [self.screenWidth - 35, 110 + i * 40, 30, 30], 1)
            # 4 hints from the mastermind to the guesser
            for j in range(0, 4):
                if j < 2:
                    self.temp.append(
                        self.pygame.draw.circle(self.screen, self.SILVER,
                                                (self.screenWidth - 27 + 14 * j, 118 + i * 40), 5,
                                                0))
                else:
                    self.temp.append(
                        self.pygame.draw.circle(self.screen, self.SILVER,
                                                (self.screenWidth - 27 + 14 * (j - 2), 132 + i * 40), 5, 0))
            self.hints.append(self.temp.copy())
            self.temp.clear()
        # 6 colors that can be selected
        self.selectableColors.update(
            {'RED': self.pygame.draw.circle(self.screen, self.RED,
                                            (int(self.screenWidth / 6) * 1 - 18, self.screenHeight - 55), 15, 0)})
        self.selectableColors.update(
            {'GREEN': self.pygame.draw.circle(self.screen, self.GREEN,
                                              (int(self.screenWidth / 6) * 2 - 18, self.screenHeight - 55), 15, 0)})
        self.selectableColors.update(
            {'BLUE': self.pygame.draw.circle(self.screen, self.BLUE,
                                             (int(self.screenWidth / 6) * 3 - 18, self.screenHeight - 55), 15, 0)})
        self.selectableColors.update(
            {'CYAN': self.pygame.draw.circle(self.screen, self.CYAN,
                                             (int(self.screenWidth / 6) * 4 - 18, self.screenHeight - 55), 15, 0)})
        self.selectableColors.update(
            {'MAGENTA': self.pygame.draw.circle(self.screen, self.MAGENTA,
                                                (int(self.screenWidth / 6) * 5 - 18, self.screenHeight - 55), 15, 0)})
        self.selectableColors.update(
            {'YELLOW': self.pygame.draw.circle(self.screen, self.YELLOW,
                                               (int(self.screenWidth / 6) * 6 - 18, self.screenHeight - 55), 15, 0)})
        # confirm button
        self.confirm = self.pygame.draw.rect(self.screen, self.WHITE,
                                             [10, self.screenHeight - 35, int(self.screenWidth / 2) - 15, 30], 0)
        # solve button
        self.solve = self.pygame.draw.rect(self.screen, self.WHITE,
                                           [int(self.screenWidth / 2) + 5, self.screenHeight - 35,
                                            int(self.screenWidth / 2) - 10,
                                            30], 0)

    def color_selected(self, pos):
        for c in self.colors:
            for _ in self.selectableColors:
                if self.selectableColors[c].collidepoint(pos):
                    self.selected_color = c
        print(self.selected_color)

    def pin_entered(self, pos):
        for color in self.guesses[self.remaining_guesses]:
            if color.collidepoint(pos):
                if self.selected_color != "":
                    self.pygame.draw.circle(self.screen, self.colors[self.selected_color],
                                            (color.left + 15, color.top + 15), 15)