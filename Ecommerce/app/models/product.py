"""
Database models for products.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import String, Text, Integer, DateTime, Boolean, ForeignKey, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Product(Base):
    """
    Product model with flexible attributes and category relationship.
    """
    __tablename__ = "products"
    
    # Primary fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Category relationship
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    
    # Flexible attributes (JSON)
    attributes: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Audit fields
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # For optimistic locking
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    
    # Relationships
    category: Mapped["Category"] = relationship("Category", back_populates="products", lazy="selectin")
    skus: Mapped[List["SKU"]] = relationship("SKU", back_populates="product", lazy="selectin")
    
    # Indexes
    __table_args__ = (
        Index('ix_products_name_not_deleted', 'name', postgresql_where=~is_deleted),
        Index('ix_products_category_not_deleted', 'category_id', postgresql_where=~is_deleted),
        Index('ix_products_created_at', 'created_at'),
    )
