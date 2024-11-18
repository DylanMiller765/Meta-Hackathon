from flask import Flask, jsonify, request
from datetime import datetime
from monitor import check_host, verify_with_peers
from config import TARGET_IPS, MONITOR_PORT

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    app.run()