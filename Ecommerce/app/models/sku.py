"""
Database models for SKUs.
"""
from datetime import datetime
from typing import Dict, Any
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class SKU(Base):
    """
    SKU model with flexible attributes and product relationship.
    """
    __tablename__ = "skus"
    
    # Primary fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sku_code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    
    # Product relationship
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    
    # Flexible attributes (JSON) - price, inventory, size, color, etc.
    attributes: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    
    # Audit fields
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # For optimistic locking
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    
    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="skus", lazy="selectin")
    
    # Indexes
    __table_args__ = (
        Index('ix_skus_code_not_deleted', 'sku_code', postgresql_where=~is_deleted),
        Index('ix_skus_product_not_deleted', 'product_id', postgresql_where=~is_deleted),
        Index('ix_skus_created_at', 'created_at'),
    )
