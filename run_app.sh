#!/bin/bash

echo "🚀 Starting File Metadata Analyzer..."
echo "📊 Open your browser to: http://localhost:8501"
echo "💡 Press Ctrl+C to stop the server"
echo ""

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the Streamlit app
streamlit run streamlit_metatool.py
