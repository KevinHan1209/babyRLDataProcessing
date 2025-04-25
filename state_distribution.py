import copy
import pandas as pd

def get_state_distribution(agent_df, original_obj_states):
    obj_states = copy.deepcopy(original_obj_states)
    time = 0
    containers = {
                    'bu': ['b', 'cu', 'p'],  # bucket can contain broom, cube, piggie bank
                    's': ['bu', 'cu', 'g', 'r'],  # stroller can contain bucket, cube, gear, rattle
                    'ca': ['b', 'cu', 'sh'],  # cart can contain broom, cube, shape sorter
                    'p': []  # piggie bank is a container but not in our two-object scenarios
                }
    
    # common states between dataframe and RL states
    state_mapping = {
        'noise': lambda obj, val: obj_states[obj][val].extend([[True, start_time], [False, end_time]]) if val in obj_states[obj] else print(f"KeyError: state {val} not found for object {obj}"),
        'popup': lambda obj, val: obj_states[obj]['popup'].append([True, start_time]),
        'open': lambda obj, val: obj_states[obj]['open'].append([True, start_time]),
        'close': lambda obj, val: obj_states[obj]['open'].append([False, start_time]),
        'detach': lambda obj, val: obj_states[obj]['attached'].append([False, start_time]), 
        'reattach': lambda obj, val: obj_states[obj]['attached'].append([True, start_time]),
        'mouth': lambda obj, val: obj_states[obj]['mouthed'].extend([[True, start_time], [False, end_time]]) if 'mouthed' in obj_states[obj] else print(f"KeyError: object {obj} does not have mouthed state"),
        'hidden': lambda obj, val: obj_states[obj]['popup'].append([False, start_time]),
    }

    action_mapping = {
        'm': ('mouthed', True),
        'k': ('kicked', True),
        'si': ('climbed', True), 
        'th': ('thrown', True),
        'pu': ('pullshed', True),
        't': ('toggled', True)
    }
    
    for index, row in agent_df.iterrows():
        start_time, end_time = row['onset'], row['offset']
        time += end_time - start_time
        
        # Get all objects first
        objects = []
        for i in range(1,4):
            obj = row[f'object{i}_clean_obj']
            if pd.isna(obj) or obj in ['dn', 'bc']:
                continue
            objects.append(obj)
        
        # Process each object's actions and states
        for i in range(1,4):
            obj = row[f'object{i}_clean_obj']
            if pd.isna(obj) or obj in ['dn', 'bc']:
                continue
                
            # Get this object's action
            dur_action = row[f'object{i}_action_state_clean_dur_action']
            point_action = row[f'object{i}_action_state_clean_point_action']

            # Process point action first
            if not pd.isna(point_action):
                action = point_action
                if action in action_mapping:
                    state_name, state_value = action_mapping[action]
                    if state_name in obj_states[obj]:
                        obj_states[obj][state_name].append([state_value, start_time])
                
                # Special handling for hit action
                if action == 'hi':
                    # Find the other object that was hit
                    other_objs = [o for o in objects if o != obj]
                    for other_obj in other_objs:
                        obj_states[obj]['gothit'].append([True, start_time])
                        obj_states[other_obj]['hitter'].append([True, start_time])
                
                # Special handling for brush action
                if action == 'b':
                    assert obj == 'b'  # brush should be the object
                    obj_states[obj]['usebrush'].append([True, start_time])

            # Then process dur action
            if not pd.isna(dur_action):
                action = dur_action
                if action in action_mapping:
                    state_name, state_value = action_mapping[action]
                    if state_name in obj_states[obj]:
                        obj_states[obj][state_name].append([state_value, start_time])
                
                # Special handling for hit action
                if action == 'hi':
                    # Find the other object that was hit
                    other_objs = [o for o in objects if o != obj]
                    for other_obj in other_objs:
                        obj_states[obj]['gothit'].append([True, start_time])
                        try:
                            obj_states[other_obj]['hitter'].append([True, start_time])
                        except KeyError:
                            print(f"KeyError: 'hitter' state not found for object {other_obj}")
                
                # Special handling for brush action
                if action == 'b':
                    assert obj == 'b'  # brush should be the object
                    obj_states[obj]['usebrush'].append([True, start_time])
            
            # Get this object's states
            state_types = ['mouth', 'noise', 'detach', 'reattach', 'takeout', 'putin', 'popup',
                          'hidden', 'open', 'close']
            states = []
            if not pd.isna(point_action) or not pd.isna(dur_action):
                # Check point states first
                if not pd.isna(point_action):
                    state_cols = [f'object{i}_action_state_clean_point_{state}' for state in state_types]
                    states = [col.split('_')[-1] for col in state_cols if row[col] == 'y']
                # Then check dur states
                if not pd.isna(dur_action):
                    state_cols = [f'object{i}_action_state_clean_dur_{state}' for state in state_types]
                    states.extend([col.split('_')[-1] for col in state_cols if row[col] == 'y'])

            # Process states for this object
            for state in states:
                if state in state_mapping:
                    state_mapping[state](obj, state)
            
            # Special handling for putin/takeout
            if 'putin' in states or 'takeout' in states:
                # Find the other object involved in the putin/takeout
                other_objs = [o for o in objects if o != obj]
                for other_obj in other_objs:
                    if 'putin' in states:
                        # Check if obj can contain other_obj
                        if obj in containers and other_obj in containers[obj]:
                            obj_states[obj]['contains'].append([other_obj, start_time])
                            try:
                                obj_states[other_obj]['inside'].append([True, start_time])
                            except KeyError:
                                print(f"KeyError: 'inside' state not found for object {other_obj}")
                    elif 'takeout' in states:
                        # Check if other_obj can contain obj
                        if other_obj in containers and obj in containers[other_obj]:
                            obj_states[other_obj]['contains'].append([obj, start_time])
                            obj_states[obj]['inside'].append([True, start_time])
    return obj_states