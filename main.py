"""
main.py
=======
"""
import argparse
from colorama import init, Fore, Style
import os
import threading
import time

from agents.player import PlayerAgent
from agents.utility import UtilityAgent
from solitaire_game import initial_state, result, terminal_test

# ------------------
# Agent Construction
# ------------------
def make_agent(name):
    name = name.lower()
    if name == 'utility':
        return UtilityAgent()
    elif name == 'player':
        return PlayerAgent()
    else:
        return ValueError('Unknown agent: ' + name + '. Choose from: Utility, player, ?, ?')
#--------------------

# ----------------
# Terminal Control
# ----------------
def clear_screen():
    """
    Clears the terminal so the next draw replaces the old one
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# ---------------
# Board Rendering
# ---------------
def render_board(board):
    def formatCard(card):
        if card == None:
            return '___ '
        elif card.visible == 0:
            return '??? '
        else:
            if card.color == 0:
                return Fore.BLACK + card.name.rjust(3) + Style.RESET_ALL + ' '
            elif card.color == 1:
                return Fore.RED   + card.name.rjust(3) + Style.RESET_ALL + ' '
    #--------------------
    lines = []
    #top dividing line
    lines.append('|----7---------8---9---10--11-|--|')
    #stock and foundations
    if len(board[7]) > 0:
        lineBuilder = '|' + str(len(board[7]) - 1).rjust(2) + '|'
    else:
        lineBuilder = '| 0|'
    for i in range(7, len(board)):
        if len(board[i]) > 0:
            lineBuilder += formatCard(board[i][len(board[i]) - 1])
        else:
            lineBuilder += formatCard(None)
        #special cases for characters
        if i == 7:
            lineBuilder += ' ' * 6
        elif i == len(board) - 1:
            lineBuilder += '|  |'
    lines.append(lineBuilder)
    #dividing line
    lines.append('|--0---1---2---3---4---5---6--|  |')
    #table
    for i in range(0, 19):
        lineBuilder = '| '
        for j in range(0, 7):
            try:
                lineBuilder += formatCard(board[j][i])
            except:
                lineBuilder += '    '
            #special case for characters
            if j == 6:
                lineBuilder += '|' + str(i).rjust(2) + '|'
        lines.append(lineBuilder)
    #last row
    lines.append('|' + ('-' * 32) + '|')
    return lines
#-----------------------

def render_info(board, moveNum, score, agentName, lastMove, totalTime, gameOver):
    lines = []
    lines.append('|'.rjust(21, '-'))
    if gameOver:
        lines.append('Game Over'.center(20, ' ') + '|')
    elif not gameOver:
        lines.append('Solitaire'.center(20, ' ') + '|')
    lines.append('|'.rjust(21, '-'))
    lines.append((' MOVES: ' + str(moveNum)).ljust(20) + '|')
    lines.append('|'.rjust(21))
    lines.append((' SCORE: ' + str(score)).ljust(20) + '|')
    lines.append('|'.rjust(21))
    lines.append((f" TIME: {totalTime:.9f}").ljust(20) + '|')
    lines.append('|'.rjust(21))
    lines.append((' AGENT: ' + agentName).ljust(20) + '|')
    lines.append('|'.rjust(21))
    lines.append(' LAST MOVE:'.ljust(20) + '|')
    if lastMove == None:
        lines.append('  (_,_) -> (_,_)'.ljust(20) + '|')
        lines.append('|'.rjust(21))
    else:
        lines.append(('  ' + str(lastMove[0]) + ' -> ' + str(lastMove[1])).ljust(20) + '|')
        lines.append(('   ' + board[lastMove[1][0]][lastMove[1][1]].name.rjust(3) + '   ->  ' + board[lastMove[1][0]][lastMove[1][1] - 1].name.rjust(3)).ljust(20) + '|')
    for i in range(1, 9):
        lines.append('|'.rjust(21))
    lines.append('|'.rjust(21, '-'))

    return lines
#---------------------------------------------------------------

def draw_screen(state, moveNum, agentName, lastMove, totalTime, gameOver):
    clear_screen()
    boardLines = render_board(state.board)
    infoLines = render_info(state.board, moveNum, state.score, agentName, lastMove, totalTime, gameOver)
    maxLen = max(len(boardLines), len(infoLines))
    while len(boardLines) < maxLen:
        boardLines.append('')
    while len(infoLines) < maxLen:
        infoLines.append('')
    for bLine, iLine in zip(boardLines, infoLines):
        print(bLine.ljust(34) + iLine)
#----------------------------------------------------------------------

# --------------
# Main Game Loop
# --------------
def play(agent, load):
    """
    Runs the game of Solitaire
    """
    state = initial_state(load)
    move = None
    moveNum = 0
    lastMove = None
    totalTime = 0
    draw_screen(state, moveNum, agent.name, lastMove, totalTime, False)
    while not terminal_test(state):
        

        # --- Draw the Board ---
        draw_screen(state, moveNum, agent.name, lastMove, totalTime, False)

        # --- Get the Move ---
        t0 = time.time()
        move = agent.get_move(state)
        totalTime += time.time() - t0
        moveNum += 1
        
        #if move == None:
        #    draw_game_over(state, moveNum, agent.name, lastMove, totalTime)
        #    break

        # --- Apply the Move
        lastMove = move
        state = result(state, move)
    
    #draw_screen(state, moveNum, agent.name, lastMove, totalTime, True)

#---------------------

# ---------------
# CLI Entry Point
# ---------------
def main():
    """
    Interfaces with the CLI to start the program
    """
    parser = argparse.ArgumentParser(description = 'Solitaire')
    parser.add_argument('--agent',
                        default = 'utility',
                        help = 'Which agent is playing: utility | ? | ? | player')
    parser.add_argument('--load',
                        action = 'store_true',
                        help = 'Load the last puzzle')
    args = parser.parse_args()
    agent = make_agent(args.agent)    
    #initialize colorama
    init()
    try:
        play(agent, args.load)
    finally:
        if hasattr(agent, 'quit'):
            agent.quit()
#----------

if __name__ == '__main__':
    main()