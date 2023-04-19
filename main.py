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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.dimensions = (25, 25)
        self.surface = pygame.image.load("player.bmp").convert()
        self.surface.set_colorkey((225, 225, 225), RLEACCEL)
        self.rect = self.surface.get_rect()
        self.surface.fill(WHITE)
        self.center = (WINDOW[0] - self.dimensions[0] >> 1,
                       WINDOW[1] - self.dimensions[1] >> 1)

    def update(self, keys):
        if keys[K_UP]:    self.rect.move_ip( 0,-5)
        if keys[K_DOWN]:  self.rect.move_ip( 0, 5)
        if keys[K_LEFT]:  self.rect.move_ip(-5, 0)
        if keys[K_RIGHT]: self.rect.move_ip( 5, 0)

        if self.rect.top  <= 0: self.rect.top  = 0
        if self.rect.left <  0: self.rect.left = 0
        if self.rect.bottom >= WINDOW[1]: self.rect.bottom = WINDOW[1]
        if self.rect.right  >  WINDOW[0]: self.rect.right  = WINDOW[0]

class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super(NPC, self).__init__()
        self.dimensions = (25, 25)
        self.surface = pygame.Surface((self.dimensions))
        self.rect = self.surface.get_rect(
            center = (
                randint(WINDOW[0] + self.dimensions[0], WINDOW[0] + 100),
                randint(0, WINDOW[1])
            )
        )
        self.surface.fill(WHITE)
        self.speed = randint(3, 12)
 
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0: self.kill()

pygame.init()

screen  = pygame.display.set_mode(WINDOW, pygame.DOUBLEBUF)
clock = pygame.time.Clock()
add_npc = pygame.USEREVENT + 1
pygame.time.set_timer(add_npc, 1000)

player  = Player()
npcs    = pygame.sprite.Group()
sprites = pygame.sprite.Group()
sprites.add(player)

running = True
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: running = False

        elif event.type == QUIT: running = False

        elif event.type == add_npc:
            new_npc = NPC()
            npcs.add(new_npc)
            sprites.add(new_npc)

    keys = pygame.key.get_pressed()

    player.update(keys)
    npcs.update()

    screen.fill(BLACK)

    for sprite in sprites: screen.blit(sprite.surface, sprite.rect)

    if pygame.sprite.spritecollideany(player, npcs):
        player.kill()
        running = False

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
