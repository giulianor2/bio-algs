import tkinter as tk
from tkinter import ttk
import data_model as d


class BasicForm(ttk.Frame):
    """This is the main application that takes in a problem and runs the solution algorithm"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        # Add header
        ttk.Label(
            self,
            text='Hybrid Greedy plus Genetic Algorithm Sudoku Solver',
            anchor='center',
            font=('arial 15'),
            padding=5
        ).grid(row=0, column=0, sticky=tk.E+tk.W)

        # Build input frame for Sudoku problem
        self.input_frame = SudokuFrame(self, 'input')
        self.input_frame.grid(column=0, row=1, sticky=tk.E+tk.W)
        self.input_variables = self.input_frame.variable_grid
        self.input_widgets = self.input_frame.widget_grid

        # Will be filled after input is finished
        self.output_frame = ttk.Frame()
        self.output_variables = list()
        self.output_widgets = list()

        # Build button frame and populate with start and quit
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=99, column=0, sticky="ew")
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        # Add status label
        self.status = tk.StringVar()
        self.status.set('Waiting for entry of sudoku problem ...')
        self.status_frame = ttk.LabelFrame(self, text='Status', padding=5)
        self.status_frame.grid(row=98, column=0, sticky='we')
        self.status_label = ttk.Label(
            self.status_frame,
            anchor='w',
            justify='left',
            textvariable=self.status
        )
        self.status_label.pack(anchor='w')

        self.quit_button = ttk.Button(
            self.button_frame,
            text='Quit',
            padding=5,
            command=self._on_quit
        )
        self.quit_button.pack(side='right')

        self.start_button = ttk.Button(
            self.button_frame,
            text='Start',
            padding=5,
            command=self._on_start
        )
        self.start_button.pack(side='right')

    def _on_start(self):
        # start greedy algorithm
        self.start_button.configure(default='disabled')
        self.event_generate('<<StartSolver>>')

    def _on_quit(self):
        self.master.destroy()

    def prepare_greedy(self):
        """Replace input frame with output frame, that visualizes solver results"""
        self.status.set('Starting greedy solver ...')
        self.input_frame.grid_forget()

        # Build output frame for Sudoku solution
        self.output_frame = SudokuFrame(self, 'output')
        self.output_variables = self.output_frame.variable_grid
        self.output_widgets = self.output_frame.widget_grid

        # Prefill output variables with input values and color respective widgets
        for i in range(9):
            for j in range(9):
                input_value = self.input_variables[i][j].get()
                if input_value:
                    self.output_variables[i][j].set(input_value)
                    self.output_widgets[i][j].configure(background='black', foreground='white')

        self.output_frame.grid(column=0, row=2, sticky=tk.E + tk.W)

    def update_output_variables(self, data):
        for i in range(9):
            for j in range(9):
                if self.output_variables[i][j].get() == '' and data[i][j] > 0:
                    self.output_variables[i][j].set(data[i][j])
                    self.output_widgets[i][j].configure(background='green', foreground='white')


class SudokuFrame(ttk.LabelFrame):
    """Label frame that either takes in input or displays solution"""
    def __init__(self, parent, kind, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.kind = kind
        self.widget_grid, self.variable_grid = self.build_sudoku_sub_frame()
        self.set_label_name()
        self.columnconfigure(0, weight=0)
        self.rowconfigure(0, weight=0)

    def build_sudoku_sub_frame(self):
        sub_frame = SudokuSubFrame(self, self.kind)
        sub_frame.grid(column=0, row=0, sticky='nsew')

        return sub_frame.get_widget_grid(), sub_frame.get_variable_grid()

    def set_label_name(self):
        my_label = 'Sudoku Problem' if self.kind == 'input' else 'Sudoku Solution'
        self.configure(text=my_label)


class SudokuSubFrame(ttk.Frame):
    """A frame that constructs a 9x9 grid with input or label widgets"""
    def __init__(self, parent, kind, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.kind = kind
        self.variable_grid = d.var_array()
        self.super_frame = self.build_super_frame()
        self.widget_grid = self.build_sudoku()

    def build_sudoku(self):
        """Based on kind constructs a 9x9 list with respective input type vars or widget"""

        if self.kind == 'input':
            wdg_type = ttk.Entry
        else:
            wdg_type = ttk.Label

        wdg_grid = list()
        for i in range(9):
            wdg_row = list()
            for j in range(9):
                # calculate address of super-frame
                super_col = j // 3
                super_row = i // 3
                sub_col = j % 3
                sub_row = i % 3

                # generate widget and var grids
                wdg = wdg_type(
                    self.super_frame[super_row][super_col],
                    textvariable=self.variable_grid[i][j],
                    width=3,
                    font=('consolas 30'),
                    justify='center'
                )
                if wdg_type == ttk.Label:
                    wdg.configure(anchor='center', borderwidth=2, relief='groove')
                wdg.grid(row=sub_row, column=sub_col)
                wdg_row.append(wdg)
            wdg_grid.append(wdg_row)
        return wdg_grid

    def build_super_frame(self):
        """Builds an array of 3x3 super-frames representing sudoku sub-arrays that are visibly separated"""
        sup_frames = list()
        for row in range(3):
            sup_row = list()
            for col in range(3):
                sup_frame = ttk.Frame(self, padding=5)
                sup_frame.grid(row=row, column=col)
                sup_row.append(sup_frame)
            sup_frames.append(sup_row)

        return sup_frames

    def get_variable_grid(self):
        return self.variable_grid

    def get_widget_grid(self):
        return self.widget_grid

    def get_super_frames(self):
        return self.super_frame
