""""
the initial idea is to make a very basic solver using straight forward approach
we loop through the whole field, and look around each cell that contain a number 
and check. if the number of unopened cells around that cell is equal to the cell's number 
we flag all of them. if one cell has the same number of flagged cells around it
as the cell's own number, we then can open any un-flagged cells around it
"""

import random
class Basic_solver:

  def __init__(self, player_map, nrow, ncol):
    self.player_map = player_map
    self.nrow = nrow
    self.ncol = ncol
    self.knownMoves = False #if there's no known moves make a random guess


# pseudo random guess that returns the first unopened cell 
  def makeRandomGuess(self):
    for i in range(self.ncol):
      for j in range(self.nrow):
        if (self.player_map[j][i] == "-" ):
          location = [i, j]
          return location    

# a function to make a random guess for the first turn
  def makeInitialGuess(self):
    x = random.randint(0, self.ncol-1)
    y = random.randint(0, self.nrow-1)
    location = [x, y]
    return location
    


  def makeGuess(self):
    # first loop through the whole field to flag around any cells that have the same number
    # of unopened cells as the cell's own number
    for i in range(self.ncol):
      for j in range(self.nrow):
        if (self.player_map[j][i] == "-" or self.player_map[j][i] == "*" or self.player_map[j][i] == 0):
          continue
        else:
          self.checkAndFlagAround(i,j)
    # then loop once again to open any unopened&unflagged cells around any cell that have the same
    # number of flagged cells around it as the cell's own number
    
    allLocations = [] # list that will hold all locations of cells that can be safely opened
    for i in range(self.ncol):
      for j in range(self.nrow):
        if (self.player_map[j][i] == "-" or self.player_map[j][i] == "*" or self.player_map[j][i] == 0):
          continue
        else:
          locations = self.checkAndOpenAround(i,j) #location of cell to be opened
          if(len(locations)):
            for location in locations:
              if not allLocations.count(location):
                allLocations.append(location)
    # if there are no known moves make a random guess
    if(not len(allLocations)):
      return self.makeRandomGuess()
    if(len(allLocations)):
    # one example of allLocations= [ [X00,Y00], [X01,Y01], [X10,Y10]
    #                              , [X20,Y20], [X21,Y21], [X22,Y22] ]                                                                                                         
      
      return allLocations.pop() # pop returns [X22,Y22]



  def checkAndFlagAround(self, x, y):
    a = []
    for i in range(x-1, x+2):
      for j in range(y-1, y+2):
        if (0 <= i < self.ncol and 0 <= j < self.nrow and (self.player_map[j][i] == "-" or self.player_map[j][i] == "*")):
          a.append([i,j])
        else:
          continue
    if len(a) == self.player_map[y][x]:
      self.knownMoves = True
      for i in a:
        self.flagCell(i[0], i[1])
    else:
      self.knownMoves = False


  def checkAndOpenAround(self, x, y):
    counter = 0
    b = []
    for i in range(x-1, x+2):
      for j in range(y-1, y+2):
        if (0 <= i < self.ncol and 0 <= j < self.nrow and self.player_map[j][i] == "*"):
          counter += 1
        else:
          continue

    if counter == self.player_map[y][x]:
      for i in range(x-1, x+2):
        for j in range(y-1, y+2):
          if (0 <= i < self.ncol and 0 <= j < self.nrow and self.player_map[j][i] == "-"):
            b.append([i,j])
          else:
            continue

    return b
    

  def flagCell(self, x, y):
    self.player_map[y][x] = "*"



    
