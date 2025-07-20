"""
Pydantic schemas for products.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict

if TYPE_CHECKING:
    from app.schemas.category import Category
    from app.schemas.sku import SKU


class ProductBase(BaseModel):
    """Base product schema."""
    name: str = Field(..., min_length=1, max_length=150, description="Product name")
    description: Optional[str] = Field(None, max_length=2000, description="Product description")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Flexible product attributes")


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    category_id: int = Field(..., description="Category ID the product belongs to")


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = Field(None, min_length=1, max_length=150, description="Product name")
    description: Optional[str] = Field(None, max_length=2000, description="Product description")
    category_id: Optional[int] = Field(None, description="Category ID the product belongs to")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Flexible product attributes")


class ProductInDBBase(ProductBase):
    """Base schema for product in database."""
    id: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    version: int = 1
    is_deleted: bool = False
    
    model_config = ConfigDict(from_attributes=True)


class Product(ProductInDBBase):
    """Schema for product response."""
    pass


class ProductWithCategory(ProductInDBBase):
    """Schema for product response with category."""
    category: "Category"


class ProductWithSKUs(ProductInDBBase):
    """Schema for product response with SKUs."""
    skus: List["SKU"] = []


class ProductWithAll(ProductInDBBase):
    """Schema for product response with category and SKUs."""
    category: "Category"
    skus: List["SKU"] = []


class ProductResponse(BaseModel):
    """Envelope response for product."""
    status: str = "success"
    data: Product
    message: str = "Product retrieved successfully"
    meta: Optional[dict] = None


class ProductsResponse(BaseModel):
    """Envelope response for products list."""
    status: str = "success"
    data: List[Product]
    message: str = "Products retrieved successfully"
    meta: Optional[dict] = None


class ProductSearchRequest(BaseModel):
    """Schema for product search request."""
    query: Optional[str] = Field(None, description="Search query for product name/description")
    category_id: Optional[int] = Field(None, description="Filter by category ID")
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Page size")
