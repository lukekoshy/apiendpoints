# Quick Start Guide

Get the Multi-Tenant API running in 5 minutes!

## Prerequisites

- Python 3.8+
- MongoDB running locally or accessible
- pip (comes with Python)

## Installation

### Step 1: Setup Python Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Database
```bash
# Ensure MongoDB is running
# Windows: mongod (in separate terminal)
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod

# Verify MongoDB is accessible
mongosh  # or mongo (old version)
> exit
```

### Step 4: Start the API
```bash
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✓ Connected to MongoDB
✓ Application started successfully
```

## Interactive API Documentation

Open your browser and visit:
```
http://localhost:8000/docs
```

This gives you an interactive API explorer (Swagger UI).

## Quick Test

### 1. Check Health
```bash
curl http://localhost:8000/health
```

### 2. Create Organization
```bash
curl -X POST http://localhost:8000/org/create \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "My Company",
    "email": "admin@mycompany.com",
    "password": "Password123!"
  }'
```

### 3. Admin Login
```bash
curl -X POST http://localhost:8000/admin/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@mycompany.com",
    "password": "Password123!"
  }'
```

Copy the `access_token` from the response.

### 4. Get Organization
```bash
curl http://localhost:8000/org/get?organization_name=My%20Company
```

### 5. Delete Organization
```bash
curl -X DELETE http://localhost:8000/org/delete?organization_name=My%20Company \
  -H "Authorization: Bearer <your_token_here>"
```

## Using Python Test Script

```bash
python test_api.py
```

This runs through all major operations with example data.

## Project Structure

```
inter/
├── app/
│   ├── main.py              # Start here
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   ├── db/                  # Database connection
│   ├── models/              # Data structures
│   ├── core/                # Security & config
│   ├── schemas/             # Request/response models
│   └── utils/               # Helpers
├── requirements.txt         # Dependencies
├── .env                     # Configuration
├── README.md                # Full documentation
├── ARCHITECTURE.md          # System design
├── DEPLOYMENT.md            # Production setup
└── POSTMAN_GUIDE.md         # API testing
```

## Common Commands

### Run API
```bash
uvicorn app.main:app --reload
```

### Run Tests
```bash
python test_api.py
```

### Install New Package
```bash
pip install package-name
pip freeze > requirements.txt
```

### Check Logs
```bash
# View real-time logs (when using --reload)
# Logs appear in the same terminal as uvicorn
```

## Environment Variables

Located in `.env`:
```env
MONGODB_URL=mongodb://localhost:27017
MASTER_DB_NAME=master_db
SECRET_KEY=your-secret-key
```

For production, see `DEPLOYMENT.md`.

## File Editing Tips

### Add New Endpoint
1. Create function in `app/routes/...`
2. Use `@router.get()`, `@router.post()`, etc.
3. Import and include router in `app/main.py`

### Add New Database Model
1. Create class in `app/models/models.py`
2. Add Pydantic schema in `app/schemas/schemas.py`
3. Use in services layer `app/services/services.py`

### Change API Port
```bash
uvicorn app.main:app --port 9000
```

## Troubleshooting

### MongoDB Not Found
```
Error: Failed to connect to MongoDB
```
**Fix**: Start MongoDB
```bash
mongod  # Windows/macOS
sudo systemctl start mongod  # Linux
```

### Port Already in Use
```
Error: Address already in use
```
**Fix**: Use different port
```bash
uvicorn app.main:app --port 8001
```

### Import Errors
```
ModuleNotFoundError: No module named 'fastapi'
```
**Fix**: Install dependencies
```bash
pip install -r requirements.txt
```

### Virtual Environment Not Activated
**Fix**: Activate it
```bash
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

## Next Steps

1. **Explore API Docs**: Visit `http://localhost:8000/docs`
2. **Review Code**: Start with `app/main.py`
3. **Read Full Docs**: See `README.md`
4. **Understand Architecture**: See `ARCHITECTURE.md`
5. **Learn Deployment**: See `DEPLOYMENT.md`

## API Endpoints Summary

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/org/create` | Create organization |
| GET | `/org/get` | Get organization details |
| PUT | `/org/update` | Update organization |
| DELETE | `/org/delete` | Delete organization |
| POST | `/admin/login` | Admin authentication |
| GET | `/health` | Health check |

## Database Schema

**master_db (Global)**
- `organizations` - Org metadata
- `admin_users` - Admin credentials

**org_<name> (Per Tenant)**
- `data` - Organization data

## Tips

✅ Use Swagger UI (`/docs`) for testing  
✅ Copy token from login for protected endpoints  
✅ All inputs are validated automatically  
✅ Passwords are securely hashed  
✅ Each org has isolated database  

## Support

See `README.md` for detailed documentation.

---

**Ready to build?** Happy coding! 🚀
