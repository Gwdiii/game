import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

WINDOW = (640, 480)
BLACK  = (0, 0, 0)
ORIGIN = 3
UP     = -10
DOWN   = 10
LEFT   = -1
RIGHT  = 1
RIGHT_BOUND = lambda x: not (x + 1) % 10
LEFT__BOUND = lambda x: not x % 10
UPPER_BOUND = lambda x: x < 10
LOWER_BOUND = lambda x: x > 189

O = [0,0,0,0,
     0,1,1,0,
     0,1,1,0,
     0,0,0,0]

I = [0,0,0,0,
     1,1,1,1,
     0,0,0,0,
     0,0,0,0]

J = [0,0,0,0,
     0,1,1,1,
     0,0,0,1,
     0,0,0,0]

L = [0,0,0,0,
     0,1,1,1,
     0,1,0,0,
     0,0,0,0]

S = [0,0,0,0,
     0,0,1,1,
     0,1,1,0,
     0,0,0,0]

Z = [0,0,0,0,
     0,1,1,0,
     0,0,1,1,
     0,0,0,0]

T = [0,0,0,0,
     0,1,1,1,
     0,0,1,0,
     0,0,0,0]

PIECES = [O, I, J, L, S, Z, T]

class Playfield():
    def __init__(self):
        self.grid = [0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,]

        self.active = set()

    def spawn(self, config):
        config_position = 4
        grid_position = -13

        for block in config:
            if config_position % 4 == 0: grid_position += 6

            if block:
                self.grid[grid_position] = block
                self.active.add(grid_position)

            config_position += 1
            grid_position   += 1

    def update(self, keys):

        offset = 0

        if keys[K_UP]:    offset += UP
        if keys[K_DOWN]:  offset += DOWN
        if keys[K_LEFT]:  offset += LEFT
        if keys[K_RIGHT]: offset += RIGHT
        if not offset: return

        next = set()

        for position in self.active:
            if offset % 10:
                if offset > 0 and RIGHT_BOUND(position): break
                if offset < 0 and LEFT__BOUND(position): break
            else:
                if offset > 0 and LOWER_BOUND(position): break
                if offset < 0 and UPPER_BOUND(position): break


            target   = position + offset
            trailing = position - offset
            if self.grid[target] == 0:
                self.grid[target] = 1
                next.add(target)

                if self.grid[trailing] and trailing in self.active:
                    self.grid[trailing] = 0
                    next.add(position)

        if next: self.active = next

    def render(self, block):
        for position, value in enumerate(self.grid):
            if value:
                x = (position  % 10) * 16
                y = (position // 10) * 16
                screen.blit(block.surface, (x, y))

class Block(pygame.sprite.Sprite):
    def __init__(self):
        self.surface = pygame.image.load("block_2.png").convert()
        self.surface.set_colorkey((BLACK))

def quit(event):
    if event.type == KEYDOWN and event.key == K_ESCAPE: return False
    if event.type == QUIT: return False
    return True

pygame.init()

screen  = pygame.display.set_mode(WINDOW, pygame.DOUBLEBUF)
clock = pygame.time.Clock()
playfield = Playfield()
playfield.spawn(O)

running = True
while running:

    for event in pygame.event.get(): running = quit(event)

    keys = pygame.key.get_pressed()
    playfield.update(keys)
    screen.fill(BLACK)
    playfield.render(Block())
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
