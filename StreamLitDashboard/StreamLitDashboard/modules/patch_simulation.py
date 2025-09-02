import time, random

def patch_server(_server_row):
    """Simulate patching with random outcome."""
    time.sleep(0.2)
    return random.choice(["Patched", "Failed", "Connectivity Issue"])

def rerun_failed(df):
    """Re-run patching only for failed servers."""
    df.loc[df["Status"] == "Failed", "Status"] = df[df["Status"] == "Failed"].apply(patch_server, axis=1)
    return df
