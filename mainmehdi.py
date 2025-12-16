import pygame
import sys
from mancala.play import Play

pygame.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mancala: Human vs AI")

TITLE_FONT = pygame.font.SysFont('Arial', 32, bold=True)
FONT = pygame.font.SysFont('Arial', 28, bold=True)
LABEL_FONT = pygame.font.SysFont('Arial', 16)
STATUS_FONT = pygame.font.SysFont('Arial', 20)
FPS = 60

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
HUMAN_COLOR = (100, 150, 255)  # Blue for Human
AI_COLOR = (255, 100, 100)     # Red for AI
VALID_MOVE_COLOR = (0, 255, 0, 100)  # Green transparent for valid moves
BACKGROUND = (40, 30, 20)

# Pit positions - Human (A-F) bottom, AI (G-L) top
PIT_POSITIONS = {
    'A': (200, 340), 'B': (300, 340), 'C': (400, 340), 'D': (500, 340), 'E': (600, 340), 'F': (700, 340),
    'G': (200, 160), 'H': (300, 160), 'I': (400, 160), 'J': (500, 160), 'K': (600, 160), 'L': (700, 160),
    'HUMAN': (800, 250),  # Human store (right)
    'AI': (100, 250)      # AI store (left)
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

def get_human_store(game):
    """Get human store value (store 2)"""
    return game.game.state.board[2]

def get_ai_store(game):
    """Get AI store value (store 1)"""
    return game.game.state.board[1]

def draw_board(game, current_player='HUMAN', valid_moves=None, selected_pit=None):
    WIN.fill(BACKGROUND)
    
    title = TITLE_FONT.render("MANCALA - HUMAN vs AI", True, TEXT_COLOR)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    
    board_rect = pygame.Rect(75, 120, 750, 300)
    pygame.draw.rect(WIN, WOOD_BORDER, board_rect.inflate(20, 20), border_radius=15)
    pygame.draw.rect(WIN, WOOD_LIGHT, board_rect, border_radius=12)
    
    for i in range(5):
        grain_rect = pygame.Rect(75, 120 + i * 60, 750, 2)
        pygame.draw.rect(WIN, WOOD_DARK, grain_rect)

    board = game.game.state.board

    # Turn indicator
    if current_player == 'HUMAN':
        turn_text = "HUMAN'S TURN - Click on your pit (A-F) to play"
        turn_color = HUMAN_COLOR
    else:
        turn_text = "AI'S TURN - Thinking..."
        turn_color = AI_COLOR
    turn_surface = STATUS_FONT.render(turn_text, True, turn_color)
    WIN.blit(turn_surface, (WIDTH // 2 - turn_surface.get_width() // 2, 60))

    # Highlight valid moves for human
    if current_player == 'HUMAN' and valid_moves:
        for pit in valid_moves:
            if pit in PIT_POSITIONS:
                pos = PIT_POSITIONS[pit]
                highlight_surf = pygame.Surface((PIT_RADIUS * 2, PIT_RADIUS * 2), pygame.SRCALPHA)
                pygame.draw.circle(highlight_surf, VALID_MOVE_COLOR, (PIT_RADIUS, PIT_RADIUS), PIT_RADIUS)
                WIN.blit(highlight_surf, (pos[0] - PIT_RADIUS, pos[1] - PIT_RADIUS))

    # Draw stores
    for store_key, (store_name, color) in [('AI', ('AI', AI_COLOR)), ('HUMAN', ('Human', HUMAN_COLOR))]:
        pos = PIT_POSITIONS[store_key]
        store_value = get_ai_store(game) if store_key == 'AI' else get_human_store(game)
        
        pygame.draw.circle(WIN, WOOD_BORDER, (pos[0] + 3, pos[1] + 3), STORE_RADIUS)
        pygame.draw.circle(WIN, STORE_COLOR, pos, STORE_RADIUS)
        pygame.draw.circle(WIN, WOOD_BORDER, pos, STORE_RADIUS, 3)
        
        # Draw seed count in store
        text = FONT.render(str(store_value), True, TEXT_COLOR)
        text_rect = text.get_rect(center=pos)
        WIN.blit(text, text_rect)
        
        # Draw store label
        label = LABEL_FONT.render(store_name, True, color)
        WIN.blit(label, (pos[0] - label.get_width() // 2, pos[1] + 60))

    # Draw pits
    for pit, pos in PIT_POSITIONS.items():
        if pit not in ['HUMAN', 'AI']:  # Skip stores, they're already drawn
            # Draw pit background
            pygame.draw.circle(WIN, WOOD_BORDER, (pos[0] + 3, pos[1] + 3), PIT_RADIUS)
            
            # Draw pit with selection highlight
            if selected_pit == pit:
                pygame.draw.circle(WIN, PIT_HIGHLIGHT, pos, PIT_RADIUS)
            else:
                pygame.draw.circle(WIN, PIT_COLOR, pos, PIT_RADIUS)
            
            pygame.draw.circle(WIN, WOOD_BORDER, pos, PIT_RADIUS, 3)
            
            # Draw seeds in pit
            count = board[pit]
            draw_seeds_in_pit(pos, count, PIT_RADIUS)
            
            # Draw pit label
            label_color = HUMAN_COLOR if pit in ['A', 'B', 'C', 'D', 'E', 'F'] else AI_COLOR
            label = LABEL_FONT.render(pit, True, label_color)
            label_pos = (pos[0] - label.get_width() // 2, 
                        pos[1] + 50 if pit in ['A', 'B', 'C', 'D', 'E', 'F'] else pos[1] - 65)
            WIN.blit(label, label_pos)

    pygame.display.update()

def draw_game_over(winner, score):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BACKGROUND)
    WIN.blit(overlay, (0, 0))
    
    game_over_text = TITLE_FONT.render("GAME OVER!", True, TEXT_COLOR)
    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    
    winner_color = HUMAN_COLOR if winner == 'HUMAN' else AI_COLOR if winner == 'COMPUTER' else TEXT_COLOR
    winner_text = STATUS_FONT.render(f"Winner: {winner}", True, winner_color)
    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 10))
    
    score_text = STATUS_FONT.render(f"Score: {score}", True, TEXT_COLOR)
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 30))
    
    restart_text = STATUS_FONT.render("Press R to restart or ESC to quit", True, TEXT_COLOR)
    WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 80))
    
    pygame.display.update()

