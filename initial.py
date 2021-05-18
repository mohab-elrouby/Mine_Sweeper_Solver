
import random
import time
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
        return board

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
                all_possible_locations.remove([i,j])

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
        print("number of moves: ", score) 
        isContinue = input("Do you want to try again? (y/n) :")
        if isContinue == 'n':
            return False
        return True


    # recursive function to update the board on click (took me the whole day)
    def updateBoard(self, minesweeper_map, player_map, y, x, width, height):

        if (x < 0 or x >= width or y < 0 or y >= height or player_map[y][x] != "-" or minesweeper_map[y][x] == "X"):
            return
        
        player_map[y][x]=minesweeper_map[y][x]
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


    def Game(self):
        GameStatus = True
        while GameStatus:
            print("Enter the cell you want to open :")
            x = int(input("X ({} to {}) :" .format(1, width)))
            y = int(input("Y ({} to {}) :" .format(1, height)))
            bombs_arr = self.make_bomb_arr(height, width, n_bombs, x, y)
            minesweeper_map = self.populate_minesweeper(bombs_arr, height, width)
            player_map = self.GeneratePlayerBoard(height, width)
            self.updateBoard(minesweeper_map, player_map, y, x, width, height)
            self.show_board(player_map)

            score = 0
            initial_time = time.time() 
            
            while True:
                if self.CheckWon(player_map, n_bombs) == False:
                    print("Enter the cell you want to open :")
                    x = input("X ({} to {}) :" .format(1, width))
                    y = input("Y ({} to {}) :" .format(1, height))
                    x = (int(x) - 1 )# 0 based indexing
                    y = (int(y) - 1 )# 0 based indexing
                    if (minesweeper_map[y][x] == 'X'):
                        print("Game Over!")
                        self.show_board(minesweeper_map)
                        final_time = time.time()
                        total_time = final_time-initial_time
                        print("your time: {} seconds" .format(int(total_time)))
                        GameStatus = self.CheckContinueGame(score)
                        break
                    else:
                        self.updateBoard(minesweeper_map, player_map, y, x, width, height)
                        self.show_board(player_map)
                        score += 1
    
                else:
                    print("You have Won!")
                    final_time = time.time()
                    total_time = final_time-initial_time
                    print("your time: {} seconds" .format(int(total_time)))
                    GameStatus = self.CheckContinueGame(score)
                    break

# Start of Program
height = int(input("enter number of rows:"))
width = int(input("enter number of columns:"))
n_bombs = int(input("enter number of bombs:"))
mineSweeper = MineSweeper(n_bombs, height, width)
if __name__ == "__main__":
    try:
        mineSweeper.Game()
    except KeyboardInterrupt:
        print('\nEnd of Game. Bye Bye!')


