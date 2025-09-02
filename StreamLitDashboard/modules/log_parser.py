# GEN_GEN_OS_D_C_LogAlertParser.py

import re
import os

def run(server: dict) -> dict:
    """Parse logs for critical entries."""
    log_path = server.get("Log Path")
    if not log_path or not os.path.exists(log_path):
        return {"Hostname": server["Hostname"], "Module": "Log Parser", "Status": "Pending"}

    keywords = ["ERROR", "CRITICAL", "FAILURE"]
    matches = []

    try:
        with open(log_path, "r") as log_file:
            for i, line in enumerate(log_file, start=1):
                if any(kw in line.upper() for kw in keywords):
                    matches.append(f"[Line {i}] {line.strip()}")

        status = "OK" if not matches else f"Alerts: {len(matches)}"
        return {"Hostname": server["Hostname"], "Module": "Log Parser", "Status": status}

    except Exception as e:
        return {"Hostname": server["Hostname"], "Module": "Log Parser", "Status": f"Error: {e}"}

