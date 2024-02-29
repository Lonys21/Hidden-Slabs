import pygame

class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.camera = pygame.Rect(0, 0, width, height)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def draw(self, surface, group):
        for sprite in group:
            surface.blit(sprite.image, self.apply(sprite))

    def update(self, target):
        x = 0
        if target.rect.y - self.game.screen.get_height()/2 <= 0:
            y = 0
        elif target.rect.y < self.game.map_height - self.game.screen.get_height() / 2:
            y = int(self.game.screen.get_height() / 2) - target.rect.centery
        else:
            y = -(self.game.map_height - self.game.screen.get_height())
        self.camera = pygame.Rect(x, y, self.width, self.height)