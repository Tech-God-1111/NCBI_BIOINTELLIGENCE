"""Shared sequence validation and normalization."""
from collections import Counter
DNA = set("ACGTN")
RNA = set("ACGUN")
PROTEIN = set("ABCDEFGHIKLMNPQRSTVWXYZJUO*")

def normalize_sequence(sequence: str) -> str:
    return "".join(sequence.split()).upper().replace("-", "").replace(".", "")

def detect_molecule(sequence: str) -> str:
    seq = normalize_sequence(sequence)
    if not seq:
        raise ValueError("Sequence is empty.")
    letters = set(seq)
    if letters <= DNA:
        return "dna"
    if letters <= RNA:
        return "rna"
    if letters <= PROTEIN:
        return "protein"
    raise ValueError("Sequence contains unsupported characters for DNA, RNA, or protein.")

def validate_sequence(sequence: str, molecule: str = "auto") -> tuple[str, str]:
    seq = normalize_sequence(sequence)
    detected = detect_molecule(seq)
    chosen = detected if molecule == "auto" else molecule
    allowed = {"dna": DNA, "rna": RNA, "protein": PROTEIN}[chosen]
    if not set(seq) <= allowed:
        raise ValueError(f"Sequence contains symbols not valid for {chosen.upper()}.")
    return seq, chosen

def composition(sequence: str) -> dict[str, int]:
    return dict(sorted(Counter(sequence).items()))
