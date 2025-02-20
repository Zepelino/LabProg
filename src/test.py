import pygame
import sys
import record_manager  # Importa o módulo de gerenciamento de recordes

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu do Jogo")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fontes
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)
tiny_font = pygame.font.Font(None, 36)

# Carrega os recordes do arquivo JSON
records = record_manager.load_records()

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
        draw_text(f"{record['name']}: {record['score']}", tiny_font, BLACK, surface, panel_x + 100, record_y + 20)
        # Botão de exclusão
        delete_button = pygame.Rect(panel_x + 200, record_y, 80, 30)
        draw_button(surface, RED, delete_button.x, delete_button.y, delete_button.width, delete_button.height, "Excluir", WHITE)

        # Verifica se o botão de exclusão foi clicado
        mouse_pos = pygame.mouse.get_pos()
        if delete_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            record_manager.delete_record_by_id(record["id"])  # Deleta o recorde pelo ID
            records = record_manager.load_records()  # Recarrega a lista de recordes
            pygame.time.delay(200)  # Pequeno delay para evitar múltiplos cliques

# Função principal do menu
def main_menu():
    global records  # Permite modificar a lista de recordes

    while True:
        screen.fill(WHITE)
        draw_text("Menu Principal", font, BLACK, screen, (SCREEN_WIDTH - 300) / 2, 100)

        # Botão Jogar
        play_button = pygame.Rect((SCREEN_WIDTH - 300) / 2 - 100, 200, 200, 50)
        draw_button(screen, GREEN, play_button.x, play_button.y, play_button.width, play_button.height, "Jogar", BLACK)

        # Botão Sair
        quit_button = pygame.Rect((SCREEN_WIDTH - 300) / 2 - 100, 300, 200, 50)
        draw_button(screen, RED, quit_button.x, quit_button.y, quit_button.width, quit_button.height, "Sair", BLACK)

        # Desenha o painel de recordes
        draw_records_panel(screen)

        # Verifica eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button.collidepoint(mouse_pos):
                    print("Jogar pressionado!")
                    # Aqui você pode chamar a função que inicia o jogo
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Executa o menu
main_menu()