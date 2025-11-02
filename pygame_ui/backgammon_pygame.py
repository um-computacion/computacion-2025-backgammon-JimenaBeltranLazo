import pygame
import os
import sys

# Añadir la ruta del directorio raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.board import Board
from core.dice import Dice, DiceGameLogic
from core.player import Player
from core.backgammongame import BackgammonGame, TurnManager, MoveManager

class PygameBuilder:
    """
    Builder que encapsula la creación de una instancia de BackgammonGame
    para la interfaz de Pygame.
    """
    def crear_juego(self, nombres: list[str]) -> BackgammonGame:
        """
        Crea y devuelve una instancia completamente funcional de BackgammonGame.

        Args:
            nombres (list[str]): Una lista con los nombres de los dos jugadores.
                                 El primer nombre será para el jugador Blanco,
                                 el segundo para el Negro.

        Returns:
            BackgammonGame: La instancia del juego lista para empezar.
        """
        # 1. Crear jugadores
        jugador_blanco = Player(nombres[0], "Blanco")
        jugador_negro = Player(nombres[1], "Negro")

        # 2. Crear componentes del juego
        tablero = Board()
        dice_logic = DiceGameLogic(Dice())
        turnos = TurnManager(jugador_blanco, jugador_negro)
        movimientos = MoveManager(tablero)

        # 3. Crear y devolver la instancia principal del juego
        game = BackgammonGame(jugador_blanco, jugador_negro, turnos, movimientos, dice_logic)
        
        return game

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
COLOR_HIGHLIGHT = (255, 215, 0) # Dorado para resaltar

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

def draw_checkers(surface, board_state):
    for point_num, checkers_on_point in enumerate(board_state):
        if not checkers_on_point:
            continue
            
        count = len(checkers_on_point)
        player_color = checkers_on_point[0]
            
        x, y_base, direction = get_point_coordinates(point_num + 1) # +1 para ajustar el índice
        if x is None: continue
        
        color = COLOR_BROWN_CHECKER if player_color == 'Negro' else COLOR_WHITE_CHECKER
        for i in range(count):
            y = y_base - (i * CHECKER_RADIUS * 2) if direction == 'down' else y_base + (i * CHECKER_RADIUS * 2)
            pygame.draw.circle(surface, color, (int(x), int(y)), CHECKER_RADIUS)
            pygame.draw.circle(surface, COLOR_OUTER_AREA, (int(x), int(y)), CHECKER_RADIUS, 2)

def draw_bar_checkers(surface, bar_state):
    """ Dibuja las fichas capturadas en la barra central. """
    bar_center_x = MARGIN_SIDES + BOARD_WIDTH / 2
    
    # Fichas blancas (arriba de la barra)
    white_checkers_count = len(bar_state.get("Blanco", []))
    for i in range(white_checkers_count):
        y = MARGIN_TOP + CHECKER_RADIUS + (i * CHECKER_RADIUS * 2)
        pygame.draw.circle(surface, COLOR_WHITE_CHECKER, (int(bar_center_x), int(y)), CHECKER_RADIUS)
        pygame.draw.circle(surface, COLOR_OUTER_AREA, (int(bar_center_x), int(y)), CHECKER_RADIUS, 2)

    # Fichas marrones (abajo de la barra)
    brown_checkers_count = len(bar_state.get("Negro", []))
    for i in range(brown_checkers_count):
        y = WINDOW_HEIGHT - MARGIN_TOP - CHECKER_RADIUS - (i * CHECKER_RADIUS * 2)
        pygame.draw.circle(surface, COLOR_BROWN_CHECKER, (int(bar_center_x), int(y)), CHECKER_RADIUS)
        pygame.draw.circle(surface, COLOR_OUTER_AREA, (int(bar_center_x), int(y)), CHECKER_RADIUS, 2)

def draw_off_checkers(surface, off_state):
    """ Dibuja las fichas que han sido retiradas del tablero. """
    # Fichas blancas retiradas (lado derecho, arriba)
    white_off_count = len(off_state.get("Blanco", []))
    for i in range(white_off_count):
        x = WINDOW_WIDTH - MARGIN_SIDES / 2
        y = MARGIN_TOP + i * (CHECKER_RADIUS * 1.5)
        pygame.draw.circle(surface, COLOR_WHITE_CHECKER, (int(x), int(y)), CHECKER_RADIUS)
        pygame.draw.circle(surface, COLOR_OUTER_AREA, (int(x), int(y)), CHECKER_RADIUS, 2)

    # Fichas marrones retiradas (lado derecho, abajo)
    brown_off_count = len(off_state.get("Negro", []))
    for i in range(brown_off_count):
        x = WINDOW_WIDTH - MARGIN_SIDES / 2
        y = WINDOW_HEIGHT - MARGIN_TOP - i * (CHECKER_RADIUS * 1.5) - CHECKER_RADIUS
        pygame.draw.circle(surface, COLOR_BROWN_CHECKER, (int(x), int(y)), CHECKER_RADIUS)
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

