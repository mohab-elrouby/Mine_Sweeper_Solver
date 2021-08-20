
import random
import time
import sys
import pygame
import math
import button


pygame.init()

GREY = (180,180,180)
DARK_GREY = (100,100,100)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREEN = (10,150,30)
BLUE = (10,50,150)
RED = (150,10,10)

class MineSweeper:
    def __init__(self, bombs, height, width ):
        self.bombs = bombs
        self.height = height
        self.width = width

# we will make a function named populate_minsweeper() this function will have 3 arguments:
# 1) bombs = list of bomb locations [x,y]
# 2) height or number of rows
# 3) width or number of columns 

    def populate_minesweeper(self, bombs, height, width):
        # initializing the game board with zeros, meaning no bombs yet
        board =[]
        for i in range (height):
            row = []
            for j in range (width):
                row.append(0)
            board.append(row)

        # looping the list of bombs locations given in the form :
        # [[y0,x0],[y1,x1],[y2,x2]...[yn,xn]]
        for bomb_location in bombs:
            # for each element [yk,xk] we assign yk to bomb_row and xk to bomb_col
            # and pass them to the place_bomb function
            bomb_row, bomb_col = bomb_location
            self.place_bomb(bomb_row, bomb_col, board)
            
            # after placing a bomb in a cell we then add +1 for it's neighboring cells 
            # if they don't contain bombs already 
            row_range = range(bomb_row-1, bomb_row+2)
            col_range = range(bomb_col-1, bomb_col+2)

            for i in row_range:
                for j in col_range:
                    if(0 <= i < height and 0 <= j < width and board[i][j] != 'X'):
                        board[i][j] += 1
        return board
            
    # after placing all the bombs we show the game board using this function
    def show_board(self,board):
        for row in board:
            print("    ".join(str(cell) for cell in row))
            print("")
        

    def make_bomb_arr(self,height, width, n_bombs, x, y):
        # creating a list of all possible bombs locations. we take the
        # first click's x & y posestions and make sure there's no bombs in it or surrounding it. 
        all_possible_locations = []
        for i in range (height):
            for j in range (width):
                all_possible_locations.append([i,j])

        # clearing all cells around the first click
        for i in range (x-1, x+2):
            for j in range (y-1, y+2):
                if(0 <= i < height and 0 <= j < width):
                    all_possible_locations.remove([j,i])

        # taking a random sample of all possible locations to place the bombs in
        bombs_arr = random.sample(all_possible_locations, k=n_bombs)
        return bombs_arr

    def place_bomb(self, bomb_row, bomb_col, board):
            board[bomb_row][bomb_col]= 'X'


    # generating the board that the player will see (initial value = "-")
    def GeneratePlayerBoard(self, height, width):
        board = []
        for i in range (height):
                row = []
                for j in range (width):
                    row.append('-')
                board.append(row)
        return board


    # function to check the number of un-opened cells, and if it's equal to the number of bombs,
    # then this must mean the player have won. and there are no more moves to play.
    def CheckWon(self, board, n_bombs):
        unOpenedCells = 0
        for row in board:
            for cell in row:
                if cell == '-':
                    unOpenedCells += 1
        return (unOpenedCells == n_bombs)


    def CheckContinueGame(self, score):

        screen_height = height*30
        screen_width = width*30
        size = (screen_width, screen_height)
        start_img = pygame.image.load('play_again_btn.png').convert_alpha()
        score_btn = button.Button(width*8, height*2, score, 0.8)
        start_button = button.Button(width*10, height*10, start_img, 0.8)

        while True:
            screen = pygame.display.set_mode(size)
            screen.fill(WHITE)
            isClicked = start_button.draw(screen)
            score_btn.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        sys.exit()
                if (event.type == pygame.MOUSEBUTTONDOWN and isClicked):
                    print("clicked")
                    screen.fill(WHITE)
                    return True
            pygame.display.update()



    # recursive function to update the board on click (took me the whole day)
    # the function now updates the gui as well using the "draw_board" function
    def updateBoard(self, minesweeper_map, player_map, y, x, width, height):
        CELLSIZE = 25
        MARGIN = 5
        screen_height = height*(CELLSIZE+MARGIN)
        screen_width = width*(CELLSIZE+MARGIN)
        size = (screen_width, screen_height)
        screen = pygame.display.set_mode(size)
        screen.fill(WHITE)
        
        if (x < 0 or x >= width or y < 0 or y >= height or player_map[y][x] != "-" or minesweeper_map[y][x] == "X"):
            return
        
        player_map[y][x]=minesweeper_map[y][x]
        
        time.sleep(0.05)
        self.draw_board(screen, CELLSIZE, player_map, MARGIN)
        
        if (x > 0 and minesweeper_map[y][x] == 0): # left
            self.updateBoard(minesweeper_map, player_map, y, x-1, width, height)
        if (y > 0 and minesweeper_map[y][x] == 0): #top
            self.updateBoard(minesweeper_map, player_map, y-1, x, width, height)
        if (x < width and minesweeper_map[y][x] == 0): # right
            self.updateBoard(minesweeper_map, player_map, y, x+1, width, height)
        if (y < height and minesweeper_map[y][x] == 0): # down
            self.updateBoard(minesweeper_map, player_map, y+1, x, width, height)

        if (y < height and minesweeper_map[y][x] == 0): # top_left
            self.updateBoard(minesweeper_map, player_map, y-1, x-1, width, height)
        if (y < height and minesweeper_map[y][x] == 0): # top_right
            self.updateBoard(minesweeper_map, player_map, y-1, x+1, width, height)
        if (y < height and minesweeper_map[y][x] == 0): # down_left
            self.updateBoard(minesweeper_map, player_map, y+1, x-1, width, height)
        if (y < height and minesweeper_map[y][x] == 0): # down_right
            self.updateBoard(minesweeper_map, player_map, y+1, x+1, width, height)


    def draw_cell(self, screen, CELLSIZE, MARGIN, row, column, color, isText, number_font, board):
        pygame.draw.rect(screen,
                                color,
                                [(MARGIN + CELLSIZE) * column + MARGIN,
                                (MARGIN + CELLSIZE) * row + MARGIN,
                                CELLSIZE,
                                CELLSIZE])
        if isText:
            number_text  = str(board[row][column] )
            number_image = number_font.render( number_text, True, BLACK )

            # centre the image in the cell by calculating the margin-distance
            margin_x = ( CELLSIZE-1  ) // 2
            margin_y = ( CELLSIZE-1 ) // 2

            # Draw the number image
            screen.blit( number_image,
                ( (MARGIN + CELLSIZE) * column + MARGIN + margin_x, 
                (MARGIN + CELLSIZE) * row + MARGIN + margin_y ) )


    def draw_board(self, screen, CELLSIZE, board, MARGIN):
        number_font = pygame.font.SysFont( None, 16 )   # default font, size 16
        for row in range(height):
            for column in range(width):
                color = GREEN
                isText = False
                if board[row][column] == 'X':
                    color = RED
                    isText = True
                elif board[row][column] == '*':
                    color = BLUE
                    isText = True
                elif board[row][column] == '-':
                    color = GREY
                    isText = False
                elif board[row][column] != 0: 
                    color = GREEN
                    isText = True
                self.draw_cell(screen, CELLSIZE, MARGIN, row, column, color, isText, number_font, board)

        pygame.display.flip()


    
    def Game(self):
        CELLSIZE = 25
        MARGIN = 5
        screen_height = height*(CELLSIZE+MARGIN)
        screen_width = width*(CELLSIZE+MARGIN)
        size = (screen_width, screen_height)               
        GameStatus = True
        firstClick = True
        while GameStatus:
            screen = pygame.display.set_mode(size)
            screen.fill(WHITE) 
            player_map=self.GeneratePlayerBoard(height, width)
            self.draw_board(screen, CELLSIZE, player_map, MARGIN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    x = (int(math.floor(event.pos[0]/(CELLSIZE+MARGIN))))
                    y = (int(math.floor(event.pos[1]/(CELLSIZE+MARGIN))))
                    bombs_arr = self.make_bomb_arr(height, width, n_bombs, x, y)
                    minesweeper_map = self.populate_minesweeper(bombs_arr, height, width)
                    player_map = self.GeneratePlayerBoard(height, width)
                    self.updateBoard(minesweeper_map, player_map, y, x, width, height)
                    self.show_board(player_map)
                    firstClick = False
                    score = 0
                    initial_time = time.time() 
                    break
            
            while not firstClick:
                for event in pygame.event.get():
                    checkWon = self.CheckWon(player_map, n_bombs)
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if checkWon == False: 
                        if (event.type == pygame.MOUSEBUTTONDOWN):                   
                            x = (int(math.floor(event.pos[0]/(CELLSIZE+MARGIN))))
                            y = (int(math.floor(event.pos[1]/(CELLSIZE+MARGIN))))
                            # the player clicked on a mine and lost
                            if (minesweeper_map[y][x] == 'X'):
                                self.updateBoard(minesweeper_map, player_map, y, x, width, height)
                                self.draw_board(screen, CELLSIZE, minesweeper_map, MARGIN)
                                final_time = time.time()
                                total_time = final_time-initial_time
                                score = pygame.image.load('lost.png').convert_alpha()
                                GameStatus = self.CheckContinueGame(score)
                                firstClick = GameStatus
                                break
                            # the player made a safe move
                            else:
                                self.updateBoard(minesweeper_map, player_map, y, x, width, height)
                    # the player successfully cleared the board and won 
                    else:
                        final_time = time.time()
                        total_time = final_time-initial_time
                        score = pygame.image.load('won.png').convert_alpha()
                        GameStatus = self.CheckContinueGame(score)
                        firstClick = GameStatus
                        break
        pygame.quit()
                        
# Start of Program
height = 9
width = 9
n_bombs = 10
mineSweeper = MineSweeper(n_bombs, height, width)
if __name__ == "__main__":
    try:
        mineSweeper.Game()
    except KeyboardInterrupt:
        print('\nEnd of Game. Bye Bye!')


