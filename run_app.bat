@echo off
echo 🚀 Starting File Metadata Analyzer...
echo 📊 Open your browser to: http://localhost:8501
echo 💡 Press Ctrl+C to stop the server
echo.

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

REM Run the Streamlit app
streamlit run streamlit_metatool.py
