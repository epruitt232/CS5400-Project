"""
Solitaire.py
============

Implements game-theoretic interface:
  - S0:             : Initial state
  - Actions(s)      : Legal moves in state s
  - Result(s, a)    : State after applying action a in state s
  - Terminal_test(s): is the game over?
"""
from deck_of_cards import deck_of_cards

class Card:
        def __init__(self):
                self.suit = 0 #The suit of the card 0(clubs), 1(diamonds), 2(hearts), 3(spades)
                self.rank = 1 #The rank of the card 1(A), 2(2), ..., 11(j), 12(q), 13(k)
                self.name = "CA"
                self.visible = True
        



# -----------------------------------
# 1. INITIAL STATE - S0
#    Builds the starting board state.
# -----------------------------------
def initial_state():
        #generates a new puzzle

        cardBox = deck_of_cards.DeckOfCards()
        cardBox.shuffle_deck()
        
        #          0   1  2   3   4   5   6   stock C   D   H   S
        #          0  1   2   3   4   5   6   7     8   9   10  11
        board = [ [], [], [], [], [], [], [], [],   [], [], [], []]
        for col in range(0, len(board)):
                if col == 0:
                        board[col].append(cardBox.give_random_card())
                elif col == 1:
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                elif col == 2:
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                elif col == 3:
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                elif col == 4:
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                elif col == 5:
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                elif col == 6:
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                        board[col].append(cardBox.give_random_card())
                elif col == 7:
                        for i in range(0, len(cardBox.deck)):
                                board[col].append(cardBox.give_random_card())

        for stack in range(0, len(board)):
                for row in range(0, len(board[stack])):
                        if row == len(board[stack]) - 1:
                                print(board[stack][row].name)
                        else:
                                print(board[stack][row].name, end=" ")


        return board



# 2. ACTIONS(s)
def actions(state):
        pass

# 3. RESULT(s, a)
def result(state, action):
        pass

# 4. TERMINAL_Test(s)
def terminal_test(state):
        return False