"""
Pydantic schemas for SKUs.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict, field_validator

if TYPE_CHECKING:
    from app.schemas.product import Product


class SKUBase(BaseModel):
    """Base SKU schema."""
    sku_code: str = Field(..., min_length=1, max_length=50, description="Unique SKU code")
    price: Decimal = Field(..., ge=0, decimal_places=2, description="SKU price")
    inventory_count: int = Field(..., ge=0, description="Inventory count")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Flexible SKU attributes")
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        """Validate price precision."""
        if v < 0:
            raise ValueError('Price must be non-negative')
        return v


class SKUCreate(SKUBase):
    """Schema for creating a SKU."""
    product_id: int = Field(..., description="Product ID the SKU belongs to")


class SKUUpdate(BaseModel):
    """Schema for updating a SKU."""
    sku_code: Optional[str] = Field(None, min_length=1, max_length=50, description="Unique SKU code")
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="SKU price")
    inventory_count: Optional[int] = Field(None, ge=0, description="Inventory count")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Flexible SKU attributes")
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        """Validate price precision."""
        if v is not None and v < 0:
            raise ValueError('Price must be non-negative')
        return v


class SKUInDBBase(SKUBase):
    """Base schema for SKU in database."""
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime
    version: int = 1
    is_deleted: bool = False
    
    model_config = ConfigDict(from_attributes=True)


class SKU(SKUInDBBase):
    """Schema for SKU response."""
    pass


class SKUWithProduct(SKUInDBBase):
    """Schema for SKU response with product."""
    product: "Product"


class InventoryUpdate(BaseModel):
    """Schema for inventory update."""
    inventory_count: int = Field(..., ge=0, description="New inventory count")
    adjustment_reason: Optional[str] = Field(None, max_length=255, description="Reason for adjustment")


class SKUResponse(BaseModel):
    """Envelope response for SKU."""
    status: str = "success"
    data: SKU
    message: str = "SKU retrieved successfully"
    meta: Optional[dict] = None


class SKUsResponse(BaseModel):
    """Envelope response for SKUs list."""
    status: str = "success"
    data: List[SKU]
    message: str = "SKUs retrieved successfully"
    meta: Optional[dict] = None


class SKUSearchRequest(BaseModel):
    """Schema for SKU search request."""
    sku_code: Optional[str] = Field(None, description="Search by SKU code")
    product_id: Optional[int] = Field(None, description="Filter by product ID")
    min_price: Optional[Decimal] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[Decimal] = Field(None, ge=0, description="Maximum price filter")
    in_stock: Optional[bool] = Field(None, description="Filter by inventory availability")
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Page size")
