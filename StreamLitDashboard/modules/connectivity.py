# GEN_GEN_OS_D_C_ConnCheck.py

import socket

def run(server: dict) -> dict:
    """Check connectivity for given server IP."""
    host = server.get("IP Address")
    os_type = server.get("OS Type", "").lower()
    port = 22 if "linux" in os_type else 3389  # Linux:22 / Windows:3389

    try:
        with socket.create_connection((host, port), timeout=2):
            status = "OK"
    except Exception:
        status = "Connectivity Issue"

    return {
        "Hostname": server["Hostname"],
        "Module": "Connectivity",
        "Status": status,
        "OS Type": server.get("OS Type", "")
    }


