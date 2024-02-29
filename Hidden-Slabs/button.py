import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        super().__init__()
        self.image_idle = pygame.image.load("assets/" + file + "_button.png")
        self.image_mouse_on = pygame.image.load("assets/" + file + "_button(mouse_on).png")
        self.image_press = pygame.image.load("assets/" + file + "_button(press).png")
        self.image = self.image_idle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def re_size(self, w, h):
        self.image_idle = pygame.transform.scale(self.image_idle, (w, h))
        self.image_mouse_on = pygame.transform.scale(self.image_mouse_on,
                                                  (w, h))
        self.image_press = pygame.transform.scale(self.image_press, (w, h))
        self.image = self.image_idle
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y