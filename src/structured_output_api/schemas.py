"""Predefined extraction schemas for structured output."""

from pydantic import BaseModel, EmailStr, Field


class ContactInfo(BaseModel):
    """Contact information extracted from free text."""

    name: str = Field(description="Full name of the person")
    email: EmailStr | None = Field(default=None, description="Email address")
    phone: str | None = Field(default=None, description="Phone number")
    company: str | None = Field(default=None, description="Company or organization name")


class InvoiceItem(BaseModel):
    """Single line item within an invoice."""

    description: str = Field(description="Item description")
    quantity: int = Field(ge=1, description="Quantity of items")
    unit_price: float = Field(ge=0, description="Price per unit")


class Invoice(BaseModel):
    """Invoice data including header fields and line items."""

    invoice_number: str = Field(description="Invoice number or ID")
    date: str = Field(description="Invoice date (YYYY-MM-DD)")
    total: float = Field(ge=0, description="Total amount")
    currency: str = Field(default="USD", description="Currency code")
    vendor: str | None = Field(default=None, description="Vendor or seller name")
    items: list[InvoiceItem] = Field(default_factory=list, description="Line items")


SCHEMA_REGISTRY: dict[str, type[BaseModel]] = {
    "contact": ContactInfo,
    "invoice": Invoice,
}
