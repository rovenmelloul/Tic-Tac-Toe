
import pygame
import random
import sys

# ---------- Config ----------
WIDTH, HEIGHT = 480, 600  # space of the board
FPS = 60
LINE_COLOR = (200, 200, 200)
BG_COLOR = (18, 18, 24)
CELL_BG = (28, 28, 34)
X_COLOR = (220, 80, 80)
O_COLOR = (80, 160, 220)
TEXT_COLOR = (230, 230, 230)
BUTTON_COLOR = (60, 160, 80)
BUTTON_TEXT = (255, 255, 255)

CELL_SIZE = WIDTH // 3
BOARD_TOP = 40

# IA delay (milliseconds)
IA_DELAY_MS = 500
IA_EVENT = pygame.USEREVENT + 1

# ---------- Game state (same logic as ton code) ----------
case_empty = " "
board = [case_empty for _ in range(9)]
symboles = ("X", "O")  # (emoji rendering not reliable in Pygame)
player = symboles[0]   
game_over = False
message = "Ton tour (X)"


# ---------- Helpers (win/draw) ----------
def check_game():
    global message, game_over
    # same win conditions as your code (checks content equal and not empty)
    if case_empty != board[0] == board[1] == board[2] \
    or case_empty != board[3] == board[4] == board[5] \
    or case_empty != board[6] == board[7] == board[8] \
    or case_empty != board[0] == board[3] == board[6] \
    or case_empty != board[1] == board[4] == board[7] \
    or case_empty != board[2] == board[5] == board[8] \
    or case_empty != board[0] == board[4] == board[8] \
    or case_empty != board[2] == board[4] == board[6]:
        message = f"Le joueur {player} gagne la partie !"
        game_over = True
        return True

    if all(cell != case_empty for cell in board):
        message = "Match nul !"
        game_over = True
        return True

    return False



def ia_move():
    free = [i for i, v in enumerate(board) if v == case_empty]
    if not free:
        return False
    return random.choice(free)


# ---------- Pygame drawing helpers ----------
def draw_board(surface, font_large):
    # background
    surface.fill(BG_COLOR)
    # draw 3x3 grid background squares
    for r in range(3):
        for c in range(3):
            rect = pygame.Rect(c * CELL_SIZE, BOARD_TOP + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, CELL_BG, rect)
    # draw grid lines
    for i in range(1, 3):
        pygame.draw.line(surface, LINE_COLOR, (i * CELL_SIZE, BOARD_TOP), (i * CELL_SIZE, BOARD_TOP + 3 * CELL_SIZE), 2)
        pygame.draw.line(surface, LINE_COLOR, (0, BOARD_TOP + i * CELL_SIZE), (WIDTH, BOARD_TOP + i * CELL_SIZE), 2)

    # draw X and O
    padding = 20
    for i, val in enumerate(board):
        if val == case_empty:
            continue
        r = i // 3
        c = i % 3
        center_x = c * CELL_SIZE + CELL_SIZE // 2
        center_y = BOARD_TOP + r * CELL_SIZE + CELL_SIZE // 2
        if val == symboles[0]:  # X
            # draw two lines
            offset = CELL_SIZE // 2 - padding
            pygame.draw.line(surface, X_COLOR, (center_x - offset, center_y - offset),
                             (center_x + offset, center_y + offset), 6)
            pygame.draw.line(surface, X_COLOR, (center_x + offset, center_y - offset),
                             (center_x - offset, center_y + offset), 6)
        else:  # O
            pygame.draw.circle(surface, O_COLOR, (center_x, center_y), CELL_SIZE // 2 - padding, 6)

    # bottom area: message and button
    # Message
    msg_surf = font_small.render(message, True, TEXT_COLOR)
    surface.blit(msg_surf, (20, BOARD_TOP + 3 * CELL_SIZE + 12))

    # Draw "Rejouer" button
    button_rect = pygame.Rect(WIDTH - 120, BOARD_TOP + 3 * CELL_SIZE + 8, 100, 36)
    pygame.draw.rect(surface, BUTTON_COLOR, button_rect, border_radius=6)
    btn_text = font_small.render("Rejouer", True, BUTTON_TEXT)
    btn_pos = (button_rect.centerx - btn_text.get_width() // 2, button_rect.centery - btn_text.get_height() // 2)
    surface.blit(btn_text, btn_pos)
    return button_rect


# ---------- Main ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Morpion - Pygame")
clock = pygame.time.Clock()
font_small = pygame.font.SysFont(None, 26)
font_large = pygame.font.SysFont(None, 48)

# Track if IA timer is scheduled (so we don't schedule multiple)
ia_timer_scheduled = False

def reset_game():
    global board, player, game_over, message, ia_timer_scheduled
    board = [case_empty for _ in range(9)]
    player = symboles[0]
    game_over = False
    message = "Ton tour (X)"
    ia_timer_scheduled = False
    pygame.time.set_timer(IA_EVENT, 0)

reset_game()

running = True
while running:
    clock.tick(FPS)
    button_rect = draw_board(screen, font_large)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            mx, my = event.pos
            # check click on board cells
            if my >= BOARD_TOP and my <= BOARD_TOP + 3 * CELL_SIZE:
                # calculate row/col
                col = mx // CELL_SIZE
                row = (my - BOARD_TOP) // CELL_SIZE
                if 0 <= col < 3 and 0 <= row < 3:
                    idx = row * 3 + col
                    if board[idx] == case_empty and player == symboles[0]:
                        board[idx] = player
                        if check_game():
                            pygame.time.set_timer(IA_EVENT, 0)
                            break
                        # switch player to IA and schedule IA move after delay
                        player = symboles[1]
                        message = "Tour IA..."
                        # set timer for IA_DELAY_MS once
                        pygame.time.set_timer(IA_EVENT, IA_DELAY_MS)
                        ia_timer_scheduled = True
            # check click on "Rejouer"
            if button_rect.collidepoint(event.pos):
                reset_game()

        if event.type == IA_EVENT and not game_over:
            # time to let IA play
            move = ia_move()
            if move is False:
                # board full
                check_game()
                pygame.time.set_timer(IA_EVENT, 0)
                break
            board[move] = player  # IA plays
            # stop IA timer
            pygame.time.set_timer(IA_EVENT, 0)
            ia_timer_scheduled = False
            # check result
            if check_game():
                break
            # switch back to human
            player = symboles[0]
            message = "Ton tour (X)"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over:
            # allow clicking "Rejouer" after game over
            if button_rect.collidepoint(event.pos):
                reset_game()

pygame.quit()
sys.exit()