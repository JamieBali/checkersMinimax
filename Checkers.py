import pygame
import math
import numpy as np

pygame.init()
screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
fontB = pygame.font.SysFont("Arial", 20, bold=True)


### ! BEGIN GLOBAL METHODS

###
#
# When generating the possible moves, we will first look for captures as they must take precedence.
# Since captures are manditory, if the possible moves stack is empty after this processing, we will
# perform a second run to get regular moves. This is slightly less efficient time-wise, but uses less
# storage space.
#
# For ease of processing, we will return the board state after each move, as opposed to the move itself.
#
###
def getPossibleMoves(inboard, player, mc = "False", mcfiller = [0]): # for some reason this wasn't working inside the class, but it's fine out here. could be something to do with recursion limits?
    moves = []
    tempBoard = np.copy(inboard)

    while len(tempBoard) != 8:
        tempBoard = tempBoard[0]

    board = tempBoard
    if player == 1: # player 1 is the human player.
        captures = False
        for i in range(0,8):             # player 1 captures
            for j in range(0,8):
                if board[i][j] == 4 or board[i][j] == 1: # king or regular
                    if i > 1 and j < 6:                  # to avoid overflow errors
                        if (board[i-1][j+1] == 2 or board[i-1][j+1] == 5) and board[i-2][j+2] == 0: # if next to an enemy tile, and beyond that is empty, we know we can take that piece
                            newBoardState = np.copy(board)
                            if newBoardState[i-1][j+1] == 5:        # this implements the regicide rule.
                                newBoardState[i-2][j+2] == 4
                            else:
                                newBoardState[i-2][j+2] = board[i][j]   # update movement
                            newBoardState[i][j] = 0         # clear previous points
                            newBoardState[i-1][j+1] = 0 
                            if i-2 == 0:                        # this checks for promotion
                                newBoardState[i-2][j+2] = 4
                            captures = True                     # this confirms that a piece was taken, so we know that non-captures aren't allowed
                            moves.append([newBoardState, mcfiller]) # mcfiller means there won't be errors in the multicapture system.
                            mcmoves = getPossibleMoves(newBoardState, 1, "True", newBoardState)     # recursion for multicaptures, as the AI doesn't always want to multicapture
                            for x in mcmoves:                       # all multicapture options are added as seperate moves.
                                moves.append([x,mcfiller])
                    if i > 1 and j > 1:                                                 # this repeats as above for all other capture directions
                        if (board[i-1][j-1] == 2 or board[i-1][j-1] == 5) and board[i-2][j-2] == 0:
                            newBoardState = np.copy(board)
                            if newBoardState[i-1][j-1] == 5:
                                newBoardState[i-2][j-2] == 4
                            else:
                                newBoardState[i-2][j-2] = board[i][j]
                            newBoardState[i][j] = 0
                            newBoardState[i-1][j-1] = 0
                            if i-2 == 0:
                                newBoardState[i-2][j-2] = 4
                            captures = True
                            moves.append([newBoardState, mcfiller])
                            mcmoves = getPossibleMoves(newBoardState, 1, "True", newBoardState)
                            for x in mcmoves:
                                moves.append([x,mcfiller])
                if board[i][j] == 4: # backwards moves means king only.
                    if i < 6 and j < 6: 
                        if (board[i+1][j+1] == 2 or board[i+1][j+1] == 5) and board[i+2][j+2] == 0:
                            newBoardState = np.copy(board)
                            if newBoardState[i+1][j+1] == 5:
                                newBoardState[i+2][j+2] == 4
                            else:
                                newBoardState[i+2][j+2] = board[i][j]
                            newBoardState[i][j] = 0
                            newBoardState[i+1][j+1] = 0
                            captures = True
                            moves.append([newBoardState, mcfiller])
                            mcmoves = getPossibleMoves(newBoardState, 1, "True", newBoardState)
                            for x in mcmoves:
                                moves.append([x,mcfiller])
                    if i < 6 and j > 1:
                        if (board[i+1][j-1] == 2 or board[i+1][j-1] == 5) and board[i+2][j-2] == 0:
                            newBoardState = np.copy(board)
                            if newBoardState[i+1][j-1] == 5:
                                newBoardState[i+2][j-2] == 4
                            else:
                                newBoardState[i+2][j-2] = board[i][j]
                            newBoardState[i][j] = 0
                            newBoardState[i+1][j-1] = 0
                            captures = True
                            moves.append([newBoardState, mcfiller])
                            mcmoves = getPossibleMoves(newBoardState, 1, "True", newBoardState)
                            for x in mcmoves:
                                moves.append([x, mcfiller])
                            
        if captures == False and mc == "False":            # player 1 non captures
            for i in range(0,8):
                for j in range(0,8):
                    if board[i][j] == 4 or board[i][j] == 1: # forward moves for both king and normal.
                        if i > 0 and j < 7:
                            if board[i-1][j+1] == 0:
                                newBoardState = np.copy(board)
                                newBoardState[i-1][j+1] = newBoardState[i][j]
                                newBoardState[i][j] = 0
                                moves.append([newBoardState, mcfiller]) # the filler is still addded so less processing is needed later.
                        if i > 0 and j > 0:
                            if board[i-1][j-1] == 0:
                                newBoardState = np.copy(board)
                                newBoardState[i-1][j-1] = newBoardState[i][j]
                                newBoardState[i][j] = 0
                                moves.append([newBoardState, mcfiller])
                    if board[i][j] == 4: # king only
                        if i < 7 and j < 7:
                            if board[i+1][j+1] == 0:
                                newBoardState = np.copy(board)
                                newBoardState[i+1][j+1] = newBoardState[i][j]
                                newBoardState[i][j] = 0
                                moves.append([newBoardState, mcfiller])
                        if i < 7 and j > 0:
                            if board[i+1][j-1] == 0:
                                newBoardState = np.copy(board)
                                newBoardState[i+1][j-1] = newBoardState[i][j]
                                newBoardState[i][j] = 0
                                moves.append([newBoardState, mcfiller])

    else: # player 2 is the artifical agent. Uses the same processing as above, so no comments have been written.
        captures = False

        for i in range(0,8):                # AI Captures
            for j in range(0,8):
                if board[i][j] == 2 or board[i][j] == 5: # king or regular
                    if i < 6 and j < 6:
                        if (board[i+1][j+1] == 1 or board[i+1][j+1] == 4) and board[i+2][j+2] == 0: # 1 is a human piece and 5 is a human king.
                            newBoardState = np.copy(board)
                            if board[i+1][j+1] == 4:
                                newBoardState[i+2][j+2] = 5
                            else:
                                newBoardState[i+2][j+2] = newBoardState[i][j]
                            newBoardState[i][j] = 0
                            newBoardState[i+1][j+1] = 0
                            if i+2 == 7:
                                newBoardState[i+2][j+2] = 5
                            captures = True
                            moves.append([newBoardState, mcfiller])
                            mcmoves = getPossibleMoves(newBoardState, 2, "True", newBoardState)
                            for x in mcmoves:
                                moves.append([x,mcfiller])
                    if i < 6 and j > 1:
                        if (board[i+1][j-1] == 1 or board[i+1][j-1] == 4) and board[i+2][j-2] == 0:
                            newBoardState = np.copy(board)
                            if board[i+1][j-1] == 4:
                                newBoardState[i+2][j-2] = 5
                            else:
                                newBoardState[i+2][j-2] = newBoardState[i][j]
                            newBoardState[i][j] = 0
                            newBoardState[i+1][j-1] = 0
                            if i+2 == 7:
                                newBoardState[i+2][j-2] = 5
                            captures = True
                            moves.append([newBoardState, mcfiller])
                            mcmoves = getPossibleMoves(newBoardState, 2, "True", newBoardState)
                            for x in mcmoves:
                                moves.append([x,mcfiller])
                if board[i][j] == 5: # king only
                    if i > 1 and j > 1:
                        if (board[i-1][j-1] == 1 or board[i-1][j-1] == 4) and board[i-2][j-2] == 0:
                            newBoardState = np.copy(board)
                            newBoardState[i-2][j-2] = newBoardState[i][j]
                            newBoardState[i][j] = 0
                            newBoardState[i-1][j-1] = 0
                            captures = True
                            moves.append([newBoardState, mcfiller])
                            mcmoves = getPossibleMoves(newBoardState, 2, "True", newBoardState)
                            for x in mcmoves:
                                moves.append([x,mcfiller])
                    if i > 1 and j < 6:
                        if (board[i-1][j+1] == 1 or board[i-1][j+1] == 4) and board[i-2][j+2] == 0:
                            newBoardState = np.copy(board)
                            newBoardState[i-2][j+2] = newBoardState[i][j]
                            newBoardState[i][j] = 0
                            newBoardState[i-1][j+1] = 0
                            captures = True
                            moves.append([newBoardState, mcfiller])
                            mcmoves = getPossibleMoves(newBoardState, 2, "True", newBoardState)
                            for x in mcmoves:
                                moves.append([x,mcfiller])
        
        if captures == False and mc == "False":               # AI non captures
            for i in range (0,8):         
                for j in range(0,8):
                    if board[i][j] == 2 or board[i][j] == 5: # king or regular
                        if i < 7 and j < 7:
                            if board[i+1][j+1] == 0:
                                newBoardState = np.copy(board)
                                newBoardState[i+1][j+1] = board[i][j]
                                newBoardState[i][j] = 0
                                if i+1 == 7:
                                    newBoardState[i+1][j+1] = 5
                                moves.append([newBoardState, mcfiller])
                            
                        if i < 7 and j > 0:
                            if board[i+1][j-1] == 0:
                                newBoardState = np.copy(board)
                                newBoardState[i+1][j-1] = board[i][j]
                                newBoardState[i][j] = 0
                                if i+1 == 7:
                                    newBoardState[i+1][j-1] = 5
                                moves.append([newBoardState, mcfiller])
                    if board[i][j] == 5: # king only
                        if i > 0 and j < 7:
                            if board[i-1][j+1] == 0:
                                newBoardState = np.copy(board)
                                newBoardState[i-1][j+1] = board[i][j]
                                newBoardState[i][j] = 0
                                moves.append([newBoardState, mcfiller])
                        if i > 0 and j > 0:
                            if board[i-1][j-1] == 0:
                                newBoardState = np.copy(board)
                                newBoardState[i-1][j-1] = board[i][j]
                                newBoardState[i][j] = 0
                                moves.append([newBoardState, mcfiller])
    return moves


