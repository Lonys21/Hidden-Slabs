import pygame
from player import Player
from slab import TrueSlab, FakeSlab
from Candy import Candy
from camera import Camera
import random

class Game:
    def __init__(self, menu, screen, rows, cols, platform_size):
        self.menu = menu
        self.screen = screen
        self.PLATFORM_SIZE = platform_size
        self.SLAB_ROWS = rows
        self.SLAB_COLS = cols
        self.SLAB_SIZE_MIN = 100
        self.SLAB_SIZE = (self.screen.get_width()-2*self.PLATFORM_SIZE)/self.SLAB_COLS
        self.SLAB_SHINE = self.menu.FPS*2.5
        self.DEAD_TIMER = self.menu.FPS*0.3

        # Map
        self.map_width = self.screen.get_width()
        self.map_height = self.SLAB_SIZE * self.SLAB_ROWS + self.PLATFORM_SIZE * 2


        # PLayer
        self.players = pygame.sprite.Group()
        self.player = Player(self)
        self.players.add(self.player)
        self.deads = 0
        self.player_dead = False

        # Camera
        self.camera = Camera(self, 1, 1)

        # Slabs
        self.slabs = pygame.sprite.Group()

        # Candy
        self.candies = pygame.sprite.Group()
        self.candy = Candy(self)
        self.candies.add(self.candy)

        # Gauge
        self.GAUGE_WIDTH = 25
        self.GAUGE_HEIGHT = 550
        self.GAUGE_MAX = self.GAUGE_HEIGHT*0.95
        self.GAUGE_BACK_COLOR = (0, 0, 0)
        self.GAUGE_FILLED_COLOR = (77, 251, 17)
        self.GAUGE_BESTFILLING_COLOR = (238, 185, 17)
        self.gauge_best_filling = 0
        self.gauge_filled = 0
        self.gauge_filled_percent = 0

        # decoration
        self.NUM_DECORATION = 50
        self.decorations_names = [('rock', 45), ('flower1', 50), ('flower2', 50)]
        self.decoration_size = 55
        self.decorations_object = pygame.sprite.Group()

        # launch
        self.start()



    def start(self):
        self.game_on = True

        # Platform
        self.platforms = pygame.sprite.Group()
        self.platorm_top = Platform(self, 0)
        self.platform_bottom = Platform(self, self.map_height - self.PLATFORM_SIZE)
        self.platforms.add(self.platorm_top, self.platform_bottom)


        # slabs
        self.grid = [0 for i in range(self.SLAB_ROWS * self.SLAB_COLS)]
        self.slabs = pygame.sprite.Group()
        self.set_patern()
        self.slab_generation()

        # gauge
        self.gauge_best_filling = 0
        self.gauge_filled = 0
        self.gauge_filled_percent = 0

        # decor
        self.decorations_object = pygame.sprite.Group()
        self.y_available = [i for i in
                            range(self.PLATFORM_SIZE, int(self.map_height))[::int(self.decoration_size * 1.5)]]
        self.x_list1 = [i for i in range(0, self.PLATFORM_SIZE - self.decoration_size - 2)[::15]]
        self.x_list2 = [i for i in range(self.map_width - self.PLATFORM_SIZE, self.map_width - self.decoration_size)[::15]]
        self.decoration_generation(self.y_available, self.x_list1)
        self.decoration_generation(self.y_available, self.x_list2)


    def set_patern(self):
        self.patern = self.grid[::]
        for i in range(self.SLAB_ROWS)[::2]:
            n = random.randint(0, self.SLAB_COLS-1)
            self.patern[i*self.SLAB_COLS+n] = 1

        self.patern_index = []
        for k in range(len(self.patern)):
            if self.patern[k] == 1:
                self.patern_index.append(k)
        for k in range(len(self.patern_index)-1):
            if self.patern_index[k]%self.SLAB_COLS < self.patern_index[k+1]%self.SLAB_COLS:
                for d in range(self.patern_index[k]+self.SLAB_COLS, self.patern_index[k+1]-self.SLAB_COLS+1):
                    self.patern[d] = 1
            elif self.patern_index[k]%self.SLAB_COLS > self.patern_index[k+1]%self.SLAB_COLS:
                for d in range(self.patern_index[k+1]-self.SLAB_COLS, self.patern_index[k]+self.SLAB_COLS+1):
                    self.patern[d] = 1
            elif self.patern_index[k]%self.SLAB_COLS == self.patern_index[k+1]%self.SLAB_COLS:
                self.patern[self.patern_index[k]+self.SLAB_COLS] = 1

        if self.SLAB_ROWS%2 == 0:
            self.patern[self.patern_index[-1]+self.SLAB_COLS]=1


    def update(self):
        self.screen.fill("darkgreen")

        # Slab
        for s in self.slabs:
            if s.player_above():
                s.down()
                if s.nature == "fake":
                    if s.dead_timer >= self.DEAD_TIMER:
                        self.replay()
                        s.dead_timer = 0
                        self.deads += 1
                    else:
                        s.dead_timer += 1
                        self.player_dead = True
                else:
                    s.timer = 0

            elif not s.player_above():
                if s.timer > self.SLAB_SHINE:
                    s.up()
                else:
                    s.timer += 1

        # Camera
        self.camera.update(self.player)
        self.camera.draw(self.screen, self.decorations_object)
        self.camera.draw(self.screen, self.platforms)
        self.camera.draw(self.screen, self.slabs)
        self.camera.draw(self.screen, self.players)
        self.camera.draw(self.screen, self.candies)


        # Gauges
        if not self.player_dead:
            self.gauge_filled_percent = (self.map_height - self.player.rect.y) / self.map_height * 100
            self.gauge_filled = self.gauge_filled_percent * (self.GAUGE_HEIGHT / 100)
        if self.gauge_filled > self.gauge_best_filling:
            self.gauge_best_filling = self.gauge_filled
        if self.gauge_filled < 20:
            self.gauge_filled = 20
        self.gauge_back = pygame.draw.rect(self.screen, self.GAUGE_BACK_COLOR,
                                     (self.map_width - self.PLATFORM_SIZE / 2 - self.GAUGE_WIDTH, self.screen.get_height()*1/4, self.GAUGE_WIDTH, self.GAUGE_HEIGHT))
        self.gauge_filled_rect = pygame.draw.rect(self.screen, self.GAUGE_FILLED_COLOR,
                                      (self.map_width - self.PLATFORM_SIZE / 2 - self.GAUGE_WIDTH*3/4,
                                       self.screen.get_height()*1/4 + 14, self.GAUGE_WIDTH*0.5, self.GAUGE_MAX))
        if not self.gauge_filled == self.gauge_best_filling:
            self.gauge_best_filling_rect = pygame.draw.rect(self.screen, self.GAUGE_BESTFILLING_COLOR,
                                                 (self.map_width - self.PLATFORM_SIZE / 2 - self.GAUGE_WIDTH * 3 / 4,
                                                  self.screen.get_height() * 1 / 4 + 14, self.GAUGE_WIDTH * 0.5,
                                                  self.GAUGE_HEIGHT-self.gauge_filled))
        self.gauge_front = pygame.draw.rect(self.screen, self.GAUGE_BACK_COLOR,
                                           (self.map_width - self.PLATFORM_SIZE / 2 - self.GAUGE_WIDTH,
                                            self.screen.get_height() * 1 / 4, self.GAUGE_WIDTH, self.GAUGE_HEIGHT-self.gauge_best_filling))



    def slab_generation(self):
        c = 0
        r = 0
        for p in self.patern:
            if p == 1:
                self.slabs.add(
                    TrueSlab(self, c * self.SLAB_SIZE + self.PLATFORM_SIZE, r * self.SLAB_SIZE + self.PLATFORM_SIZE))
            elif p == 0:
                self.slabs.add(
                    FakeSlab(self, c * self.SLAB_SIZE + self.PLATFORM_SIZE, r * self.SLAB_SIZE + self.PLATFORM_SIZE))
            if c == self.SLAB_COLS - 1:
                c = 0
                r += 1
            else:
                c += 1

    def decoration_generation(self, y_available, x_list):
        x_ = 0
        decoration_ = ''
        decoration = ''
        for y in y_available:
            while decoration == decoration_:
                decoration = random.choice(self.decorations_names)
            x = random.choice(x_list)
            if x_ == x:
                x += self.decoration_size*2
            x_ = x
            decoration_ = decoration
            self.decorations_object.add(Decoration(self, decoration, x, y))



    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def replay(self):
        self.screen.fill("black")
        pygame.display.flip()
        self.player.start_position()
        self.player_dead = False

    def update_font_size(self, value, font_size):
        add_font_x = 0
        add_font_x += len(str(value))*font_size/3 - font_size/3
        return add_font_x


