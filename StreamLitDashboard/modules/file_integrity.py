# GEN_GEN_OS_D_C_FileChangeCheck.py

import hashlib, os, json

HASH_STORE = "file_hashes.json"

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""): sha256.update(chunk)
    return sha256.hexdigest()

def run(server: dict) -> dict:
    """Check file integrity if File Path provided in Excel."""
    file_path = server.get("File Path")
    if not file_path or not os.path.exists(file_path):
        return {"Hostname": server["Hostname"], "Module": "File Integrity", "Status": "Pending"}

    try:
        hashes = {}
        if os.path.exists(HASH_STORE):
            with open(HASH_STORE, "r") as f: hashes = json.load(f)

        file_name = os.path.basename(file_path)
        new_hash = calculate_sha256(file_path)
        old_hash = hashes.get(file_name)

        if old_hash is None:
            status = "New File"
        elif old_hash != new_hash:
            status = "Changed"
        else:
            status = "OK"

        hashes[file_name] = new_hash
        with open(HASH_STORE, "w") as f: json.dump(hashes, f, indent=4)
        return {"Hostname": server["Hostname"], "Module": "File Integrity", "Status": status}
    except Exception as e:
        return {"Hostname": server["Hostname"], "Module": "File Integrity", "Status": f"Error: {e}"}

