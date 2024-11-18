from flask import Flask, jsonify
import ping3
from datetime import datetime

app = Flask(__name__)

TARGET_IPS = [
    "172.25.72.110",
    "172.17.33.245",
    "192.168.56.1"
]

@app.route('/status')
def get_status():
    results = {}
    for ip in TARGET_IPS:
        response_time = ping3.ping(ip)
        results[ip] = {
            'status': 'UP' if response_time else 'DOWN',
            'response_time': round(response_time, 3) if response_time else None,
            'last_check': datetime.now().isoformat()
        }
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)