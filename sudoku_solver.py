import numpy as np
from tqdm import tqdm
import tkinter as tk
import time

#returns the horizonatal and vertical line containing the current cell
def get_lines(sudoku, x, y):
    return sudoku[x, :], sudoku[:, y]

#returns the 3x3 grid containing the current cell
def get_sub_grid(sudoku, x, y):
    i = (x//3)*3
    j = (y//3)*3

    return sudoku[i:(i + 3), j:(j + 3)]

def back_track_solver(sudoku, root = None, tk_cells=None, index = 0, randomized = True):
    
    #base case if the index is greater than the dimension of a sudoku
    if index > 80:
        return sudoku
    
    # pylint: disable=unbalanced-tuple-unpacking
    i, j = np.unravel_index(index, sudoku.shape)
    
    #if the current value is fixed go on to the next one
    if sudoku[i, j] != 0:
        return back_track_solver(sudoku, root, tk_cells, index = index + 1)
    else:
        #getting all the invalid values 
        grid = get_sub_grid(sudoku, i, j)
        hor, vert = get_lines(sudoku, i, j)
        current_values = set(grid.reshape(-1)).union(set(hor)).union(set(vert))

        #selecting the values that can be chosen
        possible_values = list(set(range(10)) - current_values)

        #if no value can be placed in the current cell then this is an invalid solution
        if len(possible_values) == 0:
            return sudoku
        
        if randomized:
            possible_values = np.random.permutation(possible_values)
    
        for value in possible_values:

            #try to solve the sudoku using the current value
            sudoku[i, j] = value 

            if tk_cells is not None and root is not None:
                tk_cells[i][j].config(text = str_label(value))
                time.sleep(0.025)
                root.update()

            solution = back_track_solver(sudoku, root, tk_cells, index + 1) 

            #if the solution is complete return it
            if np.sum(sudoku == 0) == 0:
                return solution
            
            #needed because otherwise when backtracking the first if would be triggered even if this is an invalid solution
            sudoku[i, j] = 0
            if tk_cells is not None and root is not None:
                tk_cells[i][j].config(text = str_label(0))
                time.sleep(0.025)
                root.update()


        #if no valid solution was found backtrack
        return sudoku

#checks if the sudoku has more than one solution
def has_more_than_one_solution(sudoku):
    return find_some_solutions(sudoku) == 2

#checks if the sudoku has more than one solution stopping at 2
def find_some_solutions(sudoku, index=0):
    
    #base case if the index is greater than the dimension of a sudoku
    if index > 80:
        return 1

    # pylint: disable=unbalanced-tuple-unpacking
    i, j = np.unravel_index(index, sudoku.shape)
    number_of_solutions = 0
    
    #if the current value is fixed go on to the next one
    if sudoku[i, j] != 0:
        return find_some_solutions(sudoku, index = index + 1)
    else:

        #getting all the invalid values 
        grid = get_sub_grid(sudoku, i, j)
        hor, vert = get_lines(sudoku, i, j)
        current_values = set(grid.reshape(-1)).union(set(hor)).union(set(vert))

        #selecting the values that can be chosen
        possible_values = set(range(10)) - current_values

        #if no value can be placed in the current cell then this is an invalid solution
        if len(possible_values) == 0:
            return 0 

        for value in possible_values:
            sudoku[i, j] = value

            number_of_solutions += find_some_solutions(sudoku, index + 1) 

            if number_of_solutions >= 2:
                sudoku[i, j] = 0
                return number_of_solutions
            #needed because otherwise when backtracking the first if would be triggered even if this is an invalid solution
            sudoku[i, j] = 0

        #if two solutions were not found yet then backtrack 
        return number_of_solutions 

def generate_sudoku_game():
    
    sudoku = back_track_solver(np.zeros((9, 9), dtype = np.int))

    #list of indexes 
    removing_indexes = np.random.permutation(list(range(81)))
    #used for indexing
    unused = 0

    for index in tqdm(removing_indexes):

        # pylint: disable=unbalanced-tuple-unpacking
        i, j = np.unravel_index(index, sudoku.shape)

        temp = sudoku[i, j]
        sudoku[i, j] = 0
        
        #if there is just one solution go to the next step and remove the current index from the list
        if has_more_than_one_solution(sudoku):
            sudoku[i, j] = temp
            unused += 1

    return sudoku

def str_label(val):

    if val == 0:
        return " "

    return str(val)

class Sudoku_gi():

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")
        self.sudoku = np.zeros((9, 9)) 
        frames = [[] for i in range(3)]
        main_frame = tk.Frame(self.root, bg = "black")
        main_frame.grid(row=0)

        for i in range(3):
            for j in range(3):
                frames[i].append(tk.Frame(main_frame, bg="white", highlightcolor="black", highlightthickness=0.5, highlightbackground="black" ))
                frames[i][j].grid(row=i, column=j)

        labels = [[] for i in range(9)]

        for i in range(9):
            for j in range(9):
                labels[i].append(tk.Label(
                    frames[i//3][j//3], 
                    text = str_label(self.sudoku[i, j]),
                    bg="white",
                    height=2,
                    width=5,
                    bd=2,
                    highlightcolor="black",
                    highlightthickness=1,
                    highlightbackground="black" 
                ))
                labels[i][j].grid(row = i%3, column = j%3)

        self.labels = labels
        buttons_frame = tk.Frame(self.root)
        buttons_frame.grid(row=1)
        tk.Button(buttons_frame, text="Create Game", command=self.generate_sudoku_game, width = 15, background="Green", activebackground="LightGreen").grid(row = 3, column=0)
        tk.Button(buttons_frame, text="Start", command=self.execute_sudoku, width = 15, background="Green", activebackground="LightGreen").grid(row=3, column = 2)
        self.root.mainloop()

    def execute_sudoku(self):
        back_track_solver(self.sudoku, root = self.root, tk_cells=self.labels)

    def generate_sudoku_game(self):
        print("Generating a new game")
        self.sudoku = generate_sudoku_game()
        for i in range(9):
            for j in range(9):
                self.labels[i][j].config(text = str_label(self.sudoku[i][j]))
                if self.sudoku[i][j] != 0:
                    self.labels[i][j].config(foreground = "red")
        self.root.update()

Sudoku_gi()
