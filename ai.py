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
        self.attempts = 0 # To prevent infinite loops
        # super().__init__(gameBoard)

    def compute(self):
        '''Returns the move that should be done by the agent'''
        # print("Computing next move", self.previousMove, self.moves)
        if (self.previousMove == game2048.Direction.DOWN):
            direction = game2048.Direction.RIGHT
            self.previousMove = direction # To avoid infinite loops
            if self.gameBoard.check_if_move_legal(direction):
                
                self.moves += 1
                self.attempts = 0
                return direction
            else:
                self.attempts +=1
                if self.attempts >= 2:
                    # if there have been two consecutive whiffs, move left/right to escape infinite loop
                    self.attempts = 0
                    return game2048.Direction.LEFT
                    
        else: 
            direction = game2048.Direction.DOWN
            self.previousMove = direction  # To avoid infinite loops
            if self.gameBoard.check_if_move_legal(direction):
                self.moves += 1
                
                self.attempts = 0
                return direction
            else:
                self.attempts += 1
                if self.attempts >= 2:
                    # if there have been two consecutive whiffs, move left/right to escape infinite loop
                    self.attempts = 0
                    return game2048.Direction.UP
            

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
        
        int_to_dir = {1:game2048.Direction.UP, 2:game2048.Direction.DOWN, 3:game2048.Direction.LEFT, 4:game2048.Direction.RIGHT}
        direction = int_to_dir[randInt]
        if self.gameBoard.check_if_move_legal(direction):
            self.previousMove = direction
            self.moves += 1
            return direction
        
        


    
