import pandas as pd
from collections import defaultdict
from initial_obj_states import INITIAL_STATES

df = pd.read_csv('DevEvObject_2025-07-17.csv')

# Track which states are used by which objects
object_states_needed = defaultdict(set)

# State mapping from CSV to initial states
csv_to_state_mapping = {
    'popup': 'popup',
    'hidden': 'popup',  # hidden sets popup to False
    'open': 'open',
    'close': 'open',    # close sets open to False
    'detach': 'attached',
    'reattach': 'attached',
    'mouth': 'mouthed',
    'noise': 'noise',
    'putin': 'inside',
    'takeout': 'inside'
}

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
                if state in csv_to_state_mapping:
                    object_states_needed[obj].add(csv_to_state_mapping[state])
                
        # Check dur states  
        for state in state_types:
            if row[f'object{i}_action_state_clean_dur_{state}'] == 'y':
                if state in csv_to_state_mapping:
                    object_states_needed[obj].add(csv_to_state_mapping[state])

# Print what's missing
print("Missing states in initial_obj_states.py:")
print("=" * 60)

for obj in sorted(object_states_needed.keys()):
    if obj not in INITIAL_STATES:
        print(f"\n{obj}: OBJECT NOT DEFINED IN INITIAL_STATES")
        continue
        
    missing_states = []
    for state in sorted(object_states_needed[obj]):
        if state not in INITIAL_STATES[obj]:
            missing_states.append(state)
    
    if missing_states:
        print(f"\n{obj}: missing {missing_states}")

# Also check for objects in data but not in INITIAL_STATES
print("\n\nObjects in data but not in INITIAL_STATES:")
for obj in sorted(object_states_needed.keys()):
    if obj not in INITIAL_STATES:
        print(f"  {obj}")