from flask import Flask, jsonify
from monitor import check_host
from config import MONITOR_PORT

app = Flask(__name__)

@app.route('/check/<ip>')
def check_endpoint(ip):
    response_time = check_host(ip)
    return jsonify({
        'reachable': response_time is not None,
        'response_time': response_time
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)