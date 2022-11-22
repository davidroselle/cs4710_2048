from game2048 import GameBoard
import sys
import argparse
'''
Main Program To Play The Game
'''

parser = argparse.ArgumentParser(description = "This program runs 2048 with given settings")
parser.add_argument("-player", help = "self = you play; computer = computer plays")
parser.add_argument("-outSize", help = "small = small output, large = large output. Default: small")
args = parser.parse_args()

if args.outSize == "large":
    outputSmall = False
else:
    outputSmall = True


if args.player == 'self' or args.player == None:
    board = GameBoard()
    board.create_new_game()
    
    
elif args.player == 'computer':
    print("Computer play not implemented yet!")
else:
    print("Unknown arg for player: ", args.player)



