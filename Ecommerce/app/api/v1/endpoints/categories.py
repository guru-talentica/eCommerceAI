"""
Category API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.category_service import CategoryService
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    Category,
    CategoryResponse,
    CategoriesResponse
)

router = APIRouter()


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_create: CategoryCreate,
    db: AsyncSession = Depends(get_db)
) -> CategoryResponse:
    """Create a new category."""
    service = CategoryService(db)
    try:
        category = await service.create(category_create)
        return CategoryResponse(
            data=category,
            message="Category created successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create category"
        )


@router.get("/", response_model=CategoriesResponse)
async def get_categories(
    parent_id: Optional[int] = Query(None, description="Filter by parent category ID"),
    include_deleted: bool = Query(False, description="Include deleted categories"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: AsyncSession = Depends(get_db)
) -> CategoriesResponse:
    """Get categories with optional filtering."""
    service = CategoryService(db)
    try:
        categories = await service.get_all(
            parent_id=parent_id,
            include_deleted=include_deleted,
            page=page,
            size=size
        )
        return CategoriesResponse(
            data=categories,
            message="Categories retrieved successfully",
            meta={
                "page": page,
                "size": size,
                "parent_id": parent_id
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve categories"
        )


# @router.get("/tree", response_model=CategoriesResponse)
# async def get_category_tree(
#     root_id: Optional[int] = Query(None, description="Root category ID (null for all roots)"),
#     max_depth: int = Query(3, ge=1, le=10, description="Maximum depth to fetch"),
#     db: AsyncSession = Depends(get_db)
# ) -> CategoriesResponse:
#     """Get category hierarchy tree."""
#     service = CategoryService(db)
#     try:
#         tree = await service.get_tree(root_id=root_id, max_depth=max_depth)
#         return CategoriesResponse(
#             data=tree,
#             message="Category tree retrieved successfully",
#             meta={
#                 "root_id": root_id,
#                 "max_depth": max_depth
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to retrieve category tree"
#         )


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
) -> CategoryResponse:
    """Get category by ID."""
    service = CategoryService(db)
    try:
        category = await service.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return CategoryResponse(
            data=category,
            message="Category retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve category"
        )


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: AsyncSession = Depends(get_db)
) -> CategoryResponse:
    """Update category by ID."""
    service = CategoryService(db)
    try:
        category = await service.update(category_id, category_update)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return CategoryResponse(
            data=category,
            message="Category updated successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update category"
        )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    force: bool = Query(False, description="Force delete (permanent)"),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete category by ID (soft delete by default)."""
    service = CategoryService(db)
    try:
        success = await service.delete(category_id, force=force)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete category"
        )


@router.post("/{category_id}/move", response_model=CategoryResponse)
async def move_category(
    category_id: int,
    new_parent_id: Optional[int] = Query(None, description="New parent category ID (null for root)"),
    db: AsyncSession = Depends(get_db)
) -> CategoryResponse:
    """Move category to a new parent."""
    service = CategoryService(db)
    try:
        category = await service.move(category_id, new_parent_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return CategoryResponse(
            data=category,
            message="Category moved successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to move category"
        )
