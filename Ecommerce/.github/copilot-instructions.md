<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# E-commerce Inventory Management Service - Copilot Instructions

## Project Overview
This is a FastAPI-based e-commerce inventory management service with hierarchical categories, products, and SKUs. The project follows a modular monolith architecture with async PostgreSQL integration.

## Architecture Guidelines
- Use **async/await** patterns for all database operations
- Follow **FastAPI** best practices with dependency injection
- Implement **SQLAlchemy 2.0** async ORM patterns
- Use **Pydantic v2** for data validation and serialization
- Follow **envelope response format** for all API responses
- Implement **optimistic locking** with version fields for concurrent updates

## Code Style Guidelines
- Use **Black** for code formatting
- Use **isort** for import organization
- Follow **flake8** linting rules
- Use **type hints** for all function parameters and return values
- Write **comprehensive docstrings** for all classes and functions

## Database Guidelines
- Use **materialized path** for hierarchical categories
- Implement **soft deletes** with audit trails
- Use **JSONB** for flexible SKU attributes
- Follow **database relationship constraints** strictly
- Always use **async database sessions**

## API Guidelines
- Follow **RESTful** conventions
- Implement **cursor-based pagination** for lists
- Use **HTTP status codes** appropriately
- Include **request/response validation**
- Implement **rate limiting** considerations

## Testing Guidelines
- Write **unit tests** for services and utilities
- Write **integration tests** for API endpoints
- Use **pytest fixtures** for test data setup
- Aim for **90%+ test coverage**
- Use **async test patterns** with pytest-asyncio

## Error Handling
- Use **custom exception classes**
- Implement **global exception handlers**
- Return **structured error responses**
- Log **errors appropriately** with context

## Security Considerations
- Implement **input sanitization**
- Use **parameterized queries** to prevent SQL injection
- Prepare for **future JWT authentication**
- Include **CORS** configuration
- Implement **rate limiting** middleware

## Performance Guidelines
- Use **database indexes** appropriately
- Implement **caching strategies** where needed
- Optimize **N+1 query problems**
- Use **async I/O** for all external calls
- Consider **connection pooling**

## File Structure Conventions
- Place **models** in `app/models/`
- Place **schemas** in `app/schemas/`
- Place **services** in `app/services/`
- Place **API endpoints** in `app/api/v1/endpoints/`
- Place **tests** in `tests/` with mirror structure

## Response Format
Always use envelope format:
```json
{
  "status": "success",
  "data": {...},
  "message": "Operation completed successfully",
  "meta": {
    "pagination": {...},
    "timestamp": "2025-01-21T12:00:00Z"
  }
}
```

## Database Models Guidelines
- Include **created_at**, **updated_at**, **version** fields
- Use **soft delete** pattern with **is_deleted** field
- Implement **proper relationships** with foreign keys
- Use **JSONB** for flexible attributes in SKUs
- Include **proper indexes** for performance
