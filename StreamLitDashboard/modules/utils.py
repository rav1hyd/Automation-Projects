def status_badge(status: str) -> str:
    """Return colored HTML badge for status values."""
    color_map = {
        "Patched": "green",
        "Failed": "red",
        "Connectivity Issue": "orange",
        "Pending": "gray",
    }
    color = color_map.get(status, "gray")
    return f"<span style='color:white; background-color:{color}; padding:4px 8px; border-radius:8px;'>{status}</span>"
