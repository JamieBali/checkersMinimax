import pygame

pygame.init()
screen = pygame.display.set_mode((500,600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

class Tile:
    def __init__(self, position, piece):
        self.piece = 0       # 0 is empty, 1 for red, 2 for black
        


###
#
# The game playing agent. When initialised, it'll need to take the difficulty.
# Each turn, the board state will be passed to the agent and it use the minimax algorithm 
# with alpha-beta pruning to find an optimal move.
# The moves will be returned in the form of a tuple (or maybe a list, whichever is easier to implement),
# with the structure (from, to, ...) where the tuple will increase in size of any multiple captures the AI 
# performs.
#
###
class Agent:
    def __init__(self, difficulty):
        self.depth = difficulty

    def getBoardValue(board):
        value = 0
        
        # processing here
        
        return value

    ###
    #
    # When generating the possible moves, we will first look for captures as they must take precedence.
    # Since captures are manditory, if the possible moves stack is empty after this processing, we will
    # perform a second run to get regular moves. This is slightly less efficient time-wise, but uses less
    # storage space.
    #
    ###
    def getPossibleMoves(board, player):
        moves = []

        # processing here

        return moves

    ###
    #
    # The move function will take the board state and run minimax on it to generate an optimal move.
    #
    ###
    def move(self, boardState):
        optimal = (0,0)

        # 

        return optimal

    ###
    #
    # Rather than writing a seperate system to find hints, we can more easily rotate the board 180 degrees
    # and put the rotated board through the regular agent. We then need to remember to rotate the board back
    # to normal before returning the move.
    #
    ###
    def hint(self, boardState):
        suggestion = "temp to remove error markers"

        # rotatedBoard = rotate(boardState, 180)
        # suggestion = move(self, rotatedBoard)
        # suggestion = rotate(suggestion, 180)

        return suggestion
 
###
#
# Main function. Takes no inputs.
# This is where the checkers game will be run from.
#
###
if __name__ == '__main__':
    
    # in order to reduce the size of the grid
    board = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]: # confirm that it is a left click.
                    x, y = pygame.mouse.get_pos()
                    print(str(x) + " " + str(y))

                    # get which tile was clicked
                    # highlight possible moves

        clock.tick(30)
        pygame.display.update()
