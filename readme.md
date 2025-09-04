# 🔧 Server Health Check Dashboard

A Streamlit-based dashboard to perform automated health checks on remote servers (Linux/Windows).  
The system runs multiple checks (connectivity, SSH, disk usage, inventory, logs, etc.), aggregates the results, and presents a **condensed one-row summary per host** with filters.

---

## 🚀 Features
- Connect to servers using **PEM file (SSH key)** authentication
- Run health checks across 11+ modules:
  - Connectivity
  - SSH Executor
  - Disk Usage
  - Inventory Report
  - Job Status Check
  - Config Parser
  - Log Parser
  - File Integrity
  - Excel Updater
  - REST Caller
  - Email Notifier
- Condensed results view:
  - ✅ **One row per host** (instead of multiple rows)
  - Status = Healthy, Error, or Pending
  - OS Type and representative Output
  - Details column lists only failed/pending modules
- Filters:
  - OS Type
  - Status
- Export results as Excel

---

## 📂 Project Structure
```
StreamLitDashboard/
├── app.py                  # Streamlit entry point
├── main_runner.py          # Runs all modules
├── config.yaml             # Auth config for Streamlit login
├── modules/                # Health check modules
│   ├── connectivity.py
│   ├── ssh_exec.py
│   ├── disk_usage.py
│   ├── inventory_report.py
│   ├── job_status_check.py
│   ├── config_parser.py
│   ├── log_parser.py
│   ├── file_integrity.py
│   ├── rest_caller.py
│   ├── email_notifier.py
│   └── dashboard.py        # Dashboard UI (condensed table)
├── assets/
│   └── servers.xlsx        # Input file with server details
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Prerequisites
- Python 3.8+ installed
- Streamlit + dependencies (listed in `requirements.txt`)
- Azure/VM with **port 8501 open** for Streamlit
- `servers.xlsx` in `assets/` with this schema:

| Hostname   | IP Address    | OS Type | Username  | PEM File (path in VM) | Port | Command  | TaskName |
|------------|--------------|---------|-----------|-----------------------|------|----------|----------|
| TM1Ubuntu  | 4.157.253.86 | Linux   | azureuser | /path/to/key.pem      | 22   | hostname | sshd     |

---

## 🛠️ Installation & Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>/StreamLitDashboard
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Update Excel file**
   - Edit `assets/servers.xlsx` with your server details (Hostname, IP, OS, Username, PEM path, etc.)

---

## ▶️ Running the App

Run Streamlit from inside the project folder:
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Open in your browser:
```
http://<VM-Public-IP>:8501
```

---

## 📊 Usage Flow
1. Log in (credentials from `config.yaml`)
2. Upload or use `assets/servers.xlsx`
3. Click **Run Health Checks**
4. View results:
   - One row per server
   - Status: ✅ Healthy, ❌ Error, ⏳ Pending
   - Details list failing modules
5. Filter by OS Type or Status
6. Export results as Excel

---

## 📩 Notes
- Works best when run from a **central controller VM** that can reach other target servers
- Make sure `.pem` files have proper permissions (`chmod 600 key.pem`)
- For new servers, update Excel file and re-run

---

## 🏷️ Example Output

| Hostname   | Status    | OS Type | Output     | Details                                |
|------------|-----------|---------|------------|----------------------------------------|
| TM1Ubuntu  | ✅ Healthy| Linux   | TM1Ubuntu  | All checks passed ✅                    |
| WinServer1 | ❌ Error  | Windows | WinServer1 | • Connectivity: Timeout<br>• Logs: N/A |

---

## 👨‍💻 Author
Built with ❤️ for automating server health checks and reporting.
