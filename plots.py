import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

# Create plots directory if it doesn't exist
if not os.path.exists('plots'):
    os.makedirs('plots')

obj_name_mapping = {
    'a': 'alligator busy box',
    'b': 'broom',
    'bs': 'broom set', 
    'bu': 'bucket',
    'ca': 'cart',
    'cu': 'cube',
    'f': 'farm toy',
    'g': 'gear',
    'm': 'music toy',
    'p': 'piggie bank',
    'pb': 'pink beach ball',
    'r': 'rattle',
    'rb': 'red spiky ball',
    's': 'stroller',
    'sh': 'shape sorter',
    't': 'tree busy box',
    'c': 'winnie cabinet',
    'y': 'yellow donut ring'
}

# Go through each agent's state file
for agent_file in os.listdir('states'):
    if not agent_file.endswith('.pkl'):
        continue
        
    agent_num = agent_file.split('_')[0]
    
    # Skip averaged agent
    if agent_num == 'averaged':
        continue
    
    # Create agent directory if it doesn't exist
    agent_dir = os.path.join('plots', agent_num)
    if not os.path.exists(agent_dir):
        os.makedirs(agent_dir)
    
    # Load the agent's states
    with open(os.path.join('states', agent_file), 'rb') as f:
        new_obj_states = pickle.load(f)

    # Get unique state types across all objects
    state_types = set()
    for obj_states in new_obj_states.values():
        state_types.update(obj_states.keys())

    # Remove container-related states that don't have boolean values
    state_types = {st for st in state_types if st not in ['contains', 'inside']}

    # Find the maximum timepoint across all states and objects
    max_time = 0
    for obj_states in new_obj_states.values():
        for state_type, values in obj_states.items():
            if values:  # Check if there are any values
                for value in values:
                    if isinstance(value[1], (int, float)):  # Check if time value is numeric
                        max_time = max(max_time, value[1])

    # Create a plot for each state type
    for state_type in state_types:
        plt.figure(figsize=(12, 6))
        plt.title(f'{agent_num} Distribution of {state_type} state across objects')
        plt.xlabel('Time')
        plt.ylabel('Objects')
        
        # Plot each object's values for this state
        y_ticks = []
        y_pos = 0
        for obj, states in new_obj_states.items():
            if state_type in states:
                y_ticks.append(obj_name_mapping[obj])
                
                # Get state values and times
                values = states[state_type]
                current_state = False
                
                
                # Start with False state at time 0
                plt.hlines(y=y_pos, xmin=0, xmax=values[0][1], color='red', linewidth=2)
                
                for i in range(len(values)):
                    if isinstance(values[i][0], bool):  # Only plot boolean states
                        start_time = values[i][1]
                        # If this is True state, draw until next False or end
                        if values[i][0]:
                            end_time = values[i+1][1] if i+1 < len(values) and not values[i+1][0] else max_time
                            plt.hlines(y=y_pos, xmin=start_time, xmax=end_time, color='blue', linewidth=2)
                        # For False states, draw gray line until next state
                        else:
                            next_time = values[i+1][1] if i+1 < len(values) else max_time
                            plt.hlines(y=y_pos, xmin=start_time, xmax=next_time, color='red', linewidth=2)
                
                y_pos += 1
        
        plt.yticks(range(len(y_ticks)), y_ticks)
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.xlim(0, max_time)  # Set x-axis limit to max time
        
        # Save plot to agent's directory
        plt.savefig(os.path.join(agent_dir, f'{state_type}_distribution.png'))
        plt.close()

        # Create plots for averaged state distributions
        with open('states/averaged_state_distributions.pkl', 'rb') as f:
            averaged_distributions = pickle.load(f)

        # Create plots directory for averaged distributions if it doesn't exist
        averaged_dir = os.path.join('plots', 'averaged')
        os.makedirs(averaged_dir, exist_ok=True)

        # Create a plot for each state type showing averaged distributions
        plt.figure(figsize=(12, 6))
        plt.title(f'Average Distribution of {state_type} state across objects')
        plt.xlabel('Percentage of Time')
        plt.ylabel('Objects')

        y_ticks = []
        y_pos = 0
        
        for obj, states in averaged_distributions.items():
            if state_type in states:
                y_ticks.append(obj_name_mapping[obj])
                
                # Get percentages for true and false states
                true_pct = states[state_type]['true_percentage']
                false_pct = states[state_type]['false_percentage']
                
                # Plot stacked bars
                plt.barh(y_pos, false_pct, color='red', alpha=0.7)
                plt.barh(y_pos, true_pct, left=false_pct, color='blue', alpha=0.7)
                
                y_pos += 1

        plt.yticks(range(len(y_ticks)), y_ticks)
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.xlim(0, 100)  # Set x-axis limit to 100%

        # Add legend
        plt.legend(['False', 'True'])

        # Save averaged plot
        plt.savefig(os.path.join(averaged_dir, f'{state_type}_distribution.png'))
        plt.close()
