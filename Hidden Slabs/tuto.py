import pygame
from button import Button

class Tuto:
    def __init__(self, menu):
        self.menu = menu
        self.tutos_num = 14
        self.tutos_screens = []
        for s in range(1, self.tutos_num + 1):
            tuto = pygame.image.load("assets/tuto/Tuto" + str(s) + ".png")
            self.tutos_screens.append(tuto)
        self.screen_id = 0
        self.actual_screen = self.tutos_screens[self.screen_id]

        # Next button
        self.next_button = Button("next", 0, 0)
        self.next_button_width = 200
        self.next_button_height = 120
        self.next_button.re_size(self.next_button_width, self.next_button_height)
        self.next_button.rect.x = self.menu.screen.get_width() - self.next_button_width - 15
        self.next_button.rect.y = self.menu.screen.get_height() - self.next_button_height - 15

    def next(self):
        self.screen_id += 1
        if not self.screen_id == len(self.tutos_screens):
            self.actual_screen = self.tutos_screens[self.screen_id]
        else:
            self.menu.actual_screen = 'menu'




