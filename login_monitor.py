import time
import re
from datetime import datetime, timedelta
from collections import defaultdict, deque

# Files
LOG_FILE = "mock_auth.log"
OUTPUT_LOG = "login_attempts.log"
ALERT_LOG = "alerts.log"

# Alert threshold
FAIL_THRESHOLD = 5
TIME_WINDOW = timedelta(minutes=5)

# Track failed attempts per IP
failed_attempts = defaultdict(deque)

# Regex to extract IP from line
IP_REGEX = re.compile(r'from (\d+\.\d+\.\d+\.\d+)')

def extract_ip(line):
    match = IP_REGEX.search(line)
    return match.group(1) if match else "Unknown"

def log_event(status, line, ip):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(OUTPUT_LOG, "a") as f:
        f.write(f"[{timestamp}] [{status}] IP: {ip} | {line.strip()}\n")

def write_alert(ip):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alert_msg = f"[{timestamp}] ALERT: {ip} had {FAIL_THRESHOLD}+ failed logins in {TIME_WINDOW}!\n"
    print(alert_msg.strip())
    with open(ALERT_LOG, "a") as f:
        f.write(alert_msg)

def track_failed(ip):
    now = datetime.now()
    attempts = failed_attempts[ip]

    # Remove timestamps outside the time window
    while attempts and now - attempts[0] > TIME_WINDOW:
        attempts.popleft()

    attempts.append(now)

    if len(attempts) >= FAIL_THRESHOLD:
        write_alert(ip)
        failed_attempts[ip].clear()

def process_line(line):
    if "Failed password" in line:
        ip = extract_ip(line)
        log_event("FAILED", line, ip)
        track_failed(ip)
    elif "Accepted password" in line:
        ip = extract_ip(line)
        log_event("SUCCESS", line, ip)

def run_monitor():
    with open(LOG_FILE, "r") as file:
        for line in file:
            process_line(line)
    print("Monitoring complete.")

if __name__ == "__main__":
    run_monitor()
