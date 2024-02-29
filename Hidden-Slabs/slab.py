import pygame
import random

class Slab(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        num = random.randint(0, 1)
        if num == 1:
            self.num_image = random.randint(1, 3)
        else:
            self.num_image = ""
        self.image1 = pygame.image.load("assets/Slab" + str(self.num_image) + ".png")
        self.image1 = pygame.transform.scale(self.image1, (self.game.SLAB_SIZE, self.game.SLAB_SIZE))
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos_x = [i for i in range(self.rect.x, self.rect.x + self.rect.width)]
        self.pos_y = [i for i in range(self.rect.y, self.rect.y + self.rect.width)]
        self.first_down = True
        self.first_up = False

        # Timer
        self.timer = 95
        self.dead_timer = 0

    def up(self):
        self.image = self.image1


    def down(self):
        self.image = self.image2


    def player_above(self):
        if self.game.player.rect.x in self.pos_x and self.game.player.rect.y in self.pos_y and self.game.player.rect.x in self.pos_x and self.game.player.rect.y + self.game.player.rect.width in self.pos_y and self.game.player.rect.x + self.game.player.rect.width in self.pos_x and self.game.player.rect.y in self.pos_y and self.game.player.rect.x + self.game.player.rect.width in self.pos_x and self.game.player.rect.y + self.game.player.rect.width in self.pos_y:
            return True
        return False


class FakeSlab(Slab):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image2 = pygame.image.load("assets/fakeslab" + str(self.num_image) + ".png")
        self.image2 = pygame.transform.scale(self.image2, (self.game.SLAB_SIZE, self.game.SLAB_SIZE))
        self.nature = "fake"


class TrueSlab(Slab):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image2 = pygame.image.load("assets/trueslab" + str(self.num_image) + ".png")
        self.image2 = pygame.transform.scale(self.image2, (self.game.SLAB_SIZE, self.game.SLAB_SIZE))
        self.nature = "true"

