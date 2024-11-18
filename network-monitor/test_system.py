import requests
import ping3
import smtplib
from config import *

def test_email_config():
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            print("✅ Email configuration is working")
    except Exception as e:
        print(f"❌ Email configuration error: {e}")

def test_peer_connectivity():
    for peer in PEER_MONITORS:
        try:
            response = requests.get(f"http://{peer}/", timeout=5)
            print(f"✅ Peer {peer} is reachable")
        except Exception as e:
            print(f"❌ Peer {peer} is not reachable: {e}")

def test_target_ips():
    for ip in TARGET_IPS:
        response_time = ping3.ping(ip)
        if response_time is not None:
            print(f"✅ Target {ip} is reachable (response time: {response_time}ms)")
        else:
            print(f"❌ Target {ip} is not reachable")

if __name__ == "__main__":
    print("Testing system configuration...")
    print("\nTesting email configuration:")
    test_email_config()
    print("\nTesting peer connectivity:")
    test_peer_connectivity()
    print("\nTesting target IPs:")
    test_target_ips()