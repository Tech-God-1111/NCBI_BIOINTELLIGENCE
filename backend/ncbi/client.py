"""Asynchronous NCBI E-utilities client. See https://www.ncbi.nlm.nih.gov/books/NBK25501/."""
from typing import Any
import json
import httpx
from backend.config import settings

class NCBIError(RuntimeError):
    pass

class NCBIClient:
    def __init__(self) -> None:
        self.base_url = settings.ncbi_base_url.rstrip("/")
        self.timeout = settings.request_timeout_seconds

    def _common_params(self) -> dict[str, str]:
        params = {"tool": settings.ncbi_tool}
        if settings.ncbi_email:
            params["email"] = settings.ncbi_email
        if settings.ncbi_api_key:
            params["api_key"] = settings.ncbi_api_key
        return params

    async def _get(self, endpoint: str, params: dict[str, Any]) -> str:
        query = {**self._common_params(), **params}
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.get(f"{self.base_url}/{endpoint}.fcgi", params=query)
                response.raise_for_status()
                return response.text
        except httpx.HTTPError as exc:
            raise NCBIError(f"NCBI request failed: {exc}") from exc

    async def search(self, database: str, term: str, limit: int = 10) -> dict[str, Any]:
        text = await self._get("esearch", {"db": database, "term": term, "retmax": limit, "retmode": "json"})
        try:
            data = json.loads(text)["esearchresult"]
            return {"database": database, "query": term, "count": int(data.get("count", 0)), "ids": data.get("idlist", []), "translation": data.get("querytranslation", "")}
        except (ValueError, KeyError, TypeError) as exc:
            raise NCBIError("NCBI returned an unexpected search response.") from exc

    async def fetch(self, database: str, identifier: str, rettype: str = "fasta") -> str:
        return await self._get("efetch", {"db": database, "id": identifier, "rettype": rettype, "retmode": "text"})

ncbi_client = NCBIClient()
