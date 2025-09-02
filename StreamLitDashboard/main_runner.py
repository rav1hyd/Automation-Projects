import pandas as pd
from modules import connectivity, config_parser, ssh_exec, winrm_exec
from modules import log_parser, inventory_report, excel_updater, rest_caller
from modules import job_status_check, file_integrity, disk_usage, email_notifier

MODULES = [connectivity,
    config_parser,
    ssh_exec,
    winrm_exec,
    log_parser,
    inventory_report,
    excel_updater,
    rest_caller,
    job_status_check,
    file_integrity,
    disk_usage,
    email_notifier]

def run_all(input_excel: str):
    """Run all module tests on uploaded Excel file."""
    df = pd.read_excel(input_excel)
    results = []

    for _, row in df.iterrows():
        server = row.to_dict()
        for module in MODULES:
            try:
                result = module.run(server)
            except Exception as e:
                result = {
                    "Hostname": server.get("Hostname", "Unknown"),
                    "Module": module.__name__,
                    "Status": f"Error: {e}",
                    "OS Type": server.get("OS Type", "")
                }
            results.append(result)

    return pd.DataFrame(results)
