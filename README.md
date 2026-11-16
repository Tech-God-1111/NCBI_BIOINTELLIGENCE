# NCBI BioIntelligence

An integrated bioinformatics workstation for **gene-level and whole-genome analysis**, with live NCBI search, biological file uploads and an expanding molecular-structure explorer.

## Current capabilities

- Search NCBI Entrez databases (nucleotide, protein, gene, and genome).
- Retrieve NCBI records by accession or Entrez ID.
- Analyze DNA and RNA sequence composition, GC content, sequence length, and candidate open reading frames.
- Analyze protein sequence composition and molecular properties.
- Upload FASTA and GenBank files for local analysis.
- Compare two sequences with transparent identity and alignment statistics.
- Retrieve coordinate-bearing mmCIF structure records from the RCSB PDB archive by PDB identifier.
- Render archive structures in the browser using 3Dmol.js (V2.0 preview).
- Serve a web-based research workspace through FastAPI.

> Research-support software, not a clinical diagnostic system. Computational results are not medical advice or experimentally validated conclusions.

## Quick start

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn backend.app:app --reload
```

Open http://127.0.0.1:8000.

Alternatively, run `python main.py`.

## NCBI configuration

Set `NCBI_EMAIL` to a monitored contact email before making sustained requests. Optional `NCBI_API_KEY` can be used for an NCBI API key. Configure these as environment variables; do not commit secrets.

## Molecular structure explorer (V2.0 preview)

Open the **04 / Molecular Intelligence — 3D Structure Explorer** panel and enter a four-character PDB identifier. The backend retrieves the mmCIF coordinate file from the RCSB PDB archive and the browser renders it with 3Dmol.js.

Example identifiers included in the interface:

- `1CRN` — protein structure example.
- `1BNA` — DNA structure example.

The viewer requires an internet connection to load the 3Dmol.js browser library and retrieve archive coordinates.

### Structure API

- `GET /api/structures/rcsb/{pdb_id}`

The endpoint validates the identifier, retrieves coordinate-bearing mmCIF data, and returns provenance fields with an interpretation caveat. RCSB archive records can include different structure determination methods; archive presence alone does not establish that a structure was experimentally determined.

### Scientific boundary

A raw DNA, RNA or protein sequence is not a 3D coordinate model. The application must not generate a plausible-looking model and present it as the true structure of that sequence.

Planned V2 milestones include exact sequence-to-chain mapping, residue highlighting, AlphaFold DB prediction retrieval with confidence metadata, RNA secondary-structure prediction, and archive DNA/RNA structure workflows. Predictions and archive records must remain clearly distinguished.

See [V2.0 Structure Explorer](docs/V2_STRUCTURE_EXPLORER.md) and [Structure Validation Plan](docs/V2_STRUCTURE_VALIDATION.md).

## Project status

V1 sequence analysis and data retrieval form the working foundation. The `v2.0-structure-explorer-foundation` branch contains the initial RCSB retrieval API and interactive viewer preview. This is not yet a complete V2.0 release; automated tests and live viewer validation remain required.

## Supported inputs

- FASTA: `.fa`, `.fasta`, `.fna`, `.ffn`, `.faa`, `.frn`
- GenBank: `.gb`, `.gbk`, `.genbank`

Large genome files require streaming/chunked processing in a later milestone; the initial upload endpoint applies a configurable size limit.

## Scientific provenance

Keep accession identifiers, source database, retrieval date, software version, chain/residue mapping and analysis parameters with exported results. Distinguish source annotations from computed values and predictions.
