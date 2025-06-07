import os
import streamlit as st
from PIL import Image

def display_dashboard():
    st.title('Agent State Plots Dashboard')

    # Display notes section
    st.header('Notes')
    st.markdown("""
    - Broom and alligator busy box can make noise in data
    - Farm toy has open state but converted to popup in post processing
    - Alligator busy box can be mouthed
    - Music toy alligator can be a hitter
    """)

    # Get all plot files from plots directory
    plot_files = []
    for root, dirs, files in os.walk('plots'):
        for file in files:
            if file.endswith('.png'):
                plot_files.append(os.path.join(root, file))
    
    # Get plots from RND_distributions/plots/averaged_from_csv_stacked directory
    additional_plot_files = []
    additional_plot_dir = 'RND_distributions/plots/averaged_from_csv_stacked'
    if os.path.exists(additional_plot_dir):
        for root, dirs, files in os.walk(additional_plot_dir):
            for file in files:
                if file.endswith('.png'):
                    additional_plot_files.append(os.path.join(root, file))
    
    if not plot_files and not additional_plot_files:
        st.error("No plot files found in any directory")
        return

    # Group plots by agent and type (individual vs averaged)
    agent_plots = {}
    averaged_plots = []
    for plot_file in plot_files:
        agent = os.path.basename(os.path.dirname(plot_file))
        if agent == 'averaged':
            averaged_plots.append(plot_file)
        else:
            if agent not in agent_plots:
                agent_plots[agent] = []
            agent_plots[agent].append(plot_file)

    # Create tabs for individual agents, averaged plots, and additional plots
    tab1, tab2, tab3 = st.tabs(["Individual Agents", "Averaged Plots", "Additional Plots"])

    with tab1:
        # Create agent selector
        selected_agent = st.selectbox(
            'Select Agent',
            options=sorted(agent_plots.keys()),
            key='agent_selector'
        )

        # Display all plots for selected agent
        st.subheader(f'Plots for Agent {selected_agent}')
        plot_files = agent_plots[selected_agent]
        for plot_file in plot_files:
            img = Image.open(plot_file)
            st.image(img, use_column_width=True, caption=os.path.basename(plot_file).replace('.png',''))

    with tab2:
        st.subheader('Averaged State Distributions')
        if not averaged_plots:
            st.info("No averaged plots available yet. Run the post-processing script to generate them.")
        else:
            for plot_file in sorted(averaged_plots):
                img = Image.open(plot_file)
                st.image(img, use_column_width=True, caption=os.path.basename(plot_file).replace('.png',''))

    with tab3:
        st.subheader('RND Plots')
        if not additional_plot_files:
            st.info("No additional plots found in the RND_distributions directory.")
        else:
            for plot_file in sorted(additional_plot_files):
                img = Image.open(plot_file)
                st.image(img, use_column_width=True, caption=os.path.basename(plot_file).replace('.png',''))

if __name__ == "__main__":
    display_dashboard()
