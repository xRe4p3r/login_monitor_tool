# 🔐 Login Monitor Tool

A Python-based tool that monitors SSH login attempts by parsing a log file. It detects failed and successful logins, extracts IP addresses, and triggers alerts if too many failed logins occur from the same IP within a short time.

---

## 📦 Features

- ✅ Parses a log file (e.g., `/var/log/auth.log` or a mock log)
- ✅ Detects **failed** and **successful** SSH login attempts
- ✅ Extracts and logs IP addresses
- 🚨 Alerts when **5 failed attempts from the same IP** occur within **5 minutes**
- 🧪 Includes a test script that simulates log entries in real-time

---

## 🛠️ Usage

### 1. Clone the Repository

```bash
git clone https://github.com/xRe4p3r/login_monitor_tool.git
cd login_monitor_tool
