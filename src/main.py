import pygame
import random
import record_manager

SCREEN_WIDTH = 640 
SCREEN_HEIGHT = 640

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fontes
font = None
small_font = None
tiny_font = None

font = 0

player = {}
gravity = 500
dead = False

STATE = 0 # 0 - Main Menu; 1 - Game; 2 - Death Screen
records = None
record = False


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

input_text = ""  
input_active = False

#funções auxiliares de render

# Função para desenhar texto na tela
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


# Função para criar botões
def draw_button(surface, color, x, y, width, height, text, text_color):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, small_font, text_color, surface, x + width / 2, y + height / 2)


# Função para desenhar o painel de recordes
def draw_records_panel(surface):
    global records  # Usa a variável global records
    panel_width = 300
    panel_height = SCREEN_HEIGHT
    panel_x = SCREEN_WIDTH - panel_width
    panel_y = 0

    # Desenha o fundo do painel
    pygame.draw.rect(surface, GRAY, (panel_x, panel_y, panel_width, panel_height))

    # Título do painel
    draw_text("Recordes", small_font, BLACK, surface, panel_x + panel_width / 2, 50)

    # Desenha cada registro
    for i, record in enumerate(records):
        record_y = 100 + i * 60
        # Nome e pontuação
        draw_text(f"{record['name']}: {record['score']}", small_font, BLACK, surface, panel_x + 100, record_y + 20)
        # Botão de exclusão
        delete_button = pygame.Rect(panel_x + 200, record_y, 35, 35)
        draw_button(surface, RED, delete_button.x, delete_button.y, delete_button.width, delete_button.height, "X", WHITE)

        # Verifica se o botão de exclusão foi clicado
        mouse_pos = pygame.mouse.get_pos()
        if delete_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            record_manager.delete_record_by_id(record["id"])  # Deleta o recorde pelo ID
            records = record_manager.load_records()  # Recarrega a lista de recordes
            pygame.time.delay(200)  # Pequeno delay para evitar múltiplos cliques


