# GEN_GEN_DB_D_C_ExcelUpdater.py

from openpyxl import load_workbook

def run(server: dict) -> dict:
    """Demo: just check if Excel file is accessible."""
    file_path = server.get("Excel File")
    if not file_path:
        return {"Hostname": server["Hostname"], "Module": "Excel Updater", "Status": "Pending"}

    try:
        wb = load_workbook(file_path)
        wb.close()
        status = "OK"
    except Exception as e:
        status = f"Error: {e}"

    return {"Hostname": server["Hostname"], "Module": "Excel Updater", "Status": status}

