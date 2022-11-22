import math
import random
class GameBoard:
    def __init__(self):
        """Creates an empty game board"""
        self.board = [[],[],[],[]] # 4x4 List of GamePiece objects
    
    
    def create_new_game():
        """Makes a new game following the standard convention of putting 2 blocks of value 2 or 4 on the board"""
        
        block_1_position = (random.randint(0,3), random.randint(0,3))
        block_2_position = (random.randint(0,3), random.randint(0,3))
        
        block_1 = GamePiece(valueList={2:0.7, 4:0.3})
    
    def _place_piece(game_piece):
        """
        Places a provided GamePiece onto the board on an empty space
        :param game_piece: a GamePiece object
    
        :return: nothing
        """
        position = (random.randint(0,3), random.randint(0,3))

        


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
        else:

            # First, assert that no element is a non-power of 2 AND that the probabilities add up to 100%
            for k in valueList.keys():
                # This checks if the key is a power of 2 and does not equal 0
                # https://stackoverflow.com/questions/600293/how-to-check-if-a-number-is-a-power-of-2
                assert (k != 0) and ((k & (k - 1)) == 0)
            sum_of_probabilities = 0
            for v in valueList.values():
                # Add each probability to the total
                sum_of_probabilities += v
            assert sum_of_probabilities == 1.0
        

GameBoard()
    