import paramiko
import os

def run(server: dict) -> dict:
    """
    Check disk usage on a Linux server using PEM key authentication.
    Runs 'df -h' remotely.
    Requires: IP Address, Username, PEM File.
    """
    host = server.get("IP Address")
    port = int(server.get("Port", 22))
    username = server.get("Username")
    pem_file = server.get("PEM File")

    if not all([host, username, pem_file]):
        return {
            "Hostname": server.get("Hostname", "Unknown"),
            "Module": "Disk Usage",
            "Status": "Missing credentials (need IP, Username, PEM File)",
            "OS Type": server.get("OS Type", "")
        }

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        key = paramiko.RSAKey.from_private_key_file(pem_file)
        client.connect(hostname=host, port=port, username=username, pkey=key)

        stdin, stdout, stderr = client.exec_command("df -h")

        output = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()

        if errors:
            status = f"Error: {errors}"
        else:
            status = "OK"

    except Exception as e:
        status = f"Connection failed: {e}"
        output = ""

    finally:
        client.close()

    return {
        "Hostname": server.get("Hostname", "Unknown"),
        "Module": "Disk Usage",
        "Status": status,
        "OS Type": server.get("OS Type", ""),
        "Output": output
    }
