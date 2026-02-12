"""Structured Output API - Convert free text to structured JSON using LLMs."""

__all__ = [
    "ContactInfo",
    "ExtractionResult",
    "Extractor",
    "Invoice",
    "InvoiceItem",
    "SCHEMA_REGISTRY",
]

__version__ = "0.1.0"

from .extractor import ExtractionResult, Extractor
from .schemas import SCHEMA_REGISTRY, ContactInfo, Invoice, InvoiceItem