BEAR_OFF_RECTS = {
    "Blanco": pygame.Rect(WINDOW_WIDTH - MARGIN_SIDES, MARGIN_TOP, MARGIN_SIDES, BOARD_HEIGHT / 2),
    "Negro": pygame.Rect(WINDOW_WIDTH - MARGIN_SIDES, MARGIN_TOP + BOARD_HEIGHT / 2, MARGIN_SIDES, BOARD_HEIGHT / 2)
}

def is_bear_off_possible(game):
    """ Verifica si el jugador actual puede empezar a retirar fichas. """
    jugador_actual = game.obtener_jugador_actual()
    if not jugador_actual:
        return False
    
    color = jugador_actual.obtener_color()
    board_state = game.obtener_estado_tablero()
    home_board_indices = range(18, 24) if color == "Blanco" else range(0, 6)
    
    # Comprobar si todas las fichas están en el home board
    total_checkers_in_home = 0
    for i in home_board_indices:
        if board_state[i] and board_state[i][0] == color:
            total_checkers_in_home += len(board_state[i])
            
    # Sumar fichas ya retiradas
    total_checkers_in_home += len(game.obtener_estado_retiradas().get(color, []))

    return total_checkers_in_home == 15 # Un total de 15 fichas por jugador

def get_point_from_pos(pos):
    """ Convierte una posición (x, y) del ratón en un número de punto (1-24). """
    x, y = pos

    # Comprobar si el clic fue en una de las zonas de bear-off
    for color, rect in BEAR_OFF_RECTS.items():
        if rect.collidepoint(pos):
            # Devolver un identificador especial para la zona de bear-off
            return f"bear_off_{color}"

    if not (MARGIN_SIDES < x < WINDOW_WIDTH - MARGIN_SIDES and MARGIN_TOP < y < WINDOW_HEIGHT - MARGIN_TOP):
        return None

    # Ajustar x para tener en cuenta la barra central
    bar_center_x = MARGIN_SIDES + (BOARD_WIDTH - BAR_WIDTH) / 2
    if x > bar_center_x + BAR_WIDTH:
        x -= BAR_WIDTH
    
    col = int((x - MARGIN_SIDES) / POINT_WIDTH)

    # Mitad superior (puntos 13-24)
    if y < WINDOW_HEIGHT / 2:
        if col < 6: return 24 - col
        else: return 18 - (col - 6)
    # Mitad inferior (puntos 1-12)
    else:
        if col < 6: return col + 1
        else: return col + 7
    return None

def handle_mouse_click(pos, game, selected_point):
    """ Gestiona la lógica de selección y movimiento de fichas, incluyendo la barra. """
    jugador_actual = game.obtener_jugador_actual()
    if not jugador_actual:
        return selected_point, []

    color_jugador = jugador_actual.obtener_color()
    bar_state = game.obtener_estado_barra()
    
    clicked_point_or_area = get_point_from_pos(pos)
    if clicked_point_or_area is None:
        return None, [] # Clic fuera, deseleccionar todo y limpiar movimientos

    # --- Lógica para mover desde la barra ---
    if bar_state.get(color_jugador):
        if isinstance(clicked_point_or_area, int):
            destino_idx = clicked_point_or_area - 1
            dado_valor = -1

            if color_jugador == "Blanco":
                dado_valor = destino_idx + 1
            else: # "Negro"
                dado_valor = 25 - (destino_idx + 1)
            
            try:
                # La lógica de validación del dado está dentro de ejecutar_movimiento_barra
                game.ejecutar_movimiento_barra(destino_idx, color_jugador, dado_valor)
                print(f"Ficha de la barra movida a punto {clicked_point_or_area}")
            except Exception as e:
                print(f"Error al mover desde la barra: {e}")
        
        return None, [] # Deseleccionar después de intentar mover desde la barra

    # --- Lógica de selección y movimiento normal ---
    if selected_point is None:
        # Si no hay punto seleccionado, el clic actual intenta seleccionar uno
        if isinstance(clicked_point_or_area, int):
            casilla = game.obtener_estado_tablero()[clicked_point_or_area - 1]
            if casilla and casilla[0] == color_jugador:
                possible_moves = get_possible_moves(game, clicked_point_or_area)
                if possible_moves:
                    print(f"Punto de origen seleccionado: {clicked_point_or_area}")
                    print(f"Movimientos posibles: {possible_moves}")
                    return clicked_point_or_area, possible_moves
                else:
                    print(f"El punto {clicked_point_or_area} no tiene movimientos válidos.")
                    return None, []
    else:
        # Si ya hay un punto seleccionado, el clic actual es el destino
        
        # --- Bear-Off ---
        if isinstance(clicked_point_or_area, str) and clicked_point_or_area == f"bear_off_{color_jugador}":
            if is_bear_off_possible(game):
                casilla_idx = selected_point - 1
                dado_necesario = -1
                if color_jugador == "Blanco":
                    dado_necesario = 24 - casilla_idx
                else: # Negro
                    dado_necesario = casilla_idx + 1
                
                try:
                    game.ejecutar_retiro(casilla_idx, dado_necesario, color_jugador)
                    print(f"Ficha retirada del punto {selected_point}")
                except Exception as e:
                    print(f"Error al retirar la ficha: {e}")
            else:
                print("Aún no puedes retirar fichas.")
            return None, [] # Deseleccionar
            
        # --- Movimiento a otro punto ---
        if isinstance(clicked_point_or_area, int):
            distancia = abs(clicked_point_or_area - selected_point)
            
            try:
                game.ejecutar_movimiento(selected_point - 1, clicked_point_or_area - 1, color_jugador, distancia)
                print(f"Movimiento de {selected_point} a {clicked_point_or_area}")
            except Exception as e:
                print(f"Error al mover: {e}")
            
            return None, [] # Deseleccionar y limpiar movimientos

    return None, [] # Si no se hizo nada, deseleccionar

