# Structured Output API

[![CI](https://github.com/marlonbarreto-git/structured-output-api/actions/workflows/ci.yml/badge.svg)](https://github.com/marlonbarreto-git/structured-output-api/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

FastAPI service that converts free text into structured JSON using LLMs with Pydantic validation.

## Overview

Structured Output API takes unstructured text and extracts typed, validated data using LLMs powered by the Instructor library. It exposes a REST API with predefined schemas (contacts, invoices) and returns clean JSON that conforms to Pydantic models, eliminating the need to parse free-form LLM output manually.

## Architecture

```
HTTP Request (text + schema_name)
  |
  v
FastAPI Router (/extract/{schema_name})
  |
  v
Extractor (Instructor + OpenAI)
  |
  +---> LLM with structured output constraint
  |
  v
Pydantic Model Validation (ContactInfo, Invoice)
  |
  v
JSON Response (validated data + model + latency)
```

## Features

- Extract structured data from free text via REST API
- Pydantic-validated output schemas (ContactInfo, Invoice with line items)
- Schema registry for discovering available extraction types
- Instructor library for reliable structured LLM output
- Latency tracking per extraction request
- Health check and schema introspection endpoints

## Tech Stack

- Python 3.11+
- FastAPI + Uvicorn
- Instructor (structured LLM output)
- OpenAI SDK
- Pydantic

## Quick Start

```bash
git clone https://github.com/marlonbarreto-git/structured-output-api.git
cd structured-output-api
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
export OPENAI_API_KEY=your-key
uvicorn structured_output_api.api:app --reload
```

## Project Structure

```
src/structured_output_api/
  __init__.py
  api.py          # FastAPI app with /extract, /schemas, /health endpoints
  extractor.py    # LLM-powered extraction using Instructor
  schemas.py      # Pydantic models (ContactInfo, Invoice) and registry
tests/
  test_api.py
  test_extractor.py
  test_schemas.py
```

## Testing

```bash
pytest -v --cov=src/structured_output_api
```

13 tests covering API endpoints, extraction logic, and schema validation.

## License

MIT