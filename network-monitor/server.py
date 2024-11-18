from flask import Flask, jsonify, request, render_template
from datetime import datetime
from monitor import check_host, verify_with_peers
from config import TARGET_IPS, MONITOR_PORT

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dashboard.html', ips=TARGET_IPS)

@app.route('/api/status')
def get_status():
    results = {}
    for ip in TARGET_IPS:
        response_time = check_host(ip)
        results[ip] = {
            'status': 'up' if response_time else 'down',
            'response_time': round(response_time, 3) if response_time else None,
            'last_check': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)