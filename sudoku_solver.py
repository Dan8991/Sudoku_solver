import numpy as np

def get_lines(sudoku, x, y):
    return sudoku[x, :], sudoku[:, y]

def get_sub_grid(sudoku, x, y):
    i = (x//3)*3
    j = (y//3)*3

    return sudoku[i:(i + 3), j:(j + 3)]

def back_track_solver(sudoku, index = 0):
   
    if index > 80:
        return sudoku
    
    # pylint: disable=unbalanced-tuple-unpacking
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
            solution = back_track_solver(sudoku, index + 1) 

            if solution[8, 8] != 0:
                return solution

            sudoku[i, j] = 0

        return sudoku

def has_more_than_one_solution(sudoku):
    return find_some_solutions(sudoku) == 2

def find_some_solutions(sudoku, index=0):
    
    if index > 80:
        return 1

    # pylint: disable=unbalanced-tuple-unpacking
    i, j = np.unravel_index(index, sudoku.shape)
    number_of_solutions = 0
    
    if sudoku[i, j] != 0:
        return find_some_solutions(sudoku, index = index + 1)
    else:

        grid = get_sub_grid(sudoku, i, j)
        hor, vert = get_lines(sudoku, i, j)
        current_values = set(grid.reshape(-1)).union(set(hor)).union(set(vert))
        possible_values = set(range(10)) - current_values

        if len(possible_values) == 0:
            return 0 
    
        for value in possible_values:
            sudoku[i, j] = value

            number_of_solutions += find_some_solutions(sudoku, index + 1) 

            if number_of_solutions >= 2:
                return number_of_solutions

            sudoku[i, j] = 0

        return number_of_solutions 


            
sudoku = np.zeros((9,9)) 
good_solution = back_track_solver(sudoku)
good_solution[8, 8] = 0
print(has_more_than_one_solution(sudoku))
sudoku = np.zeros((9,9)) 
print(has_more_than_one_solution(sudoku))
