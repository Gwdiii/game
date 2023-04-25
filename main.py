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
    def __init__(self):
        super(Tetramino, self).__init__()
        self.surface = pygame.Surface((64, 64))
        self.block = Block()
        self.rect = self.surface.get_rect()

    def update(self, keys):
        if keys[K_UP]:    self.rect.move_ip( 0,-16)
        if keys[K_DOWN]:  self.rect.move_ip( 0, 16)
        if keys[K_LEFT]:  self.rect.move_ip(-16, 0)
        if keys[K_RIGHT]: self.rect.move_ip( 16, 0)

        if self.rect.top  <= 0: self.rect.top  = 0
        if self.rect.left <  0: self.rect.left = 0
        if self.rect.bottom >= WINDOW[1]: self.rect.bottom = WINDOW[1]
        if self.rect.right  >  WINDOW[0]: self.rect.right  = WINDOW[0]

class I(pygame.sprite.Sprite):
    def __init__(self):
        super(I, self).__init__()
        self.tetramino = Tetramino()
        self.tetramino.surface.blits(((self.tetramino.block.surface, (32,  0)),
                                      (self.tetramino.block.surface, (32, 16)),
                                      (self.tetramino.block.surface, (32, 32)),
                                      (self.tetramino.block.surface, (32, 48))))

class O(pygame.sprite.Sprite):
    def __init__(self):
        super(O, self).__init__()
        self.tetramino = Tetramino()
        self.tetramino.surface.blits(((self.tetramino.block.surface, (16, 16)),
                                      (self.tetramino.block.surface, (16, 32)),
                                      (self.tetramino.block.surface, (32, 16)),
                                      (self.tetramino.block.surface, (32, 32))))

class J(pygame.sprite.Sprite):
    def __init__(self):
        super(J, self).__init__()
        self.tetramino = Tetramino()
        self.tetramino.surface.blits(((self.tetramino.block.surface, ( 0, 32)),
                                      (self.tetramino.block.surface, (16, 32)),
                                      (self.tetramino.block.surface, (32, 32)),
                                      (self.tetramino.block.surface, (32, 48))))

class L(pygame.sprite.Sprite):
    def __init__(self):
        super(L, self).__init__()
        self.tetramino = Tetramino()
        self.tetramino.surface.blits(((self.tetramino.block.surface, ( 0, 32)),
                                      (self.tetramino.block.surface, (16, 32)),
                                      (self.tetramino.block.surface, (32, 32)),
                                      (self.tetramino.block.surface, ( 0, 48))))

class S(pygame.sprite.Sprite):
    def __init__(self):
        super(S, self).__init__()
        self.tetramino = Tetramino()
        self.tetramino.surface.blits(((self.tetramino.block.surface, (16, 32)),
                                      (self.tetramino.block.surface, (32, 32)),
                                      (self.tetramino.block.surface, ( 0, 48)),
                                      (self.tetramino.block.surface, (16, 48))))

class Z(pygame.sprite.Sprite):
    def __init__(self):
        super(Z, self).__init__()
        self.tetramino = Tetramino()
        self.tetramino.surface.blits(((self.tetramino.block.surface, ( 0, 32)),
                                      (self.tetramino.block.surface, (16, 32)),
                                      (self.tetramino.block.surface, (16, 48)),
                                      (self.tetramino.block.surface, (32, 48))))

class T(pygame.sprite.Sprite):
    def __init__(self):
        super(T, self).__init__()
        self.tetramino = Tetramino()
        self.tetramino.surface.blits(((self.tetramino.block.surface, (0, 32)),
                                      (self.tetramino.block.surface, (16, 32)),
                                      (self.tetramino.block.surface, (32, 32)),
                                      (self.tetramino.block.surface, (16, 48))))

pygame.init()

screen  = pygame.display.set_mode(WINDOW, pygame.DOUBLEBUF)
clock = pygame.time.Clock()
lock_tetramino = pygame.USEREVENT + 1

current = T()
sprites = pygame.sprite.Group()
locked = pygame.sprite.Group()
sprites.add(current)

running = True
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: running = False

        elif event.type == QUIT: running = False

        elif event.type == lock_tetramino:
            new_tetramino = Tetramino()
            sprites.add(new_tetramino)
            locked.add(current)

    keys = pygame.key.get_pressed()

    current.tetramino.update(keys)

    screen.fill(BLACK)

    screen.blit(current.tetramino.surface, current.tetramino.rect)
    # for sprite in sprites: screen.blit(sprite.surface, sprite.rect)

    if pygame.sprite.spritecollideany(current.tetramino, locked):
        current.kill()
        running = False

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
