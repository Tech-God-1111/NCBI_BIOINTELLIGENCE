# V2.0 Structure Validation Plan

## Archive retrieval

| Case | Expected behavior |
|---|---|
| Valid PDB identifier with coordinate mmCIF | Return source, ID, format and coordinate text |
| Invalid identifier | HTTP 422 |
| Identifier absent from RCSB | HTTP 404 |
| RCSB unavailable or times out | HTTP 502 |
| Response larger than retrieval ceiling | HTTP 502 |
| Response is not coordinate-bearing mmCIF | HTTP 502 |

## Viewer checks

- Protein example: 1CRN.
- Nucleic-acid example: 1BNA.
- Verify loading, rotation, zoom, representation changes and reset.
- Confirm that a missing CDN/WebGL dependency produces a readable error instead of a blank panel.

## Scientific checks

- Viewer metadata must show the exact source and accession.
- Do not label all RCSB records as experimental; inspect the entry's method metadata.
- Predictions must be labelled as predictions and retain confidence metadata when available.
- A sequence-to-chain link must report alignment identity and coverage before enabling residue highlighting.
- No generated schematic may be represented as a coordinate-derived molecular structure.
