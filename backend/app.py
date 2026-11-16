"""FastAPI application for NCBI BioIntelligence."""
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from Bio.Align import PairwiseAligner

from backend.analysis.common import validate_sequence
from backend.analysis.dna import analyze_dna
from backend.analysis.rna import analyze_rna
from backend.analysis.protein import analyze_protein
from backend.analysis.genome import summarize_genbank_record
from backend.config import settings
from backend.models import SequenceRequest, CompareRequest, NCBISearchRequest
from backend.ncbi.client import ncbi_client, NCBIError
from backend.services.file_parser import parse_records
from backend.structures.rcsb import (
    StructureNotFound,
    StructureProviderError,
    fetch_rcsb_mmcif,
)

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
app = FastAPI(
    title=settings.app_name,
    version="0.2.0-dev",
    description="Research-support bioinformatics workstation with a molecular structure explorer preview.",
)
app.mount("/static", StaticFiles(directory=FRONTEND / "static"), name="static")


@app.get("/", include_in_schema=False)
async def dashboard():
    return FileResponse(FRONTEND / "index.html")


@app.get("/api/health")
async def health():
    return {"status": "ok", "application": settings.app_name, "version": app.version}


@app.post("/api/ncbi/search")
async def ncbi_search(request: NCBISearchRequest):
    try:
        return await ncbi_client.search(request.database, request.term, request.limit)
    except NCBIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/api/ncbi/fetch")
async def ncbi_fetch(
    database: str = Query("nuccore"),
    identifier: str = Query(..., min_length=1),
    rettype: str = Query("fasta"),
):
    if database not in {"nuccore", "protein", "gene", "genome"}:
        raise HTTPException(status_code=400, detail="Unsupported NCBI database.")
    if rettype not in {"fasta", "gb", "gbwithparts", "xml"}:
        raise HTTPException(status_code=400, detail="Unsupported record format.")
    try:
        return {
            "database": database,
            "identifier": identifier,
            "record": await ncbi_client.fetch(database, identifier, rettype),
        }
    except NCBIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/api/structures/rcsb/{pdb_id}")
async def get_rcsb_structure(pdb_id: str):
    """Retrieve an existing coordinate-bearing mmCIF file from RCSB PDB."""
    try:
        return await fetch_rcsb_mmcif(
            pdb_id,
            timeout_seconds=settings.request_timeout_seconds,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except StructureNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except StructureProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/api/analyze/sequence")
async def analyze_sequence(request: SequenceRequest):
    try:
        sequence, molecule = validate_sequence(request.sequence, request.molecule)
        result = (
            analyze_dna(sequence)
            if molecule == "dna"
            else analyze_rna(sequence)
            if molecule == "rna"
            else analyze_protein(sequence)
        )
        result.update({"sequence_id": request.sequence_id, "analysis_type": "computed"})
        return result
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/analyze/compare")
async def compare_sequences(request: CompareRequest):
    try:
        a, kind_a = validate_sequence(request.sequence_a, request.molecule)
        b, kind_b = validate_sequence(request.sequence_b, request.molecule)
        if kind_a != kind_b:
            raise ValueError("Both sequences must be the same molecule type.")
        aligner = PairwiseAligner()
        aligner.mode = "global"
        alignment = aligner.align(a, b)[0]
        return {
            "molecule": kind_a.upper(),
            "length_a": len(a),
            "length_b": len(b),
            "alignment_score": float(alignment.score),
            "aligned_blocks_a": alignment.aligned[0].tolist(),
            "aligned_blocks_b": alignment.aligned[1].tolist(),
            "method": "Biopython PairwiseAligner global alignment",
            "note": "Inspect the alignment for rigorous gap-aware identity calculations.",
        }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/files/analyze")
async def analyze_file(file: UploadFile = File(...)):
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the {settings.max_upload_mb} MB upload limit.",
        )
    try:
        fmt, records = parse_records(file.filename or "upload.fa", content)
        output = []
        for record in records:
            if fmt == "genbank":
                summary = summarize_genbank_record(record)
            else:
                seq, kind = validate_sequence(str(record.seq), "auto")
                summary = (
                    analyze_dna(seq)
                    if kind == "dna"
                    else analyze_rna(seq)
                    if kind == "rna"
                    else analyze_protein(seq)
                )
                summary.update({"record_id": record.id, "description": record.description})
            output.append(summary)
        return {
            "filename": file.filename,
            "format": fmt,
            "record_count": len(output),
            "records": output,
        }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api")
async def api_root():
    return {
        "message": "NCBI BioIntelligence API",
        "docs": "/docs",
        "health": "/api/health",
        "structure_viewer": "/api/structures/rcsb/{pdb_id}",
    }
