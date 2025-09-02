import paramiko
import os

def run(server: dict) -> dict:
    """
    Check if a background job/service is running on a Linux server.
    Uses systemctl is-active <TaskName>.
    Requires: IP Address, Username, PEM File, TaskName.
    """
    host = server.get("IP Address")
    port = int(server.get("Port", 22))
    username = server.get("Username")
    pem_file = server.get("PEM File")
    task_name = server.get("TaskName")

    if not all([host, username, pem_file, task_name]):
        return {
            "Hostname": server.get("Hostname", "Unknown"),
            "Module": "Job Status Check",
            "Status": "Missing credentials (need IP, Username, PEM File, TaskName)",
            "OS Type": server.get("OS Type", "")
        }

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        key = paramiko.RSAKey.from_private_key_file(pem_file)
        client.connect(hostname=host, port=port, username=username, pkey=key)

        command = f"systemctl is-active {task_name}"
        stdin, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()

        if errors:
            status = f"Error: {errors}"
        elif output == "active":
            status = "Running"
        else:
            status = f"Not Running ({output})"

    except Exception as e:
        status = f"Connection failed: {e}"
        output = ""

    finally:
        client.close()

    return {
        "Hostname": server.get("Hostname", "Unknown"),
        "Module": "Job Status Check",
        "Status": status,
        "OS Type": server.get("OS Type", ""),
        "Output": output
    }
