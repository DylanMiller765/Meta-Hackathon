import ping3
import smtplib
from email.mime.text import MIMEText
import time
from datetime import datetime
from config import *
import requests

def check_host(ip, retry_count=3):
    """Ping host and return response time or None if unreachable"""
    for _ in range(retry_count):
        try:
            response_time = ping3.ping(ip)
            if response_time is not None:
                return response_time
        except Exception:
            continue
    return None

def verify_with_peers(ip):
    """Verify host status with peer monitors"""
    try:
        # Try to contact peer monitors to verify the host status
        peer_results = []
        for peer in PEER_MONITORS:
            try:
                # Using requests to check peer monitor API
                response = requests.get(f"http://{peer}/check/{ip}", timeout=5)
                if response.status_code == 200:
                    peer_results.append(response.json()['reachable'])
            except Exception as e:
                print(f"Failed to contact peer {peer}: {e}")
                continue
        
        # If any peer can reach the host, it's likely a local network issue
        if peer_results and any(peer_results):
            return True, "Local network issue detected"
        return False, "Host is down (verified by peers)"
    except Exception as e:
        print(f"Peer verification failed: {e}")
        return False, "Peer verification failed"

def send_alert(ip, message):
    """Send alert email"""
    try:
        msg = MIMEText(f"Host {ip} is experiencing issues.\n{message}")
        msg['Subject'] = f"Network Alert: {ip}"
        msg['From'] = SMTP_EMAIL
        msg['To'] = ', '.join(ALERT_EMAILS)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Alert sent for {ip}")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def monitor_network():
    """Main monitoring loop"""
    failure_counts = {ip: 0 for ip in TARGET_IPS}
    
    while True:
        for ip in TARGET_IPS:
            response_time = check_host(ip)
            
            if response_time is None:
                failure_counts[ip] += 1
                if failure_counts[ip] >= FAILURE_THRESHOLD:
                    # Verify with peers before sending alert
                    peer_status, message = verify_with_peers(ip)
                    if not peer_status:
                        send_alert(ip, message)
                        failure_counts[ip] = 0  # Reset after alert
            else:
                failure_counts[ip] = 0  # Reset on successful ping
                
            print(f"{datetime.now()}: {ip} - {'UP' if response_time else 'DOWN'}")
        
        time.sleep(CHECK_INTERVAL)

def register_with_central_server():
    try:
        response = requests.post(
            "https://your-app-name.onrender.com/register",
            json={"id": "monitor-1"}  # Unique ID for each monitor
        )
        return response.json()
    except Exception as e:
        print(f"Failed to register: {e}")
