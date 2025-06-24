@echo off
cd /d "D:\Dashboard HRD\Dashboard HRD"

call venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run main.py

pause