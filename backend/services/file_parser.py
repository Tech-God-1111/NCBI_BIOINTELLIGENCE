"""Parse uploaded FASTA and GenBank files using Biopython."""
from io import StringIO
from Bio import SeqIO
SUPPORTED_FORMATS = {".fa":"fasta", ".fasta":"fasta", ".fna":"fasta", ".ffn":"fasta", ".faa":"fasta", ".frn":"fasta", ".gb":"genbank", ".gbk":"genbank", ".genbank":"genbank"}

def parse_records(filename: str, content: bytes):
    suffix = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    fmt = SUPPORTED_FORMATS.get(suffix)
    if not fmt:
        raise ValueError("Unsupported file extension. Upload FASTA or GenBank.")
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("File must be UTF-8 text.") from exc
    records = list(SeqIO.parse(StringIO(text), fmt))
    if not records:
        raise ValueError("No valid biological records were found in the file.")
    return fmt, records
