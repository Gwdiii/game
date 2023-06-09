import pygame
import random

from pygame.key   import ScancodeWrapper
from typing       import Callable
from pygame.event import Event

from pygame.locals import (
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_j,
    K_k,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

WHITE  = (224, 224, 224)
BACKGROUND = (40, 40, 40)
BLACK  = (0, 0, 0)
WINDOW = (160, 352)
INIT_INTERVAL = 16
AUTO_INTERVAL = 6

O = [[0,1,1,0],
     [0,1,1,0]]

I = [[1,1,1,1],
     [0,0,0,0]]

J = [[0,2,2,2],
     [0,0,0,2]]

L = [[0,3,3,3],
     [0,3,0,0]]

S = [[0,0,2,2],
     [0,2,2,0]]

Z = [[0,3,3,0],
     [0,0,3,3]]

T = [[0,1,1,1],
     [0,0,1,0]]

PIECES = [O, I, J, L, S, Z, T]

PALETTE = [[(211, 211, 211), (167, 167, 167), (125, 125, 125)],
           [(255, 203, 127), (255, 151,   0), (169, 117,  46)],
           [(255, 127, 127), (255,   0,   0), (169,  46,  46)]]

class Playfield():
    def __init__(self):
        self.grid = [[0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0]]

        self.curr_piece = 0
        self.next_piece = random.randint(0, 6)
        self.curr = set()
        self.next = set()
        self.axis_y = 0
        self.axis_x = 0
        self.sprite = 0

        self.spawn()

    def spawn(self) -> None:
        self.curr_piece = self.next_piece
        self.next_piece = self.randomizer(False)
        self.axis_y = 0
        self.axis_x = 5

        index = self.curr_piece

        mask = PIECES[index]
        mask_axis_y: int = 0
        mask_axis_x: int = 2

        origin_offset_y = self.axis_y - mask_axis_y
        origin_offset_x = self.axis_x - mask_axis_x

        #mask axis should always have a sprite value
        self.sprite = mask[mask_axis_y][mask_axis_x]

        for y in range(len(mask)):
            for x in range(len(mask[0])):

                if not mask[y][x]: continue

                to_y = y + origin_offset_y
                to_x = x + origin_offset_x

                self.grid[to_y][to_x] = self.sprite
                self.curr.add((to_y, to_x))

    def randomizer(self, second_roll: bool) -> int:
        roll = random.randint(0, 7)

        if roll == 7: roll = self.randomizer(True)
        if second_roll: return roll
        if roll == self.next_piece: roll = self.randomizer(True)

        return roll

    def clear(self, cleared_row: int) -> None:
        new_row = [0] * 10
        self.grid.pop(cleared_row)
        self.grid.insert(0, new_row)
        return
        
    def lock(self) -> int:
        self.curr = set()
        total_cleared = 0

        for y, row in enumerate(playfield.grid):
            last  = len(row) - 1
            clear = True

            for x, sprite in enumerate(row):
                if sprite == 0: clear = False
                if x == last and clear == True:
                    total_cleared += 1
                    self.clear(y)

        return total_cleared

    def collision(self, y: int, x: int) -> bool:
        lower_bound_y = 0
        lower_bound_x = 0

        upper_bound_y = 20
        upper_bound_x = 10

        if not lower_bound_y <= y < upper_bound_y: return True
        if not lower_bound_x <= x < upper_bound_x: return True
        if self.grid[y][x]: return True

        return False

    def free(self,
             y: int,
             x: int,
             calc_y: Callable[[int, int], int],
             calc_x: Callable[[int, int], int]) -> bool:

        to_y = calc_y(y, x)
        to_x = calc_x(y, x)

        if y == to_y and x == to_x:  return True
        if not self.collision(y, x): return True
        if not (y, x) in self.curr:  return False
        if not self.free(to_y, to_x, calc_y, calc_x): return False

        self.next.add((to_y, to_x))

        return True

    def transform(self,
                  calc_y: Callable[[int, int], int],
                  calc_x: Callable[[int, int], int]) -> bool:

        self.next = set()
        for (y, x) in self.curr:
            to_y = calc_y(y, x)
            to_x = calc_x(y, x)

            if self.free(to_y, to_x, calc_y, calc_x):
                self.next.add((to_y, to_x))

        if len(self.next) == 4:
            self.axis_y = calc_y(self.axis_y, self.axis_x)
            self.axis_x = calc_x(self.axis_y, self.axis_x)
            for (y, x) in self.curr: self.grid[y][x] = 0
            for (y, x) in self.next: self.grid[y][x] = self.sprite
            self.curr = self.next
            return True

        return False

    def update(self,
               offset_y: int,
               offset_x: int,
               rotation: int,
               drop: bool) -> None:

        if drop:
            ok = self.transform(
                (lambda y, x: y + 1),
                (lambda y, x: x)
            )

            if not ok:
                lines_cleared = self.lock()
                score = level.calcScore(lines_cleared)
                game.score += score
                level.update(lines_cleared)
                self.spawn()
    
        if rotation and self.curr_piece:
            ok = self.transform(
                (lambda y, x: self.axis_y - (self.axis_x - x) * rotation),
                (lambda y, x: self.axis_x + (self.axis_y - y) * rotation)
            )

        if offset_y or offset_x:
            ok = self.transform(
                (lambda y, x: y + offset_y),
                (lambda y, x: x + offset_x)
            )

            if not ok: 
                game.delay['down']  = 1
                game.delay['left']  = 1
                game.delay['right'] = 1
                game.limit['down']  = True
                game.limit['left']  = True
                game.limit['right'] = True

class StatusBar:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 16)

    def formatScoreSurface(self, score: int):
        string  = str(score)
        surface = self.font.render(string, True, WHITE)
        offset  = 2

        return (surface, offset)
    
    def formatLevelSurface(self, level: int):
        string  = 'L' + str(level)
        surface = self.font.render(string, True, WHITE)
        offset  = 140

        if level > 9: offset -= 8

        return (surface, offset)

    def formatNextSurface(self, index: int):
        surface = pygame.Surface((96, 16))
        string = 'Next: '

        string_surface = self.font.render(string, True, WHITE)
        preview_surface = self.formatPiecePreview(index)

        preview_offset = 36
        if index == 1: preview_offset += 8
        
        surface.blit(string_surface,  (0, 0))
        surface.blit(preview_surface, (preview_offset, 0))
        surface.set_colorkey(BLACK)
        offset = 2

        return (surface, offset)

    def formatPiecePreview(self, index: int):
        preview_surface = pygame.Surface((32, 16))
        mask = PIECES[index]

        for y, row in enumerate(mask):
            for x, sprite in enumerate(row):

                if not sprite: continue

                block_surface = blocks[0].surface
                preview_surface.blit(block_surface, (x*8, y*8))

        return preview_surface

