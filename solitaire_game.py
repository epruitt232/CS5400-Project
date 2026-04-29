"""
solitaire_game.py
=================
Formal Game Abstraction Layer for Solitaire

Implements game-theoretic interface:
    - S0                : Initial state
    - ACTIONS(s)        : Legal moves in state s
    - RESULT(s, a)      : State after applying action a in state s
    - TERMINAL_TEST(s)  : Is the game over?
"""
import solitaire

# ---------------------
# 1. initial_state - S0
# ---------------------
def initial_state(load):
    """
    S0 - Returns the standard start for a Solitaire game
    """
    return solitaire.Board(load)

# --------------------
# 2. actions - ACTIONS(s)
# --------------------
def actions(state):
    """
    ACTIONS(s) - Returns a list of all legal moves in the current state
    """
    return solitaire.legal_moves(state)


# ------------------------
# 3. result - RESULT(s, a)
# ------------------------
def result(state, action):
    """
    RESULT(s, a) - Returns the new state after applying the given action
    """
    state = solitaire.apply(state, action)
    return state


# -----------------------------------
# 4. terminal_test - TERMINAL_TEST(s)
# -----------------------------------
def terminal_test(state):
    """
    TERMINAL_TEST(s) - Returns True when the game is over
    """
    return solitaire.is_game_over(state)

def evaluate(board, score, lastMove):
    #stock move
    if lastMove[0][0] == 7:
        #stock to board
        if lastMove[1][0] >= 0 and lastMove[1][0] < 7:
            score += 5
        #stock to foundation
        elif lastMove[1][0] > 7 and lastMove[1][0] < 12:
            score += 10
    #board move
    elif lastMove[0][0] >= 0 and lastMove[0][0] < 7:
        #board to foundation
        if lastMove[1][0] > 7 and lastMove[1][0] < 12:
            score += 10
        #board to board (revealed a card)
        



    return score

"""
    * +10 points for moving a card form the board or stock to foundation (-10 for removing a card from foundation).
    * + 5 points for revealing a card on the board.
    * + 5 points for moving a card from the stock to the board.
"""