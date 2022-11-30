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
        
        

class GreedyAgent(GenericGameAgent):
    def __init__(self, gameBoard):
        self.gameBoard = gameBoard
        self.previousMove = game2048.Direction.DOWN
        self.moves = 0

    def compute(self):
        '''

        current version just tries to keep bigger numbers in down right corner

        Probably this will be replaced by the minimax agent and minimax agent needs to be improved with better
        heuristics

        '''
        self.moves += 1
        bestMove = None
        maxScore = 0

        for nextMove in game2048.Direction:
            initial = game2048.GameBoard()  # copy of initial board
            for r in range(4):
                for c in range(4):
                    initial.set_value((r, c), self.gameBoard.get_value((r, c)))
            temp_board = game2048.simulate_move(initial, nextMove)
            total = calculate_with_grid(temp_board)
            if total >= maxScore:
                maxScore = total
                bestMove = nextMove

        return bestMove

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
            if score >= maxScore:
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
        ''' depthLimit makes sure recursion ends. Could be extended to a greater number than 1 but takes LONG '''
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

        using grid does help with result but still need better.

        from research: smoothness and monotonicity (!!)

        '''
        empty = 0
        for r in range(4):
            for c in range(4):
                if board.get_value((r,c)) == 0:
                    empty += 1

        totalValue = calculate_with_grid(board)

        score = 0.9*empty + 0.1*totalValue
        return score

def calculate_with_grid(board):
    '''

    idea: https://medium.com/@bartoszzadrony/beginners-guide-to-ai-and-writing-your-own-bot-for-the-2048-game-4b8083faaf53

    '''

    score = 0

    gridScore = game2048.GameBoard()
    gridScore.set_value((0, 0), 4**3)
    gridScore.set_value((0, 1), 4**2)
    gridScore.set_value((0, 2), 4**1)
    gridScore.set_value((0, 3), 4**0)
    gridScore.set_value((1, 0), 4**4)
    gridScore.set_value((1, 1), 4**5)
    gridScore.set_value((1, 2), 4**6)
    gridScore.set_value((1, 3), 4**7)
    gridScore.set_value((2, 0), 4**11)
    gridScore.set_value((2, 1), 4**10)
    gridScore.set_value((2, 2), 4**9)
    gridScore.set_value((2, 3), 4**8)
    gridScore.set_value((3, 0), 4**12)
    gridScore.set_value((3, 1), 4**13)
    gridScore.set_value((3, 2), 4**14)
    gridScore.set_value((3, 3), 4**15)

    for r in range(4):
        for c in range(4):
            score += gridScore.get_value((r, c)) * board.get_value((r, c))

    return score