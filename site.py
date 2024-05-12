import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.header('Compressor Health Monitoring')
#st.subheader('This is our website')

excel_file = pd.ExcelFile(r'https://github.com/pratik0199/comp_dashboard/blob/main/GERC_A_PARA_GUI_rev4.xlsm')
dict_stg = {'Stage 1': {'tab1': [7, 368, 'table1_df'], 'tab2': [372, 733, 'table2_df'], 'tab3': [745, 1106, 'table3_df'], 'tab4': [1110, 1471,'table4_df']},
            'Stage 2': {'tab1': [7, 368, 'table1_df'], 'tab2': [372, 733, 'table2_df'], 'tab3': [745, 1106, 'table3_df'], 'tab4': [1110, 1471,'table4_df']}
           }
def read_tables_from_excel(excel_file, dict_stg):
    for stg in dict_stg:
        print('#########################')
        sheet_name = stg
        print('Sheet Name: ', sheet_name)

        for tab in dict_stg[stg]:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print ('Tab: ',dict_stg[stg][tab]) 

            skip_rows = dict_stg[stg][tab][0]-1
            n_rows = dict_stg[stg][tab][1] - dict_stg[stg][tab][0] + 1
            
            print('Skip rows: ', skip_rows)
            print('N rows: ', n_rows)
            
            table_name = f"{stg}_{tab}"
            table_df = pd.read_excel(excel_file, sheet_name, header=0, skiprows=skip_rows, nrows=n_rows)
            print(f"{table_name} DataFrame: \n",table_df.head(2))
            
            dict_stg[stg][tab][2] = table_df
            print(f"{table_name} DataFrame: \n",dict_stg[stg][tab][2])
read_tables_from_excel(excel_file, dict_stg)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Function to plot pressure vs time for Stage 1
def plot_stage1():
    fig, ax = plt.subplots()
    ax.plot(dict_stg['Stage 1']['tab3'][2]['Crank angle'], dict_stg['Stage 1']['tab3'][2]['HE, Press'], color='red', label='HE')
    ax.plot(dict_stg['Stage 1']['tab3'][2]['Crank angle'], dict_stg['Stage 1']['tab4'][2]['CE'], color='orange', label='CE')
    
    ax.grid(color='white', linestyle='--', linewidth=0.25)
    ax.set_xlabel('Crank angle, deg')
    ax.set_ylabel('Pressure, bar, abs')
    ax.set_title('Stage I - Pressure vs. time', fontsize=16, fontweight='bold')
    ax.legend()
    ax.set_facecolor('black')
    return fig

# Function to plot pressure vs time for Stage 2
def plot_stage2():
    fig, ax = plt.subplots()
    ax.plot(dict_stg['Stage 2']['tab3'][2]['Crank angle'], dict_stg['Stage 2']['tab3'][2]['Pressure, Head end, bar abs'], color='red', label='HE')
    ax.plot(dict_stg['Stage 2']['tab3'][2]['Crank angle'], dict_stg['Stage 2']['tab4'][2]['Pressure, Crank end, bar abs'], color='orange', label='CE')
    
    ax.grid(color='white', linestyle='--', linewidth=0.25)
    ax.set_xlabel('Crank angle, deg')
    ax.set_ylabel('Pressure, bar, abs')
    ax.set_title('Stage II - Pressure vs. time', fontsize=16, fontweight='bold')
    ax.legend()
    ax.set_facecolor('black')
    return fig

# Function to plot HE-PV plot for Stage 1
def plot_stage1_he_pv():
    fig, ax = plt.subplots()
    ax.plot(dict_stg['Stage 1']['tab3'][2]['Swept vol, HE, %'], dict_stg['Stage 1']['tab3'][2]['HE, Press'], color='orange', label='HE')
    
    ax.grid(color='white', linestyle='--', linewidth=0.25)
    ax.set_xlabel('Swept vol, %')
    ax.set_ylabel('Pressure, bar, abs')
    ax.set_title('Stage I - HE PV Plot', fontsize=16, fontweight='bold')
    ax.legend()
    ax.set_facecolor('black')
    return fig

