"""
Database models for categories.
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, Integer, DateTime, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Category(Base):
    """
    Category model with hierarchical support using materialized path.
    """
    __tablename__ = "categories"
    
    # Primary fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Hierarchy fields
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    level: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)
    path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, index=True)  # Materialized path
    
    # Audit fields
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # For optimistic locking
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    
    # Relationships
    products: Mapped[List["Product"]] = relationship("Product", back_populates="category", lazy="selectin")
    
    # Indexes
    __table_args__ = (
        Index('ix_categories_name_not_deleted', 'name', postgresql_where=~is_deleted),
        Index('ix_categories_parent_level', 'parent_id', 'level'),
        Index('ix_categories_path', 'path'),
    )
