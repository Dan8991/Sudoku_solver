import numpy as np
import tkinter as tk
from sudoku_utils import back_track_solver, str_label, generate_sudoku_game

#class definin a grafic interface object
class Sudoku_gi():

    def __init__(self):

        #main app
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")

        #variable used to stop buttons from working if some calculation is being made
        self.is_working = False

        #sudoku game represented by the gui
        self.sudoku = np.zeros((9, 9)) 
        
        frames = [[] for i in range(3)]
        
        #frame containing the sudoku grid
        main_frame = tk.Frame(self.root, bg = "black")
        main_frame.grid(row=0)

        #all 9 3x3 blocks
        for i in range(3):
            for j in range(3):
                frames[i].append(
                        tk.Frame(
                            main_frame, 
                            bg="white", 
                            highlightcolor="black", 
                            highlightthickness=0.5, 
                            highlightbackground="black" 
                        )
                )
                frames[i][j].grid(row=i, column=j)

        labels = [[] for i in range(9)]

        #all 81 cells
        for i in range(9):
            for j in range(9):
                labels[i].append(tk.Label(
                    frames[i//3][j//3], 
                    text = str_label(self.sudoku[i, j]),
                    bg = "white",
                    height = 2,
                    width = 5,
                    bd = 2,
                    highlightcolor = "black",
                    highlightthickness = 1,
                    highlightbackground = "black" 
                ))
                labels[i][j].grid(row = i%3, column = j%3)

        self.labels = labels

        #Frame containing the buttons
        buttons_frame = tk.Frame(self.root)
        buttons_frame.grid(row=1)

        #button that creates a new sudoku game
        tk.Button(
                buttons_frame, 
                text = "Create Game", 
                command = self.generate_sudoku_game, 
                width = 15, 
                background = "Green", 
                activebackground = "LightGreen"
        ).grid(row = 3, column = 0)

        #button that solves the current sudoku
        tk.Button(
                buttons_frame, 
                text =" Start", 
                command = self.execute_sudoku, 
                width = 15, 
                background = "Green", 
                activebackground = "LightGreen"
        ).grid(row = 3, column = 2)

        #main_loop
        self.root.mainloop()

    def execute_sudoku(self):

        if not self.is_working:

            self.is_working = True
            back_track_solver(self.sudoku, root = self.root, tk_cells=self.labels)
            self.is_working = False

    def generate_sudoku_game(self):

        if not self.is_working:

            self.is_working = True

            print("Generating a new game")
            self.sudoku = generate_sudoku_game()

            #updating labels by considering the new sudkoku
            for i in range(9):
                for j in range(9):
                    self.labels[i][j].config(text = str_label(self.sudoku[i][j]))
                    if self.sudoku[i][j] != 0:
                        self.labels[i][j].config(foreground = "red")
            self.root.update()
            
            self.is_working = False

