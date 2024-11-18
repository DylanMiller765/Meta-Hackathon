from monitor import monitor_network
from api import app
import threading
from config import MONITOR_PORT
import signal
import sys

def signal_handler(sig, frame):
    print("\nShutting down gracefully...")
    sys.exit(0)

def run_api():
    app.run(host='0.0.0.0', port=MONITOR_PORT)

if __name__ == "__main__":
    print("Starting network monitor...")
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start API server in a separate thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Run the main monitoring loop
    monitor_network()