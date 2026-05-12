"""
mcts_agent.py  
=====================================

* Use the formal game functions from solitaire_game.py:
      player(state)
      actions(state)
      result(state, action)
      terminal_test(state)

MCTS OVERVIEW
-------------
Each iteration of MCTS has four phases:

  1. SELECTION     - Walk down the tree using UCT until reaching a node
                     that is not fully expanded (or is terminal).

  2. EXPANSION     - Add one new child node from an untried move.

  3. SIMULATION    - Play out randomly from the new node until terminal
                     or the rollout depth limit is reached.

  4. BACKPROP      - Walk back up to the root, updating visits and wins.

After the time budget runs out, return the action of the most-visited
child of the root.
"""

import math
import random
import time
from solitaire_game import player, actions, result, terminal_test

# ===========================================================================
# MCTS Node
# ===========================================================================
class MCTSNode:
    """
    Represents one node in the MCTS search tree.

    Attributes:
        state    - the chess.Board at this node
        parent   - the parent MCTSNode (None for root)
        action   - the chess.Move that created this node
        children - list of child MCTSNodes added during expansion
        visits   - how many times this node has been visited
        wins     - total reward accumulated through this node
        untried  - list of legal moves not yet expanded
    """

    def __init__(self, state, parent=None, action=None):
        self.state    = state
        self.parent   = parent
        self.action   = action
        self.children = []

        self.visits   = 0
        self.wins     = 0.0

        # Set self.untried to the list of legal moves from state.
        #       Shuffle it so expansion order is random.
        self.untried  = actions(state)
        self.untried  = random.shuffle(self.untried)

# ===========================================================================
# MCTS Helper Functions
# ===========================================================================

def is_fully_expanded(node):
    """
    Return True if there are no untried moves left in node.untried.
    """
    if not node.untried: return True
    else: return False


def is_terminal_node(node):
    """
    Return True if node.state is a terminal (game-over) state.
          Use terminal_test() from chess_game.py.
    """
    if terminal_test(node.state): return True
    else: return False

def uct_score(node, exploration=1.41):
    """
    Calculate and return the UCT score for this node.

    Formula:
        Q / N  +  c * sqrt( ln(N_parent) / N )

    Where:
        Q        = node.wins
        N        = node.visits
        N_parent = node.parent.visits
        c        = exploration  (default 1.41, which is approx sqrt(2))

    Use math.log() and math.sqrt().
    """
    win_rate = node.wins / node.visits
    exploration_term = exploration * math.sqrt(math.log(node.parent.visits) / node.visits)
    return win_rate + exploration_term


def best_child(node, exploration=1.41):
    """
    Return the child in node.children with the highest uct_score().
          Use the built-in max() function with a key argument.
    """
    return max(node.children, key=lambda child: uct_score(child, exploration))


def expand_node(node):
    """
        Pop one move from node.untried.
          Use result() to get the new state.
          Create a new MCTSNode with that state, node as parent,
          and the move as action.
          Append the new child to node.children.
          Return the new child.
    """
    if not node.untried: 
        return
    
    new_move = node.untried.pop()
    new_state = result(node.state, new_move)
    new_child = MCTSNode(new_state, node, new_move)
    node.children.append(new_child)
    return new_child

def update_node(node, reward):
    """
        Increment node.visits by 1.
          Add reward to node.wins.
    """
    node.visits += 1
    node.wins += reward


# ===========================================================================
# MCTS Four Phases
# ===========================================================================

def mcts_select(node):
    """
    SELECTION phase.

        Starting from node, keep moving to best_child() as long as:
            - the node is NOT terminal, AND
            - the node IS fully expanded
          Return the first node that is terminal OR not fully expanded.
    """
    if (is_terminal_node(node) == 0) or is_fully_expanded(node):
        node = best_child(node)
    else:
        return node


def mcts_simulate(state, my_player, rollout_depth):
    new_state = state.copy()
    for _ in range(rollout_depth):
        # Solitaire win: Only 1 piece left
        if terminal_test(new_state): 
            return 1.0 if len(new_state.pieces) == 1 else 0.0
        
        possible_moves = actions(new_state)
        if not possible_moves: 
            break  # No more captures possible
            
        move = random.choice(possible_moves)
        new_state = result(new_state, move)

    # Return a heuristic reward: fewer pieces left = higher reward
    # Example: (Total Starting Pieces - Pieces Left) / (Total Starting Pieces - 1)
    return state.score(new_state)


def mcts_backpropagate(node, reward):
    """
    BACKPROPAGATION phase.

         Walk from node up to the root (via node.parent).
          At each node call update_node(node, reward).
          Stop when node is None.
    """
    while node != None:
        update_node(node, reward)
        node = node.parent


# ===========================================================================
# MCTS Agent
# ===========================================================================
class MCTSAgent:
    """
    Monte Carlo Tree Search Agent.

    Runs Select -> Expand -> Simulate -> Backpropagate
    until the time budget runs out, then returns the most-visited child.
    """

    def __init__(self, time_limit=1.0, rollout_depth=20):
        self.time_limit    = time_limit
        self.rollout_depth = rollout_depth

    def get_move(self, state):
        """
          1. Create a root MCTSNode from state.
          2. Record deadline = time.time() + self.time_limit.
          3. Save my_player = player(state).
          4. Loop while time.time() < deadline:
               a. SELECTION   -> node = mcts_select(root)
               b. EXPANSION   -> if not terminal, node = expand_node(node)
               c. SIMULATION  -> reward = mcts_simulate(node.state, my_player, self.rollout_depth)
               d. BACKPROP    -> mcts_backpropagate(node, reward)
          5. Return the child of root with the highest visits count.
        """
        root = MCTSNode(state, None, None)

        if not root.children:
            return random.choice(list(state.legal_moves))

        deadline = time.time() + self.time_limit
        my_player = player(state)
        while time.time() < deadline:
            node = mcts_select(root)
            if not terminal_test(state):
                node = expand_node(node)
            reward = mcts_simulate(node.state, my_player, self.rollout_depth)
            mcts_backpropagate(node, reward)
        best_action = max(root.children, key=lambda child: child.visits).action
        return best_action
