"""
solitaire.py
===============
Formal Game Layer

Implements the Following:
  - __init__(self)      : Initialize
"""
from deck_of_cards import deck_of_cards

#=================================================
#CARD CLASS       -> Represents a card



class Card:
    """
    Card object
    Attributes:
        *suit: The suit of the card 0(spades), 1(hearts), 2(diamonds), 3(clubs)
        *rank: The rank of the card 1(A), 2(2), ..., 11(J), 12(Q), 13(K)
        *name: The display name of the card 01(" SA"), 110("H10"), 313(" CK")
        *color: The color of the card 0(black) 1(red)
        *visible: Whether the card displays as visible(1 -> "???") or hidden(1 -> "C10")
    """
    def __init__(self, rank, suit, name, color, visible):
        self.rank = rank
        self.suit = suit
        self.name = name
        self.color = color
        self.visible = visible
    
    
    def from_card(card, visible):
        rank = card.rank
        suit = card.suit
        match card.suit:
            case 0:
                cardName = "S"
                color = 0
            case 1:
                cardName = "H"
                color = 1
            case 2:
                cardName = "D"
                color = 1
            case 3:
                cardName = "C"
                color = 0
        match card.rank:
            case 1:
                cardName += "A"
            case 11:
                cardName += "J"
            case 12:
                cardName += "Q"
            case 13:
                cardName += "K"
            case _:
                cardName += str(card.rank)
        name = cardName
        return Card(rank, suit, name, color, visible)

    def from_string(cardStr, visible):
        #sets the name
        name = cardStr
        #sets the suit and color
        match cardStr[0]:
            case "S":
                suit = 0
                color = 0
            case "H":
                suit = 1
                color = 1
            case "D":
                suit = 2
                color = 1
            case "C":
                suit = 3
                color = 0
        #sets the rank
        cardStr = cardStr[1:]
        match cardStr:
            case "A":
                rank = 1
            case "J":
                rank = 11
            case "Q":
                rank = 12
            case "K":
                rank = 13
            case _:
                rank = int(cardStr)
        return Card(rank, suit, name, color, visible)
    

def Board(load):
    """
    initializes the board
    Parameters:
    * load  : whether to load the last game from file or generate a new one
    Returns   : the initialized board
    """
    #        0   1   2   3   4   5   6    stock S    H  D   C
    #        0   1   2   3   4   5   6    7     8    9  10  11
    board= [ [], [], [], [], [], [], [], [],    [], [], [], [] ]

    #generate a new puzzle
    if not load:
        cardBox = deck_of_cards.DeckOfCards()
        cardBox.shuffle_deck()
        card = None
        numCards = 1
        for stack in range(0, len(board)):
            #makes game stacks
            if stack < 7:
                for i in range(0, numCards):
                    #make the last card in the stack visible
                    if i == numCards -1:
                        card = cardBox.give_random_card()
                        board[stack].append(Card.from_card(card, True))
                    else:
                        card = cardBox.give_random_card()
                        board[stack].append(Card.from_card(card, False))
            #puts the remaining cards into the stock
            elif stack == 7:
                for i in range(0, len(cardBox.deck)):
                    card = cardBox.give_random_card()
                    board[stack].append(Card.from_card(card, True))
            numCards += 1
        #outputs the generated puzzle to text file
        with open("lastPuzzle.txt", "w") as f:
            for i in range(0, len(board)):
                for j in range(0, len(board[i])):
                    if j == len(board[i]) - 1:
                        print(board[i][j].name, file=f)
                    else:
                        print(board[i][j].name, file=f)
    #loads the last puzzle saved
    elif load:
        cardList = []
        with open("lastPuzzle.txt", "r") as f:
            inputList = f.readlines()
            for line in inputList:
                cardList.append(line.strip())
        card = ""
        numCards = 1
        listIterator = 0
        for stack in range(0, len(board)):
            #makes game stacks
            if stack < 7:
                for i in range(0, numCards):
                    #make the last card in the stack visible
                    if i == numCards -1:
                        board[stack].append(Card.from_string(cardList[listIterator], True))
                    else:
                        board[stack].append(Card.from_string(cardList[listIterator], False))
                    listIterator += 1
            #puts the remaining cards into the stock
            elif stack == 7:
                for i in range(listIterator, len(cardList)):
                    #board[stack].append(Card(cardList[listIterator], True))
                    board[stack].insert(0, Card.from_string(cardList[listIterator], True))
                    listIterator += 1
            numCards += 1

    #return the board
    return board

def legal_moves(board):
    """
    Returns a list of legal moves for the current board
    """
    legalMoves = []
    
    for i in range(0, len(board)):
        if 8 <= i <= 11:
            continue

        if len(board[i]) > 0:
            currCard = board[i][len(board[i]) - 1]
            match currCard.rank:
                #ACE
                case 1:
                    #adds the foundation move
                    match currCard.suit:
                        case 0:
                            if i != 8:
                                legalMoves.append(((i, len(board[i]) - 1), (8, 0)))
                        case 1:
                            if i != 9:
                                legalMoves.append(((i, len(board[i]) - 1), (9, 0)))
                        case 2:
                            if i != 10:
                                legalMoves.append(((i, len(board[i]) - 1), (10, 0)))
                        case 3:
                            if i != 11:
                                legalMoves.append(((i, len(board[i]) - 1), (11, 0)))
                    #adds general moves
                    for j in range(0, len(board)):
                        if len(board[j]) > 0:
                            if currCard.rank + 1 == board[j][len(board[j]) - 1].rank:
                                if currCard.color != board[j][len(board[j]) - 1].color:
                                    legalMoves.append(((i, len(board[i]) - 1), (j, len(board[j]) - 1)))
                #KING
                case 13:
                    #add empty stack
                    for j in range(0, 7):
                        if len(board[j]) == 0:
                            legalMoves.append(((i, len(board[i]) - 1), (j, len(board[j]))))
                    #add foundations
                    
                #general
                case _:
                    for j in range(0, 7):
                        if len(board[j]) > 0:
                            if currCard.rank + 1 == board[j][len(board[j]) - 1].rank:
                                if currCard.color != board[j][len(board[j]) - 1].color:
                                    legalMoves.append(((i, len(board[i]) - 1), (j, len(board[j]))))
    if len(board[7]) > 2:
        legalMoves.append(((7, len(board[7]) - 1), (7, 0)))


    return legalMoves

def apply(board, move):
    """
    Applies the move to the board
        - move is of form ((source col, source row), (destination col, destination row))
    """
    l = []
    


    #flip the stock
    if move[0][0] == 7 and move[1][0] == 7:
        board[7].insert(0, board[7][len(board[7]) - 1])
    else:
        #move the card
        board[move[1][0]].append(board[move[0][0]][move[0][1]])
        board[move[0][0]].remove(board[move[0][0]][move[0][1]])

        if len(board[move[0][0]]) > 0:
            board[move[0][0]][len(board[move[0][0]]) - 1].visible = True
    
    

    return board


def is_game_over(board):
    """
    Checks if the game has been ended or no moves remain
    """
    if legal_moves(board) == 0:
        return True
    

    return False