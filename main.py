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

        self.active = [0, 0, 0, 0]

    def spawn(self, config):
        config_position = 4
        grid_position = -13
        active_index = 0

        for block in config:
            if config_position % 4 == 0: grid_position += 6

            if block:
                self.grid[grid_position] = block
                self.active[active_index] = grid_position
                active_index += 1

            config_position += 1
            grid_position   += 1

        print(self.active)

    def update(self, keys):

        offset = 0

        if keys[K_UP]:    offset += UP
        if keys[K_DOWN]:  offset += DOWN
        if keys[K_LEFT]:  offset += LEFT
        if keys[K_RIGHT]: offset += RIGHT
        if not offset: return

        next = []
        seen = set()
        for position in self.active:
                target   = position + offset
                trailing = position - offset
                if self.grid[target] == 0:
                    self.grid[target] = 1
                    next.append(target)
                else: seen.add(position)

                if self.grid[trailing] and trailing in seen:
                    self.grid[trailing] = 0
                    print(trailing)
                    print(self.grid[trailing])
                    next.append(position)
                    seen.discard(trailing)

        # print(self.grid)
        self.active = next

    def render(self, block):
        for position, value in enumerate(self.grid):
            if value:
                x = (position  % 10) * 16
                y = (position // 10) * 16
                screen.blit(block.surface, (x, y))

class Block(pygame.sprite.Sprite):
    def __init__(self):
        self.surface = pygame.image.load("block_0.png").convert()
        self.surface.set_colorkey((BLACK))
        self.rect = self.surface.get_rect()

class Tetramino(pygame.sprite.Sprite):
    def update(self, keys, blocks):

        input_x = 0
        input_y = 0

        if keys[K_UP]:    input_y -= 16
        if keys[K_DOWN]:  input_y += 16
        if keys[K_LEFT]:  input_x -= 16
        if keys[K_RIGHT]: input_x += 16

        min_x = min_y = 0
        max_x = WINDOW[0]
        max_y = WINDOW[1]

        for block in blocks:
            
            max_x = min(max_x, input_x, WINDOW[0] - block.rect.right)
            max_y = min(max_y, input_y, WINDOW[1] - block.rect.bottom)
            min_x = max(min_x, input_x, -block.rect.left)
            min_y = max(min_y, input_y, -block.rect.top)

        next = pygame.sprite.Group()
        for block in blocks:
            block.rect.move_ip((max_x + min_x, max_y + min_y))
            next.add(block)

        return next

pygame.init()

screen  = pygame.display.set_mode(WINDOW, pygame.DOUBLEBUF)
clock = pygame.time.Clock()
playfield = Playfield()
playfield.spawn(O)

running = True
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE: running = False
        if event.type == QUIT: running = False

    keys = pygame.key.get_pressed()

    playfield.update(keys)

    screen.fill(BLACK)

    playfield.render(Block())

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
