"""LLM-powered structured data extractor using Instructor."""

import time
from dataclasses import dataclass
from typing import TypeVar

import instructor
import openai
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

MS_PER_SECOND = 1000


@dataclass
class ExtractionResult:
    """Result of a structured extraction including metadata."""

    data: BaseModel
    schema_name: str
    model: str
    latency_ms: float


class Extractor:
    """Wraps an OpenAI client with Instructor to extract typed data from text."""

    def __init__(self, openai_api_key: str, default_model: str = "gpt-4o-mini") -> None:
        self._api_key = openai_api_key
        self._default_model = default_model

    async def extract(
        self,
        text: str,
        schema: type[T],
        model: str | None = None,
    ) -> ExtractionResult:
        """Extract structured data from text using the given Pydantic schema.

        Args:
            text: Free-form text to extract data from.
            schema: Pydantic model class defining the target structure.
            model: Optional LLM model override; defaults to ``gpt-4o-mini``.

        Returns:
            ExtractionResult containing the parsed data and metadata.
        """
        model = model or self._default_model
        client = instructor.from_openai(openai.AsyncOpenAI(api_key=self._api_key))

        start = time.perf_counter()
        result = await client.chat.completions.create(
            model=model,
            response_model=schema,
            messages=[
                {
                    "role": "system",
                    "content": "Extract structured data from the following text. "
                    "Only include information explicitly stated in the text.",
                },
                {"role": "user", "content": text},
            ],
        )
        elapsed = (time.perf_counter() - start) * MS_PER_SECOND

        return ExtractionResult(
            data=result,
            schema_name=schema.__name__,
            model=model,
            latency_ms=elapsed,
        )
