# V2.0 — Molecular Structure Explorer

## Objective

Add scientifically traceable molecular structure exploration to NCBI BioIntelligence while preserving the existing V1 sequence-analysis workflows.

V2.0 must distinguish:

1. **Archive coordinates** — coordinate models retrieved from a structural archive such as RCSB PDB.
2. **Predicted structures** — computational models retrieved from a prediction resource such as AlphaFold DB, with confidence metadata retained.
3. **Visual explanations** — schematic illustrations that are explicitly labelled as illustrative and are never presented as molecular coordinates.

A primary sequence by itself is not a coordinate model. The application must not draw a plausible-looking 3D molecule and imply that it is the actual structure of the submitted sequence.

## Initial foundation delivered on this branch

- A dedicated `backend/structures/` package.
- An RCSB PDB mmCIF retrieval service using the official archive download endpoint.
- Four-character PDB identifier validation and normalization.
- A 25 MB retrieval ceiling and basic coordinate-file validation.
- Provenance fields in the API response, including source, identifier, format and interpretation note.
- A planned dashboard viewer integration using 3Dmol.js.

## Planned milestones

### V2.0-A — Archive structure viewer

- Retrieve coordinate-bearing mmCIF files from RCSB PDB.
- Render structures in the browser with 3Dmol.js.
- Provide cartoon, stick and sphere representations where supported.
- Support rotation, zoom, reset and clear loading/error states.
- Display PDB identifier, source and archive-method caveat.
- Allow user-uploaded PDB/mmCIF files after file-size and content validation.

### V2.0-B — Sequence-to-structure mapping

- Connect a selected protein sequence to an exact archive entity/chain only when sequence identity and coverage are computed and reported.
- Highlight selected residues in both the sequence and 3D viewer.
- Preserve chain identifiers, residue numbering and insertion codes.
- Never infer residue correspondence from approximate name matching.

### V2.0-C — Protein prediction records

- Query AlphaFold DB through its documented prediction API using a UniProt accession.
- Read coordinate URLs and model-version metadata from the API response rather than hardcoding versioned filenames.
- Display pLDDT and PAE context when available.
- Label every such result as a prediction, not an experimental structure.
- Do not claim that every arbitrary sequence has a matching AlphaFold entry.

### V2.0-D — RNA and DNA structural workflows

- Support retrieval and viewing of archive nucleic-acid structures.
- Add RNA secondary-structure prediction through a separately installed/configured ViennaRNA workflow, with parameters and prediction status recorded.
- Treat RNA secondary structure (base-pairing) separately from a full atomic 3D coordinate model.
- For DNA, support archive structures and clearly labelled sequence-derived diagrams; do not claim a general-purpose, validated 3D DNA predictor without a suitable scientific method.

### V2.0-E — Scientific reporting and validation

- Include source database, accession, retrieval timestamp, model method, chain, residue mapping method and software version.
- Add tests for invalid identifiers, missing entries, malformed mmCIF, oversized responses and provider/network failures.
- Add integration tests with mocked provider responses.
- Validate viewer loading with representative protein and nucleic-acid archive entries.
- Keep predictions and experimental/archive records visibly distinct throughout exports.

## Technology choices

| Area | Initial choice | Role |
|---|---|---|
| Browser molecular rendering | 3Dmol.js | Interactive PDB/mmCIF visualization |
| Experimental/archive coordinates | RCSB PDB | Existing structure records |
| Protein prediction records | AlphaFold DB API | Existing predicted protein models |
| RNA secondary structure | ViennaRNA | Base-pairing/folding prediction |
| Sequence parsing and analysis | Biopython | Existing sequence workflows |

## API foundation

- `GET /api/structures/rcsb/{pdb_id}` — retrieve a coordinate-bearing mmCIF record from RCSB PDB.

The endpoint returns the source identifier, format, coordinate text and an interpretation caveat. It does not claim to determine the experimental method; that must be read from the corresponding archive metadata before scientific interpretation.

## Scope boundary

This milestone is a research and education tool. It is not a clinical interpretation system, and visual appearance must never be treated as evidence of biological function or pathogenicity.
