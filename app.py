import streamlit as st
import pandas as pd
import numpy as np
import src.greedy_sudoku as gs
import src.ga_solver as ga
import time
import altair as alt

# if 'count' not in st.session_state:
#     st.session_state['count'] = 0

# st.session_state['count'] += 1

# st.subheader(f'Session count: {st.session_state.count}')

# CONSTANTS

SUDOKU1 = [
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

SUDOKU2 = [
            [0, 0, 7, 0, 2, 0, 0, 0, 6],
            [5, 0, 0, 0, 3, 0, 0, 0, 0],
            [0, 0, 9, 5, 0, 6, 1, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 3],
            [9, 0, 0, 4, 0, 7, 0, 8, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 6, 0, 9, 0, 0, 7],
            [0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 7, 0, 0, 0, 0, 3, 0, 0]
        ]

SUDOKU3 = [
            [9, 0, 2, 0, 0, 0, 1, 0, 0],
            [0, 4, 0, 2, 0, 7, 0, 3, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0],
            [0, 8, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 1, 5, 0, 8, 3, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 5, 0],
            [0, 0, 4, 0, 0, 0, 0, 0, 7],
            [0, 7, 0, 8, 0, 3, 0, 2, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0]
        ]

FAIL = [
            [9, 2, 2, 0, 0, 0, 1, 0, 0],
            [0, 4, 0, 2, 0, 7, 0, 3, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0],
            [0, 8, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 1, 5, 0, 8, 3, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 5, 0],
            [0, 0, 4, 0, 0, 0, 0, 0, 7],
            [0, 7, 0, 8, 0, 3, 0, 2, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0]
        ]

# FUNCTIONS

def set_phase(phase):
    """
    Sets phase of solution process based on input.

    Args:
        phase (string): name of phase
    """
    st.session_state.phase = phase

def run_greedy(data):
    """
    Starts greedy algorithm based on user input. 
    Returns solved fields as well as valid field options.
    If the sudoku puzzle could not be solved outright, the latter
    serve as input for a Genetic Algorithm approach.

    Args:
        data (array): 9x9 array (pd.DataFrame, np.array, list of lists)
            containing the user input (i.e. pre-defined fields).

    Returns:
        tuple ( tuple( array, boolean ), array ): Tuple containing 
            - a tuple of solution as a 9x9 array with solved fields plus True or False,
            indicating whether the puzzle has been solved.
            - a 9x9 array with valid field options as lists
    """
    with st.spinner('Running greedy algorithm ...'):
        time.sleep(1)
        greedy_problem = gs.GreedySolver(data)
        greedy_problem.solve_sudoku()

    return greedy_problem.get_solution(), greedy_problem.get_possibilities()

def run_ga_solver(solution_data, possibilities_data, ga_params):
    """
    Starts Genetic Algorithm based on solution and possibilities returned
    by greedy algorithm. Returns solved fields (if solvable) and 
    information on whether a solution has been found.

    Args:
        solution_data (array): 9x9 array of solved fields
        possibilities_data (array): 9x9 array of lists with valid field options

    Returns:
        tuple(array, boolean, deap.tools.Logbook): 
            - 9x9 array with solved fields 
            - boolean variable indicating whether problems was solved 
            - logbook containing statistics on genetic algorithm run
    """
    ga_problem = ga.GASolver(
        solution_data,
        possibilities_data,
        status_callback=st.write,
        **ga_params,
        # final_callback=self.final_result
    )
    ga_problem.ga_solve()
    solution, solved = ga_problem.get_solution()
    logbook = ga_problem.get_stats()

    return solution, solved, logbook

def prettify_grid(styled):
    """Builds and returns a dataframe with CSS format strings to style final sudoku grid.

    Args:
        styled (any): Not used in function, though delivered by caller

    Returns:
        pd.DataFrame: dataframe with CSS format strings to be used for sudoku grid
    """
    checkers = list()
    for i in range(9):
        if i // 3 % 2 == 0:
            first = 'background-color:#f0f2f6; color:black'
            second = 'background-color:white; color:black'
        else:
            first = 'background-color:white; color:black'
            second = 'background-color:#f0f2f6; color:black'
        check_line = [first if j // 3 % 2 == 0 else second for j in range(9)]
        checkers.append(check_line)
    checkers = pd.DataFrame(checkers, columns=range(1, 10), index=range(1, 10))
    initial = (st.session_state.input > 0).to_numpy()
    checkers = checkers.mask(initial, 'background-color:#a3a8b4; color:white')
    return checkers

def prep_input(data):
    """
    Takes in 9x9 array and returns dataframe for solution process.
    Used to format examples for input form.

    Args:
        data (array): 9x9 array of integers between 0 and 9.

    Returns:
        pd.DataFrame: 9x9 dataframe with strings of integers between 1 and 9 plus empty strings.
    """
    df = pd.DataFrame(data, index=range(1, 10), columns=range(1, 10))
    df = df.astype(str)
    df = df.mask(df=='0', '')
    return df

def run_start():
    """
    Runs script for start phase.
    """
    st.title('Welcome to a different kind of Sudoku Solver!')
    st.subheader('Hello Data Science Enthusiast :wave:')
    st.markdown(
        """
        **Genetic Algorithms** are a powerful weapon in an optimizer's armory. But can they cope
        with a structured (and hard) problem like a **Sudoku Puzzle**? :thinking_face:  
        
        **Well, let's find out!** :wink:     
        
        You will start by entering your own Sudoku problem or selecting
        from a small range of examples.
        
        In a first step a greedy alogorithm will narrow down the potential candidate numbers 
        for each cell. This makes the problem manageable for the GA part.  
        
        Next you can set parameters for a genetic algorithm to steer its performance.  
        
        Finally you will be able to inspect the results of your algorithm
        and either rerun it with different parameters or start out with a new problem.  

        And now withouth further ado ...
        """
    )
    start = st.button("Let's get started :rocket:", type='primary')
    if start:
        set_phase('input')
        st.rerun()

def run_input():
    """
    Runs script for input phase.
    """
    st.title('Sudoku Solver')
    st.markdown('Enter your Sudoku problem and press start!')
    preselect = st.sidebar.selectbox('Start with an example', options=['None', 'Example 1', 'Example 2', 'Example 3', 'FAIL'])
    with st.form('sudoku_input'):
        if preselect == 'None':
            data = pd.DataFrame({i:['']*9 for i in range(1,10)}, index=range(1, 10))
        elif preselect == 'Example 1':
            data = prep_input(SUDOKU1)
        elif preselect == 'Example 2':
            data = prep_input(SUDOKU2)
        elif preselect == 'Example 3':
            data = prep_input(SUDOKU3)
        # elif preselect == 'FAIL':
        #     data = prep_input(FAIL)
        input = st.data_editor(data=data, num_rows='fixed', key='data_editor')
        submitted = st.form_submit_button(label='Start :runner:', type='primary')
        # TODO: add validity check here
        if submitted:
            input = input.mask(input=='', 0).astype(int)
            st.session_state['input'] = input
            set_phase('start_solve')
            st.rerun()

def run_start_solve():
    """
    Runs script for greed solution phase.
    """
    st.title('Sudoku Solver')
    greedy_solved, greedy_possibilities = run_greedy(st.session_state.input)
    greedy_solution, solved = greedy_solved
    st.session_state['greedy_solution'] = greedy_solution
    st.session_state['solution'] = greedy_solution
    st.session_state['possibilities'] = greedy_possibilities
    
    if not solved:
        set_phase('configure_ga')
        st.rerun()
    else:
        st.session_state['solved'] = 'greedy'
        set_phase('start_ga')
        st.rerun()

def run_configure_ga():
    """
    Runs script for genetic algorithm configuration phase.    
    """
    st.title('Sudoku Solver')
    st.markdown('The greedy algorithm has reduced the solution possibilities per field to these options:')
    st.dataframe(st.session_state.possibilities)
    st.subheader('Adjust parameters for the Genetic Algorithm!')

    with st.form('ga_options_select', border=False):
        st.session_state['ga_params'] = {
            'generations': 500,
            'population': 1000,
            'hof_size': 50,
            'p_mating': 0.9,
            'p_mutation': 0.2,
            'shock_event': 'Radiation Leak',
            'stuck_count': 50
        }        
        generations = st.slider(
            'Number of Generations', 
            min_value=50,
            max_value=1000,
            value=st.session_state['ga_params']['generations'],
            step=50
            )
        st.write(
            'The number of generations sets the maximum number of rounds the algorithm will run. '
            'Set this conservatively to avoid overly long run times.'
            )        
        population = st.slider(
            'Population Size', 
            min_value=50,
            max_value=1000,
            value=st.session_state['ga_params']['population'],
            step=50
            )
        st.write(
            'The population size determines how many solution candidates exist in paralllel. '
            'Higher values increase the probability of finding a solution earlier - '
            'while increasing computational cost.'
            )
        hof_size = st.slider(
            'Hall of Fame Size', 
            min_value=0,
            max_value=100,
            value=st.session_state['ga_params']['hof_size'],
            step=1
        )
        st.write(
            'The hall of fame size determines how many of the fittest individuals are carried over '
            'into the next generation unaltered. Helps to preserve progress, '
            'while increasing the risk of getting stuck in local optima. '
            )
        p_mating = st.slider(
            'Probability of Mating',
            min_value=0.1,
            max_value=1.0,
            value=st.session_state['ga_params']['p_mating'],
            step=0.05
        )
        st.write(
            'The probability of mating determines how often the fittest "parent" individuals are combined '
            'to generate "offspring" individuals in the next generation.'
            )
        p_mutation = st.slider(
            'Probability of Mutation',
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['ga_params']['p_mutation'],
            step=0.05
        )
        st.write(
            'The probability of mutation determines how likely individuals are altered in a generation. '
            'While this drives the evolutionary process, high mutation rates can also interfere '
            'whith the continuous optimization process. Adjust sparingly!'
            )
        shock_event = st.radio('Shock Event', ['None', 'Radiation Leak', 'Comet Strike'], index=1)
        st.markdown(
                """
                To avoid getting caught in local minima you can chose one of two "shock" events.
                - **Radiation Leak** drastically increases mutation probability to 0.5 over a number of rounds determined by "Stuck Rounds".
                - **Comet Strike** wipes out all individuals apart from the hall of fame and generates a new random population.
                """
            )
        stuck_count = st.slider(
            'Stuck Rounds',
            min_value=10,
            max_value=100,
            value=st.session_state['ga_params']['stuck_count'],
            step=10
        )
        st.write(
            'Stuck rounds is the number of rounds the best fitness value must not improve before the shock event kicks in. '
            'Comparable to "early stopping rounds" in machine learning. No effect if shock event is "None".'
            )
        run_ga = st.form_submit_button(label='Run Algorithm :runner:', type='primary')
        if run_ga:
            st.session_state['ga_params'] = {
                'generations': generations,
                'population': population,
                'hof_size': hof_size,
                'p_mating': p_mating,
                'p_mutation': p_mutation,
                'shock_event': shock_event,
                'stuck_count': stuck_count
            }
            set_phase('start_ga')
            st.rerun()
    

def run_start_ga():
    """
    Runs final optimization phase.
    """
    if st.session_state['solved'] == 'greedy':
        st.title('Sudoku Problem Solved! :thumbsup:')
        st.subheader('That was too easy, please enter a harder problem!')
        success_message = 'This is your solution: :smiley:'
    else:
        st.title('Sudoku Solver')
        with st.status('Running genetic algorithm ...') as status:
            st.write('Starting algorithm')
            ga_solution, solved, logbook = run_ga_solver(
                st.session_state['solution'], 
                st.session_state['possibilities'],
                st.session_state['ga_params']
                )
            st.write('Finalized algorithm')
            status.update(label="Optimization complete!", state="complete")

        st.session_state['solved'] = 'ga'
        st.session_state['ga_logbook'] = logbook

        if solved:
            st.session_state['ga_solution'] = ga_solution
            st.session_state['solution'] = ga_solution
            success_message = 'This is your solution:'
        else:
            success_message = 'Problem could not be solved completely: :confounded:'
    
    tab_list = ['Final Result', 'Output Greedy Algorithm']
    if st.session_state['solved'] == 'ga':
        tab_list.append('Output Genetic Algorithm')
    tabs = st.tabs(tab_list)

    with tabs[0]:
        st.markdown(success_message)
        df_solution = pd.DataFrame(st.session_state.solution, columns=range(1, 10), index=list(range(1, 10)))
        df_solution = df_solution.mask(df_solution==0,'')
        styled = df_solution.style.apply(prettify_grid, axis=None)
        st.markdown(styled.hide(axis = 0).hide(axis = 1).to_html(), unsafe_allow_html=True)
        st.markdown('Dark grey fields represent your input.')
    with tabs[1]:
        st.markdown('The greedy algorithm has reduced the solution possibilities per field to these options:')
        st.dataframe(st.session_state.possibilities)

    if st.session_state.solved == 'ga':
        with tabs[2]:
            # plot statistics:
            min_fitness_values, mean_fitness_values = st.session_state.ga_logbook.select("min", "avg")
            fit_df = pd.DataFrame(
                {
                    'Min Fitness': min_fitness_values,
                    'Avg. Fitness': mean_fitness_values,
                    'Generation': list(range(len(mean_fitness_values)))
                }
            )
            fit_df = fit_df.melt(
                id_vars='Generation', 
                value_vars=['Min Fitness', 'Avg. Fitness'],
                value_name='Fitness',
                var_name='Type')

            chart = alt.Chart(
                fit_df, 
                title=alt.Title(
                    'Min and Average fitness over Generations',
                    align='center',
                    anchor='middle'
                    )
                ).mark_line().encode(
                x=alt.X('Generation:Q'),
                y=alt.Y('Fitness:Q'),
                color=alt.Color('Type')
            ).interactive()

            st.altair_chart(chart, use_container_width=True)

def run_phase(phase):
    """
    Takes in phase name and runs respective phase script.

    Args:
        phase (string): name of phase to be run.
    """
    phases = {
        'start': run_start,
        'input': run_input,
        'start_solve': run_start_solve,
        'configure_ga': run_configure_ga,
        'start_ga': run_start_ga
    }
    phases[phase]()

# Run App
if 'phase' not in st.session_state:
    st.session_state['phase'] = 'start'

if 'solved' not in st.session_state:
    st.session_state['solved'] = 'not_solved'

run_phase(st.session_state['phase'])

# else: 
#     st.title('Runtime Error')
    # for key in st.session_state.keys():
    #     del st.session_state[key]