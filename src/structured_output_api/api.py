"""FastAPI application for structured data extraction."""

import os
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from structured_output_api import __version__
from structured_output_api.extractor import Extractor
from structured_output_api.schemas import SCHEMA_REGISTRY

app = FastAPI(
    title="Structured Output API",
    description="Convert free text into structured JSON using LLMs with Pydantic validation.",
    version=__version__,
)


class ExtractionRequest(BaseModel):
    text: str = Field(min_length=1, description="Text to extract data from")
    model: str | None = Field(default=None, description="LLM model to use")

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v


@lru_cache
def get_extractor() -> Extractor:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    return Extractor(openai_api_key=api_key)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": __version__}


@app.get("/schemas")
async def list_schemas():
    return {
        name: schema.model_json_schema()
        for name, schema in SCHEMA_REGISTRY.items()
    }


@app.post("/extract/{schema_name}")
async def extract(schema_name: str, request: ExtractionRequest):
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
        "latency_ms": round(result.latency_ms, 1),
    }
