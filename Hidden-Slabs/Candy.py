import pygame

class Candy(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("assets/Candy.png")
        self.image = pygame.transform.scale(self.image, (self.game.SLAB_SIZE*0.7, self.game.SLAB_SIZE*0.7))
        self.rect = self.image.get_rect()
        self.start_x = self.game.screen.get_width() / 2 - self.rect.width/2
        self.start_y = 20
        self.rect.x = self.start_x
        self.rect.y = self.start_y