import tkinter as tk
from classes.CrosswordGenerator import CrosswordGenerator

class CrosswordGUI:
    def __init__(self, master):
        self.master = master

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

        self.crossword_canvases = []

        # Create a listbox to display generated crosswords
        # self.crossword_listbox = tk.Listbox(master)
        # self.crossword_listbox.pack()


        # Bind double click event on the listbox
        #self.crossword_listbox.bind("<Double-Button-1>", self.play_crossword)


    def generate_crosswords(self):
        try:
            crossword_count = int(self.crossword_count_entry.get())
            word_list = self.word_list_entry.get().split(',')
            grid_size = int(self.grid_size_entry.get())
            cell_size = 20  # Adjust the cell size as needed

            # Generate crosswords
            generator = CrosswordGenerator(grid_size, word_list)
            generator.generate_crosswords(crossword_count)

            # Display crosswords using a grid layout
            num_columns = 3  # Adjust the number of columns as needed
            crossword_canvases = []

            for k, crossword in enumerate(generator.get_crosswords()):
                canvas = tk.Canvas(self.master, width=generator.grid_size*cell_size, height=generator.grid_size*cell_size+100)
                crossword_canvases.append(canvas)

                # Calculate row and column positions
                row_position = k // num_columns + 3
                col_position = k % num_columns

                # Use the grid geometry manager
                canvas.grid(row=row_position, column=col_position, padx=10, pady=10)

                # Draw cells
                for i, row in enumerate(crossword.get_grid()):
                    for j, cell in enumerate(row):
                        x = j * cell_size
                        y = i * cell_size
                        fill_color = "black" if cell == '#' else "white"
                        canvas.create_rectangle(x, y + 70, x + cell_size, y + cell_size + 70, outline="black", fill=fill_color)
                        if cell != "#":
                            # Adjust the text position to be centered in the cell
                            text_x = x + cell_size // 2
                            text_y = y + cell_size // 2 + 70
                            canvas.create_text(text_x, text_y, text=cell)

                canvas.create_text(generator.grid_size * cell_size // 2, 10, text=f"Score: {crossword.score}", font=("Arial", 12, "bold"))
                canvas.create_text(generator.grid_size * cell_size // 2, 30, text=f"Words Used: {', '.join(crossword.words_used)}", font=("Arial", 10))
                canvas.create_text(generator.grid_size * cell_size // 2, 50, text=f"Words Unused: {', '.join(crossword.words_unused)}", font=("Arial", 10))

            # Save the canvases to class variable for later reference
            self.crossword_canvases = crossword_canvases

        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    # def play_crossword(self, event):
    #     selected_index = self.crossword_listbox.curselection()
    #     if selected_index:
    #         selected_crossword = generator.crosswords[selected_index[0]]
    #         # TODO: Implement logic to display and play the selected crossword
            
class ScrolledFrame:
    """
    A scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    :width:, :height:, :bg: are passed to the underlying Canvas
    :bg: and all other keyword arguments are passed to the inner Frame
    note that a widget layed out in this frame will have a self.master 3 layers deep,
    (outer Frame, Canvas, inner Frame) so 
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.hsb = tk.Scrollbar(self.outer, orient=tk.HORIZONTAL)

        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.hsb.pack(fill=tk.X, side=tk.BOTTOM)

        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg, yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview
        self.hsb['command'] = self.canvas.xview

        self.inner = tk.Frame(self.canvas, bg=bg)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

        self.crossword_gui = CrosswordGUI(self.inner)


    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion=(0, 0, max(x2, width), max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )

    def __str__(self):
        return str(self.outer)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Crossword Generator")
    window_width = 600  # Adjust the width as needed
    window_height = 400  # Adjust the height as needed
    root.geometry(f"{window_width}x{window_height}")
    vscf = ScrolledFrame(root)
    vscf.pack(expand=True, fill="both")
    root.mainloop()