import pygame
from mancala.play import Play
import sys

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mancala: Human vs AI")

TITLE_FONT = pygame.font.SysFont('Arial', 32, bold=True)
FONT = pygame.font.SysFont('Arial', 28, bold=True)
LABEL_FONT = pygame.font.SysFont('Arial', 16)
STATUS_FONT = pygame.font.SysFont('Arial', 20)
FPS = 30

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
HUMAN_COLOR = (100, 150, 255)
AI_COLOR = (255, 100, 100)
BACKGROUND = (40, 30, 20)

P1_PITS = ['A','B','C','D','E','F']
P2_PITS = ['G','H','I','J','K','L']
PIT_POSITIONS = {
    'A': (200, 340), 'B': (300, 340), 'C': (400, 340), 'D': (500, 340), 'E': (600, 340), 'F': (700, 340),
    'G': (200, 160), 'H': (300, 160), 'I': (400, 160), 'J': (500, 160), 'K': (600, 160), 'L': (700, 160),
    'HUMAN': (100, 250), 'COMPUTER': (800, 250)
}

PIT_RADIUS = 35
STORE_RADIUS = 50

def draw_seeds_in_pit(pos, count, radius):
    """Draw individual seeds inside a pit for visual appeal"""
    if count == 0:
        return
    
    # For small counts, draw individual seeds
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
        # For large counts, just show the number
        text = FONT.render(str(count), True, TEXT_COLOR)
        text_rect = text.get_rect(center=pos)
        WIN.blit(text, text_rect)

def draw_board(game, hovered_pit=None, current_player='HUMAN'):
    # Fill background
    WIN.fill(BACKGROUND)
    
    # Draw title
    title = TITLE_FONT.render("MANCALA", True, TEXT_COLOR)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    
    # Draw wooden board background
    board_rect = pygame.Rect(75, 120, 750, 300)
    pygame.draw.rect(WIN, WOOD_BORDER, board_rect.inflate(20, 20), border_radius=15)
    pygame.draw.rect(WIN, WOOD_LIGHT, board_rect, border_radius=12)
    
    # Add wood grain effect
    for i in range(5):
        grain_rect = pygame.Rect(75, 120 + i * 60, 750, 2)
        pygame.draw.rect(WIN, WOOD_DARK, grain_rect)

    board = game.game.state.board

    # Draw player turn indicator
    turn_text = f"{'YOUR' if current_player == 'HUMAN' else 'AI'} TURN"
    turn_color = HUMAN_COLOR if current_player == 'HUMAN' else AI_COLOR
    turn_surface = STATUS_FONT.render(turn_text, True, turn_color)
    WIN.blit(turn_surface, (WIDTH // 2 - turn_surface.get_width() // 2, 60))

    # Draw pits and stores
    for pit, pos in PIT_POSITIONS.items():
        is_store = pit in ['HUMAN', 'COMPUTER']
        radius = STORE_RADIUS if is_store else PIT_RADIUS
        
        # Determine pit color
        if pit == hovered_pit and not is_store:
            pit_color = PIT_HIGHLIGHT
        else:
            pit_color = STORE_COLOR if is_store else PIT_COLOR
        
        # Draw pit shadow for depth
        pygame.draw.circle(WIN, WOOD_BORDER, (pos[0] + 3, pos[1] + 3), radius)
        
        # Draw pit
        pygame.draw.circle(WIN, pit_color, pos, radius)
        pygame.draw.circle(WIN, WOOD_BORDER, pos, radius, 3)
        
        # Get count
        if pit in P1_PITS + P2_PITS:
            count = board[pit]
        else:
            key = game.game.playerSide['HUMAN'] if pit == 'HUMAN' else game.game.playerSide['COMPUTER']
            count = board[key]
        
        # Draw seeds
        if is_store:
            # For stores, always show number
            text = FONT.render(str(count), True, TEXT_COLOR)
            text_rect = text.get_rect(center=pos)
            WIN.blit(text, text_rect)
        else:
            draw_seeds_in_pit(pos, count, radius)

    # Draw pit labels
    for pit, pos in PIT_POSITIONS.items():
        if pit in P1_PITS + P2_PITS:
            label = LABEL_FONT.render(pit, True, LABEL_COLOR)
            label_pos = (pos[0] - label.get_width() // 2, pos[1] + 50 if pit in P1_PITS else pos[1] - 65)
            WIN.blit(label, label_pos)
        elif pit == 'HUMAN':
            label = LABEL_FONT.render("YOU", True, HUMAN_COLOR)
            WIN.blit(label, (pos[0] - label.get_width() // 2, pos[1] + 60))
        elif pit == 'COMPUTER':
            label = LABEL_FONT.render("AI", True, AI_COLOR)
            WIN.blit(label, (pos[0] - label.get_width() // 2, pos[1] + 60))
    
    # Draw instructions at bottom
    instructions = LABEL_FONT.render("Click on your pits (A-F) to play", True, LABEL_COLOR)
    WIN.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 30))

    pygame.display.update()

def draw_game_over(winner, score):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BACKGROUND)
    WIN.blit(overlay, (0, 0))
    
    # Draw game over text
    game_over_text = TITLE_FONT.render("GAME OVER!", True, TEXT_COLOR)
    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    
    # Draw winner
    winner_color = HUMAN_COLOR if winner == "HUMAN" else AI_COLOR if winner == "COMPUTER" else TEXT_COLOR
    winner_text = STATUS_FONT.render(f"Winner: {winner}", True, winner_color)
    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 10))
    
    # Draw score
    score_text = STATUS_FONT.render(f"Score: {score}", True, TEXT_COLOR)
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 30))
    
    pygame.display.update()

def get_clicked_pit(pos):
    x, y = pos
    for pit, p_pos in PIT_POSITIONS.items():
        px, py = p_pos
        is_store = pit in ['HUMAN', 'COMPUTER']
        radius = STORE_RADIUS if is_store else PIT_RADIUS
        if (x - px)**2 + (y - py)**2 <= radius**2:
            return pit
    return None

def get_hovered_pit(pos, game, human_turn):
    pit = get_clicked_pit(pos)
    if pit and pit in P1_PITS and human_turn:
        board = game.game.state.board
        if board[pit] > 0:  # Only show hover if pit has seeds
            return pit
    return None

def main():
    clock = pygame.time.Clock()
    game = Play()
    run = True
    human_turn = True
    game_over = False
    hovered_pit = None

    while run:
        clock.tick(FPS)
        
        mouse_pos = pygame.mouse.get_pos()
        hovered_pit = get_hovered_pit(mouse_pos, game, human_turn) if not game_over else None
        
        current_player = 'HUMAN' if human_turn else 'COMPUTER'
        draw_board(game, hovered_pit, current_player)

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

            if human_turn and event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pit = get_clicked_pit(pygame.mouse.get_pos())
                if pit in P1_PITS:
                    board = game.game.state.board
                    if board[pit] > 0:  # Only allow clicking non-empty pits
                        extra_turn = game.humanTurn(pit)
                        if not extra_turn:
                            human_turn = False  # Switch to computer
                        # If extra_turn is True, human_turn stays True → human plays again

        if not human_turn and not game_over:
            pygame.time.delay(500)
            extra_turn = game.computerTurn()
            if not extra_turn:
                human_turn = True  # Switch back to human
            # If extra_turn is True, human_turn stays False → computer plays again

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
