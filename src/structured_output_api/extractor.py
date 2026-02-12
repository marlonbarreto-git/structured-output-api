"""LLM-powered structured data extractor using Instructor."""

import time
from dataclasses import dataclass
from typing import TypeVar

import instructor
import openai
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@dataclass
class ExtractionResult:
    data: BaseModel
    schema_name: str
    model: str
    latency_ms: float


class Extractor:
    def __init__(self, openai_api_key: str, default_model: str = "gpt-4o-mini"):
        self._api_key = openai_api_key
        self._default_model = default_model

    async def extract(
        self,
        text: str,
        schema: type[T],
        model: str | None = None,
    ) -> ExtractionResult:
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
        elapsed = (time.perf_counter() - start) * 1000

        return ExtractionResult(
            data=result,
            schema_name=schema.__name__,
            model=model,
            latency_ms=elapsed,
        )
