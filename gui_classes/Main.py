import tkinter as tk
from gui_classes.PickingCrossword import PickingCrossword
from gui_classes.PlayingCrossword import PlayingCrossword

class MainFrame:
    """
    Handles scrolling and switching frames.
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

        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)

        self.vsb['command'] = self.canvas.yview
        self.hsb['command'] = self.canvas.xview

        self.inner = tk.Frame(self.canvas, bg=bg)

        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

        # switching frames
        self.current_frame = PickingCrossword(self.inner, self.switch_frames)

    def switch_frames(self, generated_crossword=None):
        for widget in self.current_frame.master.winfo_children():
            widget.destroy()
        self.current_frame.master.pack_forget()

        if isinstance(self.current_frame, PickingCrossword):
            self.current_frame = PlayingCrossword(self.master, self.switch_frames, generated_crossword)
        else:
            self.current_frame = PickingCrossword(self.master, self.switch_frames)

        self.current_frame.master.pack()
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