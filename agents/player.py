"""
player.py
=========
"""
from solitaire_game import actions, result

class PlayerAgent:
    """
    Class for user to play
    """
    def __init__(self):
        self.name = "PLAYER"
    
    def get_move(self, state):
        legalActions = actions(state)
        
        #prevents deadlock from asking the player for a legalMove when the list is empty
        if len(legalActions) > 0:
            print(' ', end='')
            for i in range(0, len(legalActions)):
                print('      ', str(i).rjust(2), '       ', end=' ')
            print()
            print(legalActions)
            index = input("Enter index of move to apply: ")
            return legalActions[int(index)]
        return None