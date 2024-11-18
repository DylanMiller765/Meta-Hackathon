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

def send_alert(ip, status, response_time=None, additional_info=None):
    """Send email alert for host status change"""
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            
            for recipient in ALERT_EMAILS:
                # Create a new message for each recipient
                body = f"""
                Host: {ip}
                Status: {status}
                Time: {datetime.now()}
                Response Time: {response_time if response_time else 'N/A'} ms
                Additional Info: {additional_info if additional_info else 'N/A'}
                """
                
                msg = MIMEText(body)
                msg['Subject'] = f"Network Alert - {ip} is {status}"
                msg['From'] = SMTP_EMAIL
                msg['To'] = recipient
                server.send_message(msg)
                
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_network():
    """Main monitoring loop"""
    print("Starting network monitor...")
    failure_counts = {ip: 0 for ip in TARGET_IPS}
    
    while True:
        for ip in TARGET_IPS:
            response_time = check_host(ip)
            current_status = response_time is not None
            
            if not current_status:
                failure_counts[ip] += 1
                if failure_counts[ip] >= FAILURE_THRESHOLD:
                    # Verify with peers before sending alert
                    peer_status, message = verify_with_peers(ip)
                    if not peer_status:
                        send_alert(
                            ip=ip,
                            status="DOWN",
                            response_time=None,
                            additional_info=message
                        )
            else:
                # Reset failure count if host is reachable
                if failure_counts[ip] >= FAILURE_THRESHOLD:
                    send_alert(
                        ip=ip,
                        status="UP",
                        response_time=response_time,
                        additional_info="Host is back online"
                    )
                failure_counts[ip] = 0
                
        time.sleep(CHECK_INTERVAL)
