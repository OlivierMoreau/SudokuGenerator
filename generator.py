#Sudoku Generator Algorithm - Modified from www.101computing.net/sudoku-generator-algorithm/
from threading import Thread
import functools
from random import randint, shuffle
from time import *
import pickle
import copy
import os
import sys

if len(sys.argv) < 3:
    print('Invalid arguments follow format: python generator.py <max duration for generation before timeout(int)> <ammount of grids to produce (int)> <sys shutdown when complete (bool)>')
    exit(1)

TIMEOUT = int(sys.argv[1]) or 12
GRIDS_AMMOUNT = int(sys.argv[2]) or 1
if len(sys.argv) == 4:
    SHUTDOWN = sys.argv[3]
else:
    SHUTDOWN = False

#Wrapper function to stop exectution of main function
def timeout(seconds_before_timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, seconds_before_timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(seconds_before_timeout)
            except Exception as e:
                print('error starting thread')
                raise e
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco

# Whole playable grids creation cycle wrapped in the timeout
# fillGrid() Will first generate a complete grid recusively.
# Then reducer() will remove some answers from the grid while given a set ammount of "attempts" to do so.
# Each time the program will try every possible solutions recursively to this new incomplete grid using solveGrid(), and if no solution or more than one solution is found, it will backtrack to the previous step and remove an attempt.
# Once out of attempts we have a playable grid.
# Finally we return a list with all the data we need.

@timeout(TIMEOUT)
def cycle():

    start_time = time()
    #initialise empty 9 by 9 grid
    grid = []
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])


    #A function to check if the grid is full
    def checkGrid(grid):
      for row in range(0,9):
          for col in range(0,9):
            if grid[row][col]==0:
              return False

      #We have a complete grid!
      return True

    #A backtracking/recursive function to check all possible combinations of numbers until a solution is found
    def solveGrid(grid):
      global counter
      #Find next empty cell
      for i in range(0,81):
        row=i//9
        col=i%9
        if grid[row][col]==0:
          for value in range (1,10):
            #Check that this value has not already be used on this row
            if not(value in grid[row]):
              #Check that this value has not already be used on this column
              if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
                #Identify which of the 9 squares we are working on
                square=[]
                if row<3:
                  if col<3:
                    square=[grid[i][0:3] for i in range(0,3)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(0,3)]
                  else:
                    square=[grid[i][6:9] for i in range(0,3)]
                elif row<6:
                  if col<3:
                    square=[grid[i][0:3] for i in range(3,6)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(3,6)]
                  else:
                    square=[grid[i][6:9] for i in range(3,6)]
                else:
                  if col<3:
                    square=[grid[i][0:3] for i in range(6,9)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(6,9)]
                  else:
                    square=[grid[i][6:9] for i in range(6,9)]
                #Check that this value has not already be used on this 3x3 square
                if not value in (square[0] + square[1] + square[2]):
                  grid[row][col]=value
                  if checkGrid(grid):
                    counter+=1
                    break
                  else:
                    if solveGrid(grid):
                      return True
          break
      grid[row][col]=0

    numberList=[1,2,3,4,5,6,7,8,9]
    #shuffle(numberList)

    #A backtracking/recursive function to check all possible combinations of numbers until a solution is found
    def fillGrid(grid):
      global counter
      #Find next empty cell
      for i in range(0,81):
        row=i//9
        col=i%9
        if grid[row][col]==0:
          shuffle(numberList)
          for value in numberList:
            #Check that this value has not already be used on this row
            if not(value in grid[row]):
              #Check that this value has not already be used on this column
              if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
                #Identify which of the 9 squares we are working on
                square=[]
                if row<3:
                  if col<3:
                    square=[grid[i][0:3] for i in range(0,3)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(0,3)]
                  else:
                    square=[grid[i][6:9] for i in range(0,3)]
                elif row<6:
                  if col<3:
                    square=[grid[i][0:3] for i in range(3,6)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(3,6)]
                  else:
                    square=[grid[i][6:9] for i in range(3,6)]
                else:
                  if col<3:
                    square=[grid[i][0:3] for i in range(6,9)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(6,9)]
                  else:
                    square=[grid[i][6:9] for i in range(6,9)]
                #Check that this value has not already be used on this 3x3 square
                if not value in (square[0] + square[1] + square[2]):
                  grid[row][col]=value
                  if checkGrid(grid):
                    return True
                  else:
                    if fillGrid(grid):
                      return True
          break
      grid[row][col]=0


    def reducer(grid):
        #Start Removing Numbers one by one

        #A higher number of attempts will end up removing more numbers from the grid
        #Potentially resulting in more difficiult grids to solve!
        attempts = 9
        global counter
        counter = 1
        while attempts>0:
          #Select a random cell that is not already empty
          row = randint(0,8)
          col = randint(0,8)
          while grid[row][col]==0:
            row = randint(0,8)
            col = randint(0,8)
          #Remember its cell value in case we need to put it back
          backup = grid[row][col]
          grid[row][col]=0

          #Take a full copy of the grid
          copyGrid = []
          for r in range(0,9):
             copyGrid.append([])
             for c in range(0,9):
                copyGrid[r].append(grid[r][c])

          #Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
          counter=0
          solveGrid(copyGrid)
          #If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
          if counter!=1:
            grid[row][col]=backup
            #We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
            attempts -= 1

    #Generate a Fully Solved Grid
    fillGrid(grid)
    fullGrid = copy.deepcopy(grid)
    reducer(grid)

    #Rotates grids to generate 4 playable game per cycle.
    def rotate(grid):
      list_of_tuples = zip(*grid[::-1])
      return [list(elem) for elem in list_of_tuples]
      # return map(list, list_of_tuples)


    finish = round(time() - start_time)

    rot1 = list(rotate(grid))
    full1 = list(rotate(fullGrid))


    rot2 = list(rotate(rot1))
    full2 = list(rotate(full1))

    rot3 = list(rotate(rot2))
    full3 = list(rotate(full2))

    ret = [[grid, rot1, rot2, rot3],[fullGrid, full1, full2, full3],finish]
    return ret
# END of whole cycle

#Main loop, calls grid generating functions until desired ammount is reached. If the function takes longer than the specified timeout it will raise an exception and try again.
count = 0
dump =[]

while count < GRIDS_AMMOUNT:
    try:
        grid = cycle()
        dump.append(grid)
        count += 1
    except:
        continue

# Sorts grids by how long they took to be created.
def sorter(sub_list):
    return(sorted(sub_list, key = lambda x: x[2]))

# Attempts to sort the grids by the time it took to create them. If successfull writes them to the txt file.
try:
    sorted = sorter(dump)
    with open('log.txt', 'w') as f:
        f.write(f"{sorted}")
except:
    with open('log.txt', 'w') as f:
        f.write(f"failed sort")

#Pickles the grids data to reduce size
with open('grids.data', 'wb') as f:
    pickle.dump(sorted, f)

#If specified the system will shutdown once the task is completed
if SHUTDOWN:
    os.system('shutdown -s')

exit(0)




