import streamlit as st
import pandas as pd
import numpy as np
# import greedy_sudoku as gs
import time

st.title('Sudoku Solver')

if 'phase' not in st.session_state:
    st.session_state['phase'] = 'start'

def set_phase(phase):
    st.session_state.phase = phase

def run_greedy(data):
    with st.spinner():
        time.sleep(3)

# run script for start phase
if st.session_state['phase'] == 'start':
    st.markdown('Enter your Sudoku problem and press start!')
    with st.form('sudoku_input'):
        data = pd.DataFrame({i:[0]*9 for i in range(1,10)}, index=range(1, 10))
        result = st.data_editor(data=data, num_rows='fixed')
        submitted = st.form_submit_button(label='Start :rocket:', type='primary')
        if submitted:
            st.session_state['solution'] = result
            set_phase('start_solve')
            st.rerun()
# run script for greedy phase
elif st.session_state['phase'] == 'start_solve':
    run_greedy(st.session_state.solution)
    st.markdown('Result of greedy algorithm')
    st.dataframe(data=st.session_state['solution'])