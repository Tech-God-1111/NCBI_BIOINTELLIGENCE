"""Shared request and response models."""
from pydantic import BaseModel, Field

class SequenceRequest(BaseModel):
    sequence: str = Field(min_length=1, max_length=2_000_000)
    molecule: str = Field(default="auto", pattern="^(auto|dna|rna|protein)$")
    sequence_id: str | None = None

class CompareRequest(BaseModel):
    sequence_a: str = Field(min_length=1, max_length=500_000)
    sequence_b: str = Field(min_length=1, max_length=500_000)
    molecule: str = Field(default="auto", pattern="^(auto|dna|rna|protein)$")

class NCBISearchRequest(BaseModel):
    term: str = Field(min_length=1, max_length=300)
    database: str = Field(default="nuccore", pattern="^(nuccore|protein|gene|genome)$")
    limit: int = Field(default=10, ge=1, le=50)
