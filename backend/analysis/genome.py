"""Genome-level summary helpers for parsed GenBank records."""
from backend.analysis.dna import analyze_dna

def summarize_genbank_record(record) -> dict:
    result = analyze_dna(str(record.seq).upper())
    features = getattr(record, "features", [])
    result.update({"record_id": record.id, "description": record.description, "organism": record.annotations.get("organism", "Unknown"), "topology": record.annotations.get("topology", "Unknown"), "feature_count": len(features), "annotated_gene_count": sum(f.type == "gene" for f in features), "coding_sequence_count": sum(f.type == "CDS" for f in features), "source": "Uploaded GenBank record"})
    return result
