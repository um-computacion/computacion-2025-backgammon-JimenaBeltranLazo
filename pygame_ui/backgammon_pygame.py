import pygame
import os
import random

# --- Constantes ---

# Dimensiones de la ventana
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

# Paleta de colores
COLOR_BACKGROUND = (47, 47, 47) # #2f2f2f
COLOR_LIGHT_TRIANGLE = (248, 248, 248)
COLOR_DARK_TRIANGLE = (122, 49, 8)
COLOR_WHITE_CHECKER = (242, 233, 208) # #f2e9d0
COLOR_BROWN_CHECKER = (64, 25, 12)
COLOR_BOARD_BORDER = (154, 106, 58)
COLOR_CENTER_BAR = (154, 106, 58)
COLOR_OUTER_AREA = (30, 30, 30)
COLOR_TEXT = (255, 255, 255)
COLOR_INPUT_BG = (60, 60, 60)
COLOR_BUTTON = (100, 100, 100)
COLOR_BUTTON_HOVER = (130, 130, 130)
COLOR_DICE = (240, 240, 240)
COLOR_PIP = (10, 10, 10)

# --- Dimensiones del Tablero ---
MARGIN_TOP = 50
MARGIN_SIDES = 50
BOARD_WIDTH = WINDOW_WIDTH - MARGIN_SIDES * 2
BOARD_HEIGHT = WINDOW_HEIGHT - MARGIN_TOP * 2
BAR_WIDTH = 60
# Con WINDOW_HEIGHT = 700, BOARD_HEIGHT es 600.
# Mantenemos el mismo tamaño de triángulo para que las fichas quepan.
TRIANGLE_HEIGHT = 250 
POINT_WIDTH = (BOARD_WIDTH - BAR_WIDTH) / 12
# Con TRIANGLE_HEIGHT = 250, 5 fichas necesitan un diámetro de 50 (radio 25).
CHECKER_RADIUS = 25
DICE_SIZE = 40
PIP_RADIUS = 4
DOUBLING_CUBE_SIZE = 50

# --- Posiciones Iniciales ---
initial_positions = {
    24: ('black', 2),
    19: ('white', 5),
    17: ('white', 3),
    13: ('black', 5),
    12: ('white', 5),
    8:  ('black', 3),
    6:  ('black', 5),
    1:  ('white', 2),
}

# --- Funciones de Utilidad ---

def center_window():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

