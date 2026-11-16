"""Tests for the molecular structure retrieval foundation."""
import pytest

from backend.structures.rcsb import normalize_pdb_id


def test_normalize_pdb_id_trims_and_uppercases():
    assert normalize_pdb_id(" 1crn ") == "1CRN"


@pytest.mark.parametrize("value", ["", "123", "12345", "1 CR", "AB!D", "1CRN.cif"])
def test_normalize_pdb_id_rejects_invalid_identifiers(value):
    with pytest.raises(ValueError):
        normalize_pdb_id(value)
