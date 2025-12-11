# START HERE 👋

Welcome to the Multi-Tenant Organization Management API! This guide gets you running in 5 minutes.

## ⚡ Super Quick Start (3 commands)

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start MongoDB (if not already running)
mongod

# 3. Run the API
uvicorn app.main:app --reload
```

**Done!** API is now running at `http://localhost:8000`

---

## 📖 Step-by-Step Setup

### Step 1: Prerequisites ✅
- [ ] Python 3.8+ installed
- [ ] MongoDB installed or accessible
- [ ] You're in the `c:\Users\renuh\OneDrive\Desktop\inter` directory

### Step 2: Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Start MongoDB
```powershell
# If MongoDB is installed as a service
Start-Service mongod

# Or run manually in another terminal
mongod
```

### Step 5: Run the API
```powershell
uvicorn app.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✓ Connected to MongoDB
✓ Application started successfully
```

---

## 🚀 Access the API

### Interactive API Docs (Swagger UI)
```
Open browser to: http://localhost:8000/docs
```

Here you can:
- See all endpoints
- Try them interactively
- View request/response schemas

### Quick Health Check
```powershell
curl http://localhost:8000/health
```

---

## 🧪 Test the API (2 ways)

### Option 1: Run Test Script
```powershell
python test_api.py
```

This will:
1. Create an organization
2. Login as admin
3. Update organization
4. Delete organization
5. Show all results

### Option 2: Manual Testing with curl
```powershell
# Create organization
curl -X POST http://localhost:8000/org/create `
  -H "Content-Type: application/json" `
  -d '{
    "organization_name": "My Company",
    "email": "admin@mycompany.com",
    "password": "Password123!"
  }'

# Login
curl -X POST http://localhost:8000/admin/login `
  -H "Content-Type: application/json" `
  -d '{
    "email": "admin@mycompany.com",
    "password": "Password123!"
  }'

# Get organization
curl "http://localhost:8000/org/get?organization_name=My Company"
```

---

## 📚 Next: Learn the API

### Want to understand all endpoints?
→ Read **[README.md](README.md)** (15 min read)

### Want to understand the architecture?
→ Read **[ARCHITECTURE.md](ARCHITECTURE.md)** (20 min read)

### Want to deploy to production?
→ Read **[DEPLOYMENT.md](DEPLOYMENT.md)** (20 min read)

### Want a quick 5-minute reference?
→ Read **[QUICKSTART.md](QUICKSTART.md)**

### Want to navigate all docs?
→ Read **[INDEX.md](INDEX.md)**

---

## 🎯 Common Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/org/create` | POST | Create organization |
| `/org/get` | GET | Get organization details |
| `/admin/login` | POST | Login and get token |
| `/org/update` | PUT | Update organization |
| `/org/delete` | DELETE | Delete organization |
| `/health` | GET | Health check |
| `/docs` | GET | API documentation |

---

## ❓ Troubleshooting

### "MongoDB connection failed"
```powershell
# Start MongoDB
Start-Service mongod
# Or: mongod (in separate terminal)
```

### "Port 8000 already in use"
```powershell
# Use different port
uvicorn app.main:app --port 8001 --reload
```

### "Module not found"
```powershell
# Ensure venv is activated
.\venv\Scripts\Activate.ps1

# Reinstall packages
pip install -r requirements.txt
```

### "Python not found"
```powershell
# Check Python path
python --version

# Or use full path
C:\Python311\python.exe --version
```

---

## 🎓 Learn More

### Documentation Index
| What | Where |
|------|-------|
| Quick reference | [QUICKSTART.md](QUICKSTART.md) |
| API details | [README.md](README.md) |
| System design | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Deployment | [DEPLOYMENT.md](DEPLOYMENT.md) |
| All endpoints | Swagger UI: `/docs` |
| File structure | [FILES.md](FILES.md) |
| Verification | [VERIFY.md](VERIFY.md) |

---

## ✅ Your Checklist

- [ ] Python installed
- [ ] MongoDB installed/running
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API started (`uvicorn app.main:app --reload`)
- [ ] Health check works (`curl http://localhost:8000/health`)
- [ ] Swagger UI opens (`http://localhost:8000/docs`)
- [ ] Test script runs (`python test_api.py`)

**All checked?** 🎉 You're ready to explore!

---

## 🚀 What's Next?

### Immediate (Now)
- [ ] Access Swagger UI at `/docs`
- [ ] Try creating an organization
- [ ] Test login
- [ ] Read basic endpoints

### Soon (Today)
- [ ] Read [README.md](README.md)
- [ ] Understand all endpoints
- [ ] Test all endpoints
- [ ] Review error handling

### Later (This Week)
- [ ] Read [ARCHITECTURE.md](ARCHITECTURE.md)
- [ ] Review source code
- [ ] Plan customizations
- [ ] Plan deployment

### Production (Before Deploy)
- [ ] Read [DEPLOYMENT.md](DEPLOYMENT.md)
- [ ] Choose deployment platform
- [ ] Configure production settings
- [ ] Test in production-like environment

---

## 📞 Quick Help

**Stuck?** Try:
1. Check [QUICKSTART.md](QUICKSTART.md)
2. Check [README.md](README.md) troubleshooting
3. Check [VERIFY.md](VERIFY.md) for verification
4. Check Swagger UI `/docs` for endpoint details

---

## 🎉 You're All Set!

The API is ready. Start exploring! 🚀

### Right now, you can:
1. ✅ Create organizations
2. ✅ Authenticate admins
3. ✅ Manage organizations
4. ✅ Test multi-tenancy
5. ✅ View all endpoints in Swagger UI

### Go to: http://localhost:8000/docs

---

**Questions?** Check the relevant documentation file above.  
**Ready?** Visit your Swagger UI and start testing! 🚀

---

*Version 1.0.0 | December 12, 2024*
