
import subprocess
import webbrowser
import time
import os
import sys
import signal
import argparse

def start_backend():
    """Start the FastAPI backend server"""
    print("Starting backend API server...")
    backend_process = subprocess.Popen(
        [sys.executable, "backend/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return backend_process

def start_frontend(frontend_type):
    """Start the selected frontend"""
    if frontend_type == "streamlit":
        print("Starting Streamlit frontend...")
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "frontend/app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        frontend_url = "http://localhost:8501"
    elif frontend_type == "web":
        print("Using web frontend...")
        frontend_process = None
        # Get absolute path to the HTML file
        frontend_url = f"file://{os.path.abspath('web/index.html')}"
    else:
        print("Invalid frontend type specified.")
        sys.exit(1)
    
    return frontend_process, frontend_url

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run SHL Assessment Recommender")
    parser.add_argument(
        "--frontend", 
        choices=["streamlit", "web"], 
        default="streamlit",
        help="Frontend to use (streamlit or web)"
    )
    parser.add_argument(
        "--no-browser", 
        action="store_true",
        help="Don't open browser automatically"
    )
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Start backend
    backend_process = start_backend()
    
    # Wait a bit for the backend to start
    time.sleep(2)
    
    # Start frontend
    frontend_process, frontend_url = start_frontend(args.frontend)
    
    # Wait a bit for the frontend to start
    time.sleep(3)
    
    # Open in browser
    if not args.no_browser:
        print(f"Opening {frontend_url} in browser...")
        webbrowser.open(frontend_url)
    
    print("\nSHL Assessment Recommender is running!")
    print("Backend API: http://localhost:8000")
    print(f"Frontend: {frontend_url}")
    print("\nPress CTRL+C to exit")
    
    try:
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("Goodbye!")

if __name__ == "__main__":
    main()
