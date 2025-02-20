import pygame
import random
import record_manager

font = 0

player = {}
gravity = 500
dead = False

STATE = 0 # 0 - Main Menu; 1 - Game; 2 - Death Screen

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

default_collectable = {
                'image': None,
                'pos': {'x': 700, 'y': 0},
                'x_vel': 250,
                'size': (64, 64),
                'hitbox': 0,
                'valuable': True,
            }

obstacles = []
collectables = []

obs_spawn_timer = 3.5

points = 0

def new_obstacle():
    global default_obstacle, default_collectable
    new_obs = default_obstacle.copy()
    new_obs['pos'] = {'x': 700, 'y': random.randint(-370, 0)}
    new_obs['size'] = (100, 500)
    new_obs['gap'] = random.randint(80, 150)

    if random.randint(0,100) < 30:
        new_collec = default_collectable.copy()
        new_collec['pos'] = {'x': 850, 'y': random.randint(200, 400)}
        collectables.append(new_collec)
        print("coletável")

    return new_obs


def start_menu():
    global dead
    dead = True


def start_game():
    global font, player, obstacles, default_obstacle, dead, points, obs_spawn_timer

    #setting player up
    dead = False
    sprite = pygame.image.load("res\images\jacaré.jpg").convert()
    sprite = pygame.transform.scale(sprite, (64,64))
    player = {
                'name': 'adalberto',
                'image': sprite,
                'pos': {'x': 50, 'y': 296},
                'vel': {'x': 0, 'y': -350},
                'dir': {'x': 0, 'y': 0},
                'size': sprite.get_size(),
                'hitbox': 0,
                'jump_force': -350
            }

    #setting obstacle up
    obstacles = []
    obstacles.append(new_obstacle())

    points = 0
    obs_spawn_timer = 3.5

    font = pygame.font.Font(None, size=30)

    STATE = 1

def die():
    global dead, player, points
    dead = True
    player['vel']['y'] = player['jump_force']

    record_manager.add_record(player['name'], points)
    #conversar com o módulo de pontuação

    STATE = 2

def process(delta):
    global player, obstacles, collectables, obs_spawn_timer, default_obstacle, points

    if STATE == 1 or STATE == 2:
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
    
    for collec in collectables:
        if dead:
            break

        collec['pos']['x'] -= collec['x_vel'] * delta

        if not collec['valuable'] or collec['pos']['x'] <= -100:
            collectables.remove(collec)

    obs_spawn_timer -= delta
    if obs_spawn_timer <= 0:
        obs_spawn_timer = random.uniform(1.2, 2.5)
        obstacles.append(new_obstacle())
        print(len(obstacles))


    if player['pos']['y'] < 0 or player['pos']['y'] > 640 - player['size'][1]:
        die()

    #print(player['vel'])
    

def physics_process(delta):
    global player, obstacles, collectables, dead, points
    
    if STATE != 1:
        return

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
            die()
    
    for collec in collectables:
        collec['hitbox'] = pygame.Rect(collec['pos']['x'], collec['pos']['y'], collec['size'][0], collec['size'][1])

        coll = player['hitbox'].colliderect(collec['hitbox']) 
        if coll and collec['valuable']:
            collec['valuable'] = False
            points += 3
        





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
            start_game()
    
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            player['dir']['y'] += 1
            if not dead:
                player['vel']['y'] = player['jump_force']
        if event.key == pygame.K_DOWN:
            player['dir']['y'] -= 1
            
        
        if event.key == pygame.K_RIGHT:
            player['dir']['x'] -= 1
        if event.key == pygame.K_LEFT:
            player['dir']['x'] += 1

    return True


def render(delta, screen: pygame.Surface):
    global font, obstacles, collectables, points
    screen.fill((255,255,255))

    #render obstacle
    for obs in obstacles:
        if not obs['hitbox1'] or not obs['hitbox2']:
            continue
        pygame.draw.rect(screen, (255 * obs['coll'], 255, 0), obs['hitbox1'])
        pygame.draw.rect(screen, (255 * obs['coll'], 255, 0), obs['hitbox2'])
    
    for collec in collectables:
        if not collec['hitbox']:
            continue
        pygame.draw.rect(screen, (0, 255, 255), collec['hitbox'])

    #render player
    screen.blit(player['image'], (player['pos']['x'], player['pos']['y']))

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

    start_menu()
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
