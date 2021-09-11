from Basic_solver import Basic_solver
import random
import time
import sys
import pygame
import math
import button
from pygame.locals import *

pygame.init()

height = 20 # number of rows
width = 50 # number of columns
n_bombs = 160   #number of bombs
CELLSIZE = 24
MARGIN = 1
screen_height = height*(CELLSIZE+MARGIN)
screen_width = width*(CELLSIZE+MARGIN)
size = (screen_width, screen_height)   
GREY = (180,180,180)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREEN = (115, 212, 50)
RED = (255, 60, 60)
ORANGE = (255, 190, 60)


class MineSweeper:
    def __init__(self, bombs, height, width):
        self.bombs = bombs
        self.height = height
        self.width = width
        self.subscribers = set()

# observer pattern to update the board to all ai_solvers
    def subscribe(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def dispatch(self, data):
        for solver in self.subscribers:
            solver.update(data)


# I will make a function named populate_minsweeper() this function will have 3 arguments:
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
        for i in range (y-1, y+2):
            for j in range (x-1, x+2):
                if(0 <= i < height and 0 <= j < width):
                    all_possible_locations.remove([i,j])

        # taking a random sample of all possible locations to place the bombs in
        bombs_arr = random.sample(all_possible_locations, k=n_bombs)
        return bombs_arr

    def place_bomb(self, bomb_row, bomb_col, board):
            board[bomb_row][bomb_col]= 'X'


    # generating the board that the player will see (initial value = "-")
    def generate_player_board(self, height, width):
        board = []
        for i in range (height):
                row = []
                for j in range (width):
                    row.append('-')
                board.append(row)
        return board


    # function to check the number of un-opened cells, and if it's equal to the number of bombs,
    # then this must mean the player have won. and there are no more moves to play.
    def check_won(self, board, n_bombs):
        unOpenedCells = 0
        for row in board:
            for cell in row:
                if cell == '-' or cell == '*':
                    unOpenedCells += 1
        return (unOpenedCells == n_bombs)


    def CheckContinueGame(self, score, time, screen):
        myFont = pygame.font.SysFont( None, 16 )
        textSurface = myFont.render("TIME: "+str(round(time,1))+" seconds", True, BLACK )
        start_img = pygame.image.load('assets/play_again_btn.png').convert_alpha()
        score_btn = button.Button(screen_width/3, screen_height/3, score, 1)
        start_button = button.Button(screen_width/3, screen_height/3 + 60, start_img, 1)

        while True:
            screen = pygame.display.set_mode(size)
            screen.fill(WHITE)
            isClicked = start_button.draw(screen)
            screen.blit(textSurface, (screen_width/3, screen_height/3 + 120))
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
    def update_board(self, minesweeper_map, player_map, y, x, width, height, screen):
        
        if (x < 0 or x >= width or y < 0 or y >= height or player_map[y][x] != "-" or minesweeper_map[y][x] == "X"):
            return
        
        player_map[y][x]=minesweeper_map[y][x]
        
        self.draw_board(screen, CELLSIZE, player_map, MARGIN)
        if (x > 0 and minesweeper_map[y][x] == 0): # left
            self.update_board(minesweeper_map, player_map, y, x-1, width, height, screen)
        if (y > 0 and minesweeper_map[y][x] == 0): #top
            self.update_board(minesweeper_map, player_map, y-1, x, width, height, screen)
        if (x < width and minesweeper_map[y][x] == 0): # right
            self.update_board(minesweeper_map, player_map, y, x+1, width, height, screen)
        if (y < height and minesweeper_map[y][x] == 0): # down
            self.update_board(minesweeper_map, player_map, y+1, x, width, height, screen)

        if (y < height and minesweeper_map[y][x] == 0): # top_left
            self.update_board(minesweeper_map, player_map, y-1, x-1, width, height, screen)
        if (y < height and minesweeper_map[y][x] == 0): # top_right
            self.update_board(minesweeper_map, player_map, y-1, x+1, width, height, screen)
        if (y < height and minesweeper_map[y][x] == 0): # down_left
            self.update_board(minesweeper_map, player_map, y+1, x-1, width, height, screen)
        if (y < height and minesweeper_map[y][x] == 0): # down_right
            self.update_board(minesweeper_map, player_map, y+1, x+1, width, height, screen)


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
                    color = ORANGE
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
        GameStatus = True
        firstClick = True
        selectMode = True
        player_map = self.generate_player_board(height, width)
        basicSolver = Basic_solver(player_map, height, width)
        self.subscribe(basicSolver)
        self.dispatch(player_map)
        mode = ""
        while GameStatus:
            screen = pygame.display.set_mode(size)
            screen.fill(WHITE)
        
            if(selectMode):
                normal_mode_img = pygame.image.load('assets/normal_mode_btn.png').convert_alpha()
                normal_mode_button = button.Button(screen_width/3, screen_height/3, normal_mode_img, 1)
                ai_mode_img = pygame.image.load('assets/ai_mode_btn.png').convert_alpha()
                ai_mode_button = button.Button(screen_width/3, screen_height/3 +60, ai_mode_img, 1)
                normal_mode = normal_mode_button.draw(screen)
                ai_mode = ai_mode_button.draw(screen)
            else:
                player_map = self.generate_player_board(height, width)
                self.draw_board(screen, CELLSIZE, player_map, MARGIN)
                
                if(mode == "h"):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if (event.type == pygame.MOUSEBUTTONDOWN):
                            x = (int(math.floor(event.pos[0]/(CELLSIZE+MARGIN))))
                            y = (int(math.floor(event.pos[1]/(CELLSIZE+MARGIN))))
                            bombs_arr = self.make_bomb_arr(height, width, n_bombs, x, y)
                            minesweeper_map = self.populate_minesweeper(bombs_arr, height, width)
                            player_map = self.generate_player_board(height, width)
                            self.update_board(minesweeper_map, player_map, y, x, width, height, screen)
                            # self.show_board(player_map)
                            firstClick = False
                            initial_time = time.time() 
                        
                    
                    while not firstClick:
                        for event in pygame.event.get():
                            checkWon = self.check_won(player_map, n_bombs)
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if checkWon == False: 
                                if (event.type == pygame.MOUSEBUTTONDOWN):                   
                                    x = (int(math.floor(event.pos[0]/(CELLSIZE+MARGIN))))
                                    y = (int(math.floor(event.pos[1]/(CELLSIZE+MARGIN))))
                                    # the player clicked on a mine and lost
                                    if (minesweeper_map[y][x] == 'X'):
                                        self.update_board(minesweeper_map, player_map, y, x, width, height, screen)
                                        self.draw_board(screen, CELLSIZE, minesweeper_map, MARGIN)
                                        final_time = time.time()
                                        time.sleep(2)
                                        total_time = final_time-initial_time
                                        score = pygame.image.load('assets/lost.png').convert_alpha()
                                        GameStatus = self.CheckContinueGame(score, total_time, screen)
                                        firstClick = GameStatus
                                        selectMode = GameStatus
                                        break
                                    # the player made a safe move
                                    else:
                                        self.update_board(minesweeper_map, player_map, y, x, width, height, screen)
                            # the player successfully cleared the board and won 
                            else:
                                final_time = time.time()
                                time.sleep(2)
                                total_time = final_time-initial_time
                                score = pygame.image.load('assets/won.png').convert_alpha()
                                GameStatus = self.CheckContinueGame(score, total_time, screen)
                                firstClick = GameStatus
                                selectMode = GameStatus
                                break

                elif(mode=="a"):
                    self.dispatch(player_map)
                    a = basicSolver.make_initial_guess()
                    x = a[0]
                    y = a[1]
                    bombs_arr = self.make_bomb_arr(height, width, n_bombs, x, y)
                    minesweeper_map = self.populate_minesweeper(bombs_arr, height, width)
                    player_map = self.generate_player_board(height, width)
                    self.update_board(minesweeper_map, player_map, y, x, width, height, screen)
                    # self.show_board(player_map)
                    firstClick = False
                    initial_time = time.time() 
                        
                    
                    while not firstClick:
                        if self.check_won(player_map, n_bombs) == False:
                                self.dispatch(player_map)                        
                                a = basicSolver.make_guess()
                                for pos in a:
                                    x = pos[0]
                                    y = pos[1]
                                    # the player clicked on a mine and lost
                                    if (minesweeper_map[y][x] == 'X'):
                                        self.update_board(minesweeper_map, player_map, y, x, width, height, screen)
                                        self.draw_board(screen, CELLSIZE, minesweeper_map, MARGIN)
                                        final_time = time.time()
                                        time.sleep(2)
                                        # self.show_board(player_map)
                                        total_time = final_time-initial_time
                                        score = pygame.image.load('assets/lost.png').convert_alpha()
                                        GameStatus = self.CheckContinueGame(score, total_time, screen)
                                        firstClick = GameStatus
                                        selectMode = GameStatus
                                        break
                                    # the player made a safe move
                                    else:
                                        self.update_board(minesweeper_map, player_map, y, x, width, height, screen)
                                        # self.show_board(player_map)

                        # the player successfully cleared the board and won 
                        else:
                            final_time = time.time()
                            time.sleep(2)
                            total_time = final_time-initial_time
                            score = pygame.image.load('assets/won.png').convert_alpha()
                            GameStatus = self.CheckContinueGame(score, total_time, screen)
                            firstClick = GameStatus
                            selectMode = GameStatus
                            break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        sys.exit()
                if (event.type == pygame.MOUSEBUTTONDOWN and normal_mode):
                    selectMode = False
                    print("normal")
                    mode = "h"
                if (event.type == pygame.MOUSEBUTTONDOWN and ai_mode):
                    selectMode = False
                    print("ai")
                    mode = "a"
            pygame.display.update()
        pygame.quit()
                        
# Start of Program

mineSweeper = MineSweeper(n_bombs, height, width)
if __name__ == "__main__":
    try:
        mineSweeper.Game()
    except KeyboardInterrupt:
        print('\nGame Over')
