import pygame
import random
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image_original = pygame.image.load("assets/Player.png")
        self.image_original = pygame.transform.scale(self.image_original, (self.game.SLAB_SIZE / 2, self.game.SLAB_SIZE / 2))
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.start_position()
        self.velocity = self.game.SLAB_SIZE


    def start_position(self):
        self.start_x = (self.game.map_width / 2 - self.rect.width / 2,
                        self.game.PLATFORM_SIZE + self.game.SLAB_SIZE * self.game.SLAB_COLS / 2 + self.rect.width / 2,
                        self.game.PLATFORM_SIZE + self.game.SLAB_SIZE * self.game.SLAB_COLS / 2 + self.rect.width / 2 - self.game.SLAB_SIZE
                        )
        self.start_y = self.game.map_height - self.game.PLATFORM_SIZE + self.game.SLAB_SIZE / 2 - self.rect.height / 2
        if self.game.SLAB_COLS % 2 == 1:
            self.rect.x = self.start_x[0]
        else:
            r = random.randint(1, 2)
            self.rect.x = self.start_x[r]
        self.rect.y = self.start_y
        self.image = self.image_original

    def move_right(self):
        if self.rect.x + self.rect.width + self.velocity < self.game.map_width - self.game.PLATFORM_SIZE:
            self.image = pygame.transform.rotate(self.image_original, -90)
            self.rect.x += self.velocity
    def move_left(self):
        if self.rect.x - self.velocity > self.game.PLATFORM_SIZE:
            self.image = pygame.transform.rotate(self.image_original, 90)
            self.rect.x -= self.velocity
    def move_up(self):
        if self.rect.y - self.velocity > 0:
            self.image = self.image_original
            self.rect.y -= self.velocity
    def move_down(self):
        if self.rect.y + self.rect.height +self.velocity<= self.game.map_height:
            self.image = pygame.transform.rotate(self.image_original, 180)
            self.rect.y += self.velocity