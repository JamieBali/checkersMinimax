import pygame

pygame.init()
screen = pygame.display.set_mode((500,600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

class Tile:
    def __init__(self, text,  pos, font, bg="black", feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def show(self):
        screen.blit(button1.surface, (self.x, self.y))
 
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change_text(self.feedback, bg="red")

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

    ###
    #
    # The move function will take the board state and run minimax on it to generate an optimal move 
    #
    ###
    def move(self, boardState):

 
###
#
# Main function. Takes no inputs.
# This is where the checkers game will be run from.
#
###
if __name__ == '__main__':
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event)
        button1.show()
        clock.tick(30)
        pygame.display.update()
