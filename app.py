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

if 'phase' not in st.session_state:
    st.session_state['phase'] = 'start'

if 'solved' not in st.session_state:
    st.session_state['solved'] = 'not_solved'

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

def run_ga_solver(solution_data, possibilities_data):
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
    with st.spinner('Running genetic algorithm ...'):
        ga_problem = ga.GASolver(
            solution_data,
            possibilities_data,
            # status_callback=st.write,
            # final_callback=self.final_result
        )
        ga_problem.ga_solve()
        solution, solved = ga_problem.get_solution()
        logbook = ga_problem.get_stats()

    return solution, solved, logbook

def hide_zero(styled, props=''):
    return np.where(styled == 0, props, '')

def mark_input(styled, props=''):
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
    checkers = checkers.mask(initial, props)
    return checkers

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

# short-cut for development phase only, remove before deployment
def prep_input(data):
    df = pd.DataFrame(data, index=range(1, 10), columns=range(1, 10))
    df = df.astype(str)
    df = df.mask(df=='0', '')
    return df


# run script for start phase
if st.session_state['phase'] == 'start':
    st.title('Welcome to a different kind of Sudoku Solver!')
    st.subheader('Hello Data Science Enthusiast :wave:')
    st.markdown(
        """
        **Genetic Algorithms** are a powerful weapon in an optimizer's armory. But can they cope
        with a structured (and hard) problem like a **Sudoku Puzzle**? :thinking_face:  
        
        **Yes they can**! :thumbsup: and you can try this for yourself whith this app!     
        
        We will take you through a solving process allowing you to play whith the Genetic Algorithm part. 
        You will start by entering your own Sudoku problem or selecting
        from a small range of examples.
        
        Next a greedy alogorithm will narrow down the potential candidate numbers 
        for each cell. This is essential, as the sheer number of solution candidates overwhelms
        a simple genetic algorithm approach.  
        
        Now you will able to adjust parameters for a genetic algorithm and see how this impacts
        its performance.  
        
        Finally you will be able to inspect the results of your algorithm
        and either rerun it with different parameters or start out with a new problem.  

        And now withouth further ado ...
        """
    )
    start = st.button("Let's get started :rocket:", type='primary')
    if start:
        set_phase('input')
        st.rerun()


# run script for start phase
if st.session_state['phase'] == 'input':
    st.title('Sudoku Solver')
    st.markdown('Enter your Sudoku problem and press start!')
    preselect = st.sidebar.selectbox('Start with an example', options=['Hard', 'Easy', 'None'])
    with st.form('sudoku_input'):
        if preselect == 'None':
            data = pd.DataFrame({i:['']*9 for i in range(1,10)}, index=range(1, 10))
        elif preselect == 'Easy':
            data = prep_input(SOLVABLE)
        elif preselect == 'Hard':
            data = prep_input(NOT_SOLVABLE)
        input = st.data_editor(data=data, num_rows='fixed', key='data_editor')
        submitted = st.form_submit_button(label='Start :rocket:', type='primary')
        # TODO: add validity check here
        if submitted:
            input = input.mask(input=='', 0).astype(int)
            st.session_state['input'] = input
            set_phase('start_solve')
            st.rerun()

# run script for greedy phase
elif st.session_state['phase'] == 'start_solve':
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
        set_phase('final')
        st.rerun()

# run script for ga phase
elif st.session_state['phase'] == 'configure_ga':
    with st.form('Select options for genetic algorithm'):
        generations = st.slider(
            'Number of Generations', 
            min_value=50,
            max_value=1000,
            value=500,
            step=50
            )
        population = st.slider(
            'Population Size', 
            min_value=50,
            max_value=1000,
            value=500,
            step=50
            )
        hof = st.slider(
            'Hall of Fame Size', 
            min_value=0,
            max_value=100,
            value=50,
            step=1
        )
        p_crossover = st.slider(
            'Probability of Mating',
            min_value=0.1,
            max_value=1.0,
            step=0.05,
            value=0.9
        )
        p_crossover = st.slider(
            'Probability of Mutation',
            min_value=0.0,
            max_value=1.0,
            step=0.05,
            value=0.2
        )
        run_ga = st.form_submit_button(label='Run Algorithm')
        if run_ga:
            set_phase('start_ga')
            st.rerun()

elif st.session_state['phase'] == 'start_ga':        
    ga_solution, solved, logbook = run_ga_solver(st.session_state['solution'], st.session_state['possibilities'])
    st.session_state['solved'] = 'ga'
    st.session_state['ga_logbook'] = logbook

    if solved:
        st.session_state['ga_solution'] = ga_solution
        st.session_state['solution'] = ga_solution

    set_phase('final')
    st.rerun()

# present final result 
elif st.session_state['phase'] == 'final': 

    tab_list = ['Final Result', 'Greedy Algorithm']
    if st.session_state.solved == 'ga':
        tab_list.append('Genetic Algorithm')

    tabs = st.tabs(tab_list)

    with tabs[0]:
        st.markdown('These fields could be solved by the algorithm:')
        styled = pd.DataFrame(st.session_state.solution, columns=range(1, 10), index=list(range(1, 10))).style.apply(mark_input, axis=None, props='background-color:#a3a8b4; color:white')
        st.markdown(styled.hide(axis = 0).hide(axis = 1).to_html(), unsafe_allow_html=True)
    with tabs[1]:
        st.markdown('Valid values could be reduced to these options:')
        st.dataframe(st.session_state.possibilities)

    if st.session_state.solved == 'ga':
        with tabs[2]:
            # plot statistics:
            min_fitness_values, mean_fitness_values = st.session_state.ga_logbook.select("min", "avg")
            fit_df = pd.DataFrame(
                {
                    'Min Fitness': min_fitness_values,
                    'Avg. Fitness': mean_fitness_values,
                    'Generation': list(range(1, len(mean_fitness_values) + 1))
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
    
    # for key in st.session_state.keys():
    #     del st.session_state[key]