class Level():
    def __init__(self):
        self.level = game.level
        self.start_level = 0
        self.drop_interval = 48 
        self.line_total = 0
    
    def update(self, lines: int) -> None:
        init_threshold_a = self.start_level * 10 + 10
        init_threshold_b = max(100, self.start_level * 10 - 50)
        init_threshold_min = min(init_threshold_a, init_threshold_b)
        level_complete = False

        self.line_total += lines

        if self.level == self.start_level:

            if self.line_total >= init_threshold_min:
                level_complete = True

        if self.level != self.start_level:
            levels_progressed = (self.line_total - init_threshold_min) // 10 + 1
            if self.level != self.start_level + levels_progressed:
                level_complete = True

        if level_complete:
            self.level += 1
            game.level += 1
            self.drop_interval = self.calcDropInterval(self.level)
            for block in blocks: block.updatePalette(self.level)

    def calcScore(self, lines: int) -> int:
        if lines == 1: return 40   * (self.level + 1)
        if lines == 2: return 100  * (self.level + 1)
        if lines == 3: return 300  * (self.level + 1)
        if lines == 4: return 1200 * (self.level + 1)

        return 0

    def calcDropInterval(self, level: int) -> int:
        if level <= 8:  return 48 - level * 5
        if level == 9:  return 6
        if level <= 12: return 5
        if level <= 15: return 4
        if level <= 18: return 3
        if level <= 28: return 2
        if level >= 29: return 1

        return 0 

