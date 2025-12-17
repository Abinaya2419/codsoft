import pygame
import sys
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

CELL = 100
OFFSET = 50

EMPTY = None
HUMAN = 'X'
AI = 'O'

board = [[EMPTY]*3 for _ in range(3)]
game_over = False
winner = None

def draw_board():
    screen.fill(BLACK)

    for i in range(1, 3):
        pygame.draw.line(screen, WHITE, (OFFSET + i * CELL, OFFSET), (OFFSET + i * CELL, OFFSET + 3 * CELL), 3)
        pygame.draw.line(screen, WHITE, (OFFSET, OFFSET + i * CELL), (OFFSET + 3 * CELL, OFFSET + i * CELL), 3)

    for r in range(3):
        for c in range(3):
            mark = board[r][c]
            if mark:
                text = big_font.render(mark, True, WHITE)
                screen.blit(text, (OFFSET + c * CELL + 30, OFFSET + r * CELL + 20))

            if game_over:
                if winner == AI:
                    msg = "Game Over -  AI Wins!"
                elif winner == HUMAN:
                    msg = "Game Over - You Win!"
                else:
                    msg = "Game Over - It's a Draw!"
                    
                label = font.render(msg, True, WHITE)
                screen.blit(label, (80, 10))

                pygame.draw.rect(screen, WHITE, (120, 390, 160, 40), 2)
                btn = font.render("Play Again", True, WHITE)
                screen.blit(btn, (135, 400))

    pygame.display.flip()

def check_state():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
        
        if board[0][0] == board[1][1] == board[2][2] != EMPTY:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != EMPTY:
            return board[0][2]
        
        filled = all(board[r][c] for r in range(3) for c in range(3))

        if filled:
            return "Draw"
        
        return None
    
def minimax(turn):
    result = check_state()
    if result == AI:
        return 1
    elif result == HUMAN:
        return -1
    elif result == "Draw":
        return 0
    
    if turn == AI:
        best = -math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = AI
                    score = minimax(HUMAN)
                    board[r][c] = EMPTY
                    best = max(best, score)
        return best
    else:
        worst = math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = HUMAN
                    score = minimax(AI)
                    board[r][c] = EMPTY
                    worst = min(worst, score)
        return worst

def ai_move():
    best_score = -math.inf
    move = None

    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                board[r][c] = AI
                score = minimax(HUMAN)
                board[r][c] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (r, c)
    if move:
        board[move[0]][move[1]] = AI
    
def reset_game():
    global board, game_over, winner
    board = [[EMPTY]*3 for _ in range(3)]
    game_over = False
    winner = None

while True:
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()

            if game_over and 120 <= x <= 280 and 390 <= y <= 430:
                reset_game()
                continue
            
            if not game_over:
                r = (y - OFFSET) // CELL
                c = (x - OFFSET) // CELL

                if 0 <= r < 3 and 0 <= c < 3 and board[r][c] == EMPTY:
                    board[r][c] = HUMAN
                    state = check_state()
                    if state:
                        game_over = True
                        winner = state
                    else:
                        ai_move()
                        state = check_state()
                        if state:
                            game_over = True
                            winner = state