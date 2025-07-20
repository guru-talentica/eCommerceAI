"""
Test category API endpoints.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_category(client: AsyncClient):
    """Test creating a category."""
    category_data = {
        "name": "Electronics",
        "description": "Electronic products and accessories"
    }
    
    response = await client.post("/api/v1/categories/", json=category_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["name"] == "Electronics"
    assert data["data"]["description"] == "Electronic products and accessories"
    assert data["data"]["parent_id"] is None


@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient):
    """Test getting categories."""
    # First create a category
    category_data = {
        "name": "Books",
        "description": "Books and literature"
    }
    
    await client.post("/api/v1/categories/", json=category_data)
    
    # Now get categories
    response = await client.get("/api/v1/categories/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) > 0
    assert data["data"][0]["name"] == "Books"


@pytest.mark.asyncio
async def test_get_category_by_id(client: AsyncClient):
    """Test getting category by ID."""
    # First create a category
    category_data = {
        "name": "Clothing",
        "description": "Clothing and apparel"
    }
    
    create_response = await client.post("/api/v1/categories/", json=category_data)
    category_id = create_response.json()["data"]["id"]
    
    # Get category by ID
    response = await client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["id"] == category_id
    assert data["data"]["name"] == "Clothing"


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data