# Function to plot HE-PV plot for Stage 2
def plot_stage2_he_pv():
    fig, ax = plt.subplots()
    ax.plot(dict_stg['Stage 2']['tab3'][2]['Swept vol, HE, %'], dict_stg['Stage 2']['tab3'][2]['Pressure, Head end, bar abs'], color='orange', label='HE')
    ax.grid(color='white', linestyle='--', linewidth=0.25)
    ax.set_xlabel('Swept vol, %')
    ax.set_ylabel('Pressure, bar, abs')
    ax.set_title('Stage II - HE PV Plot', fontsize=16, fontweight='bold')
    ax.legend()
    ax.set_facecolor('black')
    return fig

# Main Streamlit app
def main():
    st.title('Valve status')

    # List widget to select the plot
    plot_options = ['Pressure vs Time', 'HE-PV Plot']
    plot_choice = st.selectbox('Select Plot', plot_options)

    # Display the selected plot
    if plot_choice == 'Pressure vs Time':
        # Plot for Stage 1
        fig1 = plot_stage1()
        # Plot for Stage 2
        fig2 = plot_stage2()

        # Display plots side by side using columns layout
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(fig1)
        with col2:
            st.pyplot(fig2)
    elif plot_choice == 'HE-PV Plot':
        # Plot for Stage 1 HE-PV
        fig1 = plot_stage1_he_pv()
        # Plot for Stage 2 HE-PV
        fig2 = plot_stage2_he_pv()

        # Display plots side by side using columns layout
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(fig1)
        with col2:
            st.pyplot(fig2)

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load data from Excel file
database_df = pd.read_excel(r'https://raw.githubusercontent.com/pratik0199/comp_dashboard/main/GERC_A_PARA_GUI_rev4.xlsm', sheet_name='database')
#st.write(database_df[' Stg I Flow factor'].iloc[1:26]).head()

