"""Tests for the LLM-powered data extractor."""

from unittest.mock import AsyncMock, patch

import pytest

from structured_output_api.extractor import Extractor, ExtractionResult
from structured_output_api.schemas import ContactInfo


class TestExtractor:
    @pytest.mark.asyncio
    async def test_extract_contact_info(self):
        expected = ContactInfo(
            name="John Doe",
            email="john@acme.com",
            phone="+1-555-0123",
            company="Acme Inc",
        )

        with patch("structured_output_api.extractor.instructor") as mock_instructor:
            mock_client = AsyncMock()
            mock_client.chat.completions.create.return_value = expected
            mock_instructor.from_openai.return_value = mock_client

            extractor = Extractor(openai_api_key="test-key")
            result = await extractor.extract(
                text="Hi, I'm John Doe from Acme Inc. Reach me at john@acme.com or +1-555-0123.",
                schema=ContactInfo,
            )

        assert isinstance(result, ExtractionResult)
        assert result.data.name == "John Doe"
        assert result.data.email == "john@acme.com"
        assert result.schema_name == "ContactInfo"
        assert result.model is not None

    @pytest.mark.asyncio
    async def test_extract_returns_metadata(self):
        expected = ContactInfo(name="Jane")

        with patch("structured_output_api.extractor.instructor") as mock_instructor:
            mock_client = AsyncMock()
            mock_client.chat.completions.create.return_value = expected
            mock_instructor.from_openai.return_value = mock_client

            extractor = Extractor(openai_api_key="test-key")
            result = await extractor.extract(text="Jane called.", schema=ContactInfo)

        assert result.latency_ms >= 0
        assert result.schema_name == "ContactInfo"

    @pytest.mark.asyncio
    async def test_extract_with_custom_model(self):
        expected = ContactInfo(name="Bob")

        with patch("structured_output_api.extractor.instructor") as mock_instructor:
            mock_client = AsyncMock()
            mock_client.chat.completions.create.return_value = expected
            mock_instructor.from_openai.return_value = mock_client

            extractor = Extractor(openai_api_key="test-key")
            result = await extractor.extract(
                text="Bob here.",
                schema=ContactInfo,
                model="gpt-4o",
            )

        assert result.data.name == "Bob"
