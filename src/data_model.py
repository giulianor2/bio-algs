# Bit overdone for a simple pickle operation, could be used for more complex operations later
import pickle
import tkinter


def var_array():
    """Constructs a 9x9 list with string vars"""
    var_grid = list()
    for i in range(9):
        var_row = list()
        for j in range(9):
            var = tkinter.StringVar()
            var_row.append(var)
        var_grid.append(var_row)
    return var_grid


def save_data(data, file):
    pickle.dump(data, file)


def load_data(file):
    data = pickle.load(file)
    return data
