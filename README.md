# Multi-Tenant Organization Management API

A FastAPI-based backend service for managing organizations in a multi-tenant architecture with MongoDB.

## Features

✅ **Multi-Tenant Architecture**
- Master database for global metadata
- Dynamic collections for each organization
- Isolated data per tenant

✅ **Organization Management**
- Create organizations with admin users
- Get organization details
- Update organization credentials
- Delete organizations with data cleanup

✅ **Authentication & Security**
- JWT-based authentication
- Bcrypt password hashing
- Secure token validation

✅ **Database**
- MongoDB integration
- Automatic collection creation
- Data migration support

## Prerequisites

- Python 3.8+
- MongoDB (local or remote instance)
- pip (Python package manager)

## Installation

1. **Clone or download the project**
   ```bash
   cd inter
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # On Windows
   source venv/bin/activate     # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB**
   - Ensure MongoDB is running on `localhost:27017` (default)
   - Or update `MONGODB_URL` in `.env` file

5. **Set environment variables** (optional)
   - Copy `.env.example` to `.env` (or use existing `.env`)
   - Update `SECRET_KEY` for JWT encryption

## Running the Application

### Using Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

**Interactive API Documentation**: `http://localhost:8000/docs`

## API Endpoints

### Organization Endpoints

#### 1. Create Organization
```http
POST /org/create
Content-Type: application/json

{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "message": "Organization created successfully",
  "data": {
    "organization_name": "Acme Corp",
    "collection_name": "org_acme_corp",
    "admin_id": "507f1f77bcf86cd799439011",
    "created_at": "2024-12-12T10:30:00"
  }
}
```

#### 2. Get Organization
```http
GET /org/get?organization_name=Acme Corp
```

**Response:**
```json
{
  "message": "Organization retrieved successfully",
  "data": {
    "organization_name": "Acme Corp",
    "collection_name": "org_acme_corp",
    "admin_id": "507f1f77bcf86cd799439011",
    "created_at": "2024-12-12T10:30:00"
  }
}
```

#### 3. Update Organization
```http
PUT /org/update
Authorization: Bearer <token>
Content-Type: application/json

{
  "organization_name": "Acme Corp",
  "email": "newemail@acme.com",
  "password": "NewSecurePassword123!"
}
```

**Response:**
```json
{
  "message": "Organization updated successfully",
  "data": {
    "organization_name": "Acme Corp",
    "collection_name": "org_acme_corp_v2",
    "admin_id": "507f1f77bcf86cd799439011"
  }
}
```

#### 4. Delete Organization
```http
DELETE /org/delete?organization_name=Acme Corp
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Organization deleted successfully"
}
```

### Authentication Endpoints

