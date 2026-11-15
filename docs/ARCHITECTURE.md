# Architecture

## Layers

1. Frontend — static HTML/CSS/JavaScript dashboard.
2. API — FastAPI endpoints for search, retrieval, sequence analysis and uploads.
3. NCBI adapter — asynchronous Entrez E-utilities client.
4. Analysis engines — independent DNA, RNA, protein and genome modules.
5. File services — FASTA and GenBank parsing with Biopython.
6. Integration layer (planned) — accession-aware mapping between genomic genes, transcripts and proteins.
7. Reporting layer (planned) — provenance-rich exports.

## Current API

- GET /api/health
- POST /api/ncbi/search
- GET /api/ncbi/fetch
- POST /api/analyze/sequence
- POST /api/analyze/compare
- POST /api/files/analyze
- GET /docs

## Development principles

- Keep source annotations separate from computed statistics and predictions.
- Preserve accession identifiers and source metadata.
- Validate molecule type and sequence alphabet before analysis.
- Apply upload limits and NCBI request timeouts.
- Keep API credentials in environment variables.
- Add tests for every analysis engine and API route.