def get_possible_moves(game, start_point_num):
    """
    Calcula los posibles puntos de destino para una ficha seleccionada.
    """
    if start_point_num is None:
        return []

    jugador_actual = game.obtener_jugador_actual()
    color_jugador = jugador_actual.obtener_color()
    available_dice = game.obtener_valores_dados() # Asume que esto devuelve los dados disponibles
    
    possible_dests = []
    for die_value in set(available_dice): # Usa set para evitar duplicados si los dados son iguales
        if color_jugador == "Blanco":
            dest_point = start_point_num + die_value
        else: # Negro
            dest_point = start_point_num - die_value
        
        # Valida que el destino esté dentro del tablero (1-24)
        if 1 <= dest_point <= 24:
            # Aquí debería haber una validación más robusta llamando a la lógica del core,
            # pero por ahora simulamos la comprobación básica.
            # Por ejemplo, game.es_movimiento_valido(start_point_num - 1, dest_point - 1)
            possible_dests.append(dest_point)
            
    # Lógica para bear-off
    if is_bear_off_possible(game):
        home_board_start = 19 if color_jugador == "Blanco" else 1
        home_board_end = 24 if color_jugador == "Blanco" else 6
        
        if home_board_start <= start_point_num <= home_board_end:
            for die_value in set(available_dice):
                if color_jugador == "Blanco" and start_point_num + die_value > 24:
                    possible_dests.append(f"bear_off_{color_jugador}")
                elif color_jugador == "Negro" and start_point_num - die_value < 1:
                    possible_dests.append(f"bear_off_{color_jugador}")

    return list(set(possible_dests)) # Elimina duplicados si el bear-off se añade más de una vez

def get_point_rect(point_num):
    """ Devuelve un Rect para un punto específico, útil para dibujar resaltados. """
    x, y_base, direction = get_point_coordinates(point_num)
    if x is None:
        return None
    
    height = TRIANGLE_HEIGHT
    y = MARGIN_TOP if direction == 'up' else WINDOW_HEIGHT - MARGIN_TOP - height
    
    return pygame.Rect(x - POINT_WIDTH / 2, y, POINT_WIDTH, height)

def draw_highlights(surface, possible_moves, color_jugador):
    """ Dibuja un resaltado en los posibles puntos de destino. """
    if not possible_moves:
        return

    highlight_surface = pygame.Surface((POINT_WIDTH, TRIANGLE_HEIGHT), pygame.SRCALPHA)
    highlight_surface.fill((*COLOR_HIGHLIGHT, 100)) # Usa el color de resaltado con alpha

    for move in possible_moves:
        if isinstance(move, int):
            rect = get_point_rect(move)
            if rect:
                surface.blit(highlight_surface, rect.topleft)
        elif isinstance(move, str) and move.startswith("bear_off"):
             # Resalta la zona de bear-off correspondiente
            bear_off_rect = BEAR_OFF_RECTS[color_jugador]
            # Crea una superficie separada para el resaltado del bear-off
            bear_off_highlight = pygame.Surface(bear_off_rect.size, pygame.SRCALPHA)
            bear_off_highlight.fill((*COLOR_HIGHLIGHT, 100))
            surface.blit(bear_off_highlight, bear_off_rect.topleft)

# --- Estados del Juego ---
GAME_STATE_START_SCREEN = "start_screen"
GAME_STATE_WAITING_FOR_ROLL = "waiting_for_roll"
GAME_STATE_PLAYER_MOVE = "player_move"
GAME_STATE_GAME_OVER = "game_over"

