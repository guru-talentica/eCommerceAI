"""
Category service for business logic operations.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_, func
from sqlalchemy.orm import selectinload

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    """Service class for category operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, category_data: CategoryCreate) -> Category:
        """Create a new category."""
        # Validate parent exists if provided
        if category_data.parent_id:
            parent = await self._get_by_id(category_data.parent_id)
            if not parent:
                raise ValueError("Parent category not found")
            if parent.is_deleted:
                raise ValueError("Cannot create category under deleted parent")
        
        # Check for duplicate name at same level
        existing = await self._get_by_name_and_parent(
            category_data.name, 
            category_data.parent_id
        )
        if existing:
            raise ValueError("Category with this name already exists at this level")
        
        # Create category
        category = Category(
            name=category_data.name,
            description=category_data.description,
            parent_id=category_data.parent_id,
            attributes=category_data.attributes or {}
        )
        
        # Set materialized path
        if category_data.parent_id:
            parent = await self._get_by_id(category_data.parent_id)
            category.path = f"{parent.path}.{category_data.name}"
        else:
            category.path = category_data.name
        
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        
        return category
    
    async def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        query = select(Category).where(
            and_(Category.id == category_id, Category.is_deleted == False)
        )
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        parent_id: Optional[int] = None,
        include_deleted: bool = False,
        page: int = 1,
        size: int = 20
    ) -> List[Category]:
        """Get all categories with optional filtering."""
        query = select(Category)
        
        # Apply filters
        conditions = []
        if not include_deleted:
            conditions.append(Category.is_deleted == False)
        
        if parent_id is not None:
            conditions.append(Category.parent_id == parent_id)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # Apply pagination
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)
        
        # Order by name
        query = query.order_by(Category.name)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    # async def get_tree method removed for simplification
    
    async def update(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        """Update category."""
        category = await self._get_by_id(category_id)
        if not category:
            return None
        
        # Check optimistic locking if version provided
        if category_data.version is not None and category.version != category_data.version:
            raise ValueError("Category has been modified by another user")
        
        # Validate parent change
        if category_data.parent_id is not None and category_data.parent_id != category.parent_id:
            if category_data.parent_id == category_id:
                raise ValueError("Category cannot be its own parent")
            
            # Check for circular reference
            if await self._would_create_cycle(category_id, category_data.parent_id):
                raise ValueError("Moving category would create a circular reference")
            
            # Validate parent exists
            if category_data.parent_id:
                parent = await self._get_by_id(category_data.parent_id)
                if not parent:
                    raise ValueError("Parent category not found")
                if parent.is_deleted:
                    raise ValueError("Cannot move category under deleted parent")
        
        # Check for duplicate name at same level
        if category_data.name and category_data.name != category.name:
            existing = await self._get_by_name_and_parent(
                category_data.name,
                category_data.parent_id if category_data.parent_id is not None else category.parent_id
            )
            if existing and existing.id != category_id:
                raise ValueError("Category with this name already exists at this level")
        
        # Update fields
        update_data = {}
        if category_data.name is not None:
            update_data["name"] = category_data.name
        if category_data.description is not None:
            update_data["description"] = category_data.description
        if category_data.parent_id is not None:
            update_data["parent_id"] = category_data.parent_id
        if category_data.attributes is not None:
            update_data["attributes"] = category_data.attributes
        
        # Update version for optimistic locking
        update_data["version"] = category.version + 1
        
        if update_data:
            stmt = update(Category).where(Category.id == category_id).values(**update_data)
            await self.db.execute(stmt)
            
            # Update materialized path if name or parent changed
            if "name" in update_data or "parent_id" in update_data:
                await self._update_materialized_path(category_id)
            
            await self.db.commit()
            
            # Refresh and return updated category
            await self.db.refresh(category)
        
        return category
    
    async def delete(self, category_id: int, force: bool = False) -> bool:
        """Delete category (soft delete by default)."""
        category = await self._get_by_id(category_id)
        if not category:
            return False
        
        # Check if category has children
        children_count = await self._count_children(category_id)
        if children_count > 0:
            raise ValueError("Cannot delete category with children")
        
        # Check if category has products
        products_count = await self._count_products(category_id)
        if products_count > 0:
            raise ValueError("Cannot delete category with products")
        
        if force:
            # Hard delete
            stmt = delete(Category).where(Category.id == category_id)
            await self.db.execute(stmt)
        else:
            # Soft delete
            stmt = update(Category).where(Category.id == category_id).values(
                is_deleted=True,
                version=category.version + 1
            )
            await self.db.execute(stmt)
        
        await self.db.commit()
        return True
    
    async def move(self, category_id: int, new_parent_id: Optional[int]) -> Optional[Category]:
        """Move category to a new parent."""
        category_update = CategoryUpdate(parent_id=new_parent_id)
        return await self.update(category_id, category_update)
    
    # Private helper methods
    
    async def _get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID without deleted filter."""
        result = await self.db.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalar_one_or_none()
    
    async def _get_by_name_and_parent(self, name: str, parent_id: Optional[int]) -> Optional[Category]:
        """Get category by name and parent."""
        result = await self.db.execute(
            select(Category).where(
                and_(
                    Category.name == name,
                    Category.parent_id == parent_id,
                    Category.is_deleted == False
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def _would_create_cycle(self, category_id: int, new_parent_id: int) -> bool:
        """Check if moving category would create a circular reference."""
        # Get the path of the category being moved
        category = await self._get_by_id(category_id)
        if not category:
            return False
        
        # Get the new parent
        new_parent = await self._get_by_id(new_parent_id)
        if not new_parent:
            return False
        
        # Check if new parent is a descendant of category
        return new_parent.path.startswith(f"{category.path}.")
    
    async def _count_children(self, category_id: int) -> int:
        """Count non-deleted children of category."""
        result = await self.db.execute(
            select(func.count(Category.id)).where(
                and_(
                    Category.parent_id == category_id,
                    Category.is_deleted == False
                )
            )
        )
        return result.scalar() or 0
    
    async def _count_products(self, category_id: int) -> int:
        """Count non-deleted products in category."""
        from app.models.product import Product
        
        result = await self.db.execute(
            select(func.count(Product.id)).where(
                and_(
                    Product.category_id == category_id,
                    Product.is_deleted == False
                )
            )
        )
        return result.scalar() or 0
    
    async def _update_materialized_path(self, category_id: int) -> None:
        """Update materialized path for category and its descendants."""
        category = await self._get_by_id(category_id)
        if not category:
            return
        
        # Calculate new path
        if category.parent_id:
            parent = await self._get_by_id(category.parent_id)
            new_path = f"{parent.path}.{category.name}"
        else:
            new_path = category.name
        
        old_path = category.path
        
        # Update category path
        await self.db.execute(
            update(Category)
            .where(Category.id == category_id)
            .values(path=new_path)
        )
        
        # Update descendant paths
        if old_path != new_path:
            old_path_pattern = f"{old_path}.%"
            
            # Get all descendants
            result = await self.db.execute(
                select(Category).where(Category.path.like(old_path_pattern))
            )
            descendants = list(result.scalars().all())
            
            for descendant in descendants:
                descendant_new_path = descendant.path.replace(old_path, new_path, 1)
                await self.db.execute(
                    update(Category)
                    .where(Category.id == descendant.id)
                    .values(path=descendant_new_path)
                )
    
    def _build_tree(self, categories: List[Category], root_id: Optional[int] = None) -> List[Category]:
        """Build hierarchical tree structure from flat list."""
        category_map = {cat.id: cat for cat in categories}
        
        # Clear existing children relationships
        for cat in categories:
            cat.children = []
        
        # Build parent-child relationships
        roots = []
        for cat in categories:
            if cat.parent_id and cat.parent_id in category_map:
                parent = category_map[cat.parent_id]
                parent.children.append(cat)
            elif cat.parent_id is None:
                if root_id is None or cat.id == root_id:
                    roots.append(cat)
            elif root_id and cat.id == root_id:
                roots.append(cat)
        
        return roots
