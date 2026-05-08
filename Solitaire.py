"""
solitaire.py
============
Formal Game Layer
"""
from deck_of_cards import deck_of_cards

#===================
class Card:
    """
    Card Object
    Attributes:
        - suit:    The suit of the card 0(spades), 1(hearts), 2(diamonds), 3(clubs)
        - rank:    The rank of the card 1(A), 2(2), ..., 11(J), 12(Q), 13(K)
        - name:    The display name of the card 01(' SA'), 110('H10')
        - color:   The color of the card 0(black), 1(red)
        - visible: If the card is visible(1 -> 'C10') or hidden(0 -> '???')
    """
    def __init__(self, suit, rank, name, color, visible):
        self.suit = suit
        self.rank = rank
        self.name = name
        self.color = color
        self.visible = visible
    #----------------------------------------------------

    def from_card(card, visible):
        """
        Builds a card from a deck_of_cards card object
        """
        match card.suit:
            case 0: #spades
                suit = 0
                cardName = 'S'
                color = 0
            case 1: #hearts
                suit = 1
                cardName = 'H'
                color = 1
            case 2: #diamonds
                suit = 2
                cardName = 'D'
                color = 1
            case 3: #clubs
                suit = 3
                cardName = 'C'
                color = 0
        match card.rank:
            case 1:
                rank = 1
                cardName += 'A'
            case 11:
                rank = 11
                cardName += 'J'
            case 12:
                rank = 12
                cardName += 'Q'
            case 13:
                rank = 13
                cardName += 'K'
            case _:
                rank = card.rank
                cardName += str(card.rank)
        return Card(suit, rank, cardName, color, visible)
    #----------------------------

    def from_str(cardStr, visible):
        """
        Builds a card from a string
        """
        name = cardStr
        match cardStr[0]:
            case 'S':
                suit = 0
                color = 0
            case 'H':
                suit = 1
                color = 1
            case 'D':
                suit = 2
                color = 1
            case 'C':
                suit = 3
                color = 0
        match cardStr[1:]:
            case 'A':
                rank = 1
            case 'J':
                rank = 11
            case 'Q':
                rank = 12
            case 'K':
                rank = 13
            case _:
                rank = int(cardStr[1:])
        return Card(suit, rank, name, color, visible)
    #------------------------------
#===================

