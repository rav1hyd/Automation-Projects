import winrm

def run(server: dict) -> dict:
    """
    Execute a remote PowerShell command via WinRM.
    Requires IP Address, Username, Password, and Command in server dict.
    """
    host = server.get("IP Address")
    username = server.get("Username")
    password = server.get("Password")
    command = server.get("Command", "hostname")  # default command

    if not all([host, username, password]):
        return {
            "Hostname": server.get("Hostname", "Unknown"),
            "Module": "WinRM Executor",
            "Status": "Missing credentials",
            "OS Type": server.get("OS Type", "")
        }

    try:
        session = winrm.Session(
            f"http://{host}:5985/wsman",
            auth=(username, password)
        )
        result = session.run_cmd(command)

        if result.status_code == 0:
            status = "OK"
        else:
            status = f"Failed (Code {result.status_code})"

    except Exception as e:
        status = f"Error: {e}"

    return {
        "Hostname": server.get("Hostname", "Unknown"),
        "Module": "WinRM Executor",
        "Status": status,
        "OS Type": server.get("OS Type", "")
    }
