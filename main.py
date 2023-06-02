import pygame
import random

from typing import Callable
from pygame.event import Event
from pygame.key import ScancodeWrapper

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

WINDOW = (640, 480)
BLACK  = (0, 0, 0)
DROP_INTERVAL = 60

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

class Block(pygame.sprite.Sprite):
    def __init__(self, index: int):
        path = 'block_' + str(index) + '.png'
        image = pygame.image.load(path)
        self.surface = image.convert()
        self.surface.set_colorkey((BLACK))
        self.index = index

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
        self.curr = set()
        self.next = set()
        self.axis_y = 0
        self.axis_x = 0
        self.sprite = 0

    def spawn(self, index: int) -> None:
        self.curr_piece = index
        self.axis_y = 0
        self.axis_x = 5

        mask: list[list[int]] = PIECES[index]
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
                  calc_x: Callable[[int, int], int]) -> None:


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

    def update(self,
               offset_y: int,
               offset_x: int,
               rotation: int,
               drop: bool) -> None:

        if drop:
            self.transform(
                (lambda y, x: y + 1),
                (lambda y, x: x)
            )
    
        if rotation and self.curr_piece:
            self.transform(
                (lambda y, x: self.axis_y - (self.axis_x - x) * rotation),
                (lambda y, x: self.axis_x + (self.axis_y - y) * rotation)
            )

        if offset_y or offset_x:
            self.transform(
                (lambda y, x: y + offset_y),
                (lambda y, x: x + offset_x)
            )

class Game():
    def __init__(self):
        self.frame = 1

        self.delay = {'down' : 0,
                      'left' : 0,
                      'right': 0}

        self.limit = {'low_j': False,
                      'low_k': False}

        self.auto  = {'down' : False,
                      'left' : False,
                      'right': False}
    def delayAutoShift(self, scan: ScancodeWrapper) -> dict:
        INIT_INTERVAL = 16
        AUTO_INTERVAL = 6
        keys = {'down' : scan[K_DOWN],
                'left' : scan[K_LEFT],
                'right': scan[K_RIGHT],
                'low_j': scan[K_j],
                'low_k': scan[K_k]}
        
        for key, value in keys.items():
            if key in self.limit:
                if not value:
                    self.limit[key] = False
                    continue
                elif self.limit[key]:
                    keys[key] = False
                    continue
                keys[key] = True
                self.limit[key] = True
                continue

            if not value:
                self.delay[key] = INIT_INTERVAL
                self.auto[key]  = False
                continue

            if self.auto[key]:
                max_delay = AUTO_INTERVAL - 1
            else:
                max_delay = INIT_INTERVAL - 1

            self.delay[key] -= 1

            if 0 < self.delay[key] < max_delay: keys[key] = False
            if not self.delay[key]:
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

        if self.frame == DROP_INTERVAL:
            self.frame = 1
            drop = True
        else:
            self.frame += 1

        playfield.update(offset_y, offset_x, rotation, drop)

    def render(self, blocks: list) -> None:
        for y, row in enumerate(playfield.grid):
            for x, sprite in enumerate(row):

                if not sprite: continue

                surface = blocks[sprite].surface
                screen.blit(surface, (x*16, y*16))

    def quit(self, event: Event) -> bool:
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            return True

        if event.type == QUIT:
            return True

        return False

pygame.init()

screen = pygame.display.set_mode(WINDOW)
clock  = pygame.time.Clock()

blocks = [Block(0),
          Block(1),
          Block(2),
          Block(3)]

game = Game()
playfield = Playfield()
next_piece = random.randint(0, 6)
playfield.spawn(next_piece)

running = True
while running:

    for event in pygame.event.get(): running = not game.quit(event)
    scan = pygame.key.get_pressed()
    game.handleMovement(scan)
    screen.fill(BLACK)
    game.render(blocks)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
