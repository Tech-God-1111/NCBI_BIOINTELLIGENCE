import pytest
from backend.analysis.dna import analyze_dna
from backend.analysis.rna import analyze_rna
from backend.analysis.protein import analyze_protein
from backend.analysis.common import validate_sequence

def test_dna_gc_content():
    result = analyze_dna("AACCGGTT")
    assert result["length"] == 8
    assert result["gc_percent"] == 50.0

def test_rna_uses_uracil():
    result = analyze_rna("AAACCCGGGUUU")
    assert result["uracil_count"] == 3
    assert result["gc_percent"] == 50.0

def test_protein_properties():
    result = analyze_protein("MKWVTFISLL")
    assert result["length_aa"] == 10
    assert result["molecular_weight_da"] > 0

def test_invalid_sequence_rejected():
    with pytest.raises(ValueError):
        validate_sequence("ACGT123", "dna")
