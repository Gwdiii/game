import pygame

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

O = [[0,0,0,0],
     [0,1,1,0],
     [0,1,1,0],
     [0,0,0,0]]

I = [[0,0,0,0],
     [1,1,1,1],
     [0,0,0,0],
     [0,0,0,0]]

J = [[0,0,0,0],
     [0,2,2,2],
     [0,0,0,2],
     [0,0,0,0]]

L = [[0,0,0,0],
     [0,3,3,3],
     [0,3,0,0],
     [0,0,0,0]]

S = [[0,0,0,0],
     [0,0,2,2],
     [0,2,2,0],
     [0,0,0,0]]

Z = [[0,0,0,0],
     [0,3,3,0],
     [0,0,3,3],
     [0,0,0,0]]

T = [[0,0,0,0],
     [0,1,1,1],
     [0,0,1,0],
     [0,0,0,0]]

PIECES = [O, I, J, L, S, Z, T]

class Block(pygame.sprite.Sprite):
    def __init__(self, index):
        path = 'block_' + str(index) + '.png'
        image = pygame.image.load(path)
        self.surface = image.convert()
        self.surface.set_colorkey((BLACK))

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

        self.active = set()
        self.axis_y = 0
        self.axis_x = 0
        self.sprite = 0
        self.frame = 1
        self.delay = 0
        self.auto_shift = 6


    def spawn(self, mask):
        self.axis_y = 0
        self.axis_x = 5
        self.sprite = mask[1][2]
        for y in range(1, 3):
            for x in range(4):
                if mask[y][x]:
                    self.grid[y-1][x+3] = mask[y][x]
                    self.active.add((y-1, x+3))

    def collides_with(self, y, x):
        if not 0 <= x < 10: return True
        if not 0 <= y < 20: return True
        if self.grid[y][x]: return True
        return False

    def transform(self, to_y, to_x, from_y, from_x):
        next_active = set()
        for (y, x) in self.active:
            target_y = to_y(y, x)
            target_x = to_x(y, x)
            trail_y = from_y(y, x)
            trail_x = from_x(y, x)

            if y == target_y and x == target_x:
                next_active.add((target_y, target_x))
                continue

            if self.collides_with(target_y, target_x):
                continue

            if (trail_y, trail_x) in self.active:
                next_active.add((y, x))

            next_active.add((target_y, target_x))

            if len(next_active) == 4:
                self.axis_y = to_y(self.axis_y, self.axis_x)
                self.axis_x = to_x(self.axis_y, self.axis_x)
                for (y, x) in self.active: self.grid[y][x] = 0
                for (y, x) in next_active: self.grid[y][x] = self.sprite
                self.active = next_active

    def update_grid(self, offset_y = 0, offset_x = 0, rotation = 0, drop = False):

        if drop:
            self.transform(
                (lambda y, x: y + 1),
                (lambda y, x: x),
                (lambda y, x: y - 1),
                (lambda y, x: x)
            )

        if self.delay: return
    
        if rotation:
            self.transform(
                (lambda y, x: self.axis_y - (self.axis_x - x) * rotation),
                (lambda y, x: self.axis_x + (self.axis_y - y) * rotation),
                (lambda y, x: self.axis_y + (self.axis_x - x) * rotation),
                (lambda y, x: self.axis_x - (self.axis_y - y) * rotation),
            )
            self.delay = 16

        if offset_y or offset_x:
            self.transform(
                (lambda y, x: y + offset_y),
                (lambda y, x: x + offset_x),
                (lambda y, x: y - offset_y),
                (lambda y, x: x - offset_x)
            )
            self.delay = 16

    def handleMovement(self, keys):
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

        self.update_grid(offset_y, offset_x, rotation, drop)

    def render(self, blocks):
        for y, row in enumerate(self.grid):
            for x, sprite in enumerate(row):
                if sprite: screen.blit(blocks[sprite-1].surface, (x*16, y*16))

def quit(event):
    if event.type == KEYDOWN and event.key == K_ESCAPE: return True
    if event.type == QUIT: return True
    return False

pygame.init()

screen  = pygame.display.set_mode(WINDOW, pygame.DOUBLEBUF)
clock = pygame.time.Clock()

blocks = [Block(1), Block(2), Block(3)]
playfield = Playfield()
playfield.spawn(PIECES[5])

running = True
while running:

    for event in pygame.event.get(): running = not quit(event)
    if playfield.delay: playfield.delay -= 1
    keys = pygame.key.get_pressed()
    playfield.handleMovement(keys)
    screen.fill(BLACK)
    playfield.render(blocks)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
