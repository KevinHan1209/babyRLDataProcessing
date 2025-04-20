import pandas as pd
import numpy as np
from initial_obj_states import INITIAL_STATES
from state_distribution import get_state_distribution
import matplotlib.pyplot as plt
import pickle
import numpy as np

# Updated data labeling
df = pd.read_csv('DevEvObject_2025-01-23.csv')
df = df.fillna(np.nan)
unique_sessions = df['ID_subjsess'].unique()
for i, session in enumerate(unique_sessions, start=1):
    globals()[f'agent{i}'] = df[df['ID_subjsess'] == session]

for i in range(1, len(unique_sessions) + 1):
    original_obj_states = INITIAL_STATES.copy()
    post_processed_obj_states = get_state_distribution(globals()[f'agent{i}'], original_obj_states)
    # Save post processed states to file in states folder
    with open(f'states/agent{i}_states.pkl', 'wb') as f:
        pickle.dump(post_processed_obj_states, f)