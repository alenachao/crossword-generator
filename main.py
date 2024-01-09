import tkinter as tk
from gui_classes.Main import MainFrame

"""
Entry point for GUI
"""

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Crossword Generator")
    window_width = 600
    window_height = 400
    root.geometry(f"{window_width}x{window_height}")
    vscf = MainFrame(root)
    vscf.pack(expand=True, fill="both")
    root.mainloop()