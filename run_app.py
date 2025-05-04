
import subprocess
import webbrowser
import time
import sys
import os

def start_streamlit():
    print("Starting Streamlit app...")
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return streamlit_process

def start_api():
    print("Starting FastAPI server...")
    api_process = subprocess.Popen(
        [sys.executable, "run_api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return api_process

if __name__ == "__main__":
    # Check if data directory exists, if not create it
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Start both processes
    api_process = start_api()
    streamlit_process = start_streamlit()
    
    print("Waiting for services to start...")
    time.sleep(5)
    
    # Open Streamlit in the browser
    webbrowser.open("http://localhost:8501")
    
    print("SHL Assessment Navigator is running!")
    print("API server: http://localhost:8000")
    print("Web interface: http://localhost:8501")
    print("Press CTRL+C to exit")
    
    try:
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        api_process.terminate()
        streamlit_process.terminate()
        print("Goodbye!")
