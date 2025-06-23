import streamlit as st
import pandas as pd
from generate import generator
from datetime import datetime
from functions import load_data

st.set_page_config(
    page_title="Features: Attandances APP",
    page_icon="./Images/features_logo.jpeg",
    layout="wide",  # 'centered' or 'wide'
    initial_sidebar_state="expanded"  # 'auto', 'expanded', or 'collapsed'
)
st.markdown("<h2 style='text-align: center;'>DATA GENERATOR</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'></h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.3, 0.2, 4])

with col1:
    # Date selection
    date = st.date_input(
        "Select Date",
        value=datetime.now(),
        key="date_input"
    )

    # Branch selection
    st.markdown("<p style='text-align: center'></p>", unsafe_allow_html=True)
    branch = st.selectbox(
        "Select Branch",
        options=["RIO Utama", "RIO Digital Printing", "RIO Office Equipment"],
        index=0,  # Default to the first option
        key="branch_select"
    )

    # Data upload
    st.markdown("<p style='text-align: center'></p>", unsafe_allow_html=True)
    data = st.file_uploader("Upload your file here", type=["xlsx","xls"], key="file_uploader")

    # filename input and save button
    col1_1, col1_2 = st.columns([1, 0.4])
    with col1_1:
        st.markdown("""<p style='padding-top: 2px;'></p>""", unsafe_allow_html=True)
        filename = st.text_input('Filename')
    with col1_2:
        # Button to Save file with name file inputer
        st.markdown("<h5 style='text-align: center'></h5>", unsafe_allow_html=True)
        button_save = st.button("Save File", key="save_button")


with col3:
    if data:
        data = pd.read_excel(data, sheet_name='Lap. Log Absen')
        data = generator.data_process_1(date=date, branch=branch, data=data)
        st.write(data)

    if button_save:
        msg = load_data.load_data_excel_to_export(data=data, filename=filename)
        st.write(msg)