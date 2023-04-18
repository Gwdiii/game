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

WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
WINDOW = (640, 480)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.dimensions = (25, 25)
        self.surface = pygame.Surface((self.dimensions))
        self.rectangle = self.surface.get_rect()
        self.surface.fill(WHITE)
        self.center = (WINDOW[0] - self.dimensions[0] >> 1,
                       WINDOW[1] - self.dimensions[1] >> 1)

    def update(self, keys):
        if keys[K_UP]:    self.rectangle.move_ip( 0,-5)
        if keys[K_DOWN]:  self.rectangle.move_ip( 0, 5)
        if keys[K_LEFT]:  self.rectangle.move_ip(-5, 0)
        if keys[K_RIGHT]: self.rectangle.move_ip( 5, 0)

        if self.rectangle.top  <= 0: self.rectangle.top  = 0
        if self.rectangle.left <  0: self.rectangle.left = 0
        if self.rectangle.bottom >= WINDOW[1]: self.rectangle.bottom = WINDOW[1]
        if self.rectangle.right  >  WINDOW[0]: self.rectangle.right  = WINDOW[0]

pygame.init()

screen = pygame.display.set_mode(WINDOW)
player = Player()
running = True

while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: running = False

        if event.type == QUIT: running = False

    keys = pygame.key.get_pressed()

    player.update(keys)

    screen.fill(BLACK)

    screen.blit(player.surface, player.rectangle)

    pygame.display.flip()

pygame.quit()
