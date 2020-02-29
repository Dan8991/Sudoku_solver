import numpy as np

def get_lines(sudoku, x, y):
    return sudoku[x, :], sudoku[:, y]

def get_sub_grid(sudoku, x, y):
    i = (x//3)*3
    j = (y//3)*3

    return sudoku[i:(i + 3), j:(j + 3)]

def back_track_solver(sudoku, index = 0):
    
    i, j = np.unravel_index(index, sudoku.shape)
    
    if sudoku[i, j] != 0:
        return back_track_solver(sudoku, index = index + 1)
    else:

        grid = get_sub_grid(sudoku, i, j)
        hor, vert = get_lines(sudoku, i, j)
        current_values = set(grid.reshape(-1)).union(set(hor)).union(set(vert))
        possible_values = set(range(10)) - current_values

        if len(possible_values) == 0:
            return sudoku
    
        for value in possible_values:
            sudoku[i, j] = value

            if sudoku[8, 8] != 0:
                return sudoku 

            solution = back_track_solver(sudoku, index + 1) 

            if solution[8, 8] != 0:
                return solution

            sudoku[i, j] = 0

        return sudoku
            
sudoku = np.zeros((9,9)) 
print(back_track_solver(sudoku))
