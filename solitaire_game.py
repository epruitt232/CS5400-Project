"""
solitaire_game.py
=================
Formal Game Abstraction Layer for Solitaire

Implements the game-theoretic interface:
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
    return solitaire.GameState(load)
#-----------------------

# -----------------------
# 2. actions - ACTIONS(s)
# -----------------------
def actions(state):
    """
    ACTIONS(s) - Returns a list of all legal moves in the current state
    """
    return state.legal_moves()
#------------------

# ------------------------
# 3. result - RESULT(s, a)
# ------------------------
def result(state, action):
    """
    RESULT(s, a) - Returns the new state after applying the given action
    """
    newState = state.copyState()
    newState.push(action)
    return newState
#-------------------------

# -----------------------------------
# 4. terminal_test - TERMINAL_TEST(s)
# -----------------------------------
def terminal_test(state):
    """
    TERMINAL_TEST(s) - Returns True when game is over
    """
    return state.is_game_over()
#------------------------