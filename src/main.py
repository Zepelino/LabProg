import pygame
import random

font = 0

player = {}
gravity = 500
jump_force = -350
dead = False

default_obstacle = {
                'image': None,
                'pos': {'x': 700, 'y': 0},
                'x_vel': 250,
                'size': (100, 700),
                'hitbox1': 0,
                'hitbox2': 0,
                'gap': 128,
                'valuable': True,
                'coll': False,
            }

obstacles = []

obs_spawn_timer = 3.5

points = 0

def new_obstacle():
    global default_obstacle
    new_obs = default_obstacle.copy()
    new_obs['pos'] = {'x': 700, 'y': random.randint(-370, 0)}
    new_obs['size'] = (100, 500)
    new_obs['gap'] = random.randint(80, 150)
    return new_obs

def init():
    global font, player, obstacles, default_obstacle, dead, points, obs_spawn_timer

    #setting player up
    dead = False
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
    obstacles = []
    obstacles.append(new_obstacle())

    points = 0
    obs_spawn_timer = 3.5

    font = pygame.font.Font(None, size=30)


def process(delta):
    global player, obstacles, obs_spawn_timer, default_obstacle, points

    player['vel']['y'] += gravity * delta
    #player['pos']['x'] += player['dir']['x'] * 100 * delta
    player['pos']['y'] += player['vel']['y'] * delta

    if dead:
        return

    for obs in obstacles:
        if dead:
            break

        obs['pos']['x'] -= obs['x_vel'] * delta

        if  obs['valuable'] and obs['pos']['x'] <= player['pos']['x']:
            obs['valuable'] = False
            points += 1

        if obs['pos']['x'] < -100:
            obstacles.remove(obs)
    
    obs_spawn_timer -= delta
    if obs_spawn_timer <= 0:
        obs_spawn_timer = random.uniform(1.2, 2.5)
        obstacles.append(new_obstacle())
        print(len(obstacles))


    #print(player['vel'])
    

def physics_process(delta):
    global player, obstacles, dead

    if dead:
        return
    
    player['hitbox'] = pygame.Rect(player['pos']['x'], player['pos']['y'], player['size'][0], player['size'][1])

    for obs in obstacles:
        #if obs['pos']['x'] > 500:
        #    continue
        obs['hitbox1'] = pygame.Rect(obs['pos']['x'], obs['pos']['y'] - obs['gap'], obs['size'][0], obs['size'][1])
        obs['hitbox2'] = pygame.Rect(obs['pos']['x'], obs['pos']['y'] + obs['size'][1] + obs['gap'], obs['size'][0], obs['size'][1])

        obs['coll'] = player['hitbox'].colliderect(obs['hitbox1']) or player['hitbox'].colliderect(obs['hitbox2'])

        if obs['coll']:
            obs['valuable'] = False
            dead = True




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
        
        if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN) and dead:
            init()
    
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            player['dir']['y'] += 1
            if not dead:
                player['vel']['y'] = jump_force
        if event.key == pygame.K_DOWN:
            player['dir']['y'] -= 1
            
        
        if event.key == pygame.K_RIGHT:
            player['dir']['x'] -= 1
        if event.key == pygame.K_LEFT:
            player['dir']['x'] += 1

    return True


def render(delta, screen: pygame.Surface):
    global font, obstacles, points
    screen.fill((255,255,255))

    #render player
    screen.blit(player['image'], (player['pos']['x'], player['pos']['y']))

    #render obstacle
    for obs in obstacles:
        if not obs['hitbox1'] or not obs['hitbox2']:
            continue
        pygame.draw.rect(screen, (255 * obs['coll'], 255, 0), obs['hitbox1'])
        pygame.draw.rect(screen, (255 * obs['coll'], 255, 0), obs['hitbox2'])

    #render text
    text = font.render(str(points), True, (0,0,0))
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