# Função para aplicar efeito de blur
def apply_blur(surface, blur_level=2):
    # Reduz a resolução da superfície
    small_surface = pygame.transform.scale(surface, (surface.get_width() // blur_level, surface.get_height() // blur_level))
    # Amplia a superfície de volta ao tamanho original
    return pygame.transform.scale(small_surface, (surface.get_width(), surface.get_height()))


##################################################################################################################################


def new_obstacle():
    global default_obstacle, default_collectable
    new_obs = default_obstacle.copy()
    new_obs['pos'] = {'x': 700, 'y': random.randint(-370, 0)}
    new_obs['size'] = (100, 500)
    new_obs['gap'] = random.randint(80, 150)

    if random.randint(0,100) < 10:
        new_collec = default_collectable.copy()
        new_collec['pos'] = {'x': 850, 'y': random.randint(200, 400)}
        collectables.append(new_collec)
        print("coletável")

    return new_obs


def start_menu():
    global STATE, dead, records, blur_surface

    records = record_manager.load_records()

    STATE = 0
    global dead
    dead = True

    # Cria uma superfície para o efeito de blur
    blur_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    blur_surface.set_alpha(128)  # Define transparência (0 = totalmente transparente, 255 = totalmente opaco)

    #start_game()


def start_game(nome):
    global font, player, obstacles, default_obstacle, dead, points, obs_spawn_timer, STATE, record

    #setting player up
    dead = False
    sprite = pygame.image.load("res\images\jacaré.jpg").convert()
    sprite = pygame.transform.scale(sprite, (64,64))
    player = {
                'name': nome,
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

    #font = pygame.font.Font(None, size=30)

    record = False

    STATE = 1

def die():
    global dead, player, points, STATE, record
    dead = True
    player['vel']['y'] = player['jump_force']

    #conversar com o módulo de pontuação
    record = record_manager.add_or_update_record(player['name'], points)

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


    if player['pos']['y'] < 0 or player['pos']['y'] > 640 - player['size'][1]:
        die()

    

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
    
    if STATE == 0:
        global input_text, input_active
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if play_button.collidepoint(mouse_pos):
                start_game(input_text)
            if quit_button.collidepoint(mouse_pos):
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = event.pos
                # Verifica se o campo de texto foi clicado
                if input_rect.collidepoint(mouse_pos):
                    input_active = True
                else:
                    input_active = False
                # Verifica se o botão "Jogar" foi clicado
        
        #print(event.type)
        if event.type == pygame.KEYDOWN and input_active:
            # Captura as teclas pressionadas
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]  # Remove o último caractere
            else:
                input_text += event.unicode  # Adiciona o caractere digitado
    

    if STATE == 2:
        if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if menu_button.collidepoint(mouse_pos):
                    start_menu()
                    

    if STATE == 1 or STATE == 2:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player['dir']['y'] -= 1
            if event.key == pygame.K_DOWN:
                player['dir']['y'] += 1
            
            if event.key == pygame.K_RIGHT:
                player['dir']['x'] += 1
            if event.key == pygame.K_LEFT:
                player['dir']['x'] -= 1
            
            if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN) and STATE == 2:
                start_game(player['name'])
        
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
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
    #global font, obstacles, collectables, points
    screen.fill((255,255,255))

    if STATE == 1 or STATE == 2:

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

    if STATE == 1:
        text = font.render(str(points), True, (0,0,0))
        trect = text.get_rect()
        trect.center = (SCREEN_WIDTH/2, 50)
        screen.blit(text, trect)
    
    if STATE == 2:
        global blur_surface

        blurred_screen = apply_blur(screen, blur_level=8)  # Nível de blur (quanto maior, mais desfocado)

        # Desenha a superfície com blur na tela
        blur_surface.blit(blurred_screen, (0, 0))
        screen.blit(blur_surface, (0, 0))

        
        draw_text("Você MORREU!", small_font, BLACK, screen, SCREEN_WIDTH/2, 230)
        #text = font.render("Você MORREU!", True, (0,0,0))
        #trect = text.get_rect()
        #trect.center = (SCREEN_WIDTH/2, 270)
        #screen.blit(text, trect)

        #pontos
        draw_text(str(points), font, BLACK, screen, SCREEN_WIDTH/2, 320)
        #text = font.render(str(points), True, (0,0,0))
        #trect = text.get_rect()
        #trect.center = (SCREEN_WIDTH/2, 330)
        #screen.blit(text, trect)

        if record:
            draw_text(f"NOVO RECORD! Parabéns, {player['name']}!", tiny_font, BLACK, screen, SCREEN_WIDTH/2, 280)
            #text = font.render(f"NOVO RECORD! Parabéns, {player['name']}!", True, (0,0,0))
            #trect = text.get_rect()
            #trect.center = (SCREEN_WIDTH/2, 310)
            #screen.blit(text, trect)
        
        global menu_button

        # Botão menu
        menu_button = pygame.Rect((SCREEN_WIDTH) / 2 - 150, SCREEN_HEIGHT-80, 300, 50)
        draw_button(screen, BLUE, menu_button.x, menu_button.y, menu_button.width, menu_button.height, "Menu Principal", BLACK)

    if STATE == 0:
        global play_button, quit_button
        draw_text("Flappito", font, BLACK, screen, (SCREEN_WIDTH - 300) / 2, 100)

        # Campo de entrada de texto
        global input_rect
        # Título do campo de entrada de texto
        draw_text("Insira seu nickname", tiny_font, BLACK, screen, (SCREEN_WIDTH - 300) / 2, 170)
        input_rect = pygame.Rect((SCREEN_WIDTH - 300) / 2 - 100, 180, 200, 40)
        pygame.draw.rect(screen, (255*input_active, 255*input_active, 0), input_rect, 2)  # Desenha o retângulo do campo de texto
        draw_text(input_text, small_font, BLACK, screen, input_rect.x + input_rect.width / 2, input_rect.y + input_rect.height / 2)

        # Botão Jogar
        play_button = pygame.Rect((SCREEN_WIDTH - 300) / 2 - 100, 250, 200, 50)
        draw_button(screen, GREEN, play_button.x, play_button.y, play_button.width, play_button.height, "Jogar", BLACK)

        # Botão Sair
        quit_button = pygame.Rect((SCREEN_WIDTH - 300) / 2 - 100, 350, 200, 50)
        draw_button(screen, RED, quit_button.x, quit_button.y, quit_button.width, quit_button.height, "Sair", BLACK)

        # Desenha o painel de recordes
        draw_records_panel(screen)

    #show everything on screen
    pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    running = True
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    delta_time = 0.1

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    tiny_font = pygame.font.Font(None, 18)

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
