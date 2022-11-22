from game2048 import GameBoard
import sys
import argparse
'''
Main Program To Play The Game
'''

parser = argparse.ArgumentParser(description = "This program runs 2048 with given settings")
parser.add_argument("-player", help = "self = you play; computer = computer plays")
parser.add_argument("-outSize", help = "Small = small output, Large = large output. Default: Small")
args = parser.parse_args()

if args.outSize == "Large":
    outputSmall = False
else:
    outputSmall = True


if args.player == 'self' or args.player == None:
    board = GameBoard()
    board.create_new_game()
    board.print(smallBoard = outputSmall)
elif args.player == 'computer':
    board = GameBoard()
    board.create_new_game()
    board.print(smallBoard = outputSmall)
else:
    print("Unknown arg for player: ", args.player)



