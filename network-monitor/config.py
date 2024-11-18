SMTP_EMAIL = "metahackathonping@gmail.com"  # Replace with your Gmail address
SMTP_PASSWORD = "kwtq enpv qbwh vqgf"

TARGET_IPS = [
    "172.25.72.110",
    "172.17.33.245",
    "192.168.56.1"
]

ALERT_EMAILS = [
    "linhlam752@gmail.com",
    "arrachelcollier@gmail.com",
    "dylanjaws185323@gmail.com"
]

CHECK_INTERVAL = 3600  # 1 hour in seconds

PEER_MONITORS = [
    "meta-hackathon.onrender.com",  # Your central server
    "172.25.72.110:5000",
    "172.17.33.245:5000"
]

# Optional: Add your own machine's monitoring API port
MONITOR_PORT = 5000

FAILURE_THRESHOLD = 3  # Number of consecutive failures before alerting