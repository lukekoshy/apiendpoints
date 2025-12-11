# System Architecture Documentation

## Overview

This is a multi-tenant SaaS backend service designed to manage multiple organizations with isolated data storage, each organization has its own database instance while sharing a master database for metadata.

```
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Application                     │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Routes    │  │  Middleware  │  │ Error Handler│   │
│  │ /org/*      │  │   CORS       │  │              │   │
│  │ /admin/*    │  │              │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐   │
│  │            Services Layer                        │   │
│  │  ┌─────────────────────┐  ┌─────────────────┐   │   │
│  │  │ OrganizationService │  │ AdminUserService│   │   │
│  │  └─────────────────────┘  └─────────────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐   │
│  │            Security Layer                        │   │
│  │  ┌──────────┐  ┌──────────────┐  ┌───────────┐   │   │
│  │  │  JWT     │  │ Bcrypt Hash  │  │ Validators│   │   │
│  │  │ Security │  │              │  │           │   │   │
│  │  └──────────┘  └──────────────┘  └───────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐   │
│  │         MongoDB Connection Pool                  │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
         │                          │
         │                          │
    ┌────▼──────────────────────────▼────┐
    │     MongoDB Instance               │
    ├────────────────────────────────────┤
    │  ┌──────────────────────────────┐  │
    │  │  master_db                   │  │
    │  │  ├─ organizations            │  │
    │  │  ├─ admin_users              │  │
    │  │  └─ system_logs              │  │
    │  └──────────────────────────────┘  │
    │                                    │
    │  ┌──────────────────────────────┐  │
    │  │  org_acme_corp (Tenant DB)   │  │
    │  │  ├─ data                     │  │
    │  │  └─ [custom collections]     │  │
    │  └──────────────────────────────┘  │
    │                                    │
    │  ┌──────────────────────────────┐  │
    │  │  org_techcorp (Tenant DB)    │  │
    │  │  ├─ data                     │  │
    │  │  └─ [custom collections]     │  │
    │  └──────────────────────────────┘  │
    └────────────────────────────────────┘
```

## Component Details

### 1. API Routes Layer (`/routes`)

**Organizations Route** (`organizations.py`)
- `POST /org/create` - Create organization
- `GET /org/get` - Retrieve organization
- `PUT /org/update` - Update organization
- `DELETE /org/delete` - Delete organization

**Authentication Route** (`auth.py`)
- `POST /admin/login` - Admin authentication

### 2. Services Layer (`/services`)

**OrganizationService**
- `create_organization()` - Create org with validation
- `get_organization()` - Fetch org details
- `update_organization()` - Update org data
- `delete_organization()` - Delete org and cleanup

**AdminUserService**
- `authenticate()` - Validate credentials
- `get_admin_by_id()` - Fetch admin details
- `get_organization_by_admin()` - Get admin's org

### 3. Database Layer (`/db`)

**MongoDBClient**
- Connection management
- Master database access
- Tenant database access
- Index creation
- Database initialization

```python
mongodb_client.connect()           # Initialize
mongodb_client.get_master_db()     # Master DB
mongodb_client.get_tenant_db(org)  # Tenant DB
mongodb_client.disconnect()        # Cleanup
```

### 4. Security Layer (`/core`)

**JWT Operations** (`security.py`)
- `create_access_token()` - Generate JWT
- `decode_token()` - Validate JWT

**Password Management** (`password.py`)
- `hash_password()` - Bcrypt hashing
- `verify_password()` - Validate password

**Configuration** (`config.py`)
- Environment variables
- Settings management

### 5. Data Models (`/models`)

**Organization Model**
```python
{
  _id: ObjectId,
  organization_name: str (unique),
  collection_name: str,
  admin_id: str,
  created_at: datetime
}
```

**AdminUser Model**
```python
{
  _id: ObjectId,
  email: str (unique),
  hashed_password: str,
  organization_id: str,
  created_at: datetime
}
```

### 6. Request/Response Schemas (`/schemas`)

- `CreateOrganizationRequest`
- `UpdateOrganizationRequest`
- `GetOrganizationRequest`
- `DeleteOrganizationRequest`
- `AdminLoginRequest`
- `TokenResponse`
- `OrganizationResponse`
- `ErrorResponse`
- `SuccessResponse`

### 7. Utilities (`/utils`)

**Validators** (`validators.py`)
- `sanitize_org_name()` - Clean org names for DB
- `validate_org_name()` - Validate org name format

## Data Flow

### Create Organization Flow

```
1. POST /org/create
   ├─ Validate input (Pydantic schemas)
   ├─ Check org name doesn't exist
   ├─ Hash admin password (Bcrypt)
   ├─ Insert organization in master_db
   ├─ Insert admin user in master_db
   ├─ Create tenant database
   ├─ Create "data" collection in tenant DB
   └─ Return organization details

2. MongoDB State:
   ├─ master_db.organizations
   │  └─ {name, collection_name, admin_id, created_at}
   ├─ master_db.admin_users
   │  └─ {email, hashed_password, organization_id, created_at}
   └─ org_<name>
      └─ data (empty collection)
```

### Login Flow

```
1. POST /admin/login
   ├─ Get admin from master_db by email
   ├─ Verify password (Bcrypt comparison)
   ├─ Get organization details
   ├─ Create JWT token with:
   │  ├─ admin_id
   │  ├─ organization_id
   │  ├─ organization_name
   │  ├─ email
   │  └─ expiration time
   └─ Return token and org details
```

### Authentication Flow (Protected Routes)

