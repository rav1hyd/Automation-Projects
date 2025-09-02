# GEN_GEN_OS_D_C_ConfigParser.py

import json
import yaml
import configparser
import xml.etree.ElementTree as ET
import os

def run(server: dict) -> dict:
    """Check if config file (if provided in server dict) is parsable."""
    file_path = server.get("Config File")
    if not file_path or not os.path.exists(file_path):
        return {"Hostname": server["Hostname"], "Module": "Config Parser", "Status": "Pending"}

    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".json":
            with open(file_path) as f: json.load(f)
        elif ext in [".yaml", ".yml"]:
            with open(file_path) as f: yaml.safe_load(f)
        elif ext == ".ini":
            config = configparser.ConfigParser(); config.read(file_path)
        elif ext == ".xml":
            ET.parse(file_path)
        else:
            return {"Hostname": server["Hostname"], "Module": "Config Parser", "Status": "Unsupported File"}
        return {"Hostname": server["Hostname"], "Module": "Config Parser", "Status": "OK"}
    except Exception as e:
        return {"Hostname": server["Hostname"], "Module": "Config Parser", "Status": f"Error: {e}"}

