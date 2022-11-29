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

class MinimaxAgent(GenericGameAgent):
    '''MiniMaxi agent similar to the implementation of our pacman agent.'''

    def __init__(self, gameBoard):
        self.gameBoard = gameBoard
        self.previousMove = game2048.Direction.DOWN
        self.moves = 0

    def compute(self):
        '''Returns the move that should be done by the agent'''
        self.moves += 1
        bestMove = None
        maxScore = 0
        for nextMove in game2048.Direction:
            initial = game2048.GameBoard()  # copy of initial board
            for r in range(4):
                for c in range(4):
                    initial.set_value((r, c), self.gameBoard.get_value((r, c)))
                # print("initial board : " + "\n")
                # game2048.print_new_board(initial)
            score = self.calculateScore(initial, nextMove)
            if score > maxScore:
                maxScore = score
                bestMove = nextMove
        return bestMove

    def calculateScore(self, board, move):
        initial = game2048.GameBoard()  # copy of initial board
        for r in range(4):
            for c in range(4):
                initial.set_value((r, c), board.get_value((r, c)))
        newBoard = game2048.simulate_move(initial, move)
        if game2048.check_boards(board, newBoard):
            return 0
        return self.generateScore(newBoard, 0, 1)

    def generateScore(self, board, depth, depthLimit):
        ''' depthLimit makes sure recursion ends. Could be extended to a greater number than 3 '''
        if depth == depthLimit:
            return self.calculateFinalScore(board)

        total = 0
        for r in range(4):
            for c in range(4):
                if board.get_value((r,c)) == 0:
                    newBoard2 = board
                    newBoard2.set_value((r,c), 2)
                    moveScore2 = self.calculateMoveScore(newBoard2, depth, depthLimit)
                    total += (0.7*moveScore2) #proba based on whether new_piece is 2 or 4.
                    newBoard4 = board
                    newBoard4.set_value((r,c), 4)
                    moveScore4 = self.calculateMoveScore(newBoard4, depth, depthLimit)
                    total += (0.3*moveScore4)
        return total

    def calculateMoveScore(self, board, depth, depthLimit):
        maxScore = 0
        for move in game2048.Direction:
            initial = game2048.GameBoard()  # copy of initial board
            for r in range(4):
                for c in range(4):
                    initial.set_value((r, c), board.get_value((r, c)))
            newBoard = game2048.simulate_move(initial, move)
            if not game2048.check_boards(board, newBoard):
                score = self.generateScore(newBoard, depth+1, depthLimit)
                maxScore = max(score, maxScore)
        return maxScore

    def calculateFinalScore(self, board):
        '''

        similar to evaluation function in pacman
        need to figure out values (different factors?)
        For now, I just listed out what I could think of.

        empty : number of empty GamePiece in board
        totalValue : values of individual GamePiece

        '''
        empty = 0
        totalValue = 0
        for r in range(4):
            for c in range(4):
                if board.get_value((r,c)) == 0:
                    empty += 1
                else:
                    totalValue += board.get_value((r,c))

        score = 0.7*empty + 0.3*totalValue
        return score



