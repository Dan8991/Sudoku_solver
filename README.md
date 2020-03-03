# Sudoku Solver

Sudoku solver is a basic GUI that can generate new sudoku games and can solve them.

## Requirements 
python3 is needed in order to run sudoku solver.

The main python libraries that have to be installed in order to run the application are:
* TKinter
```
sudo apt-get install python-tk
```

* Numpy
```
pip3 install numpy
```

* Tqdm 
```
pip3 install tqdm 
```

## Starting
In order to run the sudoku solver just run
```
python3 main.py
```

## Usage
When the graphical interface pops up there are two buttons that can be pressed.

While the GUI is solving a game or generating one it will not
be possible to press the Create Game and Start buttons.

* Create Game

This button generates a new sudoku game, this process may take a while if a very unfortunate 
case happens.
A progress bar showing the state of the game generation will be displayed on the terminal.
* Start

The Start button solves the sudoku that is represented by the GUI, this is done even if the grid is empty .
