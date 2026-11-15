# NCBI BioIntelligence

An integrated bioinformatics workstation for **gene-level and whole-genome analysis**, with live NCBI search and biological file uploads.

## Initial capabilities

- Search NCBI Entrez databases (nucleotide, protein, gene, and genome).
- Retrieve NCBI records by accession or Entrez ID.
- Analyze DNA and RNA sequence composition, GC content, sequence length, and candidate open reading frames.
- Analyze protein sequence composition and molecular properties.
- Upload FASTA and GenBank files for local analysis.
- Compare two sequences with transparent identity and alignment statistics.
- Serve a web-based research dashboard through FastAPI.

> Research-support software, not a clinical diagnostic system. Computational results are not medical advice or experimentally validated conclusions.

## Quick start

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn backend.app:app --reload
```

Open http://127.0.0.1:8000.

Alternatively, run `python main.py`.

## NCBI configuration

Set `NCBI_EMAIL` to a monitored contact email before making sustained requests. Optional `NCBI_API_KEY` can be used for an NCBI API key. Configure these as environment variables; do not commit secrets.

## Project status

This is the initial foundation. The API, sequence-analysis primitives, upload parsing, and dashboard are being developed in staged modules. Advanced comparative genomics, transcript-to-gene mapping, large-genome workflows, BLAST orchestration, and richer visualizations are planned follow-on milestones.

## Supported inputs

- FASTA: `.fa`, `.fasta`, `.fna`, `.ffn`, `.faa`, `.frn`
- GenBank: `.gb`, `.gbk`, `.genbank`

Large genome files require streaming/chunked processing in a later milestone; the initial upload endpoint applies a configurable size limit.

## Scientific provenance

Keep accession identifiers, source database, retrieval date, software version, and analysis parameters with exported results. Distinguish source annotations from computed values and predictions.
