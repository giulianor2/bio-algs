from deap import base
from deap import creator
from deap import tools
import random

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import elitism
import sudoku


class GASolver:
    """Defines and controls key parameters for genetic algorithm solution"""

    def __init__(self,
                 sudoku_grid,
                 sudoku_possibilities,
                 population_size=1000,
                 max_generations=500,
                 hall_of_fame_size=50,
                 p_crossover=0.9,
                 p_mutation=0.2,
                 random_seed=42,
                 status_callback=None,
                 final_callback=None
                 ):
        self.population_size = population_size
        self.max_generations = max_generations
        self.hall_of_fame_size = hall_of_fame_size
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation
        self.status_callback = status_callback
        self.final_callback = final_callback

        random.seed(random_seed)

        # create the desired sudoku problem
        self.n_sudoku = sudoku.SudokuProblem(sudoku_grid, sudoku_possibilities)

        self.toolbox = base.Toolbox()

        # define a single objective, minimizing fitness strategy:
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

        # create the Individual class based on list of lists:
        creator.create("Individual", list, typecode='i', fitness=creator.FitnessMin)

        # create an operator that generates randomly shuffled indices:
        self.toolbox.register("randomSudoku", self.random_sudoku)

        # create the individual creation operator to fill up an Individual instance with shuffled indices:
        self.toolbox.register("individualCreator", tools.initIterate, creator.Individual, self.toolbox.randomSudoku)

        # create the population creation operator to generate a list of individuals:
        self.toolbox.register("populationCreator", tools.initRepeat, list, self.toolbox.individualCreator)

        self.toolbox.register("evaluate", self.get_violations_count)

        self.toolbox.register("select", tools.selTournament, tournsize=2)
        self.toolbox.register("mate", tools.cxOnePoint)  # , indpb=1.0 / self.n_sudoku.size)
        self.toolbox.register("mutate", tools.mutUniformInt, low=0, up=self.n_sudoku.possibility_range,
                              indpb=1.0 / self.n_sudoku.size)

    # Genetic operators:
    # Create random sudoku with given fixed numbers as individuals for initial population
    def random_sudoku(self):
        new_sudoku = [random.randint(0, i) for i in self.n_sudoku.possibility_range]
        return new_sudoku

    # fitness calculation - get the number of row or square violations for a given option:
    def get_violations_count(self, individual):
        violations = self.n_sudoku.get_position_violation_count(individual)
        return violations,  # return a tuple

    @staticmethod
    def multiline_upmx(ind1, ind2, indpb):
        pairs = list(zip(ind1, ind2))
        for i in range(len(pairs)):
            ind_i1, ind_i2 = tools.cxUniformPartialyMatched(pairs[i][0], pairs[i][1], indpb)
            ind1[i] = ind_i1
            ind2[i] = ind_i2

        return ind1, ind2

    @staticmethod
    def swap_cx(ind1, ind2, indpb):
        for i in range(len(ind1)):
            if random.random() <= indpb:
                ind1[i], ind2[i] = ind2[i], ind1[i]

        return ind1, ind2

    @staticmethod
    def multiline_shuffle_ind(ind, indpb):
        for i in range(len(ind)):
            ind_i = tools.mutShuffleIndexes(ind[i], indpb)
            ind[i] = ind_i[0]

        return ind,

    @staticmethod
    def simple_swap_mutation(ind, indpb):
        for i in range(len(ind)):
            if random.random() <= indpb:
                id1, id2 = random.sample(range(len(ind[i])), 2)
                ind[i][id1], ind[i][id2] = ind[i][id2], ind[i][id1]

        return ind,

    # Precise definition of equality of two arrays for hall of fame algorithm
    @staticmethod
    def np_equal(a, b):
        return np.all(a == b)

    @staticmethod
    def print_solution_stream(stream):
        print(stream)

    # Genetic Algorithm flow:
    def ga_solve(self):
        # print(self.n_sudoku.possibility_range)
        # create initial population (generation 0):
        new_population = self.toolbox.populationCreator(n=self.population_size)

        # prepare the statistics object:
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", np.min)
        stats.register("avg", np.mean)

        # define the hall-of-fame object:
        hof = tools.HallOfFame(self.hall_of_fame_size, similar=self.np_equal)

        # perform the Genetic Algorithm flow with hof feature added:
        new_population, logbook = elitism.eaSimpleWithElitism(new_population, self.toolbox, cxpb=self.p_crossover,
                                                              mutpb=self.p_mutation, ngen=self.max_generations,
                                                              stats=stats, halloffame=hof,
                                                              status_callback=self.status_callback,
                                                              stuck=(50, 'chernobyl'))

        # new_population, logbook = algorithms.eaSimple(new_population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
        #                                                       ngen=MAX_GENERATIONS, stats=stats, halloffame=hof,
        #                                                       verbose=True)

        solution = self.n_sudoku.get_solution(hof.items[0])
        if hof.items[0].fitness.values[0] == 0:
            self.final_callback(True, solution)
        else:
            self.final_callback(False)


        # print hall of fame members info:
        print("- Best solutions are:")
        for i in range(self.hall_of_fame_size):
            print(i, ": ", hof.items[i].fitness.values[0], " -> ", hof.items[i])

        # plot statistics:
        min_fitness_values, mean_fitness_values = logbook.select("min", "avg")
        plt.figure(1)
        sns.set_style("whitegrid")
        plt.plot(min_fitness_values, color='red')
        plt.plot(mean_fitness_values, color='green')
        plt.xlabel('Generation')
        plt.ylabel('Min / Average Fitness')
        plt.title('Min and Average fitness over Generations')

        # plot best solution:
        sns.set_style("whitegrid", {'axes.grid' : False})
        self.n_sudoku.plot_solution(hof.items[0])

        # show both plots:
        plt.show()


if __name__=="__main__":
    SOLVABLE = [
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

    sudoku_problem = GASolver(NOT_SOLVABLE_SOLUTION, NOT_SOLVABLE_POSSIBILITIES)
    sudoku_problem.ga_solve()