#### Admin Login
```http
POST /admin/login
Content-Type: application/json

{
  "email": "admin@acme.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "admin_id": "507f1f77bcf86cd799439011",
    "organization_id": "507f1f77bcf86cd799439012",
    "organization_name": "Acme Corp"
  }
}
```

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "app": "Multi-Tenant Organization Service"
}
```

## Project Structure

```
inter/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration settings
│   │   ├── security.py         # JWT token operations
│   │   └── password.py         # Password hashing
│   ├── db/
│   │   ├── __init__.py
│   │   └── mongodb.py          # MongoDB client
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py           # Data models (Organization, AdminUser)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic request/response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   └── services.py         # Business logic services
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── organizations.py    # Organization endpoints
│   │   └── auth.py             # Authentication endpoints
│   └── utils/
│       ├── __init__.py
│       └── validators.py       # Validation utilities
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
└── README.md                   # This file
```

## Database Schema

### Master Database (`master_db`)

#### Collections

**organizations**
```json
{
  "_id": ObjectId,
  "organization_name": "string",
  "collection_name": "string (org_<org_name>)",
  "admin_id": "string (ObjectId)",
  "created_at": ISODate
}
```

**admin_users**
```json
{
  "_id": ObjectId,
  "email": "string (unique)",
  "hashed_password": "string",
  "organization_id": "string (ObjectId)",
  "created_at": ISODate
}
```

### Tenant Databases

Each organization gets its own database: `org_<organization_name>`

Default collection: `data` (can be extended with more collections as needed)

## Configuration

### Environment Variables (`.env`)

```env
# MongoDB Connection
MONGODB_URL=mongodb://localhost:27017
MASTER_DB_NAME=master_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=Multi-Tenant Organization Service
DEBUG=False
```

## Error Handling

The API returns standardized error responses:

### 400 Bad Request
```json
{
  "detail": "Organization already exists"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid token"
}
```

### 404 Not Found
```json
{
  "detail": "Organization not found"
}
```

## Authentication Flow

1. **Organization Admin Registration**: Create organization with email and password
   - Password is hashed using bcrypt
   - Stored securely in master database

2. **Admin Login**: Send email and password to `/admin/login`
   - Credentials validated
   - JWT token generated with admin and organization info
   - Token contains: `admin_id`, `organization_id`, `organization_name`

3. **Token Usage**: Include token in Authorization header for protected endpoints
   ```
   Authorization: Bearer <token>
   ```

## Testing with cURL

### Create Organization
```bash
curl -X POST http://localhost:8000/org/create \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "Test Org",
    "email": "admin@testorg.com",
    "password": "TestPassword123!"
  }'
```

### Admin Login
```bash
curl -X POST http://localhost:8000/admin/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@testorg.com",
    "password": "TestPassword123!"
  }'
```

### Get Organization
```bash
curl http://localhost:8000/org/get?organization_name=Test%20Org
```

### Delete Organization (with token)
```bash
curl -X DELETE http://localhost:8000/org/delete?organization_name=Test%20Org \
  -H "Authorization: Bearer <your_token_here>"
```

## Testing with Postman

1. Import the API endpoints into Postman
2. Create environment variables:
   - `base_url`: http://localhost:8000
   - `token`: (populated after login)
   - `org_name`: Test Org

3. Use the token from login response in subsequent requests

## Security Considerations

⚠️ **Production Deployment**:

1. **Change SECRET_KEY**: Generate a strong random key
   ```python
   import secrets
   secrets.token_urlsafe(32)
   ```

2. **Use HTTPS**: Deploy behind a reverse proxy (nginx, Apache)

3. **Update MongoDB URL**: Use secure connection with authentication

4. **CORS Configuration**: Restrict allowed origins in production

5. **Rate Limiting**: Implement rate limiting for API endpoints

6. **Input Validation**: All inputs are validated server-side

## Troubleshooting

### MongoDB Connection Error
```
✗ Failed to connect to MongoDB
```
**Solution**: Ensure MongoDB is running:
```bash
# Windows
mongod

# macOS/Linux
brew services start mongodb-community
```

### Port 8000 Already in Use
```
Address already in use
```
**Solution**: Use different port:
```bash
uvicorn app.main:app --port 8001 --reload
```

### Import Errors
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Performance Optimization Tips

1. **Add Database Indexes**: Already configured for:
   - `organizations.organization_name` (unique)
   - `admin_users.email` (unique)
   - `admin_users.organization_id`

2. **Connection Pooling**: MongoDB client uses connection pooling by default

3. **Caching**: Consider adding Redis for token caching

4. **Async Operations**: FastAPI handles async requests efficiently

## Future Enhancements

- [ ] Add user management (non-admin users per organization)
- [ ] Implement organization-level roles and permissions
- [ ] Add API key authentication
- [ ] Database backup and recovery
- [ ] Audit logging
- [ ] Multi-region support
- [ ] Rate limiting and API quotas

## Support & Contribution

For issues, questions, or contributions, please create an issue in the repository.

## License

MIT License - Feel free to use this project for personal or commercial purposes.

---

**Version**: 1.0.0  
**Last Updated**: December 12, 2024  
**Framework**: FastAPI + MongoDB
