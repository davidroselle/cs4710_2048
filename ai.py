'''Put AI Code Here'''

from enum import Enum
import random
import game2048 





class GenericGameAgent():
    """Base class for other game agents to extend"""
    def __init__(self, gameBoard):
        self.gameBoard = gameBoard
        self.previousMove = game2048.Direction.DOWN
        self.moves = 0
    def compute(self):
        '''EACH CLASS SHOULD OVERRIDE THIS'''
        raise NotImplementedError

class DownRightGameAgent(GenericGameAgent) :
    """Naive game agent that simply alternates moving Down and Right. Accepts a GameBoard (and maybe other params)"""
    def __init__(self, gameBoard):
        self.gameBoard = gameBoard
        self.previousMove = game2048.Direction.DOWN
        self.moves = 0
        # super().__init__(gameBoard)

    def compute(self):
        '''Returns the move that should be done by the agent'''
        # print("Computing next move", self.previousMove, self.moves)
        if (self.previousMove == game2048.Direction.DOWN):
            self.moves+=1  ##Do we want to perform checks to make sure moves are valid?
            self.previousMove = game2048.Direction.RIGHT
            return game2048.Direction.RIGHT
        else: 
            self.moves+=1
            self.previousMove = game2048.Direction.DOWN
            return game2048.Direction.DOWN

class RandomGameAgent(GenericGameAgent) :
    """Naive game agent that randomly chooses a move different from the previous move. Accepts a GameBoard (and maybe other params)"""
    def __init__(self, gameBoard):
        self.gameBoard = gameBoard
        self.previousMove = game2048.Direction.DOWN
        self.moves = 0 

    def compute(self):
        '''Returns the move that should be done by the agent'''
        # print("Computing next move", self.previousMove, self.moves)
        randInt = random.randint(1,4)
        self.moves += 1 ##If we want to make sure moves are valid before counting in future, can modify this line.
        if randInt == 1:
            self.previousMove = game2048.Direction.UP
            return game2048.Direction.UP
        elif randInt == 2:
            self.previousMove = game2048.Direction.DOWN
            return game2048.Direction.DOWN
        elif randInt == 3:
            self.previousMove = game2048.Direction.LEFT
            return game2048.Direction.LEFT
        else:
            self.previousMove = game2048.Direction.RIGHT
            return game2048.Direction.RIGHT


    