```
1. Request with Authorization Header
   ├─ Extract token from header
   ├─ Decode JWT (verify signature & expiry)
   ├─ Extract claims (admin_id, org_id)
   ├─ Validate token not expired
   ├─ Allow or deny request
   └─ Return 401 if invalid
```

## Multi-Tenancy Implementation

### Master Database
- **Purpose**: Store global metadata
- **Collections**:
  - `organizations` - Org metadata
  - `admin_users` - Admin credentials
  - Indexes on `organization_name` (unique), `email` (unique)

### Tenant Databases
- **Naming**: `org_<sanitized_org_name>`
- **Purpose**: Isolated data storage per organization
- **Collections**:
  - `data` - Default data collection
  - Custom collections per org needs

### Data Isolation
- Each org has separate MongoDB database
- No direct cross-org data access
- Authentication validates org access

## Security Architecture

### Password Security
```
User Password
     │
     ▼
Bcrypt Hash (salt + 10 rounds)
     │
     ▼
Stored in master_db.admin_users
```

### JWT Token Structure
```
Header: {alg: "HS256", typ: "JWT"}
Payload: {
  sub: "admin_id",
  admin_id: "...",
  organization_id: "...",
  organization_name: "...",
  email: "...",
  exp: <timestamp>
}
Signature: HMAC-SHA256(base64(header) + "." + base64(payload), SECRET_KEY)
```

### Token Validation
```
Authorization: Bearer <token>
     │
     ├─ Extract token
     ├─ Verify signature (with SECRET_KEY)
     ├─ Check expiration
     ├─ Extract claims
     └─ Proceed or reject
```

## API Request/Response Flow

### Successful Request
```
Client Request
     │
     ▼
FastAPI Router
     │
     ├─ Validate request schema (Pydantic)
     │
     ├─ [If protected] Validate JWT
     │
     ▼
Service Layer
     ├─ Business logic
     ├─ Database operations
     │
     ▼
Database (MongoDB)
     │
     ▼
Service returns result
     │
     ▼
FastAPI returns response (JSON)
     │
     ▼
Client receives response
```

### Error Handling
```
Any Error
     │
     ├─ Validation Error → 400 Bad Request
     ├─ Auth Error → 401 Unauthorized
     ├─ Not Found → 404 Not Found
     ├─ Server Error → 500 Internal Server Error
     │
     ▼
Standardized Error Response
{
  "detail": "Error message"
}
```

## Configuration Management

### Environment Variables
```
MONGODB_URL          → Database connection
MASTER_DB_NAME       → Master database name
SECRET_KEY           → JWT signing key
ALGORITHM            → JWT algorithm (HS256)
ACCESS_TOKEN_EXPIRE  → Token expiry time
APP_NAME             → Application name
DEBUG                → Debug mode
```

### Runtime Configuration
```
Settings class (Pydantic)
     │
     ├─ Load from .env file
     ├─ Load from environment variables
     └─ Apply defaults
```

## Performance Considerations

### Database Indexes
```
master_db.organizations
├─ organization_name (unique)
└─ _id (default)

master_db.admin_users
├─ email (unique)
├─ organization_id
└─ _id (default)

org_<name>.data
└─ _id (default)
```

### Connection Pooling
- MongoDB client maintains connection pool
- Reuses connections across requests
- Configurable pool size (default: 50)

### Query Optimization
- Indexed lookups for common queries
- Single database per org (no sharding needed initially)
- Lazy database/collection creation

## Scalability Architecture

### Current (Single Server)
```
Single FastAPI Instance
     │
     ▼
Single MongoDB Instance
     ├─ master_db
     ├─ org_acme
     ├─ org_techcorp
     └─ ...
```

### Horizontal Scaling
```
┌─────────────────┐
│ Load Balancer   │
└────────┬────────┘
         │
    ┌────┴────┐
    │          │
┌───▼──┐   ┌──▼───┐
│ API1 │   │ API2 │
└──┬───┘   └──┬───┘
   │          │
   └────┬─────┘
        │
   ┌────▼────────────┐
   │ MongoDB Replica │
   │ Set (sharded)   │
   └─────────────────┘
```

### Future Enhancements
- API rate limiting
- Request caching (Redis)
- Event streaming (Kafka)
- Audit logging
- Backup automation
- Multi-region deployment

## Error Handling Strategy

### Validation Errors
- **Trigger**: Invalid input format
- **Status**: 400 Bad Request
- **Response**: Field validation errors

### Authentication Errors
- **Trigger**: Invalid credentials or token
- **Status**: 401 Unauthorized
- **Response**: Authentication failed message

### Resource Not Found
- **Trigger**: Org/admin doesn't exist
- **Status**: 404 Not Found
- **Response**: Resource not found message

### Server Errors
- **Trigger**: Database/system errors
- **Status**: 500 Internal Server Error
- **Response**: Error message with logging

## Testing Strategy

### Unit Tests
- Models and utilities
- Password hashing
- Token generation

### Integration Tests
- API endpoints
- Database operations
- Authentication flow

### E2E Tests
- Complete user workflows
- Organization lifecycle
- Multi-tenant isolation

## Deployment Checklist

- [ ] Change SECRET_KEY to secure random value
- [ ] Set MONGODB_URL to production database
- [ ] Enable HTTPS/TLS
- [ ] Set DEBUG=False
- [ ] Configure CORS for production domains
- [ ] Set up monitoring and logging
- [ ] Configure automated backups
- [ ] Set up CI/CD pipeline
- [ ] Load test the API
- [ ] Document runbooks
- [ ] Set up alerts

---

**Architecture Version**: 1.0.0  
**Last Updated**: December 12, 2024