# Function to update the plot data for Stage I
def update_plot_stage1():
    fig, ax = plt.subplots()
    ax.clear()
    ax.plot(database_df['Date'].iloc[1:26], database_df[' Stg I Flow factor'].iloc[1:26], marker='o', linestyle='-', color='orange')
    ax.grid(color='white', linestyle='--', linewidth=0.25)
    ax.set_ylabel('Flow factor')
    ax.set_title('Stage I - Flow Balance', fontsize=16, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.set_facecolor('black')

# Function to update the plot data for Stage II
def update_plot_stage2():
    fig, ax = plt.subplots()
    ax.clear()
    ax.plot(database_df['Date'].iloc[1:26], database_df[' Stg II Flow factor'].iloc[1:26], marker='o', linestyle='-', color='orange')
    ax.grid(color='white', linestyle='--', linewidth=0.25)
    ax.set_ylabel('Flow factor')
    ax.set_title('Stage II - Flow Balance', fontsize=16, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.set_facecolor('black')

# Streamlit app
st.title('Flow Balance Animation')

 #Main Streamlit app
def main():
    st.title('Animated charts')

    # List widget to select the plot
    plot_options = ['Flow balance']
    plot_choice = st.selectbox('Select Plot', plot_options)

    # Display the selected plot
    if plot_choice == 'Flow balance':
        # Plot for Stage 1
        fig1 = update_plot_stage1()
        # Plot for Stage 2
        fig2 = update_plot_stage2()

        # Display plots side by side using columns layout
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(fig1)
        with col2:
            st.pyplot(fig2)
    

if __name__ == "__main__":
    main()

import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

# Load the compressor image
image = Image.open(r"C:\Users\psonawane\Desktop\compressor_image.jpg")

# Display the compressor image
st.image(image, caption='Compressor Image')

# Add buttons with values in front of different parts of the compressor
st.button(label='Value 1', key='part1')
st.button(label='Value 2', key='part2')
st.button(label='Value 3', key='part3')
# Define the positions of the buttons relative to the image
#button_positions = {
    #"Value 1": (10, 10),
    #"Value 2": (20, 20),
    #"Value 3": (30, 30),
#}

# Add buttons with values in specific locations on top of the image
#for label, (x, y) in button_positions.items():
    #st.markdown(f'<button style="position:absolute;top:{y}px;left:{x}px;">{label}</button>', unsafe_allow_html=True)
excel_file1 = pd.read_excel(r'https://github.com/pratik0199/comp_dashboard/GERC_A_PARA_GUI_rev4.xlsm', sheet_name='cur_data')
# Check if any value in the "flow factor" column is greater than 1.04
valve_leakage_s1 = any(excel_file1["Flow factor for stg 1"] > 1.04)
valve_leakage_s2 = any(excel_file1["Flow factor for stg 2"] <0)
#cylinder_leakage = any(excel_file1["Dish temp - Ad. Disch temp"] > 8.5)
# Define the CSS styles for red and green checkboxes
red_checkbox_style = """<style>input[type="checkbox"].red {color:red !important;} </style>"""
green_checkbox_style = """<style>input[type="checkbox"].green {color:green !important;} </style>"""
 
# Display the CSS styles
st.write("Compressor Health Monitoring:")
col1, col2 = st.columns([10,35])
with col1:
    st.text("Valve Leakage_s1 :")
with col2:
    if valve_leakage_s1:
        st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: red;"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: green;"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([20, 70])


with col1:
    st.text("Valve Leakage_s2 :")
with col2:
    if valve_leakage_s2:
        st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: red;"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: green;"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([30, 105])


# Load the Excel file once at the beginning of the app
@st.cache_data(ttl=60)  # Cache with a timeout of 1 min
def load_data():
    return pd.read_excel(r'https://raw.githubusercontent.com/pratik0199/comp_dashboard/main/GERC_A_PARA_GUI_rev4.xlsm', sheet_name='cur_data')

# Main Streamlit app
def main():
    st.title("Compressor Health Monitoring")

    # Load data
    data = load_data()

    # Function to check valve leakage status
    def check_valve_leakage(data):
        suction_valve_leak_stage1= any(data["Flow factor for stg 1"] > 1.04)
        suction_valve_leak_stage2 = any(data["Flow factor for stg 2"] > 1.04)
        disch_valve_leak_stage1= any(data["Flow factor for stg 1"] < 0.98)
        disch_valve_leak_stage2= any(data["Flow factor for stg 2"] < 0.98)
        #cylinder_leak_stage1= any(data["Dish temp - Ad. Disch temp"] > 8.5)
        #cylinder_leak_stage2= any(data["Dish temp - Ad. Disch temp"] > 8.5)
        return suction_valve_leak_stage1, suction_valve_leak_stage2,disch_valve_leak_stage1,disch_valve_leak_stage2

    # Check valve leakage status
    suction_valve_leak_stage1, suction_valve_leak_stage2, disch_valve_leak_stage1, disch_valve_leak_stage2 = check_valve_leakage(data)
    
    # CSS styles
    red_checkbox_style = """<style>input[type="checkbox"].red {color:red !important;} </style>"""
    green_checkbox_style = """<style>input[type="checkbox"].green {color:green !important;} </style>"""

    # Display valve leakage status
    st.write("Compressor Health Monitoring:")
    col1, col2 = st.columns([30,50])
    with col1:
        st.text("suction valve leak - stage 1 :")
    with col2:
        if suction_valve_leak_stage1:
            st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: red;"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: green;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([60, 100])

    with col1:
        st.text("suction valve leak - stage 2:")
    with col2:
        if suction_valve_leak_stage2:
            st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: red;"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: green;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([90, 150])

    with col1:
        st.text("Discharge valve leak - stage 1:")
    with col2:
        if disch_valve_leak_stage1:
            st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: red;"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: green;"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([120, 200])
    with col1:
        st.text("Discharge valve leak - stage 2:")
    with col2:
        if disch_valve_leak_stage2:
            st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: red;"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="display: inline-block; width: 20px; height: 20px; background-color: green;"></div>', unsafe_allow_html=True)
    

if __name__ == "__main__":
    main()
