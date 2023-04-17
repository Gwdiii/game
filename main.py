import pygame
pygame.init()

screen = pygame.display.set_mode([640, 480])

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("quitting")
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (0, 0, 255), (320, 240), 75)

    pygame.display.flip()


pygame.quit()
