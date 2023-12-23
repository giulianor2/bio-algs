import numpy as np
from itertools import product
from functools import reduce
import random


class SudokuProblem:
    """This class encapsulates the Sudoku Problem
    """

    def __init__(self, sudoku, possibilities):
        """
        :param sudoku: Array type of shape 9, 9 containing problem to solve. Empty cells are denoted as zero.
        """
        self.sudoku = np.array(sudoku)
        self.size = self.sudoku.shape[0]
        self.possibilities = possibilities
        self.possibility_map, self.possibility_range = self.build_map()

    def build_map(self):
        """
        Based on self.possibilities builds a 9 by x array, that contains all valid possibilities per row.
        :return: list of lists of valid rows
        """
        possibility_map = list()
        possibility_range = list()
        for row in self.possibilities:
            valid_rows = [list(x) for x in product(*row) if len(set(x)) == 9]
            possibility_map.append(valid_rows)
            possibility_range.append(len(valid_rows)-1)

        return possibility_map, possibility_range

    def map_solution(self, solution):
        """
        Takes an array of indices and maps the possibility map to the indices.
        Adds rows to an empty list and returns 9x9 sudoku array.
        :return: filled in solution as np.array.
        """
        mapped_solution = list()
        for i in range(self.size):
            # print(solution)
            sudoku_row = self.possibility_map[i][solution[i]]
            mapped_solution.append(sudoku_row)

        return np.array(mapped_solution)

    def get_position_violation_count(self, solution):
        """
        Calculates the number of violations in the given solution.
        Since the input contains unique indices of columns for each row, no row or column violations are possible,
        Only the diagonal violations need to be counted.
        :param solution: Solution array type of shape 9, 9 containing a full solution.
        :return: the calculated value
        """

        # fill empty sudoku cells with solution
        mapped_solution = self.map_solution(solution)

        # count violations
        violations = 0

        # vertical violations:
        for i in range(9):
            violations += 9 - len(np.unique(mapped_solution[:, i]))

        # # horizontal violations:
        # for i in range(9):
        #     violations += 9 - len(set(mapped_solution[i, :]))

        # sector violations:
        for i in range(0, 8, 3):
            for j in range(0, 8, 3):
                violations += 9 - len(np.unique(mapped_solution[i:i+3, j:j+3]))

        # if 2 <= violations <= 4:
        #     violations = 2

        return violations

    def plot_solution(self, solution):
        """
        Plots a zero-based sudoku solution in the final one-based format
        :param solution: a sudoku solution (zero-based) to be printed
        """

        # fill empty sudoku cells with solution
        mapped_solution = self.map_solution(solution)

        print(mapped_solution)

    def get_solution(self, solution):
        """
        Returns a zero-based sudoku solution in the final one-based format
        :param solution: a sudoku solution (zero-based) to be printed
        """

        # fill empty sudoku cells with solution
        mapped_solution = self.map_solution(solution)

        return mapped_solution.tolist()



