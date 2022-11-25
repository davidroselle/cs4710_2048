import math
import random
from enum import Enum
import ai


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class GameBoard:
    def __init__(self):
        """Creates an empty game board"""
        # First fill it with None's
        self.board = [[None, None, None, None], [None, None, None, None], [
            None, None, None, None], [None, None, None, None]]  # 4x4 List of GamePiece objects
        # Then add empty GamePieces to each slot
        for r in range(4):
            for c in range(4):
                self.board[r][c] = GamePiece(empty=True)

  
    def create_new_game(self):
        """Makes a new game following the standard convention of putting 2 blocks of value 2 or 4 on the board"""

        self._clear_board()
        block_1 = GamePiece(valueList={2: 0.7, 4: 0.3})
        self._place_piece(block_1)
        block_2 = GamePiece(valueList={2: 0.7, 4: 0.3})
        self._place_piece(block_2)
        

    def play_as_person(self):
        '''Play the game as a person (as opposed to the computer'''
        self.create_new_game()
        self.__begin_game()

    def play_as_computer(self, gameAgent:ai.GenericGameAgent):
        '''Play the game as a computer. takes in the gameAgent'''
        """TODO: This is not working yet, pieces aren't moving (but they move when it's self play... weird) """
        self.create_new_game()
        agent = gameAgent(self)
        print("Initial Board")
        self.print(smallBoard=True)
        
        while True:
            if (self._check_if_lose()):
                print("After",agent.moves,"moves, you lost")
                print("YOU LOSE THE GAME")
                break
            
            
            

            self.move(agent.compute())
            self.print(smallBoard=True)
            
            if self.win_game() == True:
                print("After",agent.moves,"moves, you won")
                print("YOU WON THE GAME!")
                break

    def __begin_game(self):
        """Playing game as person"""
        # printing controls for user
        print("Commands are as follows: ")
        print("'W'/'w' : Up")
        print("'S'/'s' : Down")
        print("'A'/'a' : Left")
        print("'D'/'d' : Right")
        print("'W'/'w' : Quit game")

        print("Initial Board")
        self.print(smallBoard=True)

        while True:
            next_move = input("\n\nNext Move (w,a,s,d, or q to quit): ")
            # Before processing the move, see if there is a spot to put it (you lose it there is not)
            if (self._check_if_lose()):
                print("YOU LOSE THE GAME")
                break
            if next_move == "w" or next_move == "W":
                self.move(Direction.UP)
            elif next_move == "a" or next_move == "A":
                self.move(Direction.LEFT)
            elif next_move == "s" or next_move == "S":
                self.move(Direction.DOWN)
            elif next_move == "d" or next_move == "D":
                self.move(Direction.RIGHT)
            elif next_move == "q" or next_move == "Q":
                break
            else:
                print("Unrecognized move: '"+next_move +
                      "'... Moves must be w, a, s, d followed by Enter Key. q to Quit")
                continue
            self.print(smallBoard=True)
            if self.win_game() == True:
                print("YOU WON THE GAME!")
                break

    def _place_piece(self, game_piece):
        """
        Places a provided GamePiece onto the board on an empty space \n
        This will also check if you lose, as if a piece cannot be placed then you lose
        :param game_piece: a GamePiece object

        :return: nothing
        """

        position = (-1, -1)

        while self.get_value(position) != 0:
            position = (random.randint(0, 3), random.randint(0, 3))

        # Because the loop stopped, it must have found an empty square. Now place the gamePiece in that square
        # print("Placing "+str(game_piece.value) + " at "+str(position))
        self.board[position[0]][position[1]] = game_piece

    def _check_if_lose(self):
        """ Checks a board to see if the player should lose by counting the number of empty GamePieces
        :return: True if Lose, False otherwise
        """

        for row in range(4):
            for col in range(4):
                if (self.get_value((row, col)) == 0):
                    # if there is even a single empty square, this is not a loss
                    return False
        # If an empty was never found, then it's a loss
        return True

    def _clear_board(self):
        """Clear the board to setup for a new game"""

        for r in range(4):
            for c in range(4):
                self.board[r][c] = GamePiece(empty=True)

    def win_game(self):
        for r in range(4):
            for c in range(4):
                if self.get_value((r, c)) == 2048:
                    return True
        return False

    def get_value(self, coord):
        """
        :coord: A tuple i.e. (2,3) representing the row, column
        :return: the value on gameBoard of the tuple. -1 if coords not on the board
        """
        # Case where the coordinate is not on the board
        if coord[0] < 0 or coord[0] > 3 or coord[1] < 0 or coord[1] > 3:
            return -1
        else:
            return self.board[coord[0]][coord[1]].value

    def _shift_pieces(self, dir):
        """Called by move to shift the pieces (no combination)"""
        # First, shift everything so it is correct without doing any combinations

        # External is the row iterator for left/right; columns for up/down
        for external in range(4):
            if dir == Direction.DOWN or dir == Direction.RIGHT:
                spot_to_place = 3
            else:
                spot_to_place = 0
            for internal in range(4):
                # Now split based on whether down or up
                if dir == Direction.DOWN:
                    # Makes sense to go backwards
                    reverse_index = 3-internal
                    # the placement of the initial non-empty piece found (bottom row)

                    # Now, starting from the bottom spot shift a non-empty game piece as far down as possible
                    if self.get_value((reverse_index, external)) != 0:
                        self._shift_one_piece(
                            reverse_index, external, spot_to_place, external)
                        spot_to_place -= 1
                if dir == Direction.UP:
                    # Same as down just without the reverse_index

                    # Now, starting from the bottom spot shift a non-empty game piece as far down as possible
                    if self.get_value((internal, external)) != 0:
                        self._shift_one_piece(
                            internal, external, spot_to_place, external)
                        spot_to_place += 1
                if dir == Direction.LEFT:
                    # Same as right just without the reverse_index
                    # note that now external is rows, while internal is columns

                    # Now, starting from the bottom spot shift a non-empty game piece as far down as possible
                    if self.get_value((external, internal)) != 0:
                        self._shift_one_piece(
                            external, internal, external, spot_to_place)
                        spot_to_place += 1
                if dir == Direction.RIGHT:

                    reverse_index = 3-internal
                    # Now, starting from the bottom spot shift a non-empty game piece as far down as possible
                    if self.get_value((external, reverse_index)) != 0:
                        self._shift_one_piece(
                            external, reverse_index, external, spot_to_place)
                        spot_to_place -= 1

    def _combine_pieces(self, dir):
        """ Called by move to combine adjacent pieces """
        # Now do the combinations since everything is shifted
        # External is the row iterator for left/right; columns for up/down
        for external in range(4):

            for internal in range(4):
                # Now split based on whether down or up
                if dir == Direction.DOWN:
                    # Makes sense to go backwards
                    reverse_index = 3-internal

                    if (reverse_index >= 1):
                        # Now, starting from the bottom spot check if the spot above it is the same
                        if self.get_value((reverse_index, external)) == self.get_value((reverse_index-1, external)):
                            self._perform_combination(
                                reverse_index, external, reverse_index-1, external, dir)

                elif dir == Direction.UP:
                    # Same as down just without the reverse_index
                    if (internal <= 2):
                        # Now, starting from the bottom spot check if the spot above it is the same
                        if self.get_value((internal, external)) == self.get_value((internal+1, external)):
                            self._perform_combination(
                                internal+1, external, internal, external, dir)
                elif dir == Direction.LEFT:
                    # Same as right just without the reverse_index
                    # note that now external is rows, while internal is columns
                    if (internal <= 2):
                        # Now, starting from the bottom spot check if the spot above it is the same
                        if self.get_value((external, internal)) == self.get_value((external,internal+1)):
                            self._perform_combination(
                                external, internal,  external, internal+1, dir)
                        # else:
                            # print("Not combining",external, internal)
                elif dir == Direction.RIGHT:
                    # Makes sense to go backwards
                    reverse_index = 3-internal

                    if (reverse_index >= 1):
                        # Now, starting from the bottom spot check if the spot above it is the same
                        if self.get_value((external, reverse_index)) == self.get_value((external,reverse_index-1)):
                            self._perform_combination(
                                external, reverse_index,  external, reverse_index-1, dir)

    def move(self, dir):
        """
        Core function of when an key is pressed
        :citation: https://www.geeksforgeeks.org/2048-game-in-python/ \n
        :usage: Psuedocode about how to compute a move (transpose, etc) ONLY [remove if i never end up using this]
        """
        """TODO: don't allow a move if it doesn't change anything"""

        self._shift_pieces(dir)

        self._combine_pieces(dir)

        new_piece = GamePiece(valueList={2: 0.7, 4: 0.3})
        self._place_piece(new_piece)
        print("Moved "+str(dir))

    def _shift_one_piece(self, row, column, new_row, new_column):
        """Helper function within the move function that shifts a single piece on a gameBoard in a provided direction\n

        :row: the current row of the gamePiece
        :column: the current column of the gamePiece
        :new_row: the new row of the gamePiece
        :new_column: the new column of the gamePiece
        """
        # print("Intermediate move",row, column,"to",new_row,new_column)
        # prevent unneceesary in-place moves
        if not (row == new_row and column == new_column):
            # gather the gamepiece object
            gamepiece = self.board[row][column]
            # put the gamepiece in the new slot
            self.board[new_row][new_column] = gamepiece

            self.board[row][column] = GamePiece(empty=True)

    def _perform_combination(self, r1, c1, r2, c2, dir):
        """
        Combines two gamePieces into a single. Then performs a shift to account for the combination
        :r1: row of gamePiece 1
        :c1: column of gamePiece 1
        :r2: row of gamePiece 2
        :c2: column of gamePiece 2

        """
        # print("Combining", r1, c1, "with", r2, c2)
        # Call combine on the primary piece
        self.board[r1][c1].combine()
        self.board[r2][c2].make_empty()
        # Shift after a combination to keep it in line
        self._shift_pieces(dir)

    def print(self, smallBoard=True):
        """
        Prints the board in a human readable way
        :smallBoard: Bool that prints the board in a smaller and more efficient way if True
        :return: Nothing
        """

        # create a table of all needed strings
        # ts is a list of table strings
        ts = [[" ", " ", " ", " "], [" ", " ", " ", " "],
              [" ", " ", " ", " "], [" ", " ", " ", " "]]
        for r in range(4):
            for c in range(4):
                if self.get_value((r, c)) != 0:
                    ts[r][c] = str(self.get_value((r, c)))
        # This thing is a monster because of string interpolation

        if smallBoard:
            printed_board = f"""
            -----------------
            | {ts[0][0]} | {ts[0][1]} | {ts[0][2]} | {ts[0][3]} |
            -----------------
            | {ts[1][0]} | {ts[1][1]} | {ts[1][2]} | {ts[1][3]} |
            -----------------
            | {ts[2][0]} | {ts[2][1]} | {ts[2][2]} | {ts[2][3]} |
            -----------------
            | {ts[3][0]} | {ts[3][1]} | {ts[3][2]} | {ts[3][3]} |
            -----------------
            """

        else:
            printed_board = f"""
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
        print(printed_board)


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
            for k, v in valueList.items():
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
            for k, v in valueList.items():
                total_prob += v
                if rand_num < total_prob:
                    self.value = k
                    return

    def combine(self):
        """Multiplies a GamePiece's value by 2 (which happens when combines)"""
        self.value *= 2

    def make_empty(self):
        self.value = 0
