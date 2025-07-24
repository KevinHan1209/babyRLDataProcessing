import pandas as pd
import numpy as np
from initial_obj_states import INITIAL_STATES
from state_distribution import get_state_distribution
import matplotlib.pyplot as plt
import pickle
import numpy as np

# Updated data labeling
df = pd.read_csv('DevEvObject_2025-07-17.csv')
df = df.fillna(np.nan)
unique_sessions = df['ID_subjsess'].unique()
for i, session in enumerate(unique_sessions, start=1):
    globals()[f'agent{i}'] = df[df['ID_subjsess'] == session]

for i in range(1, len(unique_sessions) + 1):
    original_obj_states = INITIAL_STATES.copy()
    post_processed_obj_states = get_state_distribution(globals()[f'agent{i}'], original_obj_states)
    # Convert open states to popup states for farm toy
    if 'f' in post_processed_obj_states and 'open' in post_processed_obj_states['f']:
        open_states = post_processed_obj_states['f']['open']
        post_processed_obj_states['f']['popup'].extend(open_states)
        post_processed_obj_states['f'].pop('open')
    # Save post processed states to file in states folder
    with open(f'states/agent{i}_states.pkl', 'wb') as f:
        pickle.dump(post_processed_obj_states, f)

# Load all agent states
all_agent_states = []
for i in range(1, len(unique_sessions) + 1):
    with open(f'states/agent{i}_states.pkl', 'rb') as f:
        all_agent_states.append(pickle.load(f))

# Find the maximum timepoint across all states and objects
max_time = 0
for agent_states in all_agent_states:
    for obj_states in agent_states.values():
        for state_type, values in obj_states.items():
            if values:  # Check if there are any values
                for value in values:
                    if isinstance(value[1], (int, float)):  # Check if time value is numeric
                        max_time = max(max_time, value[1])

# Initialize dictionary to store averaged distributions
averaged_distributions = {}

# For each object and state in the first agent's data
for obj, states in all_agent_states[0].items():
    averaged_distributions[obj] = {}
    for state_name in states:
        all_agent_percentages = {'true': [], 'false': []}
        
        # Calculate percentages for each agent
        for agent_states in all_agent_states:
            state_changes = agent_states[obj][state_name]
            if not state_changes:
                continue
                
            # Use the max_time as total session duration
            total_time = max_time
            initial_state = state_changes[0][0]  # Get the initial state
            time_in_state = {'true': 0, 'false': 0}
            last_timestamp = 0
            
            # Handle case with only one state change
            if len(state_changes) == 1:
                state_val, timestamp = state_changes[0]
                if state_val:
                    time_in_state['true'] = total_time
                else:
                    time_in_state['false'] = total_time
            else:
                # Calculate time spent in each state
                for state_val, timestamp in state_changes:
                    # Add time to previous state
                    duration = timestamp - last_timestamp
                    if state_val:
                        time_in_state['true'] += duration
                    else:
                        time_in_state['false'] += duration
                        
                    last_timestamp = timestamp
                
                # Add time from last state change to end
                if state_changes[-1][0]:  # If last state was True
                    time_in_state['true'] += (total_time - last_timestamp)
                else:  # If last state was False
                    time_in_state['false'] += (total_time - last_timestamp)
            
            # Calculate percentages
            if total_time > 0:
                true_percentage = (time_in_state['true'] / total_time) * 100
                false_percentage = (time_in_state['false'] / total_time) * 100
                
                all_agent_percentages['true'].append(true_percentage)
                all_agent_percentages['false'].append(false_percentage)
        
        # Calculate average percentages across agents
        avg_true = np.mean(all_agent_percentages['true']) if all_agent_percentages['true'] else 0
        avg_false = np.mean(all_agent_percentages['false']) if all_agent_percentages['false'] else 0
        
        averaged_distributions[obj][state_name] = {
            'true_percentage': avg_true,
            'false_percentage': avg_false
        }

# Save averaged distributions
with open('states/averaged_state_distributions.pkl', 'wb') as f:
    pickle.dump(averaged_distributions, f)
    print("\nAveraged State Distributions:")
    for obj in averaged_distributions:
        print(f"\n{obj}:")
        for state, percentages in averaged_distributions[obj].items():
            print(f"  {state}:")
            print(f"    True: {percentages['true_percentage']:.2f}%")
            print(f"    False: {percentages['false_percentage']:.2f}%")

