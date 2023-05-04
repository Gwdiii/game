import pygame

from pygame.locals import (
    K_DOWN,
    K_LEFT,
    K_RIGHT,
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
        self.frame  = 1

    def spawn(self, config):

        for y in range(1,3):
            for x in range(4):
                if config[y][x]:
                    self.grid[y-1][x+3] = config[y][x]
                    self.active.add((y-1, x+3))

    def update(self, keys):

        offset_y = 0
        offset_x = 0

        if self.frame == DROP_INTERVAL:
            print('drop')
            offset_y += 1
            self.frame = 1
        else:
            self.frame += 1

        if keys[K_DOWN]:
            print('down')
            offset_y += 1
        if keys[K_LEFT]:
            print('left')
            offset_x -= 1
        if keys[K_RIGHT]:
            print('right')
            offset_x += 1
        if not offset_y and not offset_x:
            # print('no offset')
            return

        print(self.grid)

        next = set()

        print('offset_y: ' + str(offset_y))
        print('offset_x: ' + str(offset_x))
        print('self.active : ' + str(self.active))
        for position in self.active:
            if not 0 <= position[1] + offset_x < 10:
            # if offset_x > 0 and position[1] == 9:
                # print('right_bound')
                print('horizontal bound')
                offset_x = 0
            # if offset_x < 0 and position[1] == 0:
            #     print('left_bound')
            #     offset_x = 0

            if not 0 <= position[0] + offset_y < 20:
            # elif   offset_y > 0 and position[0] == 19:
                print('vertical_bound')
                offset_y = 0

            target = (position[0] + offset_y, position[1] + offset_x)
            trail  = (position[0] - offset_y, position[1] - offset_x)
            print('target:   ' + str(target))
            print('position: ' + str(position))
            print('trailing: ' + str(trail))
            if self.grid[target[0]][target[1]] == 0:
                print('move position to target')
                next.add(target)

                if trail in self.active: next.add(position)

        if len(next) == 4:
            print('next: ' + str(next))
            sample = list(self.active)[0]
            print('sample: ' + str(sample))
            sprite = self.grid[sample[0]][sample[1]]
            print('sprite: ' + str(sprite))
            for position in self.active:
                self.grid[position[0]][position[1]] = 0
            for position in next:
                self.grid[position[0]][position[1]] = sprite
            self.active = next
            print(self.grid)
        print('//////////////////////')

    def render(self, blocks):
        for y, row in enumerate(self.grid):
            for x, sprite in enumerate(row):
                if sprite: screen.blit(blocks[sprite-1].surface, (x*16, y*16))

class Block(pygame.sprite.Sprite):
    def __init__(self, index):
        self.surface = pygame.image.load('block_' + str(index) + '.png').convert()
        self.surface.set_colorkey((BLACK))

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

frame = 1
running = True
while running:

    for event in pygame.event.get(): running = not quit(event)

    keys = pygame.key.get_pressed()
    playfield.update(keys)
    screen.fill(BLACK)
    playfield.render(blocks)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
