import tkinter as tk
import data_model as d
import user_interface as ui
import greedy_sudoku as gs
import ga_solver as ga


from itertools import chain


# TODO: start GA to search for final solution
# TODO: Refactor ga_solver as class
# TODO: Add callback / getter functions to return results to controll.py


class Application(tk.Tk):
    """This is the main application that takes in a problem and runs the solution algorithm"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Hybrid GA Sudoku Solver')
        self.root_frame = ui.BasicForm(self, padding=10)
        self.root_frame.grid(sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.root_frame.bind('<<StartSolver>>', self._on_start)
        self.greedy_solution = ''
        self.greedy_possibilities = ''

    def _on_start(self, *_):
        input_grid = list()
        for i in range(9):
            input_row = list()
            for j in range(9):
                value = self.root_frame.input_variables[i][j].get()
                if value:
                    input_row.append(int(value))
                else:
                    input_row.append(0)
            input_grid.append(input_row)

        with open('input_grid.pkl', 'wb') as input_file:
            d.save_data(input_grid, input_file)

        self.root_frame.prepare_greedy()
        # Try greedy solution of sudoku puzzle first
        self.greedy_solution, self.greedy_possibilities = self.greedy_solver()
        self.root_frame.update_output_variables(self.greedy_solution)

        if any(x == 0 for x in chain(*self.greedy_solution)):
            self.root_frame.status.set('Starting genetic algorithm search ...')
            with open('greedy_solution_grid.pkl', 'wb') as greedy_solution_file:
                d.save_data(self.greedy_solution, greedy_solution_file)
            with open('greedy_possibilities_grid.pkl', 'wb') as greedy_possibilities_file:
                d.save_data(self.greedy_possibilities, greedy_possibilities_file)
        else:
            self.root_frame.status.set('Found solution!')

        # Start genetic algorithm search for result
        # self.ga_solver()

    def update_status(self, new_status):
        self.root_frame.status.set(new_status)
        self.update()

    def final_result(self, solved, result=None):
        if solved:
            self.root_frame.update_output_variables(result)
            self.root_frame.status.set('Solution found!')
        else:
            self.root_frame.status.set('No solution found!')

    @staticmethod
    def greedy_solver():
        """Get greedy solution for input data"""
        with open('input_grid.pkl', 'rb') as input_file:
            input_data = d.load_data(input_file)
        greedy_problem = gs.GreedySolver(input_data)
        greedy_problem.solve_sudoku()

        return greedy_problem.get_solution(), greedy_problem.get_possibilities()

    def ga_solver(self):
        """Get ga solution for greedy solution data"""

        with open('greedy_solution_grid.pkl', 'rb') as greedy_solution_file:
            greedy_solution_data = d.load_data(greedy_solution_file)
        with open('greedy_possibilities_grid.pkl', 'rb') as greedy_possibilities_file:
            greedy_possibilities_data = d.load_data(greedy_possibilities_file)

        ga_problem = ga.GASolver(
            greedy_solution_data,
            greedy_possibilities_data,
            status_callback=self.update_status,
            final_callback=self.final_result
        )
        ga_problem.ga_solve()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
