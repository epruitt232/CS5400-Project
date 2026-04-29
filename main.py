"""
main.py
=======
"""
import argparse
from colorama import init, Fore, Style
import os
import time

from solitaire_game import initial_state, terminal_test, result, evaluate


from agents.utility import UtilityAgent

from agents.player import PlayerAgent

# ------------------
# Agent Construction
# ------------------
def make_agent(name):
    name = name.lower()
    if name == 'utility':
        return UtilityAgent()
    elif name == 'player':
        return PlayerAgent()

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
def render_board(board, lastMove = None):
    def formatCard(card):
        if card == None:
            return '___'
        elif card.visible == 0:
            return '???'
        else:
            if card.color == 0:
                return Fore.BLACK + card.name.rjust(3) + Style.RESET_ALL
            elif card.color == 1:
                return Fore.RED + card.name.rjust(3) + Style.RESET_ALL
    lines = []
    #top lines
    lines.append('|--7-----------8---9---10--11-|--|')
    #stock and foundations
    lineBuilder = '| '
    for i in range(7, len(board)):
        if len(board[i]) > 0:
            lineBuilder += formatCard(board[i][len(board[i]) - 1]) + ' '
        else:
            lineBuilder += formatCard(None) + ' '
        if i == 7:
            lineBuilder += ' ' * 8
        elif i == len(board) - 1:
            lineBuilder += '| 0|'
    lines.append(lineBuilder)
    #diving line
    lines.append('|--0---1---2---3---4---5---6--|  |')
    #board
    for i in range(0, 19):
        lineBuilder = '| '
        for j in range(0, 7):
            if len(board[j]) == 0:
                lineBuilder += '    '
            else:
                try:
                    lineBuilder += formatCard(board[j][i]) + ' '
                except:
                    lineBuilder += '    '
            if j == 6:
                lineBuilder += '|' + str(i).rjust(2) + '|'
        lines.append(lineBuilder)
    #last row
    lines.append('|' + ('-' * 32) + '|')

    return lines

def render_info(moveNum, score, agentName, lastMove, totalTime):
    lines = []
    lines.append(('-' * 20) + '|')
    lines.append(' ' + 'SOLITIAIRE'.center(19, ' ') + '|')
    lines.append(('-' * 20) + '|')
    lines.append((' MOVES: ' + str(moveNum)).ljust(20) + '|')
    lines.append('|'.rjust(21))
    lines.append((' SCORE: ' + str(score)).ljust(20) + '|')
    lines.append('|'.rjust(21))
    lines.append((' TIME: ' + str(totalTime)).ljust(20) + '|')
    lines.append('|'.rjust(21))
    lines.append((' AGENT: ' + agentName).ljust(20) + '|')
    lines.append('|'.rjust(21))
    lines.append(' LAST MOVE:'.ljust(20) + '|')
    if lastMove == None:
        lines.append('  (_,_) -> (_,_)'.ljust(20) + '|')
    else:
        lines.append(('  ' + str(lastMove[0]) + ' -> ' + str(lastMove[1])).ljust(20) + '|')
    for i in range(1, 10):
        lines.append('|'.rjust(21))
    lines.append(('-' * 20) + "|")

    return lines

def draw_screen(board, moveNum, score, agentName, lastMove, totalTime):
    clear_screen()
    boardLines = render_board(board, lastMove)
    infoLines = render_info(moveNum, score, agentName, lastMove, totalTime)
    maxLen = max(len(boardLines), len(infoLines))
    while len(boardLines) < maxLen:
        boardLines.append('')
    while len(infoLines) < maxLen:
        infoLines.append('')
    for bLine, iLine in zip(boardLines, infoLines):
        print(bLine.ljust(34) + iLine)

def draw_game_over(board, lastMove):
    clear_screen()

    boardLines = render_board(board, lastMove)
    infoLines = []
    infoLines.append('--------------------|')
    infoLines.append('     GAME OVER      |')
    infoLines.append('--------------------|')

    maxLen = max(len(boardLines), len(infoLines))
    while len(boardLines) < maxLen:
        boardLines.append('')
    while len(infoLines) < maxLen:
        infoLines.append('')
    for bLine, iLine in zip(boardLines, infoLines):
        print(bLine.ljust(34) + iLine)
    print('')

# --------------
# Main Game Loop
# --------------
def play(agent, load = False):
    """
    Runs the game of Solitaire
    """
    state = initial_state(load)
    moveNum = 1
    lastMove = None
    score = 0
    startTime = time.time()
    totalTime = 0

    while not terminal_test(state):
        # --- Draw the Board ---
        draw_screen(state, moveNum, score, agent.name, lastMove, totalTime)
        # --- Get the Move
        move = agent.get_move(state)
        moveNum += 1

        # --- Apply the move
        if move == None:
            draw_game_over(state, lastMove)
            break
        else:
            lastMove = move
            state = result(state, move)
            moveNum += 1
            score = evaluate(state, score, lastMove)


# ---------------
# CLI Entry Point
# ---------------
def main():
    parser = argparse.ArgumentParser(description = 'Solitaire')
    parser.add_argument('--agent',
                        default = 'utility',
                        help = 'Which agent is playing: utility | ? | ? | player')
    parser.add_argument('--load',
                        action = 'store_true',
                        help = 'Loads the last puzzle')
    args = parser.parse_args()
    agent = make_agent(args.agent)

    #initialize colorama
    init()

    try:
        play(agent, load = args.load)
    finally:
        if hasattr(agent, 'quit'):
            agent.quit()

if __name__ == '__main__':
    main()