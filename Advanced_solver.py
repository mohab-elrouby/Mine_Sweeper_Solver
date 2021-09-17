"""
the advanced solver is the same as the basic solver but whenever it get stuck not able to 
make a certian decision instead of just guessing, it groups all the uncovered cells that 
have neighboring opened cells and tries every possible combination of mines and decides the
best choice. 
"""

import random
from itertools import  product
from collections import defaultdict


class Advanced_solver:

    def __init__(self, player_map, nrow, ncol):
        self.player_map = player_map
        self.nrow = nrow
        self.ncol = ncol

    def update(self, player_map):
        self.player_map = player_map

# pseudo random guess that returns the first unopened cell 
    def make_random_guess(self):
        for i in range(self.ncol):
            for j in range(self.nrow):
                if (self.player_map[j][i] == "-" ):
                    location = [[i, j]]
                    return location    

# a function to make a random guess for the first turn
    def make_initial_guess(self):
        x = random.randint(int(self.ncol/2), int(self.ncol-1))
        y = random.randint(int(self.nrow/2), int(self.nrow-1))
        location = [x, y]
        return location
# after stucking using straight forward approach we try to group all the border cells
# that we have partial info about them 
    def make_groups(self):
        group = []
        groups = []
        for i in range(self.ncol):
            for j in range(self.nrow):
                if (self.player_map[j][i] != "-" and self.player_map[j][i] != "*" and self.player_map[j][i] != 0):
                    cellLocations = self.check_around(i, j)
                    # if(not group):
                    #     isSameGroup = True
                    for cell in cellLocations:
                        if not group.count(cell):
                            group.append(cell)
                    if group:
                        groups.append(group)
                    group = []

        
        listsOfTuples = []
        for i in groups:
            nested_lst_of_tuples = [tuple(l) for l in i]
            listsOfTuples.append(nested_lst_of_tuples)
        groupsList = list(self.merge_common(listsOfTuples))

        return groupsList
        

    
    def merge_common(self, lists):
        neigh = defaultdict(set)
        visited = set()
        for each in lists:
            for item in each:
                neigh[item].update(each)
        def comp(node, neigh = neigh, visited = visited, vis = visited.add):
            nodes = set([node])
            next_node = nodes.pop
            while nodes:
                node = next_node()
                vis(node)
                nodes |= neigh[node] - visited
                yield node
        for node in neigh:
            if node not in visited:
                yield sorted(comp(node))

    # a function that checks whether a given permutation is possible or not
    def check_possible_permutation(self, cellsToCheck, perm):
        permutation = []
        for i in range(self.nrow):
            row=[]
            permutation.append(row)
            for j in range(self.ncol):
                row.append(perm[i][j])
                if (perm[i][j] != "-" and perm[i][j] != "*" and perm[i][j] != 0):
                    if(not self.check_possible_cell(j, i, cellsToCheck, perm)):
                        return 
        return permutation
    
    # a function that checks whether the cells we are interested in have 
    # the same number of mines around it, as their own number or not
    def check_possible_cell(self, x, y, cellsToCheck, perm):
        counter = 0
        isIncellsToCheck = False
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                cell = (i, j)
                if(cellsToCheck.count(cell)):
                    isIncellsToCheck = True
                if (0 <= i < self.ncol and 0 <= j <  self.nrow and  perm[j][i] == "*"):
                    counter += 1
        if (counter ==  perm[y][x] or not isIncellsToCheck):
            return True  
        
        return False              


    def make_guess(self):
    # first loop through the whole field to flag around any cells that have the same number
    # of unopened cells as the cell's own number
        for i in range(self.ncol):
            for j in range(self.nrow):
                if (self.player_map[j][i] != "-" and self.player_map[j][i] != "*" and self.player_map[j][i] != 0):
                    self.check_and_flag_around(i,j)

    # then loop once again to open any unopened&unflagged cells around any cell that have the same
    # number of flagged cells around it as the cell's own number
    
        allLocations = [] # list that will hold all locations of cells that can be safely opened
        for i in range(self.ncol):
            for j in range(self.nrow):
                if (self.player_map[j][i] != "-" and self.player_map[j][i] != "*" and self.player_map[j][i] != 0):
                    locations = self.check_and_open_around(i,j) #location of cell to be opened
                    if(len(locations)):
                        for location in locations:
                            if not allLocations.count(location):
                                allLocations.append(location)           
                    
    # if there are no known moves make an educated guess
        if(not len(allLocations)):
            # find all the cells that we are not sure about and segregate the un-connected
            # /un-related groups to make it faster, and in some cases just to make it doable.
            borderCells = self.make_groups()

            # for each group of cells that we are not certian about find all the possible combinations.
            # then find the cells that didn't contain any bombs in any of the combinations or contained
            # the least amount of them.
            cellsScores = {}
                    
            for group in borderCells:
                if(len(group)<14):
                    for cell in group:
                        cellsScores[cell] = 0
                    allPermutations = list(product(["-","*"], repeat=len(group)))
                    allPermutations = [list(i) for i in allPermutations] 
                    allPossibleBoards = []
                    possiblePermutation = []
                    for i in range(self.nrow):
                        possibleRow = []
                        possiblePermutation.append(possibleRow)
                        for j in range(self.ncol):
                            possibleRow.append(self.player_map[i][j])
                    for permutation in allPermutations:
                        for cell in group:
                            i = cell[0]
                            j = cell[1]
                            possiblePermutation[j][i] = permutation[group.index(cell)]

                        newPossiblePermutation = self.check_possible_permutation(group, possiblePermutation)
                        if (newPossiblePermutation is not None):
                            allPossibleBoards.append(newPossiblePermutation)
                    
                    for possibleBoard in allPossibleBoards:
                        for cell in group:
                            i = cell[0]
                            j = cell[1]
                            if(possibleBoard[j][i] == "*"):
                                cellsScores[cell] += (1/len(allPossibleBoards)) 
            if(cellsScores):
                answer = []
                for cell in cellsScores:
                    i = cell[0]
                    j = cell[1] 
                    if cellsScores[cell] < 0.2:
                        answer.append(cell)
                    if cellsScores[cell] == 1:
                        self.player_map[j][i]="*"
                if answer:
                    print(cellsScores)
                    print(answer)
                    return answer
                else:
                    safestCell = min(cellsScores, key = lambda k: cellsScores[k])
                    print(cellsScores)
                    print([safestCell])
                    if(cellsScores[safestCell] > 0.5):
                        return self.make_random_guess()
                    return [safestCell]

            else:
                return self.make_random_guess()
        if allLocations:
            return allLocations 
        else:
            return self.make_random_guess()
    # one example of allLocations= [ [X00,Y00], [X01,Y01], [X10,Y10]
    #                              , [X20,Y20], [X21,Y21], [X22,Y22] ]
            



    def check_and_flag_around(self, x, y):
        a = []
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (0 <= i < self.ncol and 0 <= j < self.nrow and (self.player_map[j][i] == "-" or self.player_map[j][i] == "*")):
                    a.append([i,j])
                else:
                    continue
        if len(a) == self.player_map[y][x]:
            for i in a:
                self.flag_cell(i[0], i[1])


    def check_and_open_around(self, x, y):
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
    

    def check_around(self, x, y):
        coveredCells = []
        for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    if (0 <= i < self.ncol and 0 <= j < self.nrow and self.player_map[j][i] == "-"):
                        coveredCells.append([i,j])
        return coveredCells

    def flag_cell(self, x, y):
        self.player_map[y][x] = "*"
