"""Helpers for reproducible analysis provenance."""
from datetime import datetime, timezone
import platform
from Bio import __version__ as biopython_version

def build_provenance(source: str, accession: str | None = None, parameters: dict | None = None) -> dict:
    return {"source": source, "accession": accession, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(), "python_version": platform.python_version(), "biopython_version": biopython_version, "parameters": parameters or {}}
