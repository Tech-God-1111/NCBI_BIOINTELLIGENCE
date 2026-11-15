"""DNA sequence statistics and candidate ORF discovery."""
from Bio.Seq import Seq
from backend.analysis.common import composition, validate_sequence

STOP_CODONS = {"TAA", "TAG", "TGA"}

def find_orfs(sequence: str, min_aa: int = 30) -> list[dict]:
    seq, _ = validate_sequence(sequence, "dna")
    results = []
    for strand, strand_seq in (("+", seq), ("-", str(Seq(seq).reverse_complement()))):
        for frame in range(3):
            i = frame
            while i + 3 <= len(strand_seq):
                if strand_seq[i:i+3] == "ATG":
                    j = i + 3
                    while j + 3 <= len(strand_seq) and strand_seq[j:j+3] not in STOP_CODONS:
                        j += 3
                    if j + 3 <= len(strand_seq):
                        aa_length = (j - i) // 3
                        if aa_length >= min_aa:
                            start, end = (i + 1, j + 3) if strand == "+" else (len(seq) - (j + 3) + 1, len(seq) - i)
                            results.append({"strand": strand, "frame": frame + 1, "start": start, "end": end, "protein_length_aa": aa_length})
                    i = j + 3
                else:
                    i += 3
    return results

def analyze_dna(sequence: str) -> dict:
    seq, _ = validate_sequence(sequence, "dna")
    counts = composition(seq)
    canonical = len(seq) - counts.get("N", 0)
    gc = ((counts.get("G", 0) + counts.get("C", 0)) / canonical * 100) if canonical else 0.0
    return {"molecule": "DNA", "length": len(seq), "composition": counts, "gc_percent": round(gc, 3), "ambiguous_bases": counts.get("N", 0), "candidate_orfs": find_orfs(seq), "notes": ["ORFs are sequence-based candidates, not confirmed genes or functional proteins."]}
