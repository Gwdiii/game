import pygame

from random import randint
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
WINDOW = (640, 480)

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.surface = pygame.image.load("block_0.png").convert()
        self.surface.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surface.get_rect()

class Tetramino(pygame.sprite.Sprite):
    def __init__(self, props):
        super(Tetramino, self).__init__()
        self.move = (0, 0)
        for position, exists in enumerate(props.grid):
            if exists:
                row = (position %  4) * 16
                col = (position // 4) * 16
                block = Block()
                block.rect = pygame.Rect(row, col, 16, 16)
                current.add(block)

    def update(self, keys, current):
        if keys[K_UP]:    self.move = ( 0,-1)
        if keys[K_DOWN]:  self.move = ( 0, 1)
        if keys[K_LEFT]:  self.move = (-1, 0)
        if keys[K_RIGHT]: self.move = ( 1, 0)

        next = pygame.sprite.Group()

        for block in current:
            block.rect.move_ip(self.move)

            if block.rect.top  < 0:
                block.rect.top = 0
                break
            if block.rect.left < 0:
                block.rect.left = 0
                break
            if block.rect.bottom > WINDOW[1]:
                block.rect.bottom = 0
                break
            if block.rect.right  > WINDOW[0]:
                block.rect.right = 0
                break

            next.add(block)

            if block == len(current) - 1: return next

        return current

class I(pygame.sprite.Sprite):
    def __init__(self):
        super(I, self).__init__()
        self.axis = 7
        self.grid = [0,0,1,0,
                     0,0,1,0,
                     0,0,1,0,
                     0,0,1,0]

class O(pygame.sprite.Sprite):
    def __init__(self):
        super(O, self).__init__()
        self.axis = 0
        self.grid = [0,0,0,0,
                     0,1,1,0,
                     0,1,1,0,
                     0,0,0,0]

class J(pygame.sprite.Sprite):
    def __init__(self):
        super(J, self).__init__()
        self.axis = 10
        self.grid = [0,0,0,0,
                     0,0,0,0,
                     0,1,1,1,
                     0,0,0,1]

class L(pygame.sprite.Sprite):
    def __init__(self):
        super(L, self).__init__()
        self.axis = 10
        self.grid = [0,0,0,0,
                     0,0,0,0,
                     0,1,1,1,
                     0,1,0,0]

class S(pygame.sprite.Sprite):
    def __init__(self):
        super(S, self).__init__()
        self.axis = 10
        self.grid = [0,0,0,0,
                     0,0,0,0,
                     0,0,1,1,
                     0,1,1,0]

class Z(pygame.sprite.Sprite):
    def __init__(self):
        super(Z, self).__init__()
        self.axis = 10
        self.grid = [0,0,0,0,
                     0,0,0,0,
                     0,1,1,0,
                     0,0,1,1]

class T(pygame.sprite.Sprite):
    def __init__(self):
        super(T, self).__init__()
        self.axis = 10
        self.grid = [0,0,0,0,
                     0,0,0,0,
                     0,1,1,1,
                     0,0,1,0]

pygame.init()

screen  = pygame.display.set_mode(WINDOW, pygame.DOUBLEBUF)
clock = pygame.time.Clock()
lock_tetramino = pygame.USEREVENT + 1
lock_event = pygame.event.Event(lock_tetramino)
pygame.event.post(lock_event)

locked  = pygame.sprite.Group()
current = pygame.sprite.Group()
tetramino = Tetramino(O())
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

    # if pygame.sprite.spritecollideany(current.tetramino, locked):
    #     current.kill()
    #     running = False

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
