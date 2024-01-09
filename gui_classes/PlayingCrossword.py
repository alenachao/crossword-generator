import tkinter as tk
from tkinter import messagebox 

class PlayingCrossword:
    """
    Handles logic for user playing the crossword.
    """
    def __init__(self, master, switch_frames, solution):
        self.master = master
        self.solution = solution
        self.solution_grid = solution.get_grid()
        self.switch_frames = switch_frames

        self.cell_size = 30
        self.canvas = tk.Canvas(master, width=len(self.solution_grid)*self.cell_size, height=len(self.solution_grid)*self.cell_size)
        self.canvas.grid(column=0, row=0) 

        self.user_entries = [['#' for _ in range(len(row))] for row in self.solution_grid]
        self.create_crossword_board()

    def create_crossword_board(self):
        for i, row in enumerate(self.solution_grid):
            for j, cell in enumerate(row):
                x = j * self.cell_size
                y = i * self.cell_size

                if cell == "#":
                    self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, outline="black", fill='black')
                else:
                    entry = tk.Entry(self.master, width=2, justify='center', font=('Arial', 18))
                    self.user_entries[i][j] = entry
                    entry_id = self.canvas.create_window(x, y, window=entry, anchor='nw')

        submit_button = tk.Button(self.master, text="Submit", command=self.check_solution)
        submit_button.grid(row=len(self.solution_grid) + 1, pady=10)

    def check_solution(self):
        for i in range(len(self.solution_grid)):
            for j in range(len(self.solution_grid)):
                letter = self.solution_grid[i][j]
                if letter != "#" and letter != self.user_entries[i][j].get():
                    print(self.user_entries[i][j].get())
                    messagebox.showinfo("Try Again", "Incorrect entries. Keep trying!")
                    return        
        messagebox.showinfo("Congratulations", "You Win!")
            
