from copy import deepcopy
import numpy as np
from itertools import chain


class GreedySolver:
    """
    Takes in a sudoku problem as a 9x9 array, where missing numbers are represented as zeroes.
    Returns a list of lists of the same format with missing numbers completed by greedy algorithm where possible.
    Does not but could return list of sets of possible solutions for non-solved fields.
    """

    def __init__(self, sudoku_problem):
        if isinstance(sudoku_problem, np.ndarray):
            self.problem = sudoku_problem
        else:
            self.problem = np.array(sudoku_problem)

        self.solution = self.problem.copy()
        # maximum number of possibilities for a given cell (1 to 9)
        self.full_range = set(range(1, 10))
        # actual possibilities at start, i.e. full range for all empty fields
        self.possibilities = self.get_initial_possibilities()

    def get_initial_possibilities(self):
        possibilities = list()
        for row in range(9):
            row_list = list()
            for col in range(9):
                if self.solution[row, col] > 0:
                    row_list.append({self.solution[row, col]})
                else:
                    row_list.append(set(range(1, 10)))
            possibilities.append(row_list)

        return possibilities

    def solve_sudoku(self):
        progress = True

        while progress:
            progress = False

            # Find solution from mutual exclusion of fixed fields
            for row in range(9):
                for col in range(9):
                    if self.solution[row, col] == 0:
                        square_row = row // 3
                        square_col = col // 3
                        possible_range = self.full_range - set(self.solution[row, :])
                        possible_range = possible_range - set(self.solution[:, col])
                        possible_range = possible_range - set(self.solution[
                                                              square_row * 3: square_row * 3 + 3,
                                                              square_col * 3: square_col * 3 + 3].flat)

                        if len(possible_range) < len(self.possibilities[row][col]):
                            progress = True

                        self.possibilities[row][col] = possible_range

                        if len(possible_range) == 1:
                            # non-destructively (i.e. not pop) get value from set of len 1
                            self.solution[row, col] = min(possible_range)

            # Find solution from mutual exclusion of solution possibilities
            for row in range(9):
                for col in range(9):
                    possible = self.possibilities[row][col]
                    if len(possible) > 1:
                        red_possibilities = deepcopy(self.possibilities)
                        red_possibilities[row][col] = set()

                        square_row = row // 3
                        square_col = col // 3

                        # this could be solved more elegantly, works perfectly though
                        overlap1 = possible - set(chain(*red_possibilities[row]))
                        overlap2 = possible - set(chain(*[el[col] for el in red_possibilities]))
                        overlap3 = possible - set(chain(*[el[i]
                                                          for el in
                                                          red_possibilities[square_row * 3: square_row * 3 + 3]
                                                          for i in range(square_col * 3, square_col * 3 + 3)]))

                        for overlap in [overlap1, overlap2, overlap3]:
                            if len(overlap) == 1:
                                self.possibilities[row][col] = overlap
                                self.solution[row, col] = min(overlap)
                                progress = True
                                break

    def get_solution(self):
        return self.solution.tolist()

    def get_possibilities(self):
        return self.possibilities