class GameSimple(Game):
    def __init__(self, menu, screen, rows, cols, platform_size):
        super().__init__(menu, screen, rows, cols, platform_size)
        # Deads
        self.deads = 0
        self.FONT_SIZE = 50
        self.font = pygame.font.SysFont("Arial", self.FONT_SIZE)
        self.font_x = 55
        self.font_y = 370
        self.tombstone = pygame.image.load("assets/tombstone.png")





    def update(self):
        super().update()

        # Candy
        if self.check_collision(self.player, self.candies):
            self.game_on = False
            self.menu.actual_screen = 'win'

        # Decor
        self.screen.blit(self.tombstone, (0, 350))

        # Text
        self.screen.blit(self.font.render(str(self.deads), 0, "darkgray"), (self.font_x-self.update_font_size(self.deads, self.FONT_SIZE), self.font_y))
class GameTimer(Game):
    def __init__(self, menu, screen, rows, cols, platform_size):
        super().__init__(menu, screen, rows, cols, platform_size)
        # Timer
        self.NEXT_LEVEL = 2
        self.augmentation = 2
        self.START_TIMER = self.menu.FPS * 60
        self.timer = self.START_TIMER
        self.complete_level = 0

        # Clock
        self.clock = pygame.image.load('assets/clock.png')
        self.clock = pygame.transform.scale(self.clock, (180, 240))
        self.FONT_SIZE = 30
        self.font = pygame.font.SysFont("Arial", self.FONT_SIZE)
        self.font_x = 68
        self.font_y = 440

        # Candy
        self.candy_x = 40
        self.candy_y = 200
        self.font_candy_x = self.candy_x + 22
        self.font_candy_y = self.candy_y + 12
    def update(self):
        super().update()
        if self.check_collision(self.player, self.candies):
            self.game_on = False
        if not self.game_on:
            self.complete_level += 1
            if self.complete_level % self.NEXT_LEVEL == 0 and self.complete_level != 0:
                self.SLAB_ROWS += self.augmentation
            self.start()
            self.timer = self.START_TIMER
        else:
            self.timer -= 1
            if self.timer <= 0:
                self.menu.actual_screen = "loose"
                self.game_on = False

        # Clock
        self.screen.blit(self.clock, (-15, 400))
        color = 'black'
        if self.timer < self.menu.FPS*15:
            color = "red"
        self.screen.blit(self.font.render(str(int(self.timer/self.menu.FPS)), 0, color), (self.font_x-self.update_font_size(int(self.timer/self.menu.FPS), self.FONT_SIZE), self.font_y))

        # Candy
        self.screen.blit(pygame.transform.scale(self.candy.image,(self.candy.image.get_width()*0.8, self.candy.image.get_height()*0.8)), (self.candy_x, self.candy_y))
        self.screen.blit(self.font.render(str(self.complete_level), 0, "black"), (self.font_candy_x-self.update_font_size(self.complete_level, self.FONT_SIZE), self.font_candy_y))

    def start(self):
        # Map
        self.map_height = self.SLAB_SIZE * self.SLAB_ROWS + self.PLATFORM_SIZE * 2
        super().start()
        # player
        self.player.start_position()

class Platform(pygame.sprite.Sprite):
    def __init__(self, game, y):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("assets/Platform.png")
        self.image = pygame.transform.scale(self.image, (1000, self.game.PLATFORM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y

class Decoration(pygame.sprite.Sprite):
    def __init__(self, game, decor, x, y):
        super().__init__()
        self.game = game
        self.angles = [i for i in range(-30, 30)]
        self.add_scale = random.randint(-10, 20)
        self.image = pygame.image.load("assets/" + decor[0] + ".png")
        self.image = pygame.transform.scale(self.image, (decor[1] + self.add_scale, decor[1] + self.add_scale))
        self.image = pygame.transform.rotate(self.image, random.choice(self.angles))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y