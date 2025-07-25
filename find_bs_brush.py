import pandas as pd

df = pd.read_csv('DevEvObject_2025-07-17.csv')

# Find rows where bs has brush action
print("Rows where bs (broom set) has brush action 'b':")
print("=" * 80)

for i in range(1, 4):
    obj_col = f'object{i}_clean_obj'
    dur_col = f'object{i}_action_state_clean_dur_action'
    point_col = f'object{i}_action_state_clean_point_action'
    
    # Find bs with b action
    bs_brush_rows = df[(df[obj_col] == 'bs') & ((df[dur_col] == 'b') | (df[point_col] == 'b'))]
    
    if len(bs_brush_rows) > 0:
        print(f"\nObject{i} = bs with brush action:")
        for idx, row in bs_brush_rows.iterrows():
            print(f"\nRow {idx}:")
            print(f"  ID_subjsess: {row['ID_subjsess']}")
            print(f"  onset: {row['onset']}, offset: {row['offset']}")
            print(f"  duration: {row['offset'] - row['onset']}ms")
            
            # Show all objects in this row
            for j in range(1, 4):
                obj = row[f'object{j}_clean_obj']
                if pd.notna(obj):
                    dur_act = row[f'object{j}_action_state_clean_dur_action']
                    point_act = row[f'object{j}_action_state_clean_point_action']
                    print(f"  object{j}: {obj}, dur_action: {dur_act}, point_action: {point_act}")