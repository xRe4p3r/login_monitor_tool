import time
from random import choice, randint

LOG_FILE = "mock_auth.log"

FAILED_TEMPLATE = "May 27 12:{minute}:{second} myhost sshd[{pid}]: Failed password for {user_type} from {ip} port {port} ssh2"
SUCCESS_TEMPLATE = "May 27 12:{minute}:{second} myhost sshd[{pid}]: Accepted password for {user} from {ip} port {port} ssh2"

users = ["root", "admin", "user1", "test"]
ips = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]
user_types = ["invalid user admin", "root", "invalid user test"]

def generate_log_entry():
    now = time.localtime()
    minute = f"{now.tm_min:02}"
    second = f"{now.tm_sec:02}"
    pid = randint(1000, 9999)
    port = randint(50000, 60000)
    ip = choice(ips)

    if randint(1, 4) != 4:
        # 75% chance to generate failed login
        user = choice(user_types)
        log = FAILED_TEMPLATE.format(minute=minute, second=second, pid=pid, user_type=user, ip=ip, port=port)
    else:
        user = choice(users)
        log = SUCCESS_TEMPLATE.format(minute=minute, second=second, pid=pid, user=user, ip=ip, port=port)

    return log

def write_log_entries(count=10, delay=1):
    with open(LOG_FILE, "a") as file:
        for _ in range(count):
            log_entry = generate_log_entry()
            print(f"Generated: {log_entry}")
            file.write(log_entry + "\n")
            file.flush()
            time.sleep(delay)

if __name__ == "__main__":
    print("Simulating login attempts...")
    write_log_entries(count=20, delay=1)
