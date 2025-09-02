import platform
import psutil
import shutil

def get_os_info():
    return {
        "System": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Architecture": platform.machine()
    }

def get_cpu_info():
    return {
        "Cores (Logical)": psutil.cpu_count(logical=True),
        "Cores (Physical)": psutil.cpu_count(logical=False),
        "CPU Usage (%)": psutil.cpu_percent(interval=1)
    }

def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "Total (GB)": round(mem.total / (1024**3), 2),
        "Used (GB)": round(mem.used / (1024**3), 2),
        "Free (GB)": round(mem.available / (1024**3), 2),
        "Memory Usage (%)": mem.percent
    }

def get_disk_info():
    disk = psutil.disk_usage('/')
    return {
        "Total (GB)": round(disk.total / (1024**3), 2),
        "Used (GB)": round(disk.used / (1024**3), 2),
        "Free (GB)": round(disk.free / (1024**3), 2),
        "Disk Usage (%)": disk.percent
    }

def run(server: dict) -> dict:
    """Collects inventory details and returns summary status."""
    try:
        os_info = get_os_info()
        cpu_info = get_cpu_info()
        memory_info = get_memory_info()
        disk_info = get_disk_info()

        # Here you can return detailed info if needed,
        # but for dashboard we summarize as "OK"
        status = "OK"

        return {
            "Hostname": server["Hostname"],
            "Module": "Inventory Report",
            "Status": status,
            "OS Type": os_info.get("System", ""),
            "Details": {
                "OS": os_info,
                "CPU": cpu_info,
                "Memory": memory_info,
                "Disk": disk_info
            }
        }

    except Exception as e:
        return {
            "Hostname": server["Hostname"],
            "Module": "Inventory Report",
            "Status": f"Error: {e}",
            "OS Type": server.get("OS Type", "")
        }
