"""FastAPI application for structured data extraction."""

import os
from functools import lru_cache
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from structured_output_api import __version__
from structured_output_api.extractor import Extractor
from structured_output_api.schemas import SCHEMA_REGISTRY

LATENCY_DECIMAL_PLACES = 1

app = FastAPI(
    title="Structured Output API",
    description="Convert free text into structured JSON using LLMs with Pydantic validation.",
    version=__version__,
)


class ExtractionRequest(BaseModel):
    """Incoming request payload for the /extract endpoint."""

    text: str = Field(min_length=1, description="Text to extract data from")
    model: str | None = Field(default=None, description="LLM model to use")

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        """Reject text that is only whitespace."""
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v


@lru_cache
def get_extractor() -> Extractor:
    """Return a cached Extractor instance configured from environment variables."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    return Extractor(openai_api_key=api_key)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return service health status and version."""
    return {"status": "healthy", "version": __version__}


@app.get("/schemas")
async def list_schemas() -> dict[str, Any]:
    """Return JSON Schema definitions for all registered extraction schemas."""
    return {
        name: schema.model_json_schema()
        for name, schema in SCHEMA_REGISTRY.items()
    }


@app.post("/extract/{schema_name}")
async def extract(schema_name: str, request: ExtractionRequest) -> dict[str, Any]:
    """Extract structured data from text using the specified schema.

    Args:
        schema_name: Key in the schema registry to use for extraction.
        request: Request body containing the text and optional model override.

    Returns:
        Extracted data, schema name, model used, and latency in milliseconds.
    """
    if schema_name not in SCHEMA_REGISTRY:
        raise HTTPException(
            status_code=404,
            detail=f"Schema '{schema_name}' not found. Available: {list(SCHEMA_REGISTRY.keys())}",
        )

    schema = SCHEMA_REGISTRY[schema_name]
    extractor = get_extractor()

    result = await extractor.extract(
        text=request.text,
        schema=schema,
        model=request.model,
    )

    return {
        "data": result.data.model_dump(),
        "schema_name": result.schema_name,
        "model": result.model,
        "latency_ms": round(result.latency_ms, LATENCY_DECIMAL_PLACES),
    }
