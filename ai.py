'''Put AI Code Here'''

from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class GenericGameAgent():
    """Base class for other game agents to extend"""
    def __init__(self, gameBoard):
        self.gameBoard = gameBoard
        self.previousMove = Direction.DOWN
        self.moves = 0
    def compute(self):
        '''EACH CLASS SHOULD OVERRIDE THIS'''
        raise NotImplementedError

class DownRightGameAgent(GenericGameAgent) :
    """Naive game agent that simply alternates moving Down and Right. Accepts a GameBoard (and maybe other params)"""
    def __init__(self, gameBoard):
        self.gameBoard = gameBoard
        self.previousMove = Direction.DOWN
        self.moves = 0
        # super().__init__(gameBoard)

    def compute(self):
        '''Returns the move that should be done by the agent'''
        # print("Computing next move", self.previousMove, self.moves)
        if (self.previousMove == Direction.DOWN):
            self.moves+=1
            self.previousMove = Direction.RIGHT
            return Direction.RIGHT
        else: 
            self.moves+=1
            self.previousMove = Direction.DOWN
            return Direction.DOWN

    
