"""
The UI for A1.

Run this file to play the game. You don't need to modify this file in any
way, nor do you need to submit it.

This file simply calls on pygame and the code from a2_game.py, which contains
all of your client code.
"""
import a2_game
import pygame
import sys

GAME_SPEED = 100
pygame.init()

PYGAME_SCREEN = None
CHARACTER_SIZE = 120
NUMBER_OF_CHARACTERS = 2
PADDING = 40
P1_POSITION = CHARACTER_SIZE // 4
P2_POSITION = CHARACTER_SIZE - (CHARACTER_SIZE // 4)
RANDOM_TIMER = 10
FONT_SIZE = 18

def start_game():
    """
    Start and initialize the game
    """
    global PYGAME_SCREEN, CHARACTER_SIZE, NUMBER_OF_CHARACTERS, FONT_SIZE
    a2_game.set_up_game()
    
    # Set up the width and height of the screen (proportional to the character
    # sizes)
    width = NUMBER_OF_CHARACTERS * CHARACTER_SIZE
    height = 1 * CHARACTER_SIZE + PADDING * 2
    
    pixel_size = width, height
    
    # set the screen to draw on
    PYGAME_SCREEN = pygame.display.set_mode(pixel_size)

def update_game():
    """
    Update the game's UI.
    """
    global PYGAME_SCREEN, CHARACTER_SIZE, P1_POSITION, P2_POSITION
    
    draw_parameters = a2_game.update_ui()
    
    p1_sprite = draw_parameters['p1_sprite']
    p1_hp = draw_parameters['p1_hp']
    p1_sp = draw_parameters['p1_sp']
    p1_name = draw_parameters['p1_name']
    
    p1_label = "{}\nHP: {}\nSP: {}".format(p1_name, p1_hp, p1_sp).split("\n")
    
    p2_sprite = draw_parameters['p2_sprite']
    p2_hp = draw_parameters['p2_hp']
    p2_sp = draw_parameters['p2_sp']
    p2_name = draw_parameters['p2_name']
    
    p2_label = "{}\nHP: {}\nSP: {}".format(p2_name, p2_hp, p2_sp).split("\n")
    
    font_type = pygame.font.get_default_font()
    font = pygame.font.SysFont(font_type, FONT_SIZE)
    
    p1_icon = pygame.image.load('sprites/' + p1_sprite + '.png')
    p2_icon = pygame.image.load('sprites/' + p2_sprite + '.png')

    PYGAME_SCREEN.fill((255, 255, 255)) # (255, 255, 255)=(r,g,b)=white
    bg = pygame.image.load('sprites/background.png')
    rect = pygame.Rect(0, 0, NUMBER_OF_CHARACTERS * CHARACTER_SIZE,
                       CHARACTER_SIZE + PADDING * 2)
    PYGAME_SCREEN.blit(bg, rect)
    
    # Draw the first character
    (x, y) = P1_POSITION, PADDING
    rect = pygame.Rect(x, y, CHARACTER_SIZE, CHARACTER_SIZE)
    PYGAME_SCREEN.blit(p1_icon, rect)
    
    y_coordinate = 0
    for line in p1_label:
        text = font.render(line, True, (0, 0, 0))
        PYGAME_SCREEN.blit(text, (P1_POSITION + PADDING, y_coordinate))
        y_coordinate += FONT_SIZE
    
    # Draw the HP bar
    # Draw the SP bar
    
    # Draw the second character
    # Flip p2 so they face p1
    p2_icon = pygame.transform.flip(p2_icon, True, False)
    (x, y) = P2_POSITION, PADDING
    rect = pygame.Rect(x, y, CHARACTER_SIZE, CHARACTER_SIZE)
    PYGAME_SCREEN.blit(p2_icon, rect)

    y_coordinate = 0
    for line in p2_label:
        text = font.render(line, True, (0, 0, 0))
        PYGAME_SCREEN.blit(text, (P2_POSITION + PADDING, y_coordinate))
        y_coordinate += FONT_SIZE    
    
    # Update the current player and available actions
    if not a2_game.GAME_IS_OVER:
        actions = draw_parameters['actions']
        current_player = draw_parameters['current_player']
        action_label = ["Current Character: {}".format(current_player),
                        "Available Actions: {}".format(", ".join(actions))]
    
        y_coordinate = CHARACTER_SIZE + PADDING
        for line in action_label:
            text = font.render(line, True, (0, 0, 0))
            PYGAME_SCREEN.blit(text, (P1_POSITION + PADDING // 2, y_coordinate))
            y_coordinate += FONT_SIZE
    else:
        game_label = ["Game over!"]
        winner = a2_game.GAME_WINNER
        if winner:
            game_label.append("The winner is {}!".format(winner.get_name()))
        else:
            game_label.append("The game ended in a tie!")
        
        y_coordinate = CHARACTER_SIZE + PADDING
        for line in game_label:
            text = font.render(line, True, (0, 0, 0))
            PYGAME_SCREEN.blit(text, (P1_POSITION + PADDING // 2, y_coordinate))
            y_coordinate += FONT_SIZE 
    
    pygame.display.flip()

if __name__ == '__main__':
    start_game()
    update_game()
    
    while True:
        pygame.time.wait(GAME_SPEED)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and not a2_game.GAME_IS_OVER:
                # If the current player is using a manual playstyle, the
                # pick a move when a key is pressed
                if (not a2_game.BATTLE_QUEUE.is_over() and 
                    a2_game.BATTLE_QUEUE.peek().playstyle.is_manual):
                    k = 'X'
                    if event.key == pygame.K_a:
                        k = 'A'
                    elif event.key == pygame.K_s:
                        k = 'S'
                        
                    a2_game.LAST_KEY_PRESSED = k
                    a2_game.perform_attack()
                
        # If the current player isn't using a manual playstyle, pick a move
        if (not a2_game.GAME_IS_OVER and
            not a2_game.BATTLE_QUEUE.is_over() and 
            not a2_game.BATTLE_QUEUE.peek().playstyle.is_manual and
            RANDOM_TIMER == 10):
            a2_game.perform_attack()
    
        # Redraw the game
        update_game()
        
        # Only let the random strategy make a decision every 10 ticks of time
        RANDOM_TIMER -= 1
        if RANDOM_TIMER == 0:
            RANDOM_TIMER = 10
    
    pygame.quit()
    sys.exit(0)        
