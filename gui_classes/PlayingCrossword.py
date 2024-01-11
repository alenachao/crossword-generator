import tkinter as tk
from tkinter import messagebox 

class PlayingCrossword:
    """
    Handles logic for user playing the crossword.
    """
    def __init__(self, master, switch_frames, solution):
        self.master = master
        self.solution = solution
        self.switch_frames = switch_frames

        self.cell_size = 30
        self.canvas = tk.Canvas(master, width=len(self.solution.get_grid())*self.cell_size, height=len(self.solution.get_grid())*self.cell_size)
        self.canvas.grid(row=0, column=0)

        self.user_entries = [['#' for _ in range(len(row))] for row in self.solution.get_grid()]

        solution.add_clue_numbers()
        solution.add_clues()
        self.create_crossword_board()
        self.display_clues()

    def create_crossword_board(self):
        # create board
        for i, row in enumerate(self.solution.get_grid()):
            for j, cell in enumerate(row):
                x = j * self.cell_size
                y = i * self.cell_size

                if cell == "#":
                    self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, outline="black", fill='black')
                else:
                    entry = tk.Entry(self.master, width=2, justify='center', font=('Arial', 16))
                    self.user_entries[i][j] = entry
                    entry_id = self.canvas.create_window(x, y, window=entry, anchor='nw')

        # add clue numbers
        for word in self.solution.get_words_used():
            x = word.get_col() * self.cell_size
            y = word.get_row() * self.cell_size
            label_text = word.get_clue_number()
            label = tk.Label(self.master, text=label_text, font=('Arial', 6, 'bold'))
            label.place(x=x, y=y)

        submit_button = tk.Button(self.master, text="Submit", command=self.check_solution)
        submit_button.grid(row=len(self.solution.get_grid()) + 1, pady=10)

    def display_clues(self):
        vertical_clues = "\n".join([f"{word.get_clue_number()}. {word.get_clue()}" for word in self.solution.get_words_used() if not word.get_hor()])
        horizontal_clues = "\n".join([f"{word.get_clue_number()}. {word.get_clue()}" for word in self.solution.get_words_used() if word.get_hor()])
        self.clues_label = tk.Label(self.master, text=f"Veritcal:\n{vertical_clues}\nHorizontal:\n{horizontal_clues}", font=('Arial', 12), wraplength=200, justify="left", anchor="nw")
        self.clues_label.grid(row=0, column=2, rowspan=len(self.solution.get_grid()) + 1)

    def check_solution(self):
        for i in range(len(self.solution.get_grid())):
            for j in range(len(self.solution.get_grid())):
                letter = self.solution.get_grid()[i][j]
                if letter != "#" and letter != self.user_entries[i][j].get():
                    print(self.user_entries[i][j].get())
                    messagebox.showinfo("Try Again", "Incorrect entries. Keep trying!")
                    return        
        messagebox.showinfo("Congratulations", "You Win!")
            
