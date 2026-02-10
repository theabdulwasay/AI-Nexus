@echo off
echo Starting Nexus AI...

:: Start API in a new window
start "Nexus AI API" cmd /k "python -m uvicorn api:app --host 0.0.0.0 --port 8001"

:: Wait for API to initialize
timeout /t 5

:: Start Streamlit UI
python -m streamlit run app.py

pause
