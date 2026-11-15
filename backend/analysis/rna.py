"""RNA sequence statistics."""
from backend.analysis.common import composition, validate_sequence

def analyze_rna(sequence: str) -> dict:
    seq, _ = validate_sequence(sequence, "rna")
    counts = composition(seq)
    canonical = len(seq) - counts.get("N", 0)
    gc = ((counts.get("G", 0) + counts.get("C", 0)) / canonical * 100) if canonical else 0.0
    return {"molecule": "RNA", "length": len(seq), "composition": counts, "gc_percent": round(gc, 3), "uracil_count": counts.get("U", 0), "ambiguous_bases": counts.get("N", 0)}