# testing the class:
def main():
    NOT_SOLVABLE_SOLUTION = [
        [0, 3, 0, 0, 0, 0, 0, 1, 0],
        [6, 0, 0, 1, 9, 5, 3, 0, 8],
        [0, 0, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 6, 8, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 2, 0, 8, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 8, 0, 4, 1, 9, 6, 3, 5],
        [0, 0, 0, 0, 0, 0, 1, 7, 0]
    ]

    NOT_SOLVABLE_POSSIBILITIES = [
        [{9, 2, 5, 7}, {3}, {2, 4, 5, 7, 9}, {2, 6, 7}, {8, 4, 7},
         {2, 4, 6, 7, 8}, {9, 4, 5, 7}, {1}, {9, 2, 4, 7}],
        [{6}, {2, 4, 7}, {2, 4, 7}, {1}, {9}, {5}, {3}, {2, 4}, {8}],
        [{1, 2, 5, 7, 9}, {1, 2, 4, 5, 7, 9}, {8}, {2, 3, 7}, {3, 4, 7},
         {2, 3, 4, 7}, {9, 4, 5, 7}, {6}, {9, 2, 4, 7}],
        [{8}, {1, 2, 5, 7, 9}, {1, 2, 5, 7, 9}, {9, 5, 7}, {6}, {1, 4, 7}, {9, 4, 5, 7}, {9, 2, 4, 5}, {3}],
        [{4}, {9, 2, 5, 7}, {6}, {8}, {3, 5, 7}, {3, 7}, {9, 5, 7}, {9, 2, 5}, {1}],
        [{1, 3, 5, 7, 9}, {1, 5, 9, 7}, {1, 3, 5, 7, 9}, {9, 3, 5, 7}, {2}, {1, 3, 4, 7}, {8}, {9, 4, 5}, {6}],
        [{1, 3, 5, 7, 9}, {6}, {1, 3, 4, 5, 7, 9}, {3, 5, 7}, {3, 5, 7}, {3, 7}, {2}, {8}, {9, 4}],
        [{2, 7}, {8}, {2, 7}, {4}, {1}, {9}, {6}, {3}, {5}],
        [{9, 2, 3, 5}, {9, 2, 4, 5}, {2, 3, 4, 5, 9}, {2, 3, 5, 6}, {8, 3, 5}, {8, 2, 3, 6}, {1}, {7}, {9, 4}]
    ]

    sudoku_problem = SudokuProblem(NOT_SOLVABLE_SOLUTION, NOT_SOLVABLE_POSSIBILITIES)
    sudoku_map, sudoku_range = sudoku_problem.build_map()
    print(sudoku_range)
    print(reduce(lambda x, y: x*y, sudoku_range))
    print(sudoku_map[1])

    random.seed(42)
    solution = [random.randint(0, i) for i in sudoku_range]
    print(solution)
    print(sudoku_problem.get_solution(solution))

    # # create a problem instance:
    # new_sudoku = SudokuProblem(
    #     [
    #         [0, 3, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 1, 9, 5, 0, 0, 0],
    #         [0, 0, 8, 0, 0, 0, 0, 6, 0],
    #         [8, 0, 0, 0, 6, 0, 0, 0, 0],
    #         [4, 0, 0, 8, 0, 0, 0, 0, 1],
    #         [0, 0, 0, 0, 2, 0, 0, 0, 0],
    #         [0, 6, 0, 0, 0, 0, 2, 8, 0],
    #         [0, 0, 0, 4, 1, 9, 0, 0, 5],
    #         [0, 0, 0, 0, 0, 0, 0, 7, 0]
    #     ]
    # )
    #
    # optimal_solution = np.array(
    #     [
    #         [5, 3, 4, 6, 7, 8, 9, 1, 2],
    #         [6, 7, 2, 1, 9, 5, 3, 4, 8],
    #         [1, 9, 8, 3, 4, 2, 5, 6, 7],
    #         [8, 5, 9, 7, 6, 1, 4, 2, 3],
    #         [4, 2, 6, 8, 5, 3, 7, 9, 1],
    #         [7, 1, 3, 9, 2, 4, 8, 5, 6],
    #         [9, 6, 1, 5, 3, 7, 2, 8, 4],
    #         [2, 8, 7, 4, 1, 9, 6, 3, 5],
    #         [3, 4, 5, 2, 8, 6, 1, 7, 9]
    #     ]
    # )
    #
    # eight_violations = np.array(
    #     [
    #         [5, 3, 4, 6, 7, 8, 9, 1, 2],
    #         [6, 2, 7, 1, 9, 5, 3, 4, 8],
    #         [1, 9, 8, 3, 4, 2, 5, 6, 7],
    #         [8, 5, 9, 7, 6, 1, 4, 9, 3],
    #         [4, 2, 6, 8, 5, 3, 7, 2, 1],
    #         [7, 1, 3, 9, 2, 4, 8, 5, 6],
    #         [9, 6, 1, 5, 3, 7, 2, 8, 4],
    #         [2, 8, 7, 4, 1, 9, 6, 3, 5],
    #         [3, 4, 5, 2, 8, 1, 6, 7, 9]
    #     ]
    # )
    #
    # def make_solution(solution):
    #
    #     solution_map = list()
    #
    #     for i in range(new_sudoku.size):
    #         row_numbers = [el for el in solution[i] if el in new_sudoku.number_map[i]]
    #         row_indices = np.array([np.where(new_sudoku.number_map[i] == el) for el in row_numbers]).flatten()
    #         solution_map.append(row_indices)
    #
    #     return solution_map
    #
    # print(new_sudoku.build_map())
    # print(new_sudoku.size)
    # print(new_sudoku.number_map)
    #
    # optimal = make_solution(optimal_solution)
    # eight = make_solution(eight_violations)
    #
    # new_sudoku.plot_solution(optimal)
    # print('Optimal solution check: ', new_sudoku.get_position_violation_count(optimal))
    # new_sudoku.plot_solution(eight)
    # print('Eight violations solution check: ', new_sudoku.get_position_violation_count(eight))


if __name__ == "__main__":
    main()

