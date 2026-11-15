"""Data models and helpers for connecting biological record layers.

A future integration workflow will resolve NCBI gene, nucleotide, transcript,
and protein accessions while retaining the source of each relationship.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class BiologicalRecordLink:
    source_database: str
    source_accession: str
    relationship: str
    target_database: str
    target_accession: str
    evidence_source: str

    def as_dict(self) -> dict[str, str]:
        return {
            "source_database": self.source_database,
            "source_accession": self.source_accession,
            "relationship": self.relationship,
            "target_database": self.target_database,
            "target_accession": self.target_accession,
            "evidence_source": self.evidence_source,
        }