# --- Elementos Interactivos ---
roll_dice_button = pygame.Rect(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT - 45, 200, 40)


# --- Bucle Principal del Juego ---
def run_pygame_app():
    pygame.init()
    center_window()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Backgammon")
    font = pygame.font.Font(None, 30)

    game_state = GAME_STATE_START_SCREEN
    game = None
    brown_player_name, white_player_name = "", ""
    selected_point = None
    possible_moves = []
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == GAME_STATE_WAITING_FOR_ROLL:
                    if roll_dice_button.collidepoint(mouse_pos):
                        game.tirar_dados_turno_actual()
                        print(f"Dados tirados: {game.obtener_valores_dados()}")
                        game_state = GAME_STATE_PLAYER_MOVE
                
                elif game_state == GAME_STATE_PLAYER_MOVE:
                    selected_point, possible_moves = handle_mouse_click(event.pos, game, selected_point)

        # --- Lógica de Transición de Estados ---
        if game_state == GAME_STATE_START_SCREEN:
            # La función start_screen es bloqueante, devuelve los nombres cuando termina.
            brown_player_name, white_player_name = start_screen(screen)
            
            # Bucle para manejar la tirada inicial hasta que no haya empate.
            jugador_inicial = None
            while jugador_inicial is None:
                builder = PygameBuilder()
                game = builder.crear_juego([white_player_name, brown_player_name])
                dado_blanco, dado_negro = game.tirar_dados_primer_turno()
                
                # Muestra la tirada inicial en la pantalla
                screen.fill(COLOR_OUTER_AREA)
                draw_text(screen, f"Tirada inicial:", font, COLOR_TEXT, WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50, center=True)
                draw_text(screen, f"{white_player_name} (Blanco): {dado_blanco}", font, COLOR_TEXT, WINDOW_WIDTH/2, WINDOW_HEIGHT/2, center=True)
                draw_text(screen, f"{brown_player_name} (Negro): {dado_negro}", font, COLOR_TEXT, WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50, center=True)
                pygame.display.flip()
                
                jugador_inicial = game.obtener_jugador_actual()
                
                if jugador_inicial is None:
                    draw_text(screen, "¡Empate! Volviendo a lanzar...", font, COLOR_HIGHLIGHT, WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 100, center=True)
                    pygame.display.flip()
                    pygame.time.wait(2000)

            print(f"El jugador inicial es: {jugador_inicial.obtener_nombre()}")
            game_state = GAME_STATE_WAITING_FOR_ROLL

        elif game_state == GAME_STATE_PLAYER_MOVE:
            # Comprueba si el jugador ha agotado sus movimientos
            if game.movimientos_restantes_count() == 0:
                game.cambiar_turno()
                game_state = GAME_STATE_WAITING_FOR_ROLL
                print("-" * 20)
                print(f"Turno de {game.obtener_jugador_actual().obtener_nombre()}. Lanza los dados.")
                selected_point = None
        
        # --- Dibujado ---
        if game_state != GAME_STATE_START_SCREEN:
            screen.fill(COLOR_OUTER_AREA)
            draw_board(screen)
            draw_triangles(screen)
            
            # Dibuja los resaltados ANTES que las fichas
            if possible_moves:
                draw_highlights(screen, possible_moves, game.obtener_jugador_actual().obtener_color())
            
            draw_checkers(screen, game.obtener_estado_tablero())
            draw_bar_checkers(screen, game.obtener_estado_barra())
            draw_off_checkers(screen, game.obtener_estado_retiradas())
            
            if game.obtener_valores_dados():
                draw_dice(screen, game.obtener_valores_dados())

            # Resaltar el nombre del jugador actual
            jugador_actual = game.obtener_jugador_actual()
            jugador_actual_nombre = jugador_actual.obtener_nombre() if jugador_actual else ""
            brown_color = COLOR_HIGHLIGHT if jugador_actual_nombre == brown_player_name else COLOR_TEXT
            white_color = COLOR_HIGHLIGHT if jugador_actual_nombre == white_player_name else COLOR_TEXT
            
            draw_text(screen, f"Marrón: {brown_player_name}", font, brown_color, MARGIN_SIDES, 20)
            draw_text(screen, f"Blanco: {white_player_name}", font, white_color, MARGIN_SIDES, WINDOW_HEIGHT - 40)

            if game_state == GAME_STATE_WAITING_FOR_ROLL:
                # Dibuja el botón de tirar dados
                btn_color = COLOR_BUTTON_HOVER if roll_dice_button.collidepoint(mouse_pos) else COLOR_BUTTON
                pygame.draw.rect(screen, btn_color, roll_dice_button)
                draw_text(screen, "Tirar Dados", font, COLOR_TEXT, roll_dice_button.centerx, roll_dice_button.centery, center=True)

            pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run_pygame_app()