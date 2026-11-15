"""Build a provenance-aware report payload from analysis results."""
from datetime import datetime, timezone

def build_report(title: str, source_records: list[dict], analyses: list[dict], methods: list[str]) -> dict:
    return {
        "title": title,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_records": source_records,
        "analyses": analyses,
        "methods": methods,
        "interpretation_notice": "Computed results and source annotations are research aids; validate biological conclusions independently.",
    }
