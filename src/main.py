import pygame

font = 0

player = {}
gravity = 500
jump_force = -350

obstacle = {}

def init():
    global font, player, obstacle

    #setting player up
    sprite = pygame.image.load("res\images\jacaré.jpg").convert()
    sprite = pygame.transform.scale(sprite, (64,64))
    player = {
                'image': sprite,
                'pos': {'x': 50, 'y': 296},
                'vel': {'x': 0, 'y': jump_force},
                'dir': {'x': 0, 'y': 0},
                'size': sprite.get_size(),
                'hitbox': 0
            }

    #setting obstacle up
    obstacle = {
                'image': None,
                'pos': {'x': 500, 'y': 0},
                'x_vel': 250,
                'size': (100, 500),
                'hitbox': 0
            }

    font = pygame.font.Font(None, size=30)


def process(delta):
    global player, obstacle

    player['vel']['y'] += gravity * delta
    player['pos']['x'] += player['dir']['x'] * 100 * delta
    player['pos']['y'] += player['vel']['y'] * delta

    obstacle['pos']['x'] -= obstacle['x_vel'] * delta
    print(player['vel'])

def physics_process(delta):
    global player, obstacle

    player['hitbox'] = pygame.Rect(player['pos']['x'], player['pos']['y'], player['size'][0], player['size'][1])

    obstacle['hitbox'] = pygame.Rect(obstacle['pos']['x'], obstacle['pos']['y'], obstacle['size'][0], obstacle['size'][1])

    #collision = player['hitbox'].colliderect(obstacle['hitbox'])


def handle_input(event: pygame.Event):
    global p_direction, p_velocity
    if event.type == pygame.QUIT:
        return False
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            player['dir']['y'] -= 1
        if event.key == pygame.K_DOWN:
            player['dir']['y'] += 1
        
        if event.key == pygame.K_RIGHT:
            player['dir']['x'] += 1
        if event.key == pygame.K_LEFT:
            player['dir']['x'] -= 1
    
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            player['dir']['y'] += 1
            player['vel']['y'] = jump_force
        if event.key == pygame.K_DOWN:
            player['dir']['y'] -= 1
            
        
        if event.key == pygame.K_RIGHT:
            player['dir']['x'] -= 1
        if event.key == pygame.K_LEFT:
            player['dir']['x'] += 1

    return True


def render(delta, screen: pygame.Surface):
    global font, obstacle
    screen.fill((255,255,255))

    #render player
    screen.blit(player['image'], (player['pos']['x'], player['pos']['y']))

    #render obstacle
    collision = player['hitbox'].colliderect(obstacle['hitbox'])
    pygame.draw.rect(screen, (255 * collision, 255, 0), obstacle['hitbox'])

    #render text
    text = font.render("OPA!", True, (0,0,0))
    screen.blit(text, (300,100))

    #show everything on screen
    pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    running = True
    screen = pygame.display.set_mode((640,640))
    clock = pygame.time.Clock()
    
    delta_time = 0.1

    init()
    while running:

        for event in pygame.event.get():
            if not handle_input(event):
                running = False
        
        delta_time = clock.tick(60) / 1000
        delta_time = max(0.001, min(0.1, delta_time))

        physics_process(delta_time)
        process(delta_time)
        render(delta_time, screen)

    pygame.quit()
