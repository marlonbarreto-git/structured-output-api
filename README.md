# structured-output-api

FastAPI service that converts free text into structured JSON using LLMs with Pydantic validation via [Instructor](https://github.com/jxnl/instructor).

## Features

- **Schema-based extraction**: Define Pydantic models, get validated structured data from any text
- **Pre-built schemas**: Contact info and invoice extraction out of the box
- **Instructor integration**: Automatic retries and validation via Instructor library
- **REST API**: FastAPI endpoints for extraction with OpenAPI docs
- **Schema registry**: List available schemas and their JSON schemas via API

## Architecture

```
structured_output_api/
├── schemas.py      # Pydantic models (ContactInfo, Invoice)
├── extractor.py    # LLM-powered extraction with Instructor
└── api.py          # FastAPI endpoints (/extract, /schemas, /health)
```

## Quick Start

```bash
# Install
uv sync

# Configure
export OPENAI_API_KEY="sk-..."

# Run server
uvicorn structured_output_api.api:app --reload

# Extract contact info
curl -X POST http://localhost:8000/extract/contact \
  -H "Content-Type: application/json" \
  -d '{"text": "Hi, I am John Doe from Acme Inc. Email: john@acme.com, Phone: +1-555-0123"}'

# List available schemas
curl http://localhost:8000/schemas
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/schemas` | List all extraction schemas with JSON schema |
| POST | `/extract/{schema_name}` | Extract structured data from text |

## Development

```bash
uv sync --all-extras
uv run pytest tests/ -v --cov=structured_output_api
```

## Roadmap

- **v2**: Dynamic schemas (user-defined Pydantic models via API), retry logic
- **v3**: Batch processing, streaming partial results, accuracy metrics per schema

## License

MIT
