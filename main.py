# main.py - Simple Hitman Card Game with PyGame
# Keep everything in main() to understand the flow

import pygame
import random
import sys

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

def main():
    # Setup PyGame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hitman Card Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Game state - same as before but all in one place
    players = ['Alice', 'Bob']
    players_alive = ['Alice', 'Bob']
    current_player_index = 0
    turn_number = 1
    deck_size = 11
    game_over = False
    winner = None
    waiting_for_input = True
    
    # Main game loop
    running = True
    while running:
        
        # Handle events (mouse clicks, keyboard)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and game_over:
                    # Restart game
                    players_alive = ['Alice', 'Bob']
                    current_player_index = 0
                    turn_number = 1
                    deck_size = 11
                    game_over = False
                    winner = None
                    waiting_for_input = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN and waiting_for_input and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check if clicked on Draw button (200, 200, 150, 50)
                if 200 <= mouse_x <= 350 and 200 <= mouse_y <= 250:
                    waiting_for_input = False
                    current_player = players_alive[current_player_index]
                    
                    # Draw a card
                    deck_size -= 1
                    card_drawn = random.choice(["Skip", "Angel", "HITMAN"])
                    
                    print(f"{current_player} drew: {card_drawn}")
                    
                    if card_drawn == "HITMAN":
                        has_angel = random.choice([True, False])
                        if has_angel:
                            print(f"{current_player} used Angel! Survived!")
                        else:
                            print(f"{current_player} died!")
                            players_alive.remove(current_player)
                            if current_player_index >= len(players_alive):
                                current_player_index = 0
                    
                    # Check win condition
                    if len(players_alive) == 1:
                        winner = players_alive[0]
                        game_over = True
                    else:
                        # Next player's turn
                        current_player_index = (current_player_index + 1) % len(players_alive)
                        turn_number += 1
                        waiting_for_input = True
                
                # Check if clicked on Play button (200, 300, 150, 50)
                elif 200 <= mouse_x <= 350 and 300 <= mouse_y <= 350:
                    waiting_for_input = False
                    current_player = players_alive[current_player_index]
                    
                    # Play a card
                    card_played = random.choice(["Skip", "Angel"])
                    print(f"{current_player} played: {card_played}")
                    
                    if card_played == "Skip":
                        # Skip ends turn
                        current_player_index = (current_player_index + 1) % len(players_alive)
                        turn_number += 1
                        waiting_for_input = True
                    elif card_played == "Angel":
                        # Angel card played, turn continues
                        waiting_for_input = True
        
        # Clear screen
        screen.fill(GREEN)
        
        # Draw title
        title = font.render("HITMAN CARD GAME", True, WHITE)
        screen.blit(title, (250, 50))
        
        # Draw current player info
        if not game_over:
            current_player = players_alive[current_player_index]
            turn_text = font.render(f"Turn {turn_number}: {current_player}", True, WHITE)
            screen.blit(turn_text, (50, 100))
        
        # Draw player status
        for i, player in enumerate(players):
            if player in players_alive:
                color = WHITE
                status = "ALIVE"
            else:
                color = RED
                status = "DEAD"
            
            player_text = font.render(f"{player}: {status}", True, color)
            screen.blit(player_text, (50, 140 + i * 30))
        
        # Draw deck info
        deck_text = font.render(f"Deck: {deck_size} cards", True, WHITE)
        screen.blit(deck_text, (50, 200))
        
        # Draw buttons (only if waiting for input and game not over)
        if waiting_for_input and not game_over:
            # Draw button
            pygame.draw.rect(screen, GRAY, (200, 200, 150, 50))
            pygame.draw.rect(screen, BLACK, (200, 200, 150, 50), 2)
            draw_text = font.render("DRAW", True, BLACK)
            screen.blit(draw_text, (240, 215))
            
            # Play button
            pygame.draw.rect(screen, GRAY, (200, 300, 150, 50))
            pygame.draw.rect(screen, BLACK, (200, 300, 150, 50), 2)
            play_text = font.render("PLAY", True, BLACK)
            screen.blit(play_text, (240, 315))
        
        # Draw game over screen
        if game_over:
            win_text = font.render(f"{winner} WINS!", True, WHITE)
            screen.blit(win_text, (300, 250))
            restart_text = font.render("Press SPACE to restart", True, WHITE)
            screen.blit(restart_text, (250, 300))
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()