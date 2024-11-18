from flask import Flask, jsonify, render_template
from datetime import datetime
import ping3
import requests
from config import TARGET_IPS, PEER_MONITORS

app = Flask(__name__)

def verify_with_peers(ip):
    """Verify host status with peer monitors"""
    try:
        peer_results = []
        for peer in PEER_MONITORS:
            if "onrender.com" not in peer:  # Only check local peers
                try:
                    response = requests.get(f"http://{peer}/check/{ip}", timeout=5)
                    if response.status_code == 200:
                        peer_results.append(response.json()['reachable'])
                except Exception as e:
                    print(f"Failed to contact peer {peer}: {e}")
                    continue
        
        if peer_results and any(peer_results):
            return True, "Host is up (verified by peers)"
        return False, "Host is down (verified by peers)"
    except Exception as e:
        print(f"Peer verification failed: {e}")
        return False, "Peer verification failed"

def check_host(ip):
    """Check host with peer verification"""
    response_time = ping3.ping(ip)
    if response_time is None:
        # If direct ping fails, check with peers
        is_reachable, message = verify_with_peers(ip)
        if is_reachable:
            return 0.001  # Nominal value if reachable through peers
    return response_time

@app.route('/')
def home():
    results = {}
    for ip in TARGET_IPS:
        response_time = check_host(ip)
        peer_status = "Verified by peers" if response_time == 0.001 else ""
        results[ip] = {
            'status': 'UP' if response_time else 'DOWN',
            'response_time': f"{round(response_time, 3)}ms" if response_time else "N/A",
            'last_check': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'peer_status': peer_status
        }
    return render_template('dashboard.html', ips=results)

@app.route('/check/<ip>')
def check_endpoint(ip):
    """API endpoint for peer checks"""
    try:
        response_time = ping3.ping(ip)
        return jsonify({
            'reachable': response_time is not None,
            'response_time': response_time,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'reachable': False
        }), 500

if __name__ == '__main__':
    print("\n=== Local Network Monitor Dashboard with Peer Checking ===")
    print("Starting server...")
    print("Access the dashboard at: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', debug=True, port=5000)