
import random
import numpy as np



height = int(input("enter number of rows:"))
width = int(input("enter number of columns:"))
n_bombs = int(input("enter number of bombs:"))


# we will make a function named populate_minsweeper() this function will have 3 arguments:
# 1) bombs = list of bomb locations [x,y]
# 2) height or number of rows
# 3) width or number of columns 

def populate_minesweeper(bombs, height, width):

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
        place_bomb(bomb_row, bomb_col, board)
        
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
def show_board(board):
    for row in board:
        print("    ".join(str(cell) for cell in row))
        print("")
    return board


# creating a list of all possible bombs locations 
all_possible_locations = []
for i in range (height):
    for j in range (width):
        all_possible_locations.append([i,j])

# taking a random sample of all possible locations to place the bombs in
bombs_arr = random.sample(all_possible_locations, k=n_bombs)

def place_bomb(bomb_row, bomb_col, board):
        board[bomb_row][bomb_col]= 'X'


# generating the board that the player will see (initial value = "-")
def GeneratePlayerBoard(height, width):
    board = []
    for i in range (height):
            row = []
            for j in range (width):
                row.append('-')
            board.append(row)
    return board


# function to check the number of un-opened cells, and if it's equal to the number of bombs,
# then this must mean the player have won. and there are no more moves to play.
def CheckWon(board):
    unOpenedCells = 0
    for row in board:
        for cell in row:
            if cell == '-':
                unOpenedCells += 1
    if (unOpenedCells != n_bombs):
        return False
    else:
        return True

def CheckContinueGame(score):
    print("Your score: ", score) 
    isContinue = input("Do you want to try again? (y/n) :")
    if isContinue == 'n':
        return False
    return True
    # change "score" with time taken, since it's more suitable measure for the score than number of clicks


# recursive function to update the board on click (took me the whole day)
def updateBoard(minesweeper_map, player_map, y, x):

    if (x < 0 or x >= width or y < 0 or y >= height or player_map[y][x] != "-" or minesweeper_map[y][x] == "X"):
        return
    
    player_map[y][x]=minesweeper_map[y][x]
    if (x > 0 and minesweeper_map[y][x] == 0): # left
        updateBoard(minesweeper_map, player_map, y, x-1)
    if (y > 0 and minesweeper_map[y][x] == 0): #up
        updateBoard(minesweeper_map, player_map, y-1, x)
    if (x < width and minesweeper_map[y][x] == 0): # right
        updateBoard(minesweeper_map, player_map, y, x+1)
    if (y < height and minesweeper_map[y][x] == 0): # down
        updateBoard(minesweeper_map, player_map, y+1, x)

    if (y < height and minesweeper_map[y][x] == 0): # top_left
        updateBoard(minesweeper_map, player_map, y-1, x-1)
    if (y < height and minesweeper_map[y][x] == 0): # top_right
        updateBoard(minesweeper_map, player_map, y-1, x+1)
    if (y < height and minesweeper_map[y][x] == 0): # down_left
        updateBoard(minesweeper_map, player_map, y+1, x-1)
    if (y < height and minesweeper_map[y][x] == 0): # down_right
        updateBoard(minesweeper_map, player_map, y+1, x+1)



def Game():
    GameStatus = True
    while GameStatus:
        minesweeper_map = populate_minesweeper(bombs_arr, height, width)
        player_map = GeneratePlayerBoard(height, width)
        score = 0

        while True:
            if CheckWon(player_map) == False:
                print("Enter the cell you want to open :")
                x = input("X ({} to {}) :" .format(1, width))
                y = input("Y ({} to {}) :" .format(1, height))
                x = (int(x) - 1 )# 0 based indexing
                y = (int(y) - 1 )# 0 based indexing
                if (minesweeper_map[y][x] == 'X'):
                    print("Game Over!")
                    show_board(minesweeper_map)
                    GameStatus = CheckContinueGame(score)
                    break
                else:
                    updateBoard(minesweeper_map, player_map, y, x)
                    show_board(player_map)
                    score += 1
 
            else:
                print("You have Won!")
                GameStatus = CheckContinueGame(score)
                break

# Start of Program
if __name__ == "__main__":
    try:
        Game()
    except KeyboardInterrupt:
        print('\nEnd of Game. Bye Bye!')


