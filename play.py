from game2048 import GameBoard, PerformanceTester
import sys
import argparse
import ai
'''
Main Program To Play The Game
'''

parser = argparse.ArgumentParser(description = "This program runs 2048 with given settings")
parser.add_argument("-player", help = "self = you play; computer = computer plays [default]")
parser.add_argument("-agent", help = "self = you play; computer = computer plays")
parser.add_argument("-iter", help = "number of AI iterations")
parser.add_argument("-graphics", help = "whether to show graphics (AI Only). Any argument is True, default is False")
# parser.add_argument("-outSize", help = "small = small output, large = large output. Default: small")
args = parser.parse_args()

# if args.outSize == "large":
#     outputSmall = False
# else:
#     outputSmall = True

# Dictionary of the Game Agents
gameAgentDict = {
    "DownRightGameAgent":ai.DownRightGameAgent,
    "RandomGameAgent":ai.RandomGameAgent,
    "MinimaxAgent":ai.MinimaxAgent
    }

if args.player == 'self' :
    board = GameBoard()
    board.create_new_game()
    board.play_as_person()
    
   
elif args.player == 'computer' or args.player == None:
    if (args.agent != None):
        if (args.agent not in gameAgentDict.keys()):
            print("Game Agent not in gameAgentDict. Be sure to add it!")
            print("Current options are:")
            print(gameAgentDict)
        else:
            if (args.iter != None):
                if (args.graphics != None):
                    runner = PerformanceTester(gameAgentDict[args.agent], iterations=int(args.iter),graphics=bool(args.graphics))
                else:   
                    runner = PerformanceTester(gameAgentDict[args.agent], iterations=int(args.iter))
            else:
                if (args.graphics != None):
                    runner = PerformanceTester(gameAgentDict[args.agent],graphics=bool(args.graphics))
                else:
                    runner = PerformanceTester(gameAgentDict[args.agent])

            
    else:
        print("You must pick a Game Agent using argument '-agent'")
else:
    print("Unknown arg for player: ", args.player)



