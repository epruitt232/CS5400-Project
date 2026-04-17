#Project Plan
Solitaire (Klondike)

#Movation:
    Klondike Solitaire is a partially observable, single agent deterministic, sequential, static, discrete, and known environment. The player must place all cards from the standard 52 card deck into 4 foundation piles sorted into suits. This project explores how AI techniques can be applied to Klondike Solitaire to find the most efficient moves to clear a board.

#Problem Statement:
    Design an enviromnent and AI system that solves Klondike Solitaire given the current board state and does so with the highest score.

#Objective:
    To measure the efficiency of agents the variables that will be recorded is their high score and the amount of moves that were made in order to win.

#Methods:
    * Intelligence: goal/utility agent
        This agent will infer the state of the game, the last action, and based off the transiton rules infer what the next move should be.
    * Adverserial Search: Monte-Carlo search tree
        This agent will infer the game state and search for the next best move.
    * Bayesian Network
        This agent will infer the game state and find the probability of the next move leading to a win.

#Percepts
    The agent can see the state of the draw deck (top card), board(visible cards), and fonudation piles(top card). The agent will also be able to see how many moves it has made and the current score it has earned.

#Environment:
    The environment will be built to have 1 draw deck, 4 foundation piles, and the staircased board of 7 piles of cards increasing in height from 1 to 7. The cards will have a variable to store if they are hidden or visible to the agent.

#Actions:
    The agent can move a card from the stock to the foundation or board, move a card from the board to foundation or another place on the board. There are 2 rules governing a legal action: rank and color.
        Rank Rule:
            A card can only be placed on an upper value. For example a 9 must be placed on a 10, a 10 cannot be placed on a 9, 8, 7, etc..
        Color Rule:
            A red card cannot be placed on a black card and a black card cannot be placed on a red card. For example a black 9 must be placed on a red 10.
        EXCEPTIONS:
            * Foundation piles: They are placed in the same color and suit in ascending order from ace to king with aces starting the stack from empty. For example Ace of spades, 2 of spades, 3 of spades, ..., king of spades
            * Empty stack: If a stack is empty then only a king can be placed to start a stack.

#Sensors:
    The agent can sense the cards on the board, stock, and foundations as well as see its move count and score.

#Performance Measure:
    We will evaluate the agent's performance primarily based on its final score and if it solved the board. However, we will also observe its final move count and score.
    The score is determined by the rules of Solitaire:
    * +10 points for moving a card form the board or stock to foundation (-10 for removing a card from foundation).
    * + 5 points for revealing a card on the board.
    * + 5 points for moving a card from the stock to the board.

#Team Members
Elijah Pruitt, Joshua Kroft, Brooklyn Hunt

#Team Name:
JEB

#Contributions:
Elijah Pruitt
    * Environment
    * Bayseian Network Agent

Joshua Kroft:
    * Environment
    * Utility Agent

Brooklyn Hunt:
    * Environment
    * Monte-Carlo Search Tree