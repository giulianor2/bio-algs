import streamlit as st
import pandas as pd
import numpy as np
import src.greedy_sudoku as gs
import src.ga_solver as ga
from itertools import chain
import time


st.title('Sudoku Solver')

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
        tuple: Tuple containing 
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
        tuple(array, boolean): tuple of 9x9 array with solved fields and boolean variable
            indicating whether problems was solved.
    """
    with st.spinner('Running genetic algorithm ...'):
        ga_problem = ga.GASolver(
            solution_data,
            possibilities_data,
            # status_callback=self.update_status,
            # final_callback=self.final_result
        )
        ga_problem.ga_solve()
        solution, solved = ga_problem.get_solution()

    return solution, solved

def hide_zero(styled, props=''):
    return np.where(styled == 0, props, '')

def mark_input(styled, props=''):
    checkers = list()
    for i in range(9):
        if i // 3 % 2 == 0:
            first = 'background-color:#f0f2f6;'
            second = 'background-color:white;'
        else:
            first = 'background-color:white;'
            second = 'background-color:#f0f2f6;'
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
    st.markdown('Enter your Sudoku problem and press start!')
    preselect = st.selectbox('Chose example', options=['Easy', 'Hard', 'None'])
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
    greedy_solved, greedy_possibilities = run_greedy(st.session_state.input)
    greedy_solution, solved = greedy_solved
    st.session_state['greedy_solution'] = greedy_solution
    st.session_state['solution'] = greedy_solution
    st.session_state['possibilities'] = greedy_possibilities
    
    if not solved:
        set_phase('start_ga')
        st.rerun()
    else:
        st.session_state['solved'] = 'greedy'
        set_phase('final')
        st.rerun()

# run script for ga phase
elif st.session_state['phase'] == 'start_ga':
    ga_solution, solved = run_ga_solver(st.session_state['solution'], st.session_state['possibilities'])

    if solved:
        st.session_state['solved'] = 'ga'
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
        st.markdown('#### These fields could be solved by the algorithm:')
        styled = pd.DataFrame(st.session_state.solution, columns=range(1, 10), index=list(range(1, 10))).style.apply(mark_input, axis=None, props='background-color:#a3a8b4; color:white')
        st.markdown(styled.hide(axis = 0).hide(axis = 1).to_html(), unsafe_allow_html=True)
    with tabs[1]:
        st.markdown('#### Valid values could be reduced to these options:')
        st.dataframe(st.session_state.possibilities)

    if st.session_state.solved == 'ga':
        with tabs[2]:
            styled_ga = pd.DataFrame(st.session_state.solution, columns=range(1, 10), index=list(range(1, 10))).style.apply(mark_input, axis=None, props='background-color:#a3a8b4; color:white')
            st.markdown(styled_ga.hide(axis = 0).hide(axis = 1).to_html(), unsafe_allow_html=True)
    
    # for key in st.session_state.keys():
    #     del st.session_state[key]