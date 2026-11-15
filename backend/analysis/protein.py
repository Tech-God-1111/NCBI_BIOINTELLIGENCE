"""Protein sequence composition and basic physicochemical estimates."""
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from backend.analysis.common import composition, validate_sequence

def analyze_protein(sequence: str) -> dict:
    seq, _ = validate_sequence(sequence, "protein")
    seq = seq.rstrip("*")
    if not seq or "*" in seq:
        raise ValueError("Protein sequence must contain amino-acid symbols only; internal stop symbols are not accepted.")
    analysis = ProteinAnalysis(seq)
    return {"molecule": "PROTEIN", "length_aa": len(seq), "amino_acid_composition": composition(seq), "molecular_weight_da": round(analysis.molecular_weight(), 3), "isoelectric_point_estimate": round(analysis.isoelectric_point(), 3), "aromaticity": round(analysis.aromaticity(), 4), "instability_index_estimate": round(analysis.instability_index(), 3), "notes": ["Physicochemical values are sequence-derived estimates, not experimental measurements."]}
