import pandas as pd
from collections import defaultdict

df = pd.read_csv('DevEvObject_2025-07-17.csv')

# Track which states are used by which objects
object_states = defaultdict(set)
object_actions = defaultdict(set)

# Check all rows
for idx, row in df.iterrows():
    for i in range(1, 4):
        obj = row[f'object{i}_clean_obj']
        if pd.isna(obj) or obj in ['dn', 'bc']:
            continue
            
        # Check states
        state_types = ['mouth', 'noise', 'detach', 'reattach', 'takeout', 'putin', 'popup',
                      'hidden', 'open', 'close']
        
        # Check point states
        for state in state_types:
            if row[f'object{i}_action_state_clean_point_{state}'] == 'y':
                object_states[obj].add(state)
                
        # Check dur states  
        for state in state_types:
            if row[f'object{i}_action_state_clean_dur_{state}'] == 'y':
                object_states[obj].add(state)
                
        # Check actions
        dur_action = row[f'object{i}_action_state_clean_dur_action']
        point_action = row[f'object{i}_action_state_clean_point_action']
        
        if pd.notna(dur_action):
            object_actions[obj].add(dur_action)
        if pd.notna(point_action):
            object_actions[obj].add(point_action)

# Print findings
print("Objects and their states/actions in the data:")
print("=" * 60)

for obj in sorted(object_states.keys()):
    print(f"\n{obj}:")
    print(f"  States: {sorted(object_states[obj])}")
    print(f"  Actions: {sorted(object_actions[obj])}")