def handle_mouse_click(game, pos, current_player, valid_moves):
    """Handle mouse clicks on pits"""
    if current_player != 'HUMAN':
        return current_player, False, None
    
    for pit, pit_pos in PIT_POSITIONS.items():
        if pit in ['HUMAN', 'AI']:  # Skip stores
            continue
        
        # Check if click is within pit radius
        distance = ((pos[0] - pit_pos[0]) ** 2 + (pos[1] - pit_pos[1]) ** 2) ** 0.5
        if distance <= PIT_RADIUS:
            if pit in valid_moves:
                # Valid move - make the move
                extra_turn = game.humanTurn(pit)
                print(f"Human moves from pit {pit}")
                
                # Check if game is over
                if game.game.gameOver():
                    return current_player, True, None
                
                # Switch turn if no extra turn
                if not extra_turn:
                    return 'AI', False, None
                else:
                    print("Human gets an extra turn!")
                    return 'HUMAN', False, None
            break
    
    return current_player, False, None

def main():
    clock = pygame.time.Clock()
    game = Play()
    run = True
    current_player = 'HUMAN'
    game_over = False
    winner = None
    score = 0
    ai_thinking = False
    selected_pit = None

    while run:
        clock.tick(FPS)
        
        # Get valid moves for human
        valid_moves = []
        if not game_over and current_player == 'HUMAN':
            valid_moves = game.game.state.possibleMoves(game.game.playerSide['HUMAN'])
        
        draw_board(game, current_player, valid_moves, selected_pit)
        
        # Handle game over state
        if game.game.gameOver() and not game_over:
            game_over = True
            winner, score = game.game.findWinner()
            print(f"Game Over! Winner: {winner} with {score} seeds.")
            draw_game_over(winner, score)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
                elif event.key == pygame.K_r and game_over:
                    # Restart game
                    game = Play()
                    current_player = 'HUMAN'
                    game_over = False
                    winner = None
                    score = 0
                    ai_thinking = False
                    selected_pit = None
                
                # Keyboard shortcuts for human moves
                elif not game_over and current_player == 'HUMAN':
                    key_to_pit = {
                        pygame.K_a: 'A', pygame.K_b: 'B', pygame.K_c: 'C',
                        pygame.K_d: 'D', pygame.K_e: 'E', pygame.K_f: 'F'
                    }
                    if event.key in key_to_pit:
                        pit = key_to_pit[event.key]
                        if pit in valid_moves:
                            extra_turn = game.humanTurn(pit)
                            print(f"Human moves from pit {pit}")
                            
                            if game.game.gameOver():
                                game_over = True
                                winner, score = game.game.findWinner()
                                draw_game_over(winner, score)
                            elif not extra_turn:
                                current_player = 'AI'
                            else:
                                print("Human gets an extra turn!")
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not game_over and current_player == 'HUMAN':
                    selected_pit = None
                    # Check if a pit was clicked
                    for pit, pit_pos in PIT_POSITIONS.items():
                        if pit in ['HUMAN', 'AI']:
                            continue
                        
                        distance = ((event.pos[0] - pit_pos[0]) ** 2 + (event.pos[1] - pit_pos[1]) ** 2) ** 0.5
                        if distance <= PIT_RADIUS:
                            selected_pit = pit
                            break
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if not game_over and current_player == 'HUMAN' and selected_pit:
                    if selected_pit in valid_moves:
                        extra_turn = game.humanTurn(selected_pit)
                        print(f"Human moves from pit {selected_pit}")
                        
                        if game.game.gameOver():
                            game_over = True
                            winner, score = game.game.findWinner()
                            draw_game_over(winner, score)
                        elif not extra_turn:
                            current_player = 'AI'
                        else:
                            print("Human gets an extra turn!")
                    selected_pit = None
        
        # AI's turn
        if not game_over and current_player == 'AI' and not ai_thinking:
            ai_thinking = True
            pygame.display.set_caption("Mancala: Human vs AI - AI thinking...")
            
            # Small delay to show thinking
            pygame.time.delay(1000)
            
            # AI makes its move
            extra_turn = game.computerTurn()
            
            pygame.display.set_caption("Mancala: Human vs AI")
            
            if game.game.gameOver():
                game_over = True
                winner, score = game.game.findWinner()
                draw_game_over(winner, score)
            elif not extra_turn:
                current_player = 'HUMAN'
            else:
                print("AI gets an extra turn!")
            
            ai_thinking = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()