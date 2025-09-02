import pandas as pd

REQUIRED_COLUMNS = {"Hostname", "IP Address", "OS Type", "OS Version"}

def load_excel(uploaded_file):
    """Validate and return DataFrame if valid."""
    if not uploaded_file:
        return None

    df = pd.read_excel(uploaded_file)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")
    return df
