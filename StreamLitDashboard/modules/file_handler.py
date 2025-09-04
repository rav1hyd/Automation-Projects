import pandas as pd

# Required columns for PEM-based SSH health checks
REQUIRED_COLUMNS = {"Hostname", "IP Address", "OS Type", "Username", "PEM File"}

def load_excel(uploaded_file):
    """Validate and return DataFrame if valid."""
    if not uploaded_file:
        return None

    df = pd.read_excel(uploaded_file)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    return df