#===================
class GameState:
    """
    State of the game
    Attributes:
        - board - the current board state
        - score - the current score
    """
    def __init__(self, load):
        """
        Initializes the state
        Parameters:
            - load: If True, loads the last game from file. If False, generates a new one
        """
        self.score = 0
        #        b1  b2  b3  b4  b5  b5  b6  stock FS  FH  FD  FC
        #        0   1   2   3   4   5   6   7     8   9   10  11
        self.board = [[], [], [], [], [], [], [], [],   [], [], [], []]
        #generate a new board
        if not load:
            cardBox = deck_of_cards.DeckOfCards()
            cardBox.shuffle_deck()
            card = None
            numCards = 1
            for i in range(0, len(self.board)):
                #make table
                if i < 7:
                    for j in range(0, numCards):
                        if j == numCards - 1:
                            card = cardBox.give_random_card()
                            self.board[i].append(Card.from_card(card, True))
                        else:
                            card = cardBox.give_random_card()
                            self.board[i].append(Card.from_card(card, False))
                #make stock
                elif i == 7:
                    for j in range(0, len(cardBox.deck)):
                        card = cardBox.give_random_card()
                        self.board[i].append(Card.from_card(card, True))
                numCards += 1
            #outputs to text file
            with open('savedBoard.txt', 'w') as f:
                for i in range(0, len(self.board)):
                    for j in range(0, len(self.board[i])):
                        print(self.board[i][j].name, file=f)
        #load saved game
        elif load:
            #removes the empty string from every line
            cardList = []
            with open('savedBoard.txt', 'r') as f:
                inputList = f.readlines()
                for line in inputList:
                    cardList.append(line.strip())
            card = ''
            numCards = 1
            listIterator = 0
            for i in range(0, len(self.board)):
                #make table
                if i < 7:
                    for j in range(0, numCards):
                        if j == numCards - 1:
                            self.board[i].append(Card.from_str(cardList[listIterator], True))
                        else:
                            self.board[i].append(Card.from_str(cardList[listIterator], False))
                        listIterator += 1
                #make stock
                elif i == 7:
                    for j in range(listIterator, len(cardList)):
                        self.board[i].insert(0, Card.from_str(cardList[listIterator], True))
                        listIterator += 1
                numCards += 1
    #------------------------

    def copyState(self):
        #creates the new state
        newState = GameState(True)
        #copies the score
        newState.score = self.score
        #copies the board
        for i in range(0, len(self.board)):
            newState.board[i].clear()
            for j in range(0, len(self.board[i])):
                newState.board[i].append(self.board[i][j])
        return newState
    #--------------------

    def legal_moves(self):
        def isValid(card, k):
            if len(self.board[k]) > 0:
                #table rules (rank must be 1 above, color must be different)
                if k < 7:
                    if card.rank + 1 == self.board[k][len(self.board[k]) - 1].rank:
                        if card.color != self.board[k][len(self.board[k]) - 1].color:
                            return True
                #stock rules (cannot place a card on the stock)
                elif k == 7:
                    return False
                #foundation rules (rank must be 1 lower, suit must be the same)
                elif k > 7:
                    if card.rank - 1 == self.board[k][len(self.board[k]) - 1].rank:
                        if card.suit == self.board[k][len(self.board[k]) - 1].suit:
                            return True
            else:
                return False
        #--------------------
        legalMoves = []
        
        #TABLE
        for i in range(0, 7):
            for j in range(0, len(self.board[i])):
                if self.board[i][j].visible == 1:
                    currCard = self.board[i][j]
                    match currCard.rank:
                        #ACE
                        case 1:
                            for k in range(0, len(self.board)):
                                #TABLE
                                if k < 7:
                                    if isValid(currCard, k):
                                        legalMoves.append(((i, j), (k, len(self.board[k]))))
                                #EMPTY FOUNDATION
                                if k > 7 and len(self.board[k]) == 0:
                                    if k == 8 and currCard.suit == 0:
                                        legalMoves.append(((i, j), (k, 0)))
                                    elif k == 9 and currCard.suit == 1:
                                        legalMoves.append(((i, j), (k, 0)))
                                    elif k == 10 and currCard.suit == 2:
                                        legalMoves.append(((i, j), (k, 0)))
                                    elif k == 11 and currCard.suit == 3:
                                        legalMoves.append(((i, j), (k, 0)))
                        #KING
                        case 13:
                            for k in range(0, len(self.board)):
                                #EMPTY TABLE
                                if k < 7 and len(self.board[k]) == 0:
                                    legalMoves.append(((i, j), (k, 0)))
                                #FULL FOUNDATION
                                elif k > 7:
                                    if isValid(currCard, k):
                                        legalMoves.append(((i, j), (k, len(self.board[k]))))
                        #GENERAL
                        case _:
                            for k in range(0, len(self.board)):
                                #TABLE
                                if k < 7:
                                    if isValid(currCard, k):
                                        legalMoves.append(((i, j), (k, len(self.board[k]))))
                                #FOUNDATION
                                elif k > 7:
                                    if j == len(self.board[i]) - 1 and isValid(currCard, k):
                                        legalMoves.append(((i, j), (k, len(self.board[k]))))
        #FOUNDATION
        for i in range(8, 12):
            if len(self.board[i]) > 0:
                currCard = self.board[i][len(self.board[i]) - 1]
                match currCard.rank:
                    #ACE
                    case 1:
                        for k in range(0, 7):
                            #TABLE
                            if len(self.board[k]) > 0:
                                if isValid(currCard, k):
                                    legalMoves.append(((i, len(self.board[i]) - 1), (k, len(self.board[k]))))
                    #KING
                    case 13:
                        for k in range(0, 7):
                            if len(self.board[k]) == 0:
                                if isValid(currCard, k):
                                    legalMoves.append(((i, len(self.board[i]) - 1), (k, 0)))
                    #GENERAL
                    case _:
                        for k in range(0, 7):
                            if len(self.board[k]) > 0:
                                if isValid(currCard, k):
                                    legalMoves.append(((i, len(self.board[i]) - 1), (k, len(self.board[k]))))
        #STOCK
        if len(self.board[7]) > 0:
            currCard = self.board[7][len(self.board[7]) - 1]
            match currCard.rank:
                #ACE
                case 1:
                    for k in range(0, len(self.board)):
                        #TABLE
                        if k < 7:
                            if isValid(currCard, k):
                                legalMoves.append(((7, len(self.board[7]) - 1), (k, len(self.board[k]))))
                        #EMPTY FOUNDATION
                        if k > 7 and len(self.board[k]) == 0:
                            if k == 8 and currCard.suit == 0:
                                legalMoves.append(((7, len(self.board[7]) -1), (k, 0)))
                            elif k == 9 and currCard.suit == 1:
                                legalMoves.append(((7, len(self.board[7]) - 1), (k, 0)))
                            elif k == 10 and currCard.suit == 2:
                                legalMoves.append(((7, len(self.board[7]) - 1), (k, 0)))
                            elif k == 11 and currCard.suit == 3:
                                legalMoves.append(((7, len(self.board[7]) - 1), (k, 0)))
                #KING
                case 13:
                    for k in range(0, len(self.board)):
                        #EMPTY TABLE
                        if k < 7 and len(self.board[k]) == 0:
                            legalMoves.append(((7, len(self.board[7]) - 1), (k, 0)))
                        #FULL FOUNDATION
                        elif k > 7:
                            if isValid(currCard, k):
                                legalMoves.append(((7, len(self.board[7]) - 1), (k, len(self.board[k]))))
                #GENERAL
                case _:
                    for k in range(0, len(self.board)):
                        #TABLE
                        if k < 7:
                            if isValid(currCard, k):
                                legalMoves.append(((7, len(self.board[7]) - 1), (k, len(self.board[k]))))
                        #FOUNDATION
                        elif k > 7:
                            if isValid(currCard, k):
                                legalMoves.append(((7, len(self.board[7]) - 1), (k, len(self.board[k]))))
            #FLIP
            if len(self.board[7]) > 1:
                legalMoves.append(((7, len(self.board[7]) - 1), (7, 0)))
            
        return legalMoves
    #----------------

    def push(self, action):
        """
        Applies the action to the board and updates the score
        """
        srcLoc = action[0]
        dstLoc = action[1]

        #FLIP FOUNDATION
        if dstLoc[0] == 7:
            self.board[7].insert(0, self.board[7][len(self.board[7]) - 1])
            self.board[7].pop()
        #TO TABLE
        elif dstLoc[0] < 7:
            #FROM TABLE
            if srcLoc[0] < 7:
                #Last card?
                if srcLoc[1] == len(self.board[srcLoc[0]]) - 1:
                    #hidden card underneath?
                    if len(self.board[srcLoc[0]]) > 1 and self.board[srcLoc[0]][srcLoc[1] -1].visible == 0:
                        self.board[dstLoc[0]].append(self.board[srcLoc[0]][srcLoc[1]])
                        self.board[srcLoc[0]].remove(self.board[srcLoc[0]][srcLoc[1]])
                        self.board[srcLoc[0]][srcLoc[1] - 1].visible = True
                        self.score += 5
                    else:
                        self.board[dstLoc[0]].append(self.board[srcLoc[0]][srcLoc[1]])
                        self.board[srcLoc[0]].remove(self.board[srcLoc[0]][srcLoc[1]])
                #Middle Card
                else:
                    #hidden card underneath?
                    if len(self.board[srcLoc[0]]) > 1 and self.board[srcLoc[0]][srcLoc[1] -1].visible == 0:
                        self.board[dstLoc[0]].append(self.board[srcLoc[0]][srcLoc[1]])
                        self.board[srcLoc[0]].remove(self.board[srcLoc[0]][srcLoc[1]])
                        self.board[srcLoc[0]][srcLoc[1] - 1].visible = True
                        self.score += 5
                    else:
                        self.board[dstLoc[0]].append(self.board[srcLoc[0]][srcLoc[1]])
                        self.board[srcLoc[0]].remove(self.board[srcLoc[0]][srcLoc[1]])
                    #move the rest of the cards in the stack
                    for i in range(srcLoc[1], len(self.board[srcLoc[0]])):
                        self.board[dstLoc[0]].append(self.board[srcLoc[0]][srcLoc[1]])
                        self.board[srcLoc[0]].remove(self.board[srcLoc[0]][srcLoc[1]])
            #FROM STOCK
            elif srcLoc[0] == 7:
                self.board[dstLoc[0]].append(self.board[srcLoc[0]][srcLoc[1]])
                self.board[srcLoc[0]].remove(self.board[srcLoc[0]][srcLoc[1]])
                self.score += 5
            #FROM FOUNDATION
            elif srcLoc[0] > 7:
                self.board[dstLoc[0]].append(self.board[srcLoc[0]][srcLoc[1]])
                self.board[srcLoc[0]].remove(self.board[srcLoc[0]][srcLoc[1]])
                self.score -= 10
        #TO FOUNDATION
        elif dstLoc[0] > 7:
            #FROM TABLE
            if srcLoc[0] < 7:
                #Last card?
                if srcLoc[1] == len(self.board[srcLoc[0]]) - 1:
                    #hidden card underneath?
                    if len(self.board[srcLoc[0]]) > 1 and self.board[srcLoc[0]][srcLoc[1] -1].visible == 0:
                        self.board[dstLoc[0]].append(self.board[srcLoc[0]][srcLoc[1]])
                        self.board[srcLoc[0]].remove(self.board[srcLoc[0]][srcLoc[1]])
                        self.board[srcLoc[0]][srcLoc[1] - 1].visible = True
                        self.score += 15
                    else:
                        self.board[dstLoc[0]].append(self.board[srcLoc[0]][srcLoc[1]])
                        self.board[srcLoc[0]].remove(self.board[srcLoc[0]][srcLoc[1]])
                        self.score += 10
            elif srcLoc[0] == 7:
                self.board[dstLoc[0]].append(self.board[srcLoc[0]][srcLoc[1]])
                self.board[srcLoc[0]].remove(self.board[srcLoc[0]][srcLoc[1]])
                self.score += 10
    #-----------------------

    def is_game_over(self):
        """
        Checks if the game has been ended
        """
        currLM = self.legal_moves()
        moveCounter = 0
        #count the number of king swaps in the current moves
        for move in currLM:
            if move[0][1] == move[1][1]:
                moveCounter += 1
        #count the number of other card swaps in the current moves
        

        #if there are no cards in the stock and all moves are swaps there is no progression
        if len(self.board[7]) == 0 and moveCounter == len(currLM):
            return True
        #there are cards left in the stock and all moves are swaps
        elif len(self.board[7]) > 0 and moveCounter == len(currLM) - 1:
            #swaps the stock
            nextState = self.copyState()
            #go through every card in the stock and see if there will be more moves in the future
            for i in range(0, len(nextState.board[7])):
                #performs the stock flip
                nextState.push(currLM[len(currLM) - 1])
                #if the new stock card has more moves than the current then it offers a solution
                nextLM = nextState.legal_moves()
                if len(nextLM) > len(currLM):
                    return False
            #if no next card offers a solution there are no logical moves left
            return True

            raise NotImplementedError("check next moves")
    #-----------------------
#===================

"""
for i in range(0, len(self.board)):
    for j in range(0, len(self.board[i])):
        if j == len(self.board[i]) - 1:
            print(self.board[i][j].name)
        else:
            print(self.board[i][j].name, end = ' ')
"""

"""
#count the number of king swaps in the current moves
        for move in currLM:
            if move[0][1] == move[1][1]:
                moveCounter += 1
        #count the number of other card swaps in the current moves
        

        #if there are no cards in the stock and all moves are swaps there is no progression
        if len(self.board[7]) == 0 and moveCounter == len(currLM):
            return True
        #there are cards left in the stock and all moves are swaps
        elif len(self.board[7]) > 0 and moveCounter == len(currLM) - 1:
            #swaps the stock
            nextState = self.copyState()
            #go through every card in the stock and see if there will be more moves in the future
            for i in range(0, len(nextState.board[7])):
                #performs the stock flip
                nextState.push(currLM[len(currLM) - 1])
                #if the new stock card has more moves than the current then it offers a solution
                nextLM = nextState.legal_moves()
                if len(nextLM) > len(currLM):
                    return False
            #if no next card offers a solution there are no logical moves left
            return True

            raise NotImplementedError("check next moves")
"""