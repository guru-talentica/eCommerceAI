# E-commerce Inventory Management Service

A FastAPI-based e-commerce inventory management service that provides CRUD operations for Categories, Products, and SKUs with hierarchical support, search capabilities, and production-ready features.

## Features

- **RESTful API** with FastAPI and async support
- **Hierarchical Categories** with materialized path implementation
- **Product Management** with flexible attributes
- **SKU Management** with inventory tracking
- **Search & Filtering** with pagination support
- **Data Validation** with Pydantic models
- **Database** PostgreSQL with async SQLAlchemy
- **Testing** Comprehensive test suite with 90%+ coverage
- **Production Ready** with logging, monitoring, and error handling

## Tech Stack

- **Backend**: FastAPI 0.104.1
- **Database**: PostgreSQL with AsyncPG
- **ORM**: SQLAlchemy 2.0 (async)
- **Validation**: Pydantic 2.5
- **Testing**: Pytest with async support
- **Code Quality**: Black, Flake8, isort

## Project Structure

```
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── categories.py
│       │   ├── products.py
│       │   └── skus.py
│       └── api.py
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
├── models/
│   ├── category.py
│   ├── product.py
│   └── sku.py
├── schemas/
│   ├── category.py
│   ├── product.py
│   └── sku.py
├── services/
│   ├── category_service.py
│   ├── product_service.py
│   └── sku_service.py
├── tests/
└── main.py
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Virtual environment tool

### Installation

1. **Clone and setup virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Set up database:**
   ```bash
   # Create PostgreSQL database
   createdb ecommerce_inventory
   
   # Run migrations
   alembic upgrade head
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Development

1. **Run tests:**
   ```bash
   pytest
   ```

2. **Run tests with coverage:**
   ```bash
   pytest --cov=app --cov-report=html
   ```

3. **Code formatting:**
   ```bash
   black app/
   isort app/
   flake8 app/
   ```

## API Endpoints

### Categories
- `POST /api/v1/categories` - Create category
- `GET /api/v1/categories` - List all categories
- `GET /api/v1/categories/{id}` - Get category by ID
- `PUT /api/v1/categories/{id}` - Update category
- `DELETE /api/v1/categories/{id}` - Delete category

### Products
- `POST /api/v1/products` - Create product
- `GET /api/v1/products` - List products (with search, filter, pagination)
- `GET /api/v1/products/{id}` - Get product by ID
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

### SKUs
- `POST /api/v1/products/{product_id}/skus` - Create SKU for product
- `GET /api/v1/products/{product_id}/skus` - List SKUs for product
- `GET /api/v1/skus/{id}` - Get SKU by ID
- `PUT /api/v1/skus/{id}` - Update SKU
- `DELETE /api/v1/skus/{id}` - Delete SKU

## Configuration

Key environment variables:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost/ecommerce_inventory

# Application
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME=E-commerce Inventory Management Service

# Security
SECRET_KEY=your-secret-key-here
```

## Testing

The project includes comprehensive tests:

- **Unit Tests**: For individual components
- **Integration Tests**: For API endpoints
- **Database Tests**: For model operations
- **Coverage Target**: 90%+

Run specific test categories:
```bash
# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# With coverage report
pytest --cov=app --cov-report=term-missing
```

## Production Deployment

For production deployment considerations:

1. **Database**: Use managed PostgreSQL (AWS RDS, etc.)
2. **Application**: Deploy with Docker on ECS Fargate
3. **Monitoring**: Integrate with ELK Stack and Sentry
4. **Caching**: Add Redis for performance
5. **Search**: Integrate Elasticsearch for advanced search

## Contributing

1. Follow the existing code style (Black, isort, flake8)
2. Write tests for new features
3. Ensure test coverage remains above 90%
4. Update documentation as needed

## License

This project is licensed under the MIT License.
