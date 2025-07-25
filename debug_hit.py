import pandas as pd

df = pd.read_csv('DevEvObject_2025-07-17.csv')

# Find rows with hit actions involving stroller
found_issue = False
for i in range(1, 4):
    dur_col = f'object{i}_action_state_clean_dur_action'
    point_col = f'object{i}_action_state_clean_point_action'
    obj_col = f'object{i}_clean_obj'
    
    # Find hits
    hit_rows = df[(df[dur_col] == 'hi') | (df[point_col] == 'hi')]
    
    for idx, row in hit_rows.iterrows():
        hitting_obj = row[obj_col]
        # Check other objects
        for j in range(1, 4):
            if j != i:
                other_obj = row[f'object{j}_clean_obj']
                if pd.notna(other_obj) and other_obj == 's':
                    print(f'Row {idx}: object{i}={hitting_obj} hits object{j}=stroller')
                    found_issue = True
                    
# Also check for 'b' action on non-brush objects
print("\nChecking for brush actions on non-brush objects:")
for i in range(1, 4):
    dur_col = f'object{i}_action_state_clean_dur_action'
    point_col = f'object{i}_action_state_clean_point_action'
    obj_col = f'object{i}_clean_obj'
    
    # Find brush actions
    brush_rows = df[(df[dur_col] == 'b') | (df[point_col] == 'b')]
    
    for idx, row in brush_rows.iterrows():
        obj = row[obj_col]
        if pd.notna(obj) and obj != 'b':
            print(f'Row {idx}: object{i}={obj} has brush action but is not a brush!')