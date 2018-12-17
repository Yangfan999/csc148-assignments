"""
The client code for A2.

Replace the 'None's in the dictionary with the classes you define. Make sure
you import those classes. We've added Mage, Rogue, and BattleQueue for you
already.

Do NOT run PythonTA on this file.
We will not grade the documentation of this file.
"""
# Import classes as needed
from a2_battle_queue import BattleQueue, RestrictedBattleQueue
from a2_playstyle import *
from a2_characters import *
from a2_skill_decision_tree import create_default_tree

# Replace None with the name of your Character classes
# v should map to your class for your Vampire
# s should map to your class for your Sorcerer
CHARACTER_CLASSES = {'m': Mage,
                     'r': Rogue,
                     'v': Vampire,
                     's': Sorcerer
                    }

# Replace None with the name of your Playstyle classes
# mr should map to your class for your recursive minimax playstyle
# mi should map to your class for your iterative minimax playstyle
PLAYSTYLE_CLASSES = {'m': ManualPlaystyle,
                     'r': RandomPlaystyle,
                     'mr': MinimaxRecPlaystyle,
                     'mi': MinimaxIterPlaystyle
                    }

BATTLE_QUEUE_CLASSES = {'n': BattleQueue,
                        'r': RestrictedBattleQueue
                        }

# Do not change any of the code below
# You may NOT use or modify any of the variables defined below within your code
# they're only to be used by a1_game.py and a1_ui.py.
# (i.e. don't reference BATTLE_QUEUE, LAST_KEY_PRESSED, P1, P2, GAME_IS_OVER,
#  or GAME_WINNER anywhere in your code.)
BATTLE_QUEUE = None
LAST_KEY_PRESSED = None
P1 = None
P2 = None
GAME_IS_OVER = False
GAME_WINNER = None

def perform_attack():
    """
    Uses the next character's playstyle to decide on and perform an attack.
    """
    global BATTLE_QUEUE, GAME_IS_OVER, GAME_WINNER, LAST_KEY_PRESSED

    # Get the next character in the battle queue, but don't remove them.
    next_character = BATTLE_QUEUE.peek()
    playstyle = next_character.playstyle

    # Uses the next character's playstyle to select an attack
    if playstyle.is_manual:
        move_to_make = playstyle.select_attack(LAST_KEY_PRESSED)
    else:
        move_to_make = playstyle.select_attack()

    # Check if the next_character can make that action ('A' represents
    # a normal attack, 'S' represents a special attack.)
    # If a move that is not 'A' or 'S' is passed in, this should return False.
    if next_character.is_valid_action(move_to_make):
        if move_to_make == 'A':
            next_character.attack()
        else:
            next_character.special_attack()

        # Call remove() to remove the next_character from the battle_queue
        # (if they still have SP; otherwise the next call to remove()
        # should skip them)
        if next_character.get_available_actions() != []:
            BATTLE_QUEUE.remove()

    # Check if the game is over.
    GAME_IS_OVER = BATTLE_QUEUE.is_over()

    # Get the winner of the game. If the game is not over yet, get_winner()
    # should return None. Otherwise, it should return the character that won.
    GAME_WINNER = BATTLE_QUEUE.get_winner()

