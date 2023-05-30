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
        self.frame = 1

    def spawn(self, mask):
        self.axis_y = 0
        self.axis_x = 5
        for y in range(1, 3):
            for x in range(4):
                if mask[y][x]:
                    self.grid[y-1][x+3] = mask[y][x]
                    self.active.add((y-1, x+3))

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

    def collides_with(self, y, x):
        if not 0 <= x < 10: return True
        if not 0 <= y < 20: return True
        if self.grid[y][x]: return True
        return False

    def update_grid(self, offset_y = 0, offset_x = 0, rotation = 0, drop = False):
        sample = list(self.active)[0]
        sprite = self.grid[sample[0]][sample[1]]

        if drop:
            next_active = set()
            for (y, x) in self.active:
                target_y = y + 1
                target_x = x
                if self.collides_with(target_y, target_x):
                    continue

                trail_y = y - 1
                trail_x = x
                if (trail_y, trail_x) in self.active:
                    next_active.add((y, x))

                next_active.add((target_y, target_x))

            if len(next_active) == 4:
                self.axis_y += 1
                for (y, x) in self.active: self.grid[y][x] = 0
                for (y, x) in next_active: self.grid[y][x] = sprite
                self.active = next_active

        if rotation:
            next_active = set()
            for (y, x) in self.active:
                axis_offset_y = self.axis_y - y
                axis_offset_x = self.axis_x - x
                target_y = self.axis_y - (axis_offset_x * rotation)
                target_x = self.axis_x + (axis_offset_y * rotation)

                if y == target_y and x == target_x:
                    next_active.add((target_y, target_x))
                    continue

                if self.collides_with(target_y, target_x):
                    continue

                trail_y = self.axis_y + (axis_offset_x * rotation)
                trail_x = self.axis_x - (axis_offset_y * rotation)

                if (trail_y, trail_x) in self.active:
                    next_active.add((y, x))

                next_active.add((target_y, target_x))

            if len(next_active) == 4:
                for (y, x) in self.active: self.grid[y][x] = 0
                for (y, x) in next_active: self.grid[y][x] = sprite
                self.active = next_active

        if offset_y or offset_x:
            next_active = set()
            for (y, x) in self.active:
                target_y = y + offset_y
                target_x = x + offset_x

                if self.collides_with(target_y, target_x):
                    continue

                trail_y = y - offset_y
                trail_x = x - offset_x

                if (trail_y, trail_x) in self.active:
                    next_active.add((y, x))

                next_active.add((target_y, target_x))

            if len(next_active) == 4:
                self.axis_y += offset_y
                self.axis_x += offset_x
                for (y, x) in self.active: self.grid[y][x] = 0
                for (y, x) in next_active: self.grid[y][x] = sprite
                self.active = next_active

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

    keys = pygame.key.get_pressed()
    playfield.handleMovement(keys)
    screen.fill(BLACK)
    playfield.render(blocks)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
