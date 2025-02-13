import pygame


if __name__ == '__main__':
    pygame.init()
    running = True
    screen = pygame.display.set_mode((640,640))
    clock = pygame.time.Clock()
    
    blessing = pygame.image.load("res\images\jacaré.jpg").convert()
    x = 0

    delta_time = 0.1

    while running:

        
        screen.blit(blessing, (x, 320, 64, 64))
        x += 100 * delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()
        delta_time = clock.tick(60) / 1000
        delta_time = max(0.001, min(0.1, delta_time))

    pygame.quit()