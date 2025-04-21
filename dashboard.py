import os
import streamlit as st
from PIL import Image

def display_dashboard():
    st.title('Agent State Plots Dashboard')

    # Display notes section
    st.header('Notes')
    st.markdown("""
    - Broom and alligator busy box can make noise in data
    - Farm toy has open state 
    - Alligator busy box can be mouthed
    - Music toy alligator can be a hitter
    """)

    # Get all plot files from plots directory
    plot_files = []
    for root, dirs, files in os.walk('plots'):
        for file in files:
            if file.endswith('.png'):
                plot_files.append(os.path.join(root, file))
    
    if not plot_files:
        st.error("No plot files found in plots directory")
        return

    # Group plots by agent
    agent_plots = {}
    for plot_file in plot_files:
        agent = os.path.basename(os.path.dirname(plot_file))
        if agent not in agent_plots:
            agent_plots[agent] = []
        agent_plots[agent].append(plot_file)

    # Create agent selector
    selected_agent = st.selectbox(
        'Select Agent',
        options=sorted(agent_plots.keys()),
        key='agent_selector'
    )

    # Display all plots for selected agent
    plot_files = agent_plots[selected_agent]
    for plot_file in plot_files:
        img = Image.open(plot_file)
        st.image(img, use_column_width=True, caption=os.path.basename(plot_file).replace('.png',''))

if __name__ == "__main__":
    display_dashboard()
