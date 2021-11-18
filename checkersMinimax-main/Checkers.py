import pygame
import math
import numpy as np

pygame.init()
screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
fontB = pygame.font.SysFont("Arial", 20, bold=True)


### TO DO LIST:
# - Alpha-Beta Pruning
# - Title Page
# - Multi-Capture (Human)
# - Multi-Capture (AI)
# - Hints

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
    def __init__(self, difficulty = 2):
        self.maxDepth = difficulty + 1

    def getBoardValue(self, board):
        value = 0
        for i in range (0,8):
            for j in range (0,8):
                if board[i][j] == 1:
                    value -= (8-i)      # the regular pieces are worth more, if they are closer to becoming kings
                elif board[i][j] == 2:
                    value += (i+1)      # same as above, but for the max agent's pieces
                elif board[i][j] == 4:
                    value -= 18         # 4 is an enemy king. The position is irrelevant, only that it is a king
                elif board[i][j] == 5:
                    value += 15         # 5 is an ally king, meaning we want as many of these as possible.
        return value

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
    def getPossibleMoves(self, board, player):
        moves = []
        if player == 1: # player 1 is the human player.
            captures = False
            for i in range(0,8):             # player 1 captures
                for j in range(0,8):
                    if board[i][j] == 4 or board[i][j] == 1: # king or regular
                        if i > 1 and j < 6:
                            if (board[i-1][j+1] == 1 or board[i-1][j+1] == 4) and board[i-2][j+2] == 0:
                                newBoardState = np.copy(board)
                                if newBoardState[i-1][j+1] == 5:
                                    newBoardState[i-2][j+2] == 4
                                else:
                                    newBoardState[i-2][j+2] = board[i][j]
                                newBoardState[i][j] = 0
                                newBoardState[i-1][j+1] = 0
                                if i-2 == 0:
                                    newBoardState[i-2][j+2] = 4
                                captures = True
                                moves.append(newBoardState)
                        if i > 1 and j > 1:
                            if (board[i-1][j-1] == 1 or board[i-1][j-1] == 4) and board[i-2][j-2] == 0:
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
                                moves.append(newBoardState)
                    if board[i][j] == 4: # king only
                        if i < 6 and j < 6:
                            if (board[i+1][j+1] == 2 or board[i+1][j+1] == 4) and board[i+2][j+2] == 0:
                                newBoardState = np.copy(board)
                                if newBoardState[i+1][j+1] == 5:
                                    newBoardState[i+2][j+2] == 4
                                else:
                                    newBoardState[i+2][j+2] = board[i][j]
                                newBoardState[i][j] = 0
                                newBoardState[i+1][j+1] = 0
                                captures = True
                                moves.append(newBoardState)
                        if i < 6 and j > 1:
                            if (board[i+1][j-1] == 2 or board[i+1][j-1] == 4) and board[i+2][j-2] == 0:
                                newBoardState = np.copy(board)
                                if newBoardState[i+1][j-1] == 5:
                                    newBoardState[i+2][j-2] == 4
                                else:
                                    newBoardState[i+2][j-2] = board[i][j]
                                newBoardState[i][j] = 0
                                newBoardState[i+1][j-1] = 0
                                captures = True
                                moves.append(newBoardState)
            if captures == False:            # player 1 non captures
                for i in range(0,8):
                    for j in range(0,8):
                        if board[i][j] == 4 or board[i][j] == 1: # king or regular
                            if i > 0 and j < 7:
                                if board[i-1][j+1] == 0:
                                    newBoardState = np.copy(board)
                                    newBoardState[i-1][j+1] = newBoardState[i][j]
                                    newBoardState[i][j] = 0
                                    moves.append(newBoardState)
                            if i > 0 and j > 0:
                                if board[i-1][j-1] == 0:
                                    newBoardState = np.copy(board)
                                    newBoardState[i-1][j-1] = newBoardState[i][j]
                                    newBoardState[i][j] = 0
                                    moves.append(newBoardState)
                        if board[i][j] == 4: # king only
                            if i < 7 and j < 7:
                                if board[i+1][j+1] == 0:
                                    newBoardState = np.copy(board)
                                    newBoardState[i+1][j+1] = newBoardState[i][j]
                                    newBoardState[i][j] = 0
                                    moves.append(newBoardState)
                            if i < 7 and j > 0:
                                if board[i+1][j-1] == 0:
                                    newBoardState = np.copy(board)
                                    newBoardState[i+1][j-1] = newBoardState[i][j]
                                    newBoardState[i][j] = 0
                                    moves.append(newBoardState)

        else: # player 2 is the artifical agent.
            captures = False

            for i in range(0,8):                # AI Captures
                for j in range(0,8):
                    if board[i][j] == 2 or board[i][j] == 5: # king or regular
                        if i < 6 and j < 6:
                            if (board[i+1][j+1] == 1 or board[i+1][j+1] == 4) and board[i+2][j+2] == 0:
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
                                moves.append(newBoardState)
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
                                moves.append(newBoardState)
                    if board[i][j] == 5: # king only
                        if i > 1 and j > 1:
                            if (board[i-1][j-1] == 1 or board[i-1][j-1] == 4) and board[i-2][j-2] == 0:
                                newBoardState = np.copy(board)
                                newBoardState[i-2][j-2] = newBoardState[i][j]
                                newBoardState[i][j] = 0
                                newBoardState[i-1][j-1] = 0
                                captures = True
                                moves.append(newBoardState)
                        if i > 1 and j < 6:
                            if (board[i-1][j+1] == 1 or board[i-1][j+1] == 4) and board[i-2][j+2] == 0:
                                newBoardState = np.copy(board)
                                newBoardState[i-2][j+2] = newBoardState[i][j]
                                newBoardState[i][j] = 0
                                newBoardState[i-1][j+1] = 0
                                captures = True
                                moves.append(newBoardState)
            
            if captures == False:               # AI non captures
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
                                    moves.append(newBoardState)
                                
                            if i < 7 and j > 0:
                                if board[i+1][j-1] == 0:
                                    newBoardState = np.copy(board)
                                    newBoardState[i+1][j-1] = board[i][j]
                                    newBoardState[i][j] = 0
                                    if i+1 == 7:
                                        newBoardState[i+1][j-1] = 5
                                    moves.append(newBoardState)
                        if board[i][j] == 5: # king only
                            if i > 0 and j < 7:
                                if board[i-1][j+1] == 0:
                                    newBoardState = np.copy(board)
                                    newBoardState[i-1][j+1] = board[i][j]
                                    newBoardState[i][j] = 0
                                    moves.append(newBoardState)
                            if i > 0 and j > 0:
                                if board[i-1][j-1] == 0:
                                    newBoardState = np.copy(board)
                                    newBoardState[i-1][j-1] = board[i][j]
                                    newBoardState[i][j] = 0
                                    moves.append(newBoardState)
                
        return moves

    def minimax(self, boardState, player, depth, maxDepth, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.maxDepth = maxDepth
        self.depth = depth
        self.boardState = boardState
        self.player = player

        self.moves = self.getPossibleMoves(self.boardState, self.player)    
        
        self.minval = 100
        self.maxval = -100
        
        self.breaker = False
        self.x = 0

        ### BOTTOM LAYER OF TREE
        if self.depth == 1:
            while self.x < len(self.moves) and self.breaker == False:
                self.temp = self.getBoardValue(self.moves[self.x])
                print(self.temp)
                if self.player == 2:
                    if self.temp > self.maxval:
                        self.maxval = self.temp
                    if self.temp > self.alpha:
                        self.alpha = self.temp
                if self.player == 1:
                    if self.temp < self.minval:
                        self.minval = self.temp
                    if self.temp < self.beta:
                        self.beta = self.temp
                self.x += 1
            if self.player == 2:
                return self.maxval, self.alpha
            else:
                return self.minval, self.beta

        ### MIDDLE LAYERS OF TREE
        elif self.depth != self.maxDepth:
            self.agent = Agent()
            while self.x < len(self.moves) and self.breaker == False:
                if player == 1:
                    self.temp, self.beta = self.agent.minimax(self.moves[self.x], (self.player%2)+1, self.depth - 1, self.maxDepth, self.alpha, self.beta)
                else:
                    self.temp, self.alpha = self.agent.minimax(self.moves[self.x], (self.player%2)+1, self.depth - 1, self.maxDepth, self.alpha, self.beta)
                print(self.temp)
                if self.player == 2:
                    if self.temp > self.maxval:
                        self.maxval = self.temp
                    if self.temp > self.alpha:
                        self.alpha = self.temp
                    if self.alpha >= self.beta:
                        self.breaker = True
                if self.player == 1:
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
            self.agent = Agent()
            self.maxIndex = -1
            while self.x < len(self.moves) and self.breaker == False:
                self.temp, self.alpha, self.beta = self.agent.minimax(self.moves[self.x], (self.player%2)+1, self.depth - 1, self.maxDepth, self.alpha, self.beta)
                print(self.temp)
                if self.temp > self.maxval:
                    self.maxval = self.temp
                    self.maxIndex = self.x
                if self.temp > self.alpha:
                    self.alpha = self.temp
                if self.alpha >= self.beta:
                    self.breaker = True
                self.x += 1
            print(self.maxIndex)
            return self.moves[self.maxIndex]
    
    ###
    #
    # The move function will take the board state and run minimax on it to generate an optimal move.
    #
    ###
    def move(self, boardState):
        self.boardState = boardState
        stateOfChosen = self.minimax(boardState, 2, self.maxDepth, self.maxDepth, -100, 100)
        return stateOfChosen

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

def clearBoard(board):
    for i in range(0,8): # clear board
        for j in range(0,8):
            if board[i][j] == 3:
                board[i][j] = 0

def drawBoard(board):
    screen.fill((255,255,255))
    
    darkSquare = (138,120,93)
    lightSquare = (220,211,234)

    for x in range(0,8):
        for y in range(0,8):
            if x % 2 == 1:
                if y % 2 == 1:
                    pygame.draw.rect(screen, darkSquare, pygame.Rect(10 + (40*x),10 + (40*y),40,40))
                else:
                    pygame.draw.rect(screen, lightSquare, pygame.Rect(10 + (40*x),10 + (40*y),40,40))
            else:
                if y % 2 == 1:
                    pygame.draw.rect(screen, lightSquare, pygame.Rect(10 + (40*x),10 + (40*y),40,40)) 
                else:
                    pygame.draw.rect(screen, darkSquare, pygame.Rect(10 + (40*x),10 + (40*y),40,40))

    for x in range(0,8):
        for y in range(0,8):
            if board[y][x] == 1:
                pygame.draw.circle(screen, (255,0,0), ((x*40)+30,(y*40)+30),15)
            elif board[y][x] == 2:
                pygame.draw.circle(screen, (0,0,0), ((x*40)+30,(y*40)+30),15)
            elif board[y][x] == 3:
                pygame.draw.circle(screen, (0,225,0), ((x*40)+30,(y*40)+30),10)
            elif board[y][x] == 4:
                pygame.draw.circle(screen, (255,0,0), ((x*40)+30,(y*40)+30),15)
                king = fontB.render("!", 1, (0,0,0))
                screen.blit(king, ((x*40)+27,(y*40)+19))
            elif board[y][x] == 5:
                pygame.draw.circle(screen, (0,0,0), ((x*40)+30,(y*40)+30),15)
                king = fontB.render("!", 1, (225,225,225))
                screen.blit(king, ((x*40)+27,(y*40)+19))

def capturesAvailable(board):
    captures = False
    for a in range(0,8):            # go through all possible moves to see if a valid capture is available
        for b in range(0,8):
            if (board[a][b] == 1 or board[a][b] == 4) and a > 1 and b < 6:
                if board[a-1][b+1] == 2 or board[a-1][b+1] == 5:
                    if board[a-2][b+2] == 0:
                        captures = True
            if (board[a][b] == 1 or board[a][b] == 4) and a > 1 and b > 1:
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
# Main function. Takes no inputs.
# This is where the checkers game will be run from.
#
###
if __name__ == '__main__':
    
    agent = Agent(4)
    
    pastClick = (-1,-1)

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

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]: # confirm that it is a left click.
                    y, x = pygame.mouse.get_pos()
                    
                    # get which tile was clicked
                    x = math.floor((x-10)/40)
                    y = math.floor((y-10)/40)
                    
                    if x >= 0 and x < 8 and y >= 0 and y < 8:

                        moved = False
                        if board[x][y] == 3:
                            board[x][y] = board[pastClick[0]][pastClick[1]]
                            board[pastClick[0]][pastClick[1]] = 0
                            if x == 0:
                                board[x][y] = 4
                                Text = font.render("PROMOTION!", 1, (0,0,0))
                                screen.blit(Text, (20,360))
                            clearBoard(board)
                            temp = x-pastClick[0]
                            if abs(temp) == 2: # this means it was a capture
                                dx = int((x - pastClick[0])/2)         
                                dy = int((y - pastClick[1])/2)
                                if board[x-dx][y-dy] == 5: # this line implements regicide
                                    board[x][y] = 4
                                board[x-dx][y-dy] = 0

                            # put multicapture here


                            pastClick = (-1,-1)
                            clearBoard(board)
                            drawBoard(board)
                            moved = True
                            Text = font.render("I'm thinking...", 1, (0,0,0))
                            screen.blit(Text, (20,360))

                            pygame.display.update()

                            # AI 
                            tempBoard = agent.move(board)

                            drawBoard(board)

                        else:
                            pastClick = (x,y)    
                    
                        clearBoard(board)
                        

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

                            if captures == True and valid == False: # and show an error message
                                errorText = font.render("There is a valid capture available!", 1, (0,0,0))
                                screen.blit(errorText, (20,360))
                                
                        captures = False
                    x = -1
                    y = -1    
                        


        clock.tick(30)
        pygame.display.update()
