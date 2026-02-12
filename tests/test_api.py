"""Tests for the FastAPI endpoints."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from structured_output_api.api import app
from structured_output_api.extractor import ExtractionResult
from structured_output_api.schemas import ContactInfo


class TestAPI:
    @pytest.mark.asyncio
    async def test_health_check(self):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_extract_contact(self):
        mock_result = ExtractionResult(
            data=ContactInfo(name="John Doe", email="john@example.com"),
            schema_name="ContactInfo",
            model="gpt-4o-mini",
            latency_ms=150.0,
        )

        with patch("structured_output_api.api.get_extractor") as mock_get:
            mock_extractor = AsyncMock()
            mock_extractor.extract.return_value = mock_result
            mock_get.return_value = mock_extractor

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/extract/contact",
                    json={"text": "Hi, I'm John Doe, john@example.com"},
                )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == "John Doe"
        assert data["data"]["email"] == "john@example.com"
        assert data["schema_name"] == "ContactInfo"

    @pytest.mark.asyncio
    async def test_extract_empty_text_returns_422(self):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/extract/contact", json={"text": ""})
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_list_schemas(self):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/schemas")
        assert response.status_code == 200
        schemas = response.json()
        assert "contact" in schemas
        assert "invoice" in schemas
