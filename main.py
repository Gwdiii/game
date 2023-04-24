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
        self.surface.blits(((self.block.surface, (32,  0)),
                            (self.block.surface, (32, 16)),
                            (self.block.surface, (32, 32)),
                            (self.block.surface, (32, 48))))

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

pygame.init()

screen  = pygame.display.set_mode(WINDOW, pygame.DOUBLEBUF)
clock = pygame.time.Clock()
lock_tetramino = pygame.USEREVENT + 1

current = Tetramino()
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

    current.update(keys)

    screen.fill(BLACK)

    screen.blit(current.surface, current.rect)
    # for sprite in sprites: screen.blit(sprite.surface, sprite.rect)

    if pygame.sprite.spritecollideany(current, locked):
        current.kill()
        running = False

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
