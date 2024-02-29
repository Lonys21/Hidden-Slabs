import pygame
from game import GameTimer, GameSimple
from button import Button
from tuto import Tuto

class Menu:
    def __init__(self, screen, FPS):
        self.init_finish = False
        self.screen = screen
        self.FPS = FPS
        self.games = []

        # font
        self.FONT_SIZE = 20
        self.FONT_COLOR = (200, 10, 10)
        self.font = pygame.font.SysFont("Arial", self.FONT_SIZE)

        # font_win
        self.FONT_WIN_X = 250
        self.FONT_WIN_Y = 400
        self.FONT_WIN_COLOR = (500, 500, 500)
        self.font_win = pygame.font.SysFont("Arial", 50)

        # Buttons Constants
        self.MENU_BUTTON_SIMPLEMODE_Y = 170
        self.MENU_BUTTON_SPECIALMODE_Y = 650

        # welcome screen buttons
        self.welcome_button_y = 485
        self.welcome_button_size = 250
        self.welcome_buttons = pygame.sprite.Group()
        self.welcome_button_menu = Button("menu", 100, self.welcome_button_y)
        self.welcome_button_tutoriel = Button("tuto", 625, self.welcome_button_y)
        self.welcome_buttons.add(self.welcome_button_menu, self.welcome_button_tutoriel)
        for b in self.welcome_buttons:
            b.re_size(self.welcome_button_size, self.welcome_button_size)

        # Menu Buttons
        self.menu_buttons = pygame.sprite.Group()
        self.easy_button = Button("easy", 55, self.MENU_BUTTON_SIMPLEMODE_Y)
        self.medium_button = Button("medium", 365, self.MENU_BUTTON_SIMPLEMODE_Y)
        self.hard_button = Button("hard", 675, self.MENU_BUTTON_SIMPLEMODE_Y)
        self.timer_button = Button("timer", self.screen.get_width()/2-self.easy_button.rect.width/2, self.MENU_BUTTON_SPECIALMODE_Y)
        self.menu_buttons.add(self.easy_button, self.medium_button, self.hard_button, self.timer_button)

        # Screen
        self.actual_screen = "welcome"
        self.background_color = "darkgreen"
        self.menu_background = pygame.image.load("assets/menu_screen.png")

        # Welcome screen
        self.welcome_screen = pygame.image.load("assets/welcome_screen.png")

        # Tuto
        self.tuto = Tuto(self)

        # Win screen mode
        self.font_mode_size = 75
        self.font_mode = pygame.font.SysFont('Libre Baskerville', self.font_mode_size)
        self.font_mode_color = "black"
        self.menu_button = Button("menu", 350, 600)

        # Win screen simple mode
        self.win_screen_simple_mode = pygame.image.load("assets/win_screen.png")
        self.font_simple_mode_x = 390
        self.font_simple_mode_y = 237

        # win screen timer mode
        self.candy_marge = 40
        self.candy_y = 315
        self.num_candies_per_row = 10
        self.win_screen_timer_no_candy = pygame.image.load('assets/win_screen_timer_mode3.png')
        self.win_screen_timer_one_candy = pygame.image.load('assets/win_screen_timer_mode2.png')
        self.win_screen_timer_some_candy = pygame.image.load('assets/win_screen_timer_mode1.png')
        self.font_timer_mode_x = 368
        self.font_timer_mode_y = 249

        self.init_finish = True


    def launch(self, mode, rows, cols,  plaform_size=140,):
        # Create a game
        if mode == 'simple':
            self.games.append(GameSimple(self, self.screen, rows, cols, plaform_size))
        elif mode == "timer":
            self.games.append(GameTimer(self, self.screen, rows, cols, plaform_size))


    def update(self):
        self.screen.fill(self.background_color)
        if self.game_on():
            self.actual_game.update()
        elif self.actual_screen == "welcome":
            self.screen.blit(self.welcome_screen, (0, 0))
            for b in self.welcome_buttons:
                self.screen.blit(b.image, (b.rect.x, b.rect.y))
        elif self.actual_screen == "tuto":
            self.screen.blit(self.tuto.actual_screen, (0, 0))
            self.screen.blit(self.tuto.next_button.image, (self.tuto.next_button.rect.x, self.tuto.next_button.rect.y))
        elif self.actual_screen == "menu":
            self.screen.blit(self.menu_background, (0, 0))
            for button in self.menu_buttons:
                self.screen.blit(button.image, (button.rect.x, button.rect.y))
        elif self.actual_screen == "win":
            self.screen.blit(self.win_screen_simple_mode, (0, 0))
            self.screen.blit(self.font_mode.render(str(self.actual_game.deads), True, self.font_mode_color),
                             (self.font_simple_mode_x-self.actual_game.update_font_size(self.actual_game.deads, self.font_mode_size), self.font_simple_mode_y))
            self.screen.blit(self.menu_button.image, (self.menu_button.rect.x, self.menu_button.rect.y))
        elif self.actual_screen == "loose":
            self.print_loose_screen()
            self.screen.blit(self.menu_button.image, (self.menu_button.rect.x, self.menu_button.rect.y))


    def print_loose_screen(self):
        if self.actual_game.complete_level == 0:
            self.screen.blit(self.win_screen_timer_no_candy, (0, 0))
        elif self.actual_game.complete_level == 1:
            self.screen.blit(self.win_screen_timer_one_candy, (0, 0))
        else:
            self.screen.blit(self.win_screen_timer_some_candy, (0, 0))
            self.screen.blit(self.font_mode.render(str(self.actual_game.complete_level), True, self.font_mode_color), (self.font_timer_mode_x-self.actual_game.update_font_size(self.actual_game.complete_level, self.font_mode_size), self.font_timer_mode_y))
            self.print_candies()

    def print_candies(self):
        candy_start_y = self.candy_y
        candy_y = self.candy_y
        for i in range(self.actual_game.complete_level):
            if i / self.num_candies_per_row >= 1 or i == 0:
                if i % self.num_candies_per_row == 0:
                    if self.actual_game.complete_level-i >= self.num_candies_per_row:
                        candy_x = self.calcul_candy_start_x(self.num_candies_per_row)
                    else:
                        candy_x = self.calcul_candy_start_x(self.actual_game.complete_level-i)
                candy_y = candy_start_y + self.candy_marge * int(i/10)
            self.screen.blit(self.actual_game.candy.image, (candy_x, candy_y))
            candy_x += self.candy_marge

    def calcul_candy_start_x(self, num_candies):
        candies_width = (self.candy_marge * (num_candies - 1) + self.actual_game.candy.rect.width)
        candy_start_x = self.screen.get_width() / 2 - candies_width / 2
        return candy_start_x

    def game_on(self):
        for g in self.games:
            if g.game_on:
                self.actual_game = g
                self.actual_screen = "game"
                return True
        return False
