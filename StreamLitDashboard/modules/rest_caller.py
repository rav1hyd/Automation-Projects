import requests

def run(server: dict) -> dict:
    """Call REST API based on server details."""
    url = server.get("API Endpoint")
    method = server.get("API Method", "GET")  # default GET
    payload = server.get("API Payload")
    headers = server.get("API Headers")

    if not url:
        return {"Hostname": server["Hostname"], "Module": "REST Caller", "Status": "Pending"}

    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=payload)
        else:
            return {"Hostname": server["Hostname"], "Module": "REST Caller", "Status": "Unsupported Method"}

        status = f"{response.status_code}"
        return {"Hostname": server["Hostname"], "Module": "REST Caller", "Status": status}

    except Exception as e:
        return {"Hostname": server["Hostname"], "Module": "REST Caller", "Status": f"Error: {e}"}
