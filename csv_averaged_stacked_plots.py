import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Load the CSV data
csv_path = 'merged_rnd_multi_seed.csv'
df = pd.read_csv(csv_path)

# Pretty names for objects (add more as needed)
obj_name_mapping = {
    'coin': 'Coin',
    'gear': 'Gear',
    'shape_toy': 'Shape Toy',
    'mini_broom': 'Mini Broom',
    'piggie_bank': 'Piggie Bank',
    'beach_ball': 'Beach Ball',
    'farm_toy': 'Farm Toy',
    'broom': 'Broom',
    'broom_set': 'Broom Set',
    'rattle': 'Rattle',
    'red_spiky_ball': 'Red Spiky Ball',
    'tree_busy_box': 'Tree Busy Box',
    'stroller': 'Stroller',
    'gear_toy': 'Gear Toy',
    'shape_sorter': 'Shape Sorter',
    # add more as needed
}

output_dir = 'babyRLDataProcessing/plots/averaged_from_csv_stacked'
os.makedirs(output_dir, exist_ok=True)

# Object types to average across indices
average_types = ['coin', 'gear', 'shape_toy', 'piggie_bank', 'gear_toy', 'shape_sorter']

# Get all unique state names
state_names = df['state_name'].unique()

for state in state_names:
    # For each object, get the total activity_count for this state
    object_percentages = {}
    
    # Handle combined statistics for specific pairs
    combined_pairs = {
        'coin': 'piggie_bank',
        'gear': 'gear_toy',
        'shape_toy': 'shape_sorter'
    }
    
    for obj_type in df['object_type'].unique():
        if obj_type in average_types:
            # Skip if this is the second part of a combined pair
            if obj_type in combined_pairs.values():
                continue
                
            # Check if this object type has a pair to combine with
            if obj_type in combined_pairs:
                pair_type = combined_pairs[obj_type]
                # Get data for both objects
                obj_df = df[(df['object_type'] == obj_type) & (df['state_name'] == state)]
                pair_df = df[(df['object_type'] == pair_type) & (df['state_name'] == state)]
                
                # Calculate combined statistics
                total_count = (obj_df['activity_count'].sum() + pair_df['activity_count'].sum()) / 2
                if total_count > 0:
                    label = pair_type  # Use the second object's name as the label
                    object_percentages[label] = total_count / 5000
            else:
                # Handle regular object types
                obj_df = df[(df['object_type'] == obj_type) & (df['state_name'] == state)]
                total_count = obj_df['activity_count'].sum()
                if total_count > 0:
                    label = obj_type
                    object_percentages[label] = total_count / 5000
        else:
            for obj_idx in df[df['object_type'] == obj_type]['object_index'].unique():
                obj_df = df[(df['object_type'] == obj_type) & (df['object_index'] == obj_idx) & (df['state_name'] == state)]
                total_count = obj_df['activity_count'].sum()
                if total_count > 0:
                    label = f"{obj_type}_{obj_idx}"
                    object_percentages[label] = total_count / 5000

    # Skip if no objects have activity for this state
    if not object_percentages:
        continue

    # Prepare data for plotting
    labels = []
    true_percents = []
    false_percents = []
    for label, true_percent in object_percentages.items():
        # Use pretty name if available
        pretty_label = obj_name_mapping.get(label.split('_')[0], label)
        labels.append(pretty_label)
        true_percents.append(true_percent * 100)
        false_percents.append(100 - true_percent * 100)

    y_pos = np.arange(len(labels))

    plt.figure(figsize=(12, 6))
    plt.title(f'Average Distribution of {state} state across objects')
    plt.xlabel('Percentage of Steps')
    plt.ylabel('Objects')

    plt.barh(y_pos, false_percents, color='red', alpha=0.7, label='False')
    plt.barh(y_pos, true_percents, left=false_percents, color='blue', alpha=0.7, label='True')

    plt.yticks(y_pos, labels)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.xlim(0, 100)
    plt.legend(['False', 'True'])
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{state}_distribution.png")
    plt.close() 