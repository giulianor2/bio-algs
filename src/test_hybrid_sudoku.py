import unittest
import controll
import data_model
import user_interface
import tkinter
import greedy_sudoku


class TestFrontend(unittest.TestCase):

    def test_grid_hook(self):
        app = tkinter.Tk()
        sub_frame = user_interface.SudokuSubFrame(app, 'input')
        var_grid = sub_frame.get_variable_grid()
        wdg_grid = sub_frame.get_widget_grid()

        self.assertEqual(wdg_grid[2][8].cget('textvariable'), str(var_grid[2][8]))

    def test_start(self):
        app = controll.Application()
        app.root_frame.input_variables[0][0].set('5')
        app._on_start()

        with open('input_grid.pkl', 'rb') as input_file:
            saved_list = data_model.load_data(input_file)

        check_list = [
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.assertEqual(saved_list, check_list)

    def test_greedy_sudoku(self):
        SOLVABLE = [
            [0, 0, 0, 0, 1, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 6, 7, 4],
            [0, 4, 9, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 9, 0],
            [0, 0, 0, 0, 8, 7, 0, 0, 0],
            [6, 9, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 7, 0, 4, 0, 0, 0],
            [2, 0, 0, 6, 0, 0, 0, 0, 1],
            [0, 5, 0, 0, 0, 0, 0, 4, 3]
        ]

        NOT_SOLVABLE = [
            [0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 0, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 0],
            [4, 0, 0, 8, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 0, 0, 0, 7, 0]
        ]

        SOLVABLE_SOLUTION = [
            [7, 6, 5, 4, 1, 3, 9, 2, 8],
            [3, 1, 2, 8, 9, 5, 6, 7, 4],
            [8, 4, 9, 2, 7, 6, 1, 3, 5],
            [4, 8, 7, 3, 6, 1, 5, 9, 2],
            [5, 2, 3, 9, 8, 7, 4, 1, 6],
            [6, 9, 1, 5, 4, 2, 3, 8, 7],
            [1, 3, 8, 7, 5, 4, 2, 6, 9],
            [2, 7, 4, 6, 3, 9, 8, 5, 1],
            [9, 5, 6, 1, 2, 8, 7, 4, 3]
        ]

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

        SOLVABLE_POSSIBILITIES = [
            [{7}, {6}, {5}, {4}, {1}, {3}, {9}, {2}, {8}],
            [{3}, {1}, {2}, {8}, {9}, {5}, {6}, {7}, {4}],
            [{8}, {4}, {9}, {2}, {7}, {6}, {1}, {3}, {5}],
            [{4}, {8}, {7}, {3}, {6}, {1}, {5}, {9}, {2}],
            [{5}, {2}, {3}, {9}, {8}, {7}, {4}, {1}, {6}],
            [{6}, {9}, {1}, {5}, {4}, {2}, {3}, {8}, {7}],
            [{1}, {3}, {8}, {7}, {5}, {4}, {2}, {6}, {9}],
            [{2}, {7}, {4}, {6}, {3}, {9}, {8}, {5}, {1}],
            [{9}, {5}, {6}, {1}, {2}, {8}, {7}, {4}, {3}]
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

        solvable = greedy_sudoku.GreedySolver(SOLVABLE)
        solvable.solve_sudoku()
        self.assertEqual(solvable.get_solution(), SOLVABLE_SOLUTION)
        self.assertEqual(solvable.get_possibilities(), SOLVABLE_POSSIBILITIES)

        not_solvable = greedy_sudoku.GreedySolver(NOT_SOLVABLE)
        not_solvable.solve_sudoku()
        self.assertEqual(not_solvable.get_solution(), NOT_SOLVABLE_SOLUTION)
        self.assertEqual(not_solvable.get_possibilities(), NOT_SOLVABLE_POSSIBILITIES)
