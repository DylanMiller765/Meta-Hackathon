from flask import Flask, jsonify, request, render_template
from datetime import datetime
from monitor import check_host, verify_with_peers
from config import TARGET_IPS, MONITOR_PORT
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dashboard.html', ips=TARGET_IPS)

@app.route('/api/status')
def get_status():
    results = {}
    for ip in TARGET_IPS:
        response_time = check_host(ip)
        is_reachable, message = verify_with_peers(ip) if not response_time else (True, "Direct connection successful")
        
        results[ip] = {
            'status': 'up' if (response_time or is_reachable) else 'down',
            'response_time': round(response_time, 3) if response_time else None,
            'last_check': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'message': message if not response_time else "Direct connection successful"
        }
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', MONITOR_PORT))
    app.run(host='0.0.0.0', port=port)