def draw_text(surface, text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center: text_rect.center = (x, y)
    else: text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# --- Funciones de Dibujo del Juego ---

def draw_board(surface):
    board_rect = pygame.Rect(MARGIN_SIDES, MARGIN_TOP, BOARD_WIDTH, BOARD_HEIGHT)
    pygame.draw.rect(surface, COLOR_BACKGROUND, board_rect)
    bar_rect = pygame.Rect(MARGIN_SIDES + (BOARD_WIDTH - BAR_WIDTH) / 2, MARGIN_TOP, BAR_WIDTH, BOARD_HEIGHT)
    pygame.draw.rect(surface, COLOR_CENTER_BAR, bar_rect)
    pygame.draw.rect(surface, COLOR_BOARD_BORDER, board_rect, 5)

def draw_triangles(surface):
    for i in range(12):
        color = COLOR_LIGHT_TRIANGLE if i % 2 == 0 else COLOR_DARK_TRIANGLE
        base_x = MARGIN_SIDES + i * POINT_WIDTH
        if i >= 6: base_x += BAR_WIDTH
        
        # Triángulos superiores (apuntando hacia abajo)
        pygame.draw.polygon(surface, color, [
            (base_x + POINT_WIDTH / 2, MARGIN_TOP + TRIANGLE_HEIGHT), # Punta
            (base_x, MARGIN_TOP),                                     # Base izquierda
            (base_x + POINT_WIDTH, MARGIN_TOP)                        # Base derecha
        ])
        
        color = COLOR_DARK_TRIANGLE if i % 2 == 0 else COLOR_LIGHT_TRIANGLE
        # Triángulos inferiores (apuntando hacia arriba)
        pygame.draw.polygon(surface, color, [
            (base_x + POINT_WIDTH / 2, WINDOW_HEIGHT - MARGIN_TOP - TRIANGLE_HEIGHT), # Punta
            (base_x, WINDOW_HEIGHT - MARGIN_TOP),                                     # Base izquierda
            (base_x + POINT_WIDTH, WINDOW_HEIGHT - MARGIN_TOP)                        # Base derecha
        ])

def get_point_coordinates(point_num):
    """ Convierte un número de punto (1-24) a coordenadas en la pantalla. """
    i = -1
    # Mapea el número de punto a un índice de dibujo 'i' (de 0 a 11).
    if 1 <= point_num <= 6:       # Inferior izquierdo
        i = point_num - 1
    elif 7 <= point_num <= 12:      # Inferior derecho
        i = point_num - 1
    elif 13 <= point_num <= 18:     # Superior derecho
        i = 18 - point_num + 6
    elif 19 <= point_num <= 24:     # Superior izquierdo
        i = 24 - point_num
    else:
        return None, None, None

    # Determina la coordenada Y y la dirección de apilamiento según la fila.
    if 1 <= point_num <= 12:
        base_y, direction = WINDOW_HEIGHT - MARGIN_TOP - CHECKER_RADIUS, 'down'
    else: # 13 a 24
        base_y, direction = MARGIN_TOP + CHECKER_RADIUS, 'up'
    
    # Calcula la coordenada X basándose en el índice 'i', igual que al dibujar los triángulos.
    x = MARGIN_SIDES + i * POINT_WIDTH + (POINT_WIDTH / 2)
    if i >= 6:
        x += BAR_WIDTH

    return x, base_y, direction

def draw_checkers(surface, positions):
    for point, (player, count) in positions.items():
        x, y_base, direction = get_point_coordinates(point)
        if x is None: continue
        color = COLOR_BROWN_CHECKER if player == 'black' else COLOR_WHITE_CHECKER
        for i in range(count):
            y = y_base - (i * CHECKER_RADIUS * 2) if direction == 'down' else y_base + (i * CHECKER_RADIUS * 2)
            pygame.draw.circle(surface, color, (int(x), int(y)), CHECKER_RADIUS)
            pygame.draw.circle(surface, COLOR_OUTER_AREA, (int(x), int(y)), CHECKER_RADIUS, 2)

def draw_single_die(surface, value, x, y):
    die_rect = pygame.Rect(x, y, DICE_SIZE, DICE_SIZE)
    pygame.draw.rect(surface, COLOR_DICE, die_rect, border_radius=5)
    
    positions = {
        1: [(0.5, 0.5)],
        2: [(0.25, 0.25), (0.75, 0.75)],
        3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
        4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
        5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
        6: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.5), (0.75, 0.5), (0.25, 0.75), (0.75, 0.75)]
    }
    if value in positions:
        for (px, py) in positions[value]:
            pygame.draw.circle(surface, COLOR_PIP, (int(x + px * DICE_SIZE), int(y + py * DICE_SIZE)), PIP_RADIUS)

def draw_dice(surface, values):
    x_pos = WINDOW_WIDTH - MARGIN_SIDES + 10
    draw_single_die(surface, values[0], x_pos, WINDOW_HEIGHT / 2 - DICE_SIZE - 5)
    draw_single_die(surface, values[1], x_pos, WINDOW_HEIGHT / 2 + 5)

def draw_doubling_cube(surface):
    cube_x = WINDOW_WIDTH - MARGIN_SIDES + 5
    cube_y = WINDOW_HEIGHT / 2 - DOUBLING_CUBE_SIZE / 2 - 100
    cube_rect = pygame.Rect(cube_x, cube_y, DOUBLING_CUBE_SIZE, DOUBLING_CUBE_SIZE)
    pygame.draw.rect(surface, COLOR_DICE, cube_rect, border_radius=8)
    font = pygame.font.Font(None, 40)
    draw_text(surface, "64", font, COLOR_PIP, cube_rect.centerx, cube_rect.centery, center=True)

