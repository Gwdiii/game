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

        self.active_piece = 0
        self.active = set()
        self.axis_y = 0
        self.axis_x = 0
        self.sprite = 0

    def spawn(self, index: int) -> None:
        self.active_piece = index
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

                target_y = y + origin_offset_y
                target_x = x + origin_offset_x

                if mask[y][x]:
                    self.grid[target_y][target_x] = self.sprite
                    self.active.add((target_y, target_x))

    def collides_with(self, y: int, x: int) -> bool:
        lower_bound_y = 0
        lower_bound_x = 0

        upper_bound_y = 20
        upper_bound_x = 10

        if not lower_bound_y <= y < upper_bound_y: return True
        if not lower_bound_x <= x < upper_bound_x: return True
        if self.grid[y][x]: return True

        return False

    def transform(self,
                  push_y: Callable[[int, int], int],
                  push_x: Callable[[int, int], int],
                  pull_y: Callable[[int, int], int],
                  pull_x: Callable[[int, int], int]) -> None:

        next_active = set()
        for (y, x) in self.active:
            target_y = push_y(y, x)
            target_x = push_x(y, x)
            trail_y  = pull_y(y, x)
            trail_x  = pull_x(y, x)

            if y == target_y and x == target_x:
                next_active.add((target_y, target_x))
                continue

            if self.collides_with(target_y, target_x):
                continue

            if (trail_y, trail_x) in self.active:
                next_active.add((y, x))

            next_active.add((target_y, target_x))

            if len(next_active) == 4:
                self.axis_y = push_y(self.axis_y, self.axis_x)
                self.axis_x = push_x(self.axis_y, self.axis_x)
                for (y, x) in self.active: self.grid[y][x] = 0
                for (y, x) in next_active: self.grid[y][x] = self.sprite
                self.active = next_active

    def update(self,
               offset_y: int,
               offset_x: int,
               rotation: int,
               drop: bool) -> None:

        if drop:
            self.transform(
                (lambda y, x: y + 1),
                (lambda y, x: x),
                (lambda y, x: y - 1),
                (lambda y, x: x)
            )

        if game.delay: return
    
        if rotation and self.active_piece:
            self.transform(
                (lambda y, x: self.axis_y - (self.axis_x - x) * rotation),
                (lambda y, x: self.axis_x + (self.axis_y - y) * rotation),
                (lambda y, x: self.axis_y + (self.axis_x - x) * rotation),
                (lambda y, x: self.axis_x - (self.axis_y - y) * rotation),
            )
            game.delay = 16

        if offset_y or offset_x:
            self.transform(
                (lambda y, x: y + offset_y),
                (lambda y, x: x + offset_x),
                (lambda y, x: y - offset_y),
                (lambda y, x: x - offset_x)
            )
            game.delay = 16

class Game():
    def __init__(self):
        self.frame = 1
        self.delay = 0
        self.auto_shift = 6

    def handleMovement(self, keys: ScancodeWrapper) -> None:
        offset_y = 0
        offset_x = 0
        rotation = 0
        drop = False

        if keys[K_DOWN]:  offset_y += 1
        if keys[K_LEFT]:  offset_x -= 1
        if keys[K_RIGHT]: offset_x += 1
        if keys[K_j]: rotation = -1
        if keys[K_k]: rotation =  1

        if self.frame == DROP_INTERVAL:
            self.frame = 1
            drop = True
        else:
            self.frame += 1

        playfield.update(offset_y, offset_x, rotation, drop)

    def render(self, blocks: list) -> None:
        block_width = block_height = 16
        for y, row in enumerate(playfield.grid):
            for x, sprite in enumerate(row):
                if sprite: screen.blit(blocks[sprite].surface,
                                      (x * block_width, y * block_height))

    def quit(self, event: Event) -> bool:
        if event.type == KEYDOWN and event.key == K_ESCAPE: return True
        if event.type == QUIT: return True
        return False

pygame.init()

screen = pygame.display.set_mode(WINDOW)
clock  = pygame.time.Clock()

blocks = [Block(0),
          Block(1),
          Block(2),
          Block(3)]
print(type(blocks[0]))

game = Game()
playfield = Playfield()
next_piece = random.randint(0, len(PIECES))
playfield.spawn(next_piece)

running = True
while running:

    for event in pygame.event.get(): running = not game.quit(event)
    if game.delay: game.delay -= 1
    keys = pygame.key.get_pressed()
    game.handleMovement(keys)
    screen.fill(BLACK)
    game.render(blocks)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
