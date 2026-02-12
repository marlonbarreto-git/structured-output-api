"""Tests for predefined extraction schemas."""

import pytest
from pydantic import ValidationError

from structured_output_api.schemas import ContactInfo, Invoice, InvoiceItem


class TestContactInfo:
    def test_valid_contact(self):
        contact = ContactInfo(
            name="John Doe",
            email="john@example.com",
            phone="+1-555-0123",
            company="Acme Inc",
        )
        assert contact.name == "John Doe"
        assert contact.email == "john@example.com"

    def test_optional_fields(self):
        contact = ContactInfo(name="Jane Doe")
        assert contact.name == "Jane Doe"
        assert contact.email is None
        assert contact.phone is None
        assert contact.company is None

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            ContactInfo(name="John", email="not-an-email")

    def test_model_json_schema(self):
        schema = ContactInfo.model_json_schema()
        assert "name" in schema["properties"]
        assert schema["properties"]["name"]["type"] == "string"


class TestInvoice:
    def test_valid_invoice(self):
        invoice = Invoice(
            invoice_number="INV-001",
            date="2026-01-15",
            total=150.00,
            currency="USD",
            vendor="Acme Corp",
            items=[
                InvoiceItem(description="Widget", quantity=3, unit_price=50.00),
            ],
        )
        assert invoice.total == 150.00
        assert len(invoice.items) == 1

    def test_empty_items_allowed(self):
        invoice = Invoice(
            invoice_number="INV-002",
            date="2026-02-01",
            total=0.0,
            currency="USD",
        )
        assert invoice.items == []
