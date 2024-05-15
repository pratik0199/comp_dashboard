import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
st.set_page_config(layout="wide")

# Load client logo and company logo
company_logo = Image.open(r'C:\Users\psonawane\Downloads\ingenero1.png')
client_logo = Image.open(r'C:\Users\psonawane\Downloads\dresser rand.png')

# Main Streamlit app


# Layout the top portion with columns
col1, col2, col3 = st.columns([1, 3, 1])  # Adjust width ratios as needed

# Display client logo in the top left column
with col1:
    st.image(client_logo, use_column_width=True)

# Display title in the middle column
with col2:
    st.markdown('<h1 style="text-align: center;">Compressor Health Monitoring</h1>', unsafe_allow_html=True)

# Display company logo in the top right column
with col3:
    st.image(company_logo, use_column_width=True)

#For stage 1/2 plot
excel_file = pd.ExcelFile(r'C:\Users\psonawane\Documents\GERC_A_PARA_GUI_rev4.xlsm')
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
c2_col1, c2_col2 = st.columns([0.75,0.75])
with c2_col2:
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


with c2_col1:

# Load the Excel file once at the beginning of the app
    @st.cache_data(ttl=60)  # Cache with a timeout of 1 min
    def load_data():
        return pd.read_excel(r'C:\Users\psonawane\Documents\GERC_A_PARA_GUI_rev4.xlsm', sheet_name='cur_data')

# Main Streamlit app
    def main():
        st.header("Valve Leakge status")

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