def set_up_game():
    """
    Sets up the battle queue and characters for the game.
    """
    global P1, P2, BATTLE_QUEUE

    # Create a new battle queue
    bq = ''
    while bq not in list(BATTLE_QUEUE_CLASSES.keys()):
        bq = input("Select a Battle Queue type (n for a Normal Battle Queue, " +
                   "r for a Restricted Battle Queue): ").strip()

    BATTLE_QUEUE = BATTLE_QUEUE_CLASSES[bq]()

    # Get the parameters for the first character
    player_1 = ''
    player_1_playstyle = ''

    while player_1 not in list(CHARACTER_CLASSES.keys()):
        player_1 = input("Select a class for the first character (m for " +
                         "Mage, r for Rogue, v for Vampire, s for " +
                         "Sorcerer): ").strip()

    player_1_name = input("Select a name for the first character: ").strip()

    while player_1_playstyle not in list(PLAYSTYLE_CLASSES.keys()):
        player_1_playstyle = input("Select a playstyle for the first " +
                                   "character (m for Manual, r for Random, " +
                                   "mr for Minimax (Recursive), " +
                                   "mi for Minimax (Iterative)): ")
        player_1_playstyle = player_1_playstyle.strip()

    # Get the parameters for the second character
    player_2 = ''
    player_2_playstyle = ''

    while player_2 not in list(CHARACTER_CLASSES.keys()):
        player_2 = input("Select a class for the second character (m for " +
                         "Mage, r for Rogue, v for Vampire, s for " +
                         "Sorcerer): ").strip()

    player_2_name = input("Select a name for the second character: ").strip()

    while player_2_playstyle not in list(PLAYSTYLE_CLASSES.keys()):
        player_2_playstyle = input("Select a playstyle for the second " +
                                   "character (m for Manual, r for Random, " +
                                   "mr for Minimax (Recursive), " +
                                   "mi for Minimax (Iterative)): ")
        player_2_playstyle = player_2_playstyle.strip()

    # Store the classes in other variable names for convenience
    P1_Character = CHARACTER_CLASSES[player_1]
    P2_Character = CHARACTER_CLASSES[player_2]
    p1_playstyle = PLAYSTYLE_CLASSES[player_1_playstyle](BATTLE_QUEUE)
    p2_playstyle = PLAYSTYLE_CLASSES[player_2_playstyle](BATTLE_QUEUE)

    # Call the corresponding __init__ for each player's character class
    # The parameters passed in are: their name, the battle queue and an
    # instance of their playstyle
    P1 = P1_Character(player_1_name, BATTLE_QUEUE, p1_playstyle)
    P2 = P2_Character(player_2_name, BATTLE_QUEUE, p2_playstyle)

    if player_1 == 's':
        default_tree = create_default_tree()
        P1.set_skill_decision_tree(default_tree)

    if player_2 == 's':
        default_tree = create_default_tree()
        P2.set_skill_decision_tree(default_tree)

    # Set the enemy attribute of the characters
    # You can assume this will be called before any attacks are performed
    P1.enemy = P2
    P2.enemy = P1

    # Add the characters to the Battle Queue
    BATTLE_QUEUE.add(P1)
    BATTLE_QUEUE.add(P2)

def update_ui():
    """
    Return the parameters to update the UI for the game.

    Note: This function is a bit silly, but the alternative was either calling
    pygame methods here, or having you read through a1_ui.py to find client
    code. Silly is the better option, in this case. :)
    """
    global P1, P2, BATTLE_QUEUE

    # Get the names
    p1_name = P1.get_name()
    p2_name = P2.get_name()

    # Get the sprite to draw
    p1_current_sprite = P1.get_next_sprite()
    p2_current_sprite = P2.get_next_sprite()

    # Get the character HPs
    p1_current_hp = P1.get_hp()
    p2_current_hp = P2.get_hp()

    # Get the character SPs
    p1_current_sp = P1.get_sp()
    p2_current_sp = P2.get_sp()

    if not BATTLE_QUEUE.is_over():
        # Get the actions that the current player can make (this should be a
        # list containing 'A' and/or 'S', or be empty if there are no actions.)
        current_available_actions = BATTLE_QUEUE.peek().get_available_actions()

        # Get the current player's name
        current_player = BATTLE_QUEUE.peek().get_name()
    else:
        current_available_actions = []
        current_player = None

    ui_to_draw = {'p1_sprite': p1_current_sprite,
                  'p2_sprite': p2_current_sprite,
                  'p1_hp': p1_current_hp,
                  'p2_hp': p2_current_hp,
                  'p1_sp': p1_current_sp,
                  'p2_sp': p2_current_sp,
                  'p1_name': p1_name,
                  'p2_name': p2_name,
                  'actions': current_available_actions,
                  'current_player': current_player}

    return ui_to_draw
