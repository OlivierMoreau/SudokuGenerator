## Sudoku Grids generator

Command line python program that generate playable sudoku grids.

Takes 3 arguments 

1. Int- Timeout : The maximum time in sec the program should take when attempting to generate a grid. 
2. Int- Amount : How many grids should the program will generate.
3. Bool- SysShutdown : If the system should shutdown once the task is complete (this process is pretty long). False by default.

exemple :

```
$>python generator.py 12 2000 True
```

The program will output 2 files a  .txt file for debugging purposes, and a binary file where the data has been "pickled" <https://docs.python.org/3/library/pickle.html>.

To be as efficient as possible each grids will be rotated 4 times by 90° creating 4 games of sudoku per program cycle.

For each created grid the output data will present as follow:

* the 4 rotations of the incomplete grid
* those same grade fully completed 
* how long it took to generate this grid

The completed grids are saved as to not have to run the solving algorithm every time we need to access the final value of a cell.

The time spent is only here because its used after creation of all the grids as a crude way of sorting them by difficulty. 

This is going off the assumption that given that the algorithm to solve and create a grid are basically the same reversed, on average the longer it takes to create one the harder it will be to solve. (this could be completely wrong).