### ! END GLOBAL METHODS

###
#
# The game playing agent. When initialised, it'll need to take the difficulty.
# Each turn, the board state will be passed to the agent and it use the minimax algorithm 
# with alpha-beta pruning to find an optimal move.
# The moves will be returned in the form of a tuple (or maybe a list, whichever is easier to implement),
# with the structure (from, to, ...) where the tuple will increase in size of any multiple captures the AI 
# performs.
#
# The default difficulty of 5 means that it will think 5 moves ahead when looking for a hint for the player.
#
###
class Agent:
    def __init__(self, difficulty = 5):
        self.maxDepth = difficulty          # the difficulty refers to how deep the AI will search.
    
    ###
    #
    # This function calculates the value of the board based on a hueristic.
    # A positive value means the AI is winning, and a negative value means the AI is losing.
    #
    ###
    def getBoardValue(self, board):
        value = 0
        while len(board) != 8:  # only gets the most up to date version of the board
                                # ignoring the multicapture inbetweens.
            board = board[0]
        for i in range (0,8):           # for each tile on the board
            for j in range (0,8):
                if board[i][j] == 1:
                    value -= (7-i)      # the regular pieces are worth more if they are closer to becoming kings
                elif board[i][j] == 2:
                    value += i          # same as above, but for the AI's pieces
                elif board[i][j] == 4:
                    value -= 10         # 4 is an enemy king. The position is irrelevant, only that it is a king
                elif board[i][j] == 5:
                    value += 10         # 5 is an ally king, meaning we want as many of these as possible.
        return value

    ###
    #
    # This method runs the actual minimax algorithm.
    # It is divided into 3 sections:
    # - The leaf nodes of the tree at the bottom, where the board state values are found
    # - The middle nodes of the tree in the middle, where comparisons are made
    # - and the root node of the tree at the top, where no pruning happens and additional comparisons are made to return the optimal move
    #
    # Writing the method this way isn't as efficient in terms of lines of code, but has no effect on the speed processing.
    #
    ###
    def minimax(self, boardState, player, depth, maxDepth, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.maxDepth = maxDepth
        self.depth = depth
        self.boardState = boardState
        self.player = player

        self.moves = getPossibleMoves(self.boardState, self.player)    # start by getting all the valid moves it could take at a point.
        
        self.minval = 100
        self.maxval = -100
        
        self.breaker = False
        self.x = 0

        ### BOTTOM LAYER OF TREE
        if self.depth == 1:
            while self.x < len(self.moves):                                 # the breaker exists so we don't have to use a break command to
                                                                            # exit the loop when the path is pruned.
                self.temp = self.getBoardValue(self.moves[self.x][0])        # get value of a board state after a certain move
                if self.player == 2:                # meaning it's the max agent
                    if self.temp > self.maxval:             
                        self.maxval = self.temp
                    if self.temp > self.alpha:
                        self.alpha = self.temp
                    if self.alpha >= self.beta:       # this is the alpha-beta pruning check
                        self.breaker = True
                if self.player == 1:                # meaning it's the min agent
                    if self.temp < self.minval:
                        self.minval = self.temp
                    if self.temp < self.beta:   
                        self.beta = self.temp
                    if self.alpha >= self.beta:
                        self.breaker = True
                self.x += 1

            if self.player == 2:
                return self.maxval, self.alpha      # the max agent wants to return the alpha
            else:
                return self.minval, self.beta       # and the min agent wants to return the beta

        ### MIDDLE LAYERS OF TREE
        elif self.depth != self.maxDepth:
            self.agent = Agent()
            while self.x < len(self.moves) and self.breaker == False:

                # this if statement makes sure the pruning functions correctly, by modifying alpha and beta respective to which agent is processing.
                if player == 1:
                    self.temp, self.beta = self.agent.minimax(self.moves[self.x][0], (self.player%2)+1, self.depth - 1, self.maxDepth, self.alpha, self.beta)
                else:
                    self.temp, self.alpha = self.agent.minimax(self.moves[self.x][0], (self.player%2)+1, self.depth - 1, self.maxDepth, self.alpha, self.beta)
                
                if self.player == 2:                # Max agent
                    if self.temp > self.maxval:
                        self.maxval = self.temp
                    if self.temp > self.alpha:
                        self.alpha = self.temp
                    if self.alpha >= self.beta:
                        self.breaker = True
                if self.player == 1:                # Min agent
                    if self.temp < self.minval:
                        self.minval = self.temp
                    if self.temp < self.beta:
                        self.beta = self.temp
                    if self.alpha >= self.beta:
                        self.breaker = True
                self.x += 1

            if self.player == 2:
                return self.maxval, self.alpha
            else:
                return self.minval, self.beta

        ### ROOT OF TREE
        else:
            if len(self.moves) == 0:    # if there are no moves available, then the AI has lost.
                return "Loss"
            if len(self.moves) == 1:    # if there is only 1 move available, then we don't need to run the minimax algorithm
                return self.moves[0]

            self.agent = Agent()
            self.bestIndex = -1

            while self.x < len(self.moves):    # there is no breaker here, as alpha-beta pruning doesn't function on the root node
                if player == 2:
                    self.temp, self.alpha = self.agent.minimax(self.moves[self.x][0], (self.player%2)+1, self.depth - 1, self.maxDepth, self.alpha, self.beta)
                else:
                    self.temp, self.beta = self.agent.minimax(self.moves[self.x][0], (self.player%2)+1, self.depth - 1, self.maxDepth, self.alpha, self.beta)
                if player == 2:
                    if self.temp > self.maxval:
                        self.maxval = self.temp
                        self.bestIndex = self.x     # keeps an index of the best move.
                else:
                    if self.temp < self.minval:
                        self.minval = self.temp
                        self.bestIndex = self.x   
                self.x += 1
            return self.moves[self.bestIndex] # returns the move with the best value
    
    ###
    #
    # The move function will take the board state and run minimax on it to generate an optimal move.
    # This just means that only 1 variable needs to be passed when calling for the AI to make a move,
    # instead of having to pass all 6 variables from the main.
    #
    ###
    def move(self, boardState):
        self.boardState = boardState
        stateOfChosen = self.minimax(self.boardState, 2, self.maxDepth, self.maxDepth, -100, 100)
        return stateOfChosen
    
    ###
    #
    # The hint function functions the same as the move function above, but passes a different player number, so that we find the best
    # move for the human instead of the computer.
    #
    ###
    def hint(self, boardState):
        self.boardState = boardState
        self.stateOfChosen = self.minimax(self.boardState, 1, self.maxDepth, self.maxDepth, -100, 100)[0]
        
        if len(self.stateOfChosen) != 8:    # since the hint function will look through multicaptues and possibly return a multicapture
                                            # we want to filter out the multicapture so we only show the first step of that multiple.
                                            # This will make it easier for the human player to understand.
            self.stateOfChosen = self.stateOfChosen[len(self.stateOfChosen)-1]
            print(self.stateOfChosen)

        hx = 0  # hx and hy are the hint coordinates, representing the tile that needs to be moved,
        hy = 0  # and the for loop below finds the location it is being moved to.

        for x in range(0,8):
                for y in range(0,8):
                    if (self.stateOfChosen[x][y] == 1 or self.stateOfChosen[x][y] == 4) and self.boardState[x][y] == 0:
                        self.boardState[x][y] = 9   # we are using 9 to mark the suggested move.
                    if self.stateOfChosen[x][y] == 0 and (self.boardState[x][y] == 1 or self.boardState[x][y] == 4):
                        hx = x
                        hy = y
                        
        return self.boardState, hx, hy
    
    ### ! END CLASS AGENT

###
#
# This function removes all the hints and valid tile markers from the grid.
#
###
def clearBoard(board):
    for i in range(0,8): # clear board
        for j in range(0,8):
            if board[i][j] == 3 or board[i][j] == 9:    # 3 is the valid moves that get highlighted
                                                        # 9 is the suggested hint
                board[i][j] = 0

###
#
# This function actually displays the board.
#
# The default values for hx and hy mean that no tiles will be highlighted as hints unless a hint is passed to the function.
#
###
def drawBoard(board, hx = -1, hy = -1):

    screen.fill((255,255,255))      # fill screen in white. This also covers the previous drawings so they can be redisplayed correctly
    
    darkSquare = (138,120,93)
    lightSquare = (220,211,234)


    for x in range(0,8):
        for y in range(0,8):
            if x % 2 == 1:      
                if y % 2 == 1:  # the mod operator means that each alternating tile is highted a different colour.
                    pygame.draw.rect(screen, darkSquare, pygame.Rect(10 + (40*x),10 + (40*y),40,40))
                else:
                    pygame.draw.rect(screen, lightSquare, pygame.Rect(10 + (40*x),10 + (40*y),40,40))
            else:
                if y % 2 == 1:  # as above.
                    pygame.draw.rect(screen, lightSquare, pygame.Rect(10 + (40*x),10 + (40*y),40,40)) 
                else:
                    pygame.draw.rect(screen, darkSquare, pygame.Rect(10 + (40*x),10 + (40*y),40,40))
    
    # this rectangle is drawn as the hint button.
    pygame.draw.rect(screen, lightSquare, pygame.Rect(340, 30, 40, 40))
    txt = font.render("?", 1, (0,0,0))
    screen.blit(txt, (355, 38))

    for x in range(0,8):
        for y in range(0,8):
            if board[y][x] == 1:
                pygame.draw.circle(screen, (255,0,0), ((x*40)+30,(y*40)+30),15) # red circle for human regular piece
            elif board[y][x] == 2:
                pygame.draw.circle(screen, (0,0,0), ((x*40)+30,(y*40)+30),15)   # black circle for AI regular piece
            elif board[y][x] == 3:
                pygame.draw.circle(screen, (0,225,0), ((x*40)+30,(y*40)+30),10) # smaller green circle for valid move highlights
            elif board[y][x] == 4:
                pygame.draw.circle(screen, (255,0,0), ((x*40)+30,(y*40)+30),15) # red circle with ! for human king
                king = fontB.render("!", 1, (0,0,0))
                screen.blit(king, ((x*40)+27,(y*40)+19))
            elif board[y][x] == 5:
                pygame.draw.circle(screen, (0,0,0), ((x*40)+30,(y*40)+30),15)   # black circle with ! for AI king
                king = fontB.render("!", 1, (225,225,225))
                screen.blit(king, ((x*40)+27,(y*40)+19))
            elif board[y][x] == 9:
                pygame.draw.circle(screen, (0,255,0), ((x*40)+30,(y*40)+30),10) # smaller green circle for hint

    if hx > -1 and hy > -1: # if hx and hy are greater than -1, it means that a hint has been passed through.
        pygame.draw.circle(screen, (0,0,128), ((hx*40)+30,(hy*40)+30),15) # blue circle for hint start point

###
#
# A smaller version of the availableMoves function that just returns whether or not captures are available.
# It does not, however, highglight moves if captures are found.
#
###
def capturesAvailable(board):
    captures = False
    for a in range(0,8):            # go through all possible moves to see if a valid capture is available
        for b in range(0,8):
            if (board[a][b] == 1 or board[a][b] == 4) and a > 1 and b < 6:      # if tile contains human piece, and capture wouldn't cause overflow
                if board[a-1][b+1] == 2 or board[a-1][b+1] == 5:                # if diagonal tile contains AI piece
                    if board[a-2][b+2] == 0:                                    # and if tile beyond there is empty
                        captures = True                                         # then a capture is available
            if (board[a][b] == 1 or board[a][b] == 4) and a > 1 and b > 1:      # repeat for all possible moves the human has
                if board[a-1][b-1] == 2 or board[a-1][b-1] == 5:
                    if board[a-2][b-2] == 0:
                            captures = True
            if board[a][b] == 4 and a < 6 and b < 6:
                if board[a+1][b+1] == 2 or board[a+1][b+1] == 5:
                    if board[a+2][b+2] == 0:
                        captures = True
            if board[a][b] == 4 and a < 6 and b > 1:
                if board[a+1][b-1] == 2 or board[a+1][b-1] == 5:
                    if board[a+2][b-2] == 0:
                        captures = True
    return captures

###
#
# This just displays the title page at the start so the user can select the difficulty they want to play at.
#
###
def drawTitlePage(diff):
    darkSquare = (138,120,93)
    lightSquare = (220,211,234)

    screen.fill((255,255,255))
    titleText = font.render("Checkers !", 1, (0,0,0))
    screen.blit(titleText, (150,80))
    diffText = font.render("Select your difficulty!", 1, (0,0,0))
    screen.blit(diffText, (110,150))
    
    # these here are the difficulty buttons
    pygame.draw.rect(screen, lightSquare, pygame.Rect(50,200,40,40))
    pygame.draw.rect(screen, lightSquare, pygame.Rect(102,200,40,40))
    pygame.draw.rect(screen, lightSquare, pygame.Rect(154,200,40,40))
    pygame.draw.rect(screen, lightSquare, pygame.Rect(206,200,40,40))
    pygame.draw.rect(screen, lightSquare, pygame.Rect(258,200,40,40))
    pygame.draw.rect(screen, lightSquare, pygame.Rect(310,200,40,40))

    # this here highlights the selected difficulty in a darker colour
    if diff == 1:
        pygame.draw.rect(screen, darkSquare, pygame.Rect(50,200,40,40))
    elif diff == 2:
        pygame.draw.rect(screen, darkSquare, pygame.Rect(102,200,40,40))
    elif diff == 3:
        pygame.draw.rect(screen, darkSquare, pygame.Rect(154,200,40,40))
    elif diff == 4:
        pygame.draw.rect(screen, darkSquare, pygame.Rect(206,200,40,40))
    elif diff == 5:
        pygame.draw.rect(screen, darkSquare, pygame.Rect(258,200,40,40))
    else:
        pygame.draw.rect(screen, darkSquare, pygame.Rect(310,200,40,40))
    
    # this puts the numbers onto the difficulty buttons
    numText = font.render("1", 1, (0,0,0))
    screen.blit(numText, (66,208))
    numText = font.render("2", 1, (0,0,0))
    screen.blit(numText, (118,208))
    numText = font.render("3", 1, (0,0,0))
    screen.blit(numText, (170,208))
    numText = font.render("4", 1, (0,0,0))
    screen.blit(numText, (222,208))
    numText = font.render("5", 1, (0,0,0))
    screen.blit(numText, (274,208))
    numText = font.render("6", 1, (0,0,0))
    screen.blit(numText, (326,208))

    # this creates the "play game" button
    pygame.draw.rect(screen, lightSquare, pygame.Rect(100, 300, 200, 50))
    goText = font.render("Let's Play!", 1, (0,0,0))
    screen.blit(goText, (160,312))
    
###
#
# Main function. Takes no inputs.
# This is where the checkers game will be run from.
#
###
if __name__ == '__main__':
    title = True
    difficulty = 3
    while title:
        drawTitlePage(difficulty)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:                  
                if pygame.mouse.get_pressed()[0]:                       # if player right clicks on a button, difficulty changes
                    x, y = pygame.mouse.get_pos()
                    if x > 100 and x < 300 and y > 300 and y < 350:  # these coordinates are for the "play game" button
                        title = False
                    elif y > 200 and y < 240:                       # this coordinates are for the respective buttons.
                        if x > 50 and x < 90:
                            difficulty = 1
                        elif x > 102 and x < 142:
                            difficulty = 2
                        elif x > 154 and x < 194:
                            difficulty = 3
                        elif x > 206 and x < 246:
                            difficulty = 4
                        elif x > 258 and x < 298:
                            difficulty = 5
                        elif x > 310 and x < 350:
                            difficulty = 6
            clock.tick(30)
            pygame.display.update()   
             

    # the difficulty is the selected value +2, as thinking only 1 move ahead would be too easy at the start, and we want difficulty to scale linearly
    difficulty = difficulty + 2
    agent = Agent(difficulty)
    
    pastClick = (-1,-1)

    # this block creates the initial board state
    board = []
    board.append([0,2,0,2,0,2,0,2])
    board.append([2,0,2,0,2,0,2,0])
    board.append([0,2,0,2,0,2,0,2])
    board.append([0,0,0,0,0,0,0,0])
    board.append([0,0,0,0,0,0,0,0])
    board.append([1,0,1,0,1,0,1,0])
    board.append([0,1,0,1,0,1,0,1])
    board.append([1,0,1,0,1,0,1,0])
    drawBoard(board)


    mcavailable = False

    gameRunning = 0

    while gameRunning == 0:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]: # confirm that it is a left click.
                    dy, dx = pygame.mouse.get_pos()
                    
                    # get which tile was clicked
                    x = math.floor((dx-10)/40)
                    y = math.floor((dy-10)/40)

                   
                    if x >= 0 and x < 8 and y >= 0 and y < 8:   # as long as it is a valid tile
                        wascap = False
                        moved = False
                        if board[x][y] == 3:                    # check if it was a valid movement
                            board[x][y] = board[pastClick[0]][pastClick[1]]     # if so, make the move
                            board[pastClick[0]][pastClick[1]] = 0
                            if x == 0:                                      # check for promotion
                                board[x][y] = 4                                             
                                Text = font.render("PROMOTION!", 1, (0,0,0))
                                screen.blit(Text, (20,360))
                            clearBoard(board)
                            temp = x-pastClick[0]
                            if abs(temp) == 2: # this means it was a capture
                                wascap = True                   # wasCapture is used for multicapture capability
                                dx = int((x - pastClick[0])/2)         
                                dy = int((y - pastClick[1])/2)
                                if board[x-dx][y-dy] == 5: # this line implements regicide
                                    board[x][y] = 4
                                board[x-dx][y-dy] = 0
                            moved = True

                            mcavailable = False
                            if wascap:              # if it was a capture, we check if multicapture is possible.
                                if (board[x][y] == 4 or board[x][y] == 1) and x > 1:
                                    if y > 1:
                                        if (board[x-1][y-1] == 2 or board[x-1][y-1] == 5) and board[x-2][y-2] == 0:
                                            mcavailable = True
                                    if y < 6:
                                        if (board[x-1][y+1] == 2 or board[x-1][y+1] == 5) and board[x-2][y+2] == 0:
                                            mcavailable = True
                                if board[x][y] == 4 and x < 6:
                                    if y > 1:
                                        if (board[x+1][y-1] == 2 or board[x+1][y-1] == 5) and board[x+2][y-2] == 0:
                                            mcavailable = True
                                    if y < 6:
                                        if (board[x+1][y+1] == 2 or board[x+1][y+1] == 5) and board[x+2][y+2] == 0:
                                            mcavailable = True
                            if not mcavailable: # if it wasn't a multicapture, we go straight to running the AI
                                pastClick = (-1,-1)
                                clearBoard(board)
                                drawBoard(board)
                            
                                Text = font.render("I'm thinking...", 1, (0,0,0))
                                screen.blit(Text, (20,360))

                                pygame.display.update()

                                # AI 
                                agentMove = agent.move(board)
                                if agentMove == "Loss":
                                    # the human has won
                                    gameRunning = 1
                                else:
                                    agentMove = agentMove[0]

                                if len(agentMove) != 8:                     # this is how the AI does multicaptures
                                    for mcmoves in range(1, len(agentMove)+1):          # we itterate throught he AI's multicapture
                                                                                        # steps and display them all seperately
                                        board = agentMove[len(agentMove) - mcmoves]
                                        drawBoard(board)
                                        pygame.display.update()
                                        pygame.time.delay(600)              # we found that 600 ms is about long enough of a delay between steps
                                    errorText = font.render("The computer used a multicapture!", 1, (0,0,0))    # announce what happened
                                    screen.blit(errorText, (20,360))
                                else:                           # if the AI doens't multicapture, we just display the move
                                    board = agentMove
                                    drawBoard(board)
                            else:
                                clearBoard(board)           # redisplay the board without the green markers if no move was made
                                drawBoard(board)
                                pygame.display.update()


                        else:   
                            pastClick = (x,y)    

                        clearBoard(board)

                        if mcavailable:         
                            errorText = font.render("There is a valid multicapture available!", 1, (0,0,0))
                            screen.blit(errorText, (20,360))
                            pygame.draw.rect(screen, (220,211,234), (pygame.Rect(340, 340, 40, 40)))   # show the skip button if the user doesn't want to multicapture
                            txt = font.render("Skip", 1, (0,0,0))
                            screen.blit(txt, (341,344))
                            pygame.display.update()

                        if moved == False: # mark valid moves
                            captures = capturesAvailable(board)

                            if captures == False:          # if there wasn't a capture, then any valid movement is a valid move
                                if board[x][y] == 1 or board[x][y] == 4:
                                    if x > 0 and y < 7 and board[x-1][y+1] == 0:
                                        board[x-1][y+1] = 3
                                    if x > 0 and y > 0 and board[x-1][y-1] == 0:
                                        board[x-1][y-1] = 3
                                if board[x][y] == 4:
                                    if x < 7 and y < 7 and board[x+1][y+1] == 0:
                                        board[x+1][y+1] = 3
                                    if x < 7 and y > 0 and board[x+1][y-1] == 0:
                                        board[x+1][y-1] = 3

                            if captures == True:           # if there was a capture, only captures are valid moves
                                valid = False   # this is a tracker to see if you highlighted a valid move so i can provide an error message
                                if board[x][y] == 1 or board[x][y] == 4:
                                    if x > 1 and y < 6 and (board[x-1][y+1] == 2 or board[x-1][y+1] == 5) and board[x-2][y+2] == 0:
                                        board[x-2][y+2] = 3
                                        valid = True
                                    if x > 1 and y > 1 and (board[x-1][y-1] == 2 or board[x-1][y-1] == 5) and board[x-2][y-2] == 0:
                                        board[x-2][y-2] = 3
                                        valid = True
                                if board[x][y] == 4:
                                    if x < 6 and y < 6 and (board[x+1][y+1] == 2 or board[x+1][y+1] == 5) and board[x+2][y+2] == 0:
                                        board[x+2][y+2] = 3
                                        valid = True
                                    if x < 6 and y > 1 and (board[x+1][y-1] == 2 or board[x+1][y-1] == 5) and board[x+2][y-2] == 0:
                                        board[x+2][y-2] = 3
                                        valid = True
                            
                            
                            drawBoard(board) # update the green movement tiles
                            if mcavailable:
                                errorText = font.render("There is a valid multicapture available!", 1, (0,0,0)) # show an error maessage
                                screen.blit(errorText, (20,360))
                                pygame.draw.rect(screen, (220,211,234), (pygame.Rect(340, 340, 40, 40)))
                                txt = font.render("Skip", 1, (0,0,0))
                                screen.blit(txt, (341,344))
                                pygame.display.update()

                            if captures == True and valid == False and mcavailable == False: 
                                errorText = font.render("There is a valid capture available!", 1, (0,0,0))  # show an error message
                                screen.blit(errorText, (20,360))
                                
                        captures = False
                    elif dy > 340 and dy < 380 and dx > 30 and dx < 70:     # these are the coordinates of the hint button
                        clearBoard(board)
                        drawBoard(board)
                        txt = font.render("Let's have a look for you!", 1, (0,0,0))     # anounce that it is searching
                        screen.blit(txt, (20,360))
                        pygame.display.update()
                        board, hx, hy = agent.hint(board)
                        drawBoard(board, hy, hx)
                        txt = font.render("Try moving here!", 1, (0,0,0))               # this hint will just show where the best move would end up
                        screen.blit(txt, (20,360))
                    
                    elif dy > 340 and dy < 380 and dx > 340 and dx < 380 and mcavailable == True:   # this is the skip button, but it will only function if multicaptures are available.
                        mcavailable = False
                        pastClick = (-1,-1)
                        clearBoard(board)
                        drawBoard(board)
                        Text = font.render("I'm thinking...", 1, (0,0,0))
                        screen.blit(Text, (20,360))
                        pygame.display.update()
                        # AI 
                        agentMove = agent.move(board)
                        if agentMove == "Loss":
                            # the human has won
                            gameRunning = 1
                        else:
                            agentMove = agentMove[0]

                        if len(agentMove) != 8:
                            for mcmoves in range(1, len(agentMove)+1):
                                board = agentMove[len(agentMove) - mcmoves]
                                drawBoard(board)
                                pygame.display.update()
                                pygame.time.delay(600)
                            errorText = font.render("The computer used a multicapture!", 1, (0,0,0))
                            screen.blit(errorText, (20,360))
                        else:
                            board = agentMove
                            drawBoard(board)
                    x = -1
                    y = -1 

        loss = True
        for x in range(0,8):                                # this is to check if the player has lost yet.
            for y in range(0,8):
                if board[x][y] == 1 or board[x][y] == 4:    # no human pieces on the board means they have lost.
                    loss = False
        if loss:
            gameRunning = 2
        clock.tick(30)
        pygame.display.update()
    
    
    ender = False # variable to wait for the user to click anywhere to close the game
    
    while ender == False:
        if gameRunning == 1:
            errorText = font.render("CONGRATULATIONS! YOU WON!", 1, (0,0,0))    # announce victory or loss
            screen.blit(errorText, (20,360))
        else:
            errorText = font.render("THE COMPUTER WINS!", 1, (0,0,0))           
            screen.blit(errorText, (20,360))
        pygame.display.update()                                 # clicking anywhere ends the game and shuts the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                ender = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                ender = True

    ### END CLASS MAIN
    
 # END
