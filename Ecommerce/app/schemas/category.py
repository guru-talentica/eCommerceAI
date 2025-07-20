from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    attributes: Optional[Dict[str, Any]] = Field(None)

class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = Field(None)

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[int] = Field(None)
    attributes: Optional[Dict[str, Any]] = Field(None)
    version: Optional[int] = Field(None)

class CategoryInDBBase(CategoryBase):
    id: int
    parent_id: Optional[int] = None
    path: str
    created_at: datetime
    updated_at: datetime
    version: int = 1
    is_deleted: bool = False
    
    model_config = ConfigDict(from_attributes=True)

class Category(CategoryInDBBase):
    pass

class CategoryResponse(BaseModel):
    status: str = "success"
    data: Category
    message: str = "Category retrieved successfully"
    meta: Optional[dict] = None

class CategoriesResponse(BaseModel):
    status: str = "success"
    data: List[Category]
    message: str = "Categories retrieved successfully"
    meta: Optional[dict] = None