# --- Pantalla de Inicio ---
def start_screen(screen):
    font_title = pygame.font.Font(None, 74)
    font_input = pygame.font.Font(None, 32)
    player1_name, player2_name, active_box, player1_starts_as_brown = "", "", None, True

    input_box1 = pygame.Rect(WINDOW_WIDTH/2-150, 200, 300, 40); input_box2 = pygame.Rect(WINDOW_WIDTH/2-150, 280, 300, 40)
    color_button = pygame.Rect(WINDOW_WIDTH/2-150, 360, 300, 40); start_button = pygame.Rect(WINDOW_WIDTH/2-100, 440, 200, 50)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos): active_box = 1
                elif input_box2.collidepoint(event.pos): active_box = 2
                elif color_button.collidepoint(event.pos): player1_starts_as_brown = not player1_starts_as_brown
                elif start_button.collidepoint(event.pos):
                    p1 = player1_name or ("Jugador Marrón" if player1_starts_as_brown else "Jugador Blanco")
                    p2 = player2_name or ("Jugador Blanco" if player1_starts_as_brown else "Jugador Marrón")
                    return (p1, p2) if player1_starts_as_brown else (p2, p1)
                else: active_box = None
            if event.type == pygame.KEYDOWN and active_box:
                if event.key == pygame.K_BACKSPACE:
                    if active_box==1: player1_name = player1_name[:-1]
                    else: player2_name = player2_name[:-1]
                else:
                    if active_box==1: player1_name += event.unicode
                    else: player2_name += event.unicode
        
        screen.fill(COLOR_OUTER_AREA)
        draw_text(screen, "Backgammon", font_title, COLOR_TEXT, WINDOW_WIDTH/2, 100, center=True)
        draw_text(screen, "Jugador 1:", font_input, COLOR_TEXT, input_box1.x, input_box1.y-30)
        pygame.draw.rect(screen, COLOR_INPUT_BG, input_box1); draw_text(screen, player1_name, font_input, COLOR_TEXT, input_box1.x+5, input_box1.y+10)
        draw_text(screen, "Jugador 2:", font_input, COLOR_TEXT, input_box2.x, input_box2.y-30)
        pygame.draw.rect(screen, COLOR_INPUT_BG, input_box2); draw_text(screen, player2_name, font_input, COLOR_TEXT, input_box2.x+5, input_box2.y+10)
        
        color_text = "Jugador 1 es Marrón" if player1_starts_as_brown else "Jugador 1 es Blanco"
        pygame.draw.rect(screen, COLOR_BUTTON_HOVER if color_button.collidepoint(mouse_pos) else COLOR_BUTTON, color_button)
        draw_text(screen, color_text, font_input, COLOR_TEXT, color_button.centerx, color_button.centery, center=True)
        pygame.draw.rect(screen, COLOR_BUTTON_HOVER if start_button.collidepoint(mouse_pos) else COLOR_BUTTON, start_button)
        draw_text(screen, "Comenzar", font_input, COLOR_TEXT, start_button.centerx, start_button.centery, center=True)
        
        pygame.display.flip()

# --- Bucle Principal del Juego ---
def run_pygame_app():
    pygame.init()
    center_window()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Backgammon")

    brown_player_name, white_player_name = start_screen(screen)
    
    positions = initial_positions.copy()
    dice = [1, 1]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    dice = [random.randint(1, 6), random.randint(1, 6)]
                    print(f"Dados tirados: {dice}")

        screen.fill(COLOR_OUTER_AREA)
        draw_board(screen)
        draw_triangles(screen)
        draw_checkers(screen, positions)
        draw_dice(screen, dice)
        # draw_doubling_cube(screen) # Eliminado según feedback
        
        font = pygame.font.Font(None, 30)
        draw_text(screen, f"Marrón: {brown_player_name}", font, COLOR_TEXT, MARGIN_SIDES, 20)
        draw_text(screen, f"Blanco: {white_player_name}", font, COLOR_TEXT, MARGIN_SIDES, WINDOW_HEIGHT - 40)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_pygame_app()