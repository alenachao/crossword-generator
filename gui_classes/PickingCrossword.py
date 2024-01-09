import tkinter as tk
from generator_classes.CrosswordGenerator import CrosswordGenerator

class PickingCrossword:
    """
    User inputs grid size, word list, and number of crosswords. Return back generated crosswords for them to choose.
    """
    def __init__(self, master, switch_frames):
        self.master = master
        self.switch_frames = switch_frames
        self.crossword = None

        # Create labels and entry widgets for user input
        self.label1 = tk.Label(master, text="Number of Crosswords:")
        self.label1.grid(row=0, column=0)

        self.crossword_count_entry = tk.Entry(master)
        self.crossword_count_entry.grid(row=1, column=0)

        self.label2 = tk.Label(master, text="Word List (comma-separated):")
        self.label2.grid(row=0, column=1)

        self.word_list_entry = tk.Entry(master)
        self.word_list_entry.grid(row=1, column=1)

        self.label3 = tk.Label(master, text="Grid Size:")
        self.label3.grid(row=0, column=2)

        self.grid_size_entry = tk.Entry(master)
        self.grid_size_entry.grid(row=1, column=2)

        # Create a button to generate crosswords
        self.generate_button = tk.Button(master, text="Generate Crosswords", command=self.generate_crosswords)
        self.generate_button.grid(row=2, column=1)

    def generate_crosswords(self):
        try:
            crossword_count = int(self.crossword_count_entry.get())
            word_list = self.word_list_entry.get().split(',')
            grid_size = int(self.grid_size_entry.get())
            cell_size = 20
            num_columns = 3  
            crossword_canvases = []

            # Generate crosswords
            generator = CrosswordGenerator(grid_size, word_list)
            generator.generate_crosswords(crossword_count)

            # Display crosswords
            for k, crossword in enumerate(generator.get_crosswords()):
                canvas = CrosswordCanvas(self.master, width=generator.grid_size*cell_size, height=generator.grid_size*cell_size+100, crossword=crossword, switch_frames=self.switch_frames)
                crossword_canvases.append(canvas)

                # Place canvas on grid
                row_position = k // num_columns + 3
                col_position = k % num_columns
                canvas.canvas.grid(row=row_position, column=col_position, padx=10, pady=10)

                # Draw cells
                for i, row in enumerate(crossword.get_grid()):
                    for j, cell in enumerate(row):
                        x = j * cell_size
                        y = i * cell_size
                        fill_color = "black" if cell == '#' else "white"
                        canvas.canvas.create_rectangle(x, y + 70, x + cell_size, y + cell_size + 70, outline="black", fill=fill_color)

                # Display crossword info
                canvas.canvas.create_text(generator.grid_size * cell_size // 2, 10, text=f"Score: {crossword.score}", font=("Arial", 12, "bold"))
                canvas.canvas.create_text(generator.grid_size * cell_size // 2, 30, text=f"Words Used: {', '.join(crossword.words_used)}", font=("Arial", 10))
                canvas.canvas.create_text(generator.grid_size * cell_size // 2, 50, text=f"Words Unused: {', '.join(crossword.words_unused)}", font=("Arial", 10))

        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

class CrosswordCanvas:
    def __init__(self, master, width, height, crossword, switch_frames):
        self.master = master
        self.crossword = crossword
        self.canvas = tk.Canvas(master, width=width, height=height)
        self.switch_frames = switch_frames
        self.canvas.bind("<Button-1>", self.crossword_clicked) 

    def crossword_clicked(self, event=None):
        self.switch_frames(self.crossword)