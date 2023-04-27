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

I = (7, [0,0,1,0,
         0,0,1,0,
         0,0,1,0,
         0,0,1,0])

O = (0, [0,0,0,0,
         0,1,1,0,
         0,1,1,0,
         0,0,0,0])

J = (10, [0,0,0,0,
          0,0,0,0,
          0,1,1,1,
          0,0,0,1])

L = (10, [0,0,0,0,
          0,0,0,0,
          0,1,1,1,
          0,1,0,0])

S = (10, [0,0,0,0,
          0,0,0,0,
          0,0,1,1,
          0,1,1,0])

Z = (10, [0,0,0,0,
          0,0,0,0,
          0,1,1,0,
          0,0,1,1])

T = (10, [0,0,0,0,
          0,0,0,0,
          0,1,1,1,
          0,0,1,0])

grid = [0,0,0,0,0,0,0,0,0,0,
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

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.surface = pygame.image.load("block_0.png").convert()
        self.surface.set_colorkey((BLACK))
        self.rect = self.surface.get_rect()

class Tetramino(pygame.sprite.Sprite):
    def __init__(self, props):
        super(Tetramino, self).__init__()
        for position, exists in enumerate(props[1]):
            if exists:
                row = (position %  4) * 16
                col = (position // 4) * 16
                block = Block()
                block.rect = pygame.Rect(row, col, 16, 16)
                current.add(block)

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
lock_tetramino = pygame.USEREVENT + 1
lock_event = pygame.event.Event(lock_tetramino)
pygame.event.post(lock_event)

locked  = pygame.sprite.Group()
current = pygame.sprite.Group()
tetramino = Tetramino(Z)
running = True
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: running = False

        elif event.type == QUIT: running = False

        elif event.type == lock_tetramino:
            locked.add(current)

    keys = pygame.key.get_pressed()

    current = tetramino.update(keys, current)

    screen.fill(BLACK)

    for sprite in current: screen.blit(sprite.surface, sprite.rect)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
