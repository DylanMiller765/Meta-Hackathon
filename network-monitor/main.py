from monitor import monitor_network
from api import app
import threading
from config import MONITOR_PORT

def run_api():
    app.run(host='0.0.0.0', port=MONITOR_PORT)

if __name__ == "__main__":
    print("Starting network monitor...")
    
    # Start API server in a separate thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Run the main monitoring loop
    monitor_network()