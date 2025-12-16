import pygame
import sys
from mancala.playAI import PlayAI

pygame.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mancala: AI vs AI")

TITLE_FONT = pygame.font.SysFont('Arial', 32, bold=True)
FONT = pygame.font.SysFont('Arial', 28, bold=True)
LABEL_FONT = pygame.font.SysFont('Arial', 16)
STATUS_FONT = pygame.font.SysFont('Arial', 20)
FPS = 2

WOOD_DARK = (101, 67, 33)
WOOD_LIGHT = (139, 90, 43)
WOOD_BORDER = (70, 47, 25)
PIT_COLOR = (80, 54, 28)
PIT_HIGHLIGHT = (120, 80, 40)
STORE_COLOR = (90, 60, 30)
SEED_COLOR = (210, 180, 140)
SEED_SHADOW = (160, 130, 100)
TEXT_COLOR = (240, 230, 210)
LABEL_COLOR = (200, 190, 170)
AI1_COLOR = (100, 150, 255)
AI2_COLOR = (255, 100, 100)
BACKGROUND = (40, 30, 20)

P1_PITS = ['A','B','C','D','E','F']
P2_PITS = ['G','H','I','J','K','L']
PIT_POSITIONS = {
    'A': (200, 340), 'B': (300, 340), 'C': (400, 340), 'D': (500, 340), 'E': (600, 340), 'F': (700, 340),
    'G': (200, 160), 'H': (300, 160), 'I': (400, 160), 'J': (500, 160), 'K': (600, 160), 'L': (700, 160),
    'C1': (100, 250), 'C2': (800, 250)
}

PIT_RADIUS = 35
STORE_RADIUS = 50

def draw_seeds_in_pit(pos, count, radius):
    """Draw individual seeds inside a pit for visual appeal"""
    if count == 0:
        return
    
    if count <= 8:
        angle_step = 360 / max(count, 1)
        for i in range(count):
            angle = i * angle_step
            offset_x = int((radius - 15) * 0.5 * pygame.math.Vector2(1, 0).rotate(angle).x)
            offset_y = int((radius - 15) * 0.5 * pygame.math.Vector2(1, 0).rotate(angle).y)
            seed_pos = (pos[0] + offset_x, pos[1] + offset_y)
            pygame.draw.circle(WIN, SEED_SHADOW, (seed_pos[0] + 1, seed_pos[1] + 1), 6)
            pygame.draw.circle(WIN, SEED_COLOR, seed_pos, 6)
    else:
        text = FONT.render(str(count), True, TEXT_COLOR)
        text_rect = text.get_rect(center=pos)
        WIN.blit(text, text_rect)

def draw_board(game, current_player='C1'):
    WIN.fill(BACKGROUND)
    
    title = TITLE_FONT.render("MANCALA - AI vs AI", True, TEXT_COLOR)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    
    board_rect = pygame.Rect(75, 120, 750, 300)
    pygame.draw.rect(WIN, WOOD_BORDER, board_rect.inflate(20, 20), border_radius=15)
    pygame.draw.rect(WIN, WOOD_LIGHT, board_rect, border_radius=12)
    
    for i in range(5):
        grain_rect = pygame.Rect(75, 120 + i * 60, 750, 2)
        pygame.draw.rect(WIN, WOOD_DARK, grain_rect)

    board = game.game.state.board

    turn_text = f"{'AI PLAYER 1' if current_player == 'C1' else 'AI PLAYER 2'} TURN"
    turn_color = AI1_COLOR if current_player == 'C1' else AI2_COLOR
    turn_surface = STATUS_FONT.render(turn_text, True, turn_color)
    WIN.blit(turn_surface, (WIDTH // 2 - turn_surface.get_width() // 2, 60))

    for pit, pos in PIT_POSITIONS.items():
        is_store = pit in ['C1', 'C2']
        radius = STORE_RADIUS if is_store else PIT_RADIUS
        
        is_active = (pit == current_player)
        pit_color = PIT_HIGHLIGHT if is_active and is_store else (STORE_COLOR if is_store else PIT_COLOR)
        
        pygame.draw.circle(WIN, WOOD_BORDER, (pos[0] + 3, pos[1] + 3), radius)
        
        pygame.draw.circle(WIN, pit_color, pos, radius)
        pygame.draw.circle(WIN, WOOD_BORDER, pos, radius, 3)
        
        if pit in P1_PITS + P2_PITS:
            count = board[pit]
        else:
            key = 1 if pit == 'C1' else 2
            count = board[key]
        
        if is_store:
            text = FONT.render(str(count), True, TEXT_COLOR)
            text_rect = text.get_rect(center=pos)
            WIN.blit(text, text_rect)
        else:
            draw_seeds_in_pit(pos, count, radius)

    for pit, pos in PIT_POSITIONS.items():
        if pit in P1_PITS + P2_PITS:
            label = LABEL_FONT.render(pit, True, LABEL_COLOR)
            label_pos = (pos[0] - label.get_width() // 2, pos[1] + 50 if pit in P1_PITS else pos[1] - 65)
            WIN.blit(label, label_pos)
        elif pit == 'C1':
            label = LABEL_FONT.render("AI P1", True, AI1_COLOR)
            WIN.blit(label, (pos[0] - label.get_width() // 2, pos[1] + 60))
        elif pit == 'C2':
            label = LABEL_FONT.render("AI P2", True, AI2_COLOR)
            WIN.blit(label, (pos[0] - label.get_width() // 2, pos[1] + 60))

    pygame.display.update()

def draw_game_over(winner, score):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BACKGROUND)
    WIN.blit(overlay, (0, 0))
    
    game_over_text = TITLE_FONT.render("GAME OVER!", True, TEXT_COLOR)
    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    
    winner_color = AI1_COLOR if "Player 1" in winner else AI2_COLOR if "Player 2" in winner else TEXT_COLOR
    winner_text = STATUS_FONT.render(f"Winner: {winner}", True, winner_color)
    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 10))
    
    score_text = STATUS_FONT.render(f"Score: {score}", True, TEXT_COLOR)
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 30))
    
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    game = PlayAI()
    run = True
    turn = 'C1'
    game_over = False

    while run:
        clock.tick(4)
        
        draw_board(game, turn)

        if game.game.gameOver() and not game_over:
            game_over = True
            winner, score = game.game.findWinner()
            print(f"Game Over! Winner: {winner} with {score} seeds.")
            draw_game_over(winner, score)
            pygame.time.delay(5000)
            run = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        if not game_over:
            if turn == 'C1':
                extra = game.computerTurn()
                turn = 'C1' if extra else 'C2'
            else:
                extra = game.computer2Turn()
                turn = 'C2' if extra else 'C1'

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

