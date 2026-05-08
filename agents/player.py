"""
player.py
=========
"""
from solitaire_game import actions

class PlayerAgent:
    """
    Class for user to play
    """
    def __init__(self):
        self.name = "PLAYER"
    #------------------

    def get_move(self, state):
        """
        Get a list of each possible action and display it for the user to pick.
        """
        legalActions = actions(state)
        if len(legalActions) > 0:
            for i in range(0, len(legalActions)):
                print('       ', str(i).rjust(2), '       ', end='')
            print()
            print(legalActions)
            while True:
                index = input("Enter index of move to apply or q to quit: ").strip()
                #quit character
                if index.lower() == "q":
                    quit()
                #empty input
                if index == "":
                    print("Enter an integer between 0 and ", len(legalActions) - 1, ", or q.")
                    continue
                #not a number
                if not index.isdigit():
                    print("Enter an integer between 0 and ", len(legalActions) - 1, ", or q.")
                    continue
                #check the range
                index = int(index)
                if index < 0 or index >= len(legalActions):
                    print("Enter an integer between 0 and ", len(legalActions) - 1, ", or q.")
                    continue
                return legalActions[int(index)]

        return None
    #-------------------------