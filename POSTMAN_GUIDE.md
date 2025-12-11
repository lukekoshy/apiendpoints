# Postman Collection for Multi-Tenant API

This collection provides pre-configured requests for testing the Multi-Tenant Organization Management API.

## Import Instructions

1. Open Postman
2. Click "Import" → "Import From" → "Paste Raw Text"
3. Paste the JSON below into the text area
4. Click "Continue" → "Import"

## Environment Variables Setup

Before running requests, set up the following environment variables in Postman:

```
base_url: http://localhost:8000
token: (will be auto-populated after login)
org_name: Test Organization
admin_email: admin@testorg.com
admin_password: TestPassword123!
```

## Collection JSON

```json
{
  "info": {
    "name": "Multi-Tenant Organization API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": {
          "raw": "{{base_url}}/health",
          "host": ["{{base_url}}"],
          "path": ["health"]
        }
      }
    },
    {
      "name": "Create Organization",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\\n  \\\"organization_name\\\": \\\"{{org_name}}\\\",\\n  \\\"email\\\": \\\"{{admin_email}}\\\",\\n  \\\"password\\\": \\\"{{admin_password}}\\\"\\n}"
        },
        "url": {
          "raw": "{{base_url}}/org/create",
          "host": ["{{base_url}}"],
          "path": ["org", "create"]
        }
      }
    },
    {
      "name": "Get Organization",
      "request": {
        "method": "GET",
        "url": {
          "raw": "{{base_url}}/org/get?organization_name={{org_name}}",
          "host": ["{{base_url}}"],
          "path": ["org", "get"],
          "query": [
            {
              "key": "organization_name",
              "value": "{{org_name}}"
            }
          ]
        }
      }
    },
    {
      "name": "Admin Login",
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "if (pm.response.code === 200) {",
              "  const response = pm.response.json();",
              "  pm.environment.set('token', response.data.access_token);",
              "  pm.environment.set('admin_id', response.data.admin_id);",
              "  pm.environment.set('organization_id', response.data.organization_id);",
              "}"
            ]
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\\n  \\\"email\\\": \\\"{{admin_email}}\\\",\\n  \\\"password\\\": \\\"{{admin_password}}\\\"\\n}"
        },
        "url": {
          "raw": "{{base_url}}/admin/login",
          "host": ["{{base_url}}"],
          "path": ["admin", "login"]
        }
      }
    },
    {
      "name": "Update Organization",
      "request": {
        "method": "PUT",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          },
          {
            "key": "Authorization",
            "value": "Bearer {{token}}"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\\n  \\\"organization_name\\\": \\\"{{org_name}}\\\",\\n  \\\"email\\\": \\\"newemail@testorg.com\\\",\\n  \\\"password\\\": \\\"NewPassword123!\\\"\\n}"
        },
        "url": {
          "raw": "{{base_url}}/org/update",
          "host": ["{{base_url}}"],
          "path": ["org", "update"]
        }
      }
    },
    {
      "name": "Delete Organization",
      "request": {
        "method": "DELETE",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{token}}"
          }
        ],
        "url": {
          "raw": "{{base_url}}/org/delete?organization_name={{org_name}}",
          "host": ["{{base_url}}"],
          "path": ["org", "delete"],
          "query": [
            {
              "key": "organization_name",
              "value": "{{org_name}}"
            }
          ]
        }
      }
    }
  ]
}
```

## Usage Guide

### 1. Health Check
- **Purpose**: Verify API is running
- **No authentication required**
- Expected response: `{"status": "healthy", "app": "Multi-Tenant Organization Service"}`

### 2. Create Organization
- **Purpose**: Create new organization with admin user
- **No authentication required**
- **Required fields**: organization_name, email, password
- Expected response: Organization details with admin_id

### 3. Get Organization
- **Purpose**: Retrieve organization details
- **No authentication required**
- **Query parameter**: organization_name
- Expected response: Organization details

### 4. Admin Login
- **Purpose**: Authenticate admin and get JWT token
- **No authentication required**
- **Required fields**: email, password
- **Note**: Token is automatically saved to environment variable "token"
- Expected response: JWT token, organization details

### 5. Update Organization
- **Purpose**: Update organization credentials
- **Requires**: Bearer token in Authorization header
- **Required fields**: organization_name, email, password
- Expected response: Updated organization details

### 6. Delete Organization
- **Purpose**: Delete organization and all data
- **Requires**: Bearer token in Authorization header
- **Query parameter**: organization_name
- Expected response: Success message

## Workflow Example

1. Create Organization
   ```
   POST /org/create
   {
     "organization_name": "Acme Corp",
     "email": "admin@acme.com",
     "password": "SecurePass123!"
   }
   ```

2. Login
   ```
   POST /admin/login
   {
     "email": "admin@acme.com",
     "password": "SecurePass123!"
   }
   ```

3. Get Organization
   ```
   GET /org/get?organization_name=Acme Corp
   ```

4. Update Organization (use token from login)
   ```
   PUT /org/update
   Authorization: Bearer <token>
   {
     "organization_name": "Acme Corp",
     "email": "newemail@acme.com",
     "password": "NewPass123!"
   }
   ```

5. Delete Organization (use token)
   ```
   DELETE /org/delete?organization_name=Acme Corp
   Authorization: Bearer <token>
   ```

## Tips

- Always run "Admin Login" before running protected endpoints (Update, Delete)
- Token is automatically saved after successful login
- Use different organization names for testing multiple organizations
- Check the "Tests" tab in each request to see validation scripts
