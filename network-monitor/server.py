from flask import Flask, jsonify, request, render_template
from datetime import datetime
from monitor import check_host, verify_with_peers
from config import TARGET_IPS, MONITOR_PORT

app = Flask(__name__)

@app.route('/')
def home():
    # Get initial status for all IPs
    results = {}
    for ip in TARGET_IPS:
        response_time = check_host(ip)
        results[ip] = {
            'status': 'UP' if response_time else 'DOWN',
            'response_time': f"{round(response_time, 3)}ms" if response_time else "N/A",
            'last_check': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    return render_template('dashboard.html', ips=results)

@app.route('/api/status')
def get_status():
    results = {}
    for ip in TARGET_IPS:
        response_time = check_host(ip)
        results[ip] = {
            'status': 'UP' if response_time else 'DOWN',
            'response_time': round(response_time, 3) if response_time else None,
            'last_check': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=MONITOR_PORT)