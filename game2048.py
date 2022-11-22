import math
import random
class GameBoard:
    def __init__(self):
        """Creates an empty game board"""
        # First fill it with None's
        self.board = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]] # 4x4 List of GamePiece objects
        # Then add empty GamePieces to each slot
        for r in range(4):
            for c in range(4):
                self.board[r][c] = GamePiece(empty=True)
    
    def create_new_game(self):
        """Makes a new game following the standard convention of putting 2 blocks of value 2 or 4 on the board"""
        
        self._clear_board()
        block_1 = GamePiece(valueList={2:0.7, 4:0.3})
        self._place_piece(block_1)
        block_2 = GamePiece(valueList={2:0.7, 4:0.3})
        self._place_piece(block_2)
    
    def _place_piece(self, game_piece):
        """
        Places a provided GamePiece onto the board on an empty space
        :param game_piece: a GamePiece object
    
        :return: nothing
        """
        position = (-1,-1)
        while self.get_value(position) != 0:
            position = (random.randint(0,3), random.randint(0,3))

        # Because the loop stopped, it must have found an empty square. Now place the gamePiece in that square
        print("Placing "+str(game_piece.value) + " at "+str(position))
        self.board[position[0]][position[1]] = game_piece

    def _clear_board(self):
        """Clear the board to setup for a new game"""
        
        for r in range(4):
            for c in range(4):
                self.board[r][c] = GamePiece(empty=True)

    def get_value(self, coord):
        """
        :coord: A tuple i.e. (2,3) representing the row, column
        :return: the value on gameBoard of the tuple. -1 if coords not on the board
        """
        # Case where the coordinate is not on the board
        if coord[0] < 0 or coord[0]>3 or coord[1] < 0 or coord[1] > 3:
            return -1
        else:
            return self.board[coord[0]][coord[1]].value
    
    def print(self):
        """
        Prints the board in a human readable way
        :return: Nothing
        """

        # create a table of all needed strings
        # ts is a list of table strings
        ts = [[" "," ", " ", " "],[" "," ", " ", " "],[" "," ", " ", " "],[" "," ", " ", " "]]
        for r in range(4):
            for c in range(4):
                if self.get_value((r,c)) != 0:
                    ts[r][c] = str(self.get_value((r,c)))
        # This thing is a monster because of string interpolation
        empty_board = f"""
            ------------------------------------------------                     
            |{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}|{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}|{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}|{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}|
            |{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}|{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}|{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}|{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}|
            |{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}|{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}|{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}|{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}|
            |{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}{ts[0][0]}|{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}{ts[0][1]}|{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}{ts[0][2]}|{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}{ts[0][3]}|
            ------------------------------------------------
            |{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}|{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}|{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}|{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}|
            |{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}|{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}|{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}|{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}|
            |{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}|{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}|{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}|{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}|
            |{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}{ts[1][0]}|{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}{ts[1][1]}|{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}{ts[1][2]}|{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}{ts[1][3]}|
            ------------------------------------------------
            |{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}|{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}|{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}|{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}|
            |{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}|{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}|{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}|{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}|
            |{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}|{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}|{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}|{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}|
            |{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}{ts[2][0]}|{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}{ts[2][1]}|{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}{ts[2][2]}|{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}{ts[2][3]}|
            ------------------------------------------------
            |{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}|{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}|{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}|{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}|
            |{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}|{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}|{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}|{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}|
            |{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}|{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}|{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}|{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}|
            |{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}{ts[3][0]}|{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}{ts[3][1]}|{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}{ts[3][2]}|{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}{ts[3][3]}|
            ------------------------------------------------
            
        """
        # self.__single_print_block()
        print(empty_board)

    

        
   
class GamePiece:
    def __init__(self, value=0, valueList={}, empty=False):
        """
        Initializer that takes a value OR map of values and their probability and creates a game piece accordingly \n
        To pass a value directly, simply do not supply a valueList. If you supply a valueList, the value param is ignored \n
        For example valueList of {2:0.3, 4:0.4, 8:0.3} would have a 30% chance of 2, 40% chance of 4, etc

        :value: Pass a value directly into the GamePiece
        :valueList: Map of value:probabilities i.e. {2:0.3, 4:0.4, 8:0.3}
        :empty: Make an empty GamePiece if true
        """
        # If valueList was empty, then just make it the value
        if empty:
            self.value = 0
        elif (len(valueList) == 0):
            self.value = value
        elif (len(valueList) == 1):
            # if one element in valueList, make that the answer
            self.value = valueList.keys()[1]
        else:

            # First, assert that no element is a non-power of 2 AND that the probabilities add up to 100%
            sum_of_probabilities = 0
            for k,v in valueList.items():
                # This checks if the key is a power of 2 and does not equal 0
                # https://stackoverflow.com/questions/600293/how-to-check-if-a-number-is-a-power-of-2
                assert (k != 0) and ((k & (k - 1)) == 0)
                sum_of_probabilities += v
                if v == 1.0:
                    # if something an 100% chance, that's the value
                    self.value = k
                    return
                
            # This ensures that all of the probabilities add up to 1.0
            assert sum_of_probabilities == 1.0
        
            #  Now, we can actually find the value
            #  Create a random number between 0 and 1
            rand_num = random.random()
            total_prob = 0.0
            for k,v in valueList.items():
                total_prob += v
                if rand_num < total_prob:
                    self.value = k
                    return
            
        

board = GameBoard()
board.create_new_game()
board.print()