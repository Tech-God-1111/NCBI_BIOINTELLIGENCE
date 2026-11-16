"""RCSB PDB archive retrieval for molecular structure visualization.

This module retrieves existing coordinate files. It does not predict or invent
three-dimensional structures from primary sequences.
"""
import re
from typing import Any

import httpx

RCSB_CIF_URL = "https://files.rcsb.org/download/{pdb_id}.cif"
MAX_STRUCTURE_BYTES = 25 * 1024 * 1024
PDB_ID_PATTERN = re.compile(r"^[A-Za-z0-9]{4}$")


class StructureNotFound(RuntimeError):
    """Raised when the requested structure is absent from the archive."""


class StructureProviderError(RuntimeError):
    """Raised when the structure provider cannot be reached or parsed."""


def normalize_pdb_id(pdb_id: str) -> str:
    """Validate and normalize a four-character PDB archive identifier."""
    normalized = pdb_id.strip().upper()
    if not PDB_ID_PATTERN.fullmatch(normalized):
        raise ValueError("Enter a four-character PDB identifier, for example 1CRN or 1BNA.")
    return normalized


async def fetch_rcsb_mmcif(pdb_id: str, timeout_seconds: float = 30.0) -> dict[str, Any]:
    """Fetch an existing mmCIF coordinate file from the public RCSB archive."""
    normalized = normalize_pdb_id(pdb_id)
    url = RCSB_CIF_URL.format(pdb_id=normalized)
    content_buffer = bytearray()

    try:
        async with httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=True) as client:
            async with client.stream("GET", url) as response:
                if response.status_code == 404:
                    raise StructureNotFound(f"No RCSB PDB archive entry was found for {normalized}.")
                response.raise_for_status()

                declared_size = response.headers.get("content-length")
                if declared_size and declared_size.isdigit() and int(declared_size) > MAX_STRUCTURE_BYTES:
                    raise StructureProviderError(
                        f"The structure file exceeds the current {MAX_STRUCTURE_BYTES // (1024 * 1024)} MB retrieval limit."
                    )

                async for chunk in response.aiter_bytes():
                    content_buffer.extend(chunk)
                    if len(content_buffer) > MAX_STRUCTURE_BYTES:
                        raise StructureProviderError(
                            f"The structure file exceeds the current {MAX_STRUCTURE_BYTES // (1024 * 1024)} MB retrieval limit."
                        )
    except (StructureNotFound, StructureProviderError):
        raise
    except httpx.HTTPError as exc:
        raise StructureProviderError(f"RCSB structure retrieval failed: {exc}") from exc

    try:
        mmcif_text = bytes(content_buffer).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StructureProviderError("RCSB returned a structure file that is not valid UTF-8 text.") from exc

    if "_atom_site." not in mmcif_text or not mmcif_text.lstrip().startswith("data_"):
        raise StructureProviderError(
            "The downloaded file does not appear to contain a coordinate-bearing mmCIF structure."
        )

    return {
        "pdb_id": normalized,
        "format": "mmcif",
        "source": "RCSB PDB archive",
        "source_url": url,
        "structure_data": mmcif_text,
        "structure_classification": "archive_coordinate_record",
        "interpretation_note": (
            "This is an archived coordinate model. Check the RCSB entry metadata for its "
            "experimental or computational method; archive presence alone does not establish "
            "that a structure was experimentally determined."
        ),
    }
