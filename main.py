import argparse
import os
from Solitaire import initial_state, result, terminal_test

from agents.utility import UtilityAgent

from agents.player import PlayerAgent


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



def render(board):
    print("|--------------------------------|------------|")    
    print("|  0   1   2   3   4   5   6     |            |")
    
    print("|--------------------------------|------------|")
    print("| ???         ??? ??? ??? ??? | 0| MOVES: 999 |")
    print("|-----------------------------|  |            |")
    print("| ??? ??? ??? ??? ??? ??? ??? | 1| SCORE: 999 |")# k
    print("|     ??? ??? ??? ??? ??? ??? | 2|            |")# q
    print("|         ??? ??? ??? ??? ??? | 3| TIME: 999  |")# j
    print("|             ??? ??? ??? ??? | 4|            |")#10
    print("|                 ??? ??? ??? | 5| AGENT:     |")# 9
    print("|                     ??? ??? | 6|   PLAYER   |")# 8
    print("|                         ??? | 7|            |")# 7  k
    print("|                             | 8| LAST MOVE: |")# 6  q
    print("|                             | 9| 0,1 -> 2,3 |")# 5  j
    print("|                             |10|            |")# 4 10
    print("|                             |11|            |")# 3  9
    print("|                             |12|            |")# 2  8
    print("|                             |13|            |")# A  7
    print("|                             |14|            |")#    6
    print("|                             |15|            |")#    5
    print("|                             |16|            |")#    4
    print("|                             |17|            |")#    3
    print("|                             |18|            |")#    2
    print("|                             |19|            |")#    A
    print("|---------------------------------------------|")


def make_agent(name):
    name = name.lower()
    if name == 'utility':
        return UtilityAgent()
    elif name == 'player':
        return PlayerAgent()


def play(agent):
    state = initial_state()

    render(state)
    moveCount = 0
    lastMove = None
    elapsed = 0.0

    while not terminal_test(state):
        # --- Get the move ---
        move = agent.get_move(state)

        # --- apply the move
        last_move   = move
        #state       = result(state, move)

        # --- draw board showing new state
        
        



# ---------------
# CLI entry point
# ---------------
def main():
    parser = argparse.ArgumentParser(description='Solitaire table')
    
    parser.add_argument('--agent',
                        default='utility',
                        help='agent: utility | ? | ? | player')

    args = parser.parse_args()

    player = make_agent(args.agent)

    try:
        outcome = play(player)

    finally:
        if hasattr(player, 'quit'):
            player.quit()

if __name__ == '__main__':
    main()