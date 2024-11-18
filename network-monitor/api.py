from flask import Flask, jsonify
from monitor import check_host
from config import MONITOR_PORT
from datetime import datetime

app = Flask(__name__)

@app.route('/check/<ip>')
def check_endpoint(ip):
    try:
        response_time = check_host(ip)
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
    app.run(port=MONITOR_PORT, debug=True)