class Game():
    def __init__(self):
        self.frame = 1
        self.level = 0
        self.score = 0
        self.delay = {'down' : 0,
                      'left' : 0,
                      'right': 0}

        self.limit = {'low_j': False,
                      'low_k': False}

        self.auto  = {'down' : False,
                      'left' : False,
                      'right': False}

    def delayAutoShift(self, scan: ScancodeWrapper) -> dict:
        max_delay = INIT_INTERVAL

        keys = {'down' : scan[K_DOWN],
                'left' : scan[K_LEFT],
                'right': scan[K_RIGHT],
                'low_j': scan[K_j],
                'low_k': scan[K_k]}
        
        for key, value in keys.items():
            if key == 'low_j' or key == 'low_k':

                if value == False:
                    self.limit[key] = False
                    continue

                elif self.limit[key]:
                    keys[key] = False
                    continue

                keys[key] = True
                self.limit[key] = True
                continue

            if value == False:
                self.delay[key] = INIT_INTERVAL
                self.auto[key]  = False
                continue

            self.delay[key] -= 1

            if self.auto[key] == True:  max_delay = AUTO_INTERVAL - 1
            if self.auto[key] == False: max_delay = INIT_INTERVAL - 1

            if 0 < self.delay[key] < max_delay: keys[key] = False
            if self.delay[key] < 1:
                self.delay[key] = AUTO_INTERVAL
                self.auto[key]  = True

        return keys

    def handleMovement(self, scan: ScancodeWrapper) -> None:
        offset_y = 0
        offset_x = 0
        rotation = 0
        drop = False

        keys = self.delayAutoShift(scan)

        if keys['down'] : offset_y += 1
        if keys['left'] : offset_x -= 1
        if keys['right']: offset_x += 1
        if keys['low_j']: rotation = -1
        if keys['low_k']: rotation =  1

        if self.frame == level.drop_interval:
            self.frame = 1
            drop = True
        else:
            self.frame += 1

        playfield.update(offset_y, offset_x, rotation, drop)

    def render(self, blocks: list) -> None:
        (level_surface, level_offset) = statusbar.formatLevelSurface(self.level)
        (score_surface, score_offset) = statusbar.formatScoreSurface(self.score)
        (next_surface, next_offset) = statusbar.formatNextSurface(playfield.next_piece)

        screen.blit(level_surface, (level_offset, 0))
        screen.blit(score_surface, (score_offset, 0))
        screen.blit(next_surface,  (next_offset, 16))
        
        for y, row in enumerate(playfield.grid):
            for x, sprite in enumerate(row):

                if not sprite: continue

                surface = blocks[sprite].surface
                screen.blit(surface, (x*16, 32+y*16))

    def quit(self, event: Event) -> bool:
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            return True

        if event.type == QUIT:
            return True

        return False

class Block(pygame.sprite.Sprite):
    def __init__(self, index: int):
        path = 'block_' + str(index) + '.bmp'
        self.image = pygame.image.load(path)
        self.surface = self.image.convert()
        self.surface.set_colorkey((BLACK))
        self.palette = PALETTE[0]

    def paletteSwap(self, old_color, new_color) -> pygame.Surface:

        new_surface = pygame.Surface(self.surface.get_size())
        new_surface.fill(new_color)
        self.surface.set_colorkey(old_color)
        new_surface.blit(self.surface, (0, 0))

        return new_surface

    def updatePalette(self, level: int) -> None:
        new_palette = PALETTE[level % len(PALETTE)]
        old_palette = self.palette

        for i in range(len(new_palette)):
            self.surface = self.paletteSwap(old_palette[i],
                                            new_palette[i])
        self.surface.set_colorkey(BLACK)
        self.palette = new_palette

pygame.init()

screen = pygame.display.set_mode(WINDOW)
pygame.display.set_caption('Tetris')
clock  = pygame.time.Clock()

blocks = [Block(0),
          Block(1),
          Block(2),
          Block(3)]

game = Game()
level = Level()
playfield = Playfield()
statusbar = StatusBar()

running = True
while running:

    for event in pygame.event.get(): running = not game.quit(event)
    scan = pygame.key.get_pressed()
    game.handleMovement(scan)
    screen.fill(BACKGROUND)
    game.render(blocks)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
