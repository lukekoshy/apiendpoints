# Deployment Guide

## Prerequisites

- Python 3.8 or higher
- MongoDB 4.0 or higher
- pip (Python package manager)
- Git (for version control)

## Local Development Setup

### 1. Clone Repository
```bash
cd /path/to/project
git init
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# On Windows, use: copy .env.example .env
```

### 5. Verify MongoDB
```bash
# Ensure MongoDB is running
# Windows: mongod
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod
```

### 6. Run Application
```bash
uvicorn app.main:app --reload --port 8000
```

Access API at: `http://localhost:8000`
Docs at: `http://localhost:8000/docs`

## Production Deployment

### Docker Deployment

#### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Create Docker Compose
```bash
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongo:27017
      - MASTER_DB_NAME=master_db
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
    depends_on:
      - mongo
    restart: always

  mongo:
    image: mongo:6.0
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    restart: always

volumes:
  mongo_data:
```

#### 3. Deploy with Docker Compose
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

### Cloud Deployment

#### AWS (Elastic Beanstalk)

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize EB Application**
```bash
eb init -p python-3.11 multi-tenant-api
```

3. **Create Environment**
```bash
eb create production
```

4. **Deploy**
```bash
eb deploy
```

#### Google Cloud (Cloud Run)

1. **Build and Push Image**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/multi-tenant-api
```

2. **Deploy**
```bash
gcloud run deploy multi-tenant-api \
  --image gcr.io/PROJECT_ID/multi-tenant-api \
  --platform managed \
  --region us-central1 \
  --set-env-vars "MONGODB_URL=mongodb://..." \
  --allow-unauthenticated
```

#### Heroku

1. **Login**
```bash
heroku login
```

2. **Create App**
```bash
heroku create multi-tenant-api
```

3. **Set Environment Variables**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set MONGODB_URL=your-mongodb-url
```

4. **Deploy**
```bash
git push heroku main
```

### Traditional Server Deployment

#### Ubuntu/Debian

1. **Update System**
```bash
sudo apt update
sudo apt upgrade -y
```

2. **Install Python and Dependencies**
```bash
sudo apt install python3 python3-pip python3-venv -y
```

3. **Install MongoDB**
```bash
sudo apt install -y gnupg
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

4. **Create Application User**
```bash
sudo useradd -m -s /bin/bash appuser
sudo su - appuser
cd /home/appuser
```

5. **Clone and Setup Application**
```bash
git clone <repo-url> multi-tenant-api
cd multi-tenant-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Create Systemd Service**
```bash
sudo nano /etc/systemd/system/multi-tenant-api.service
```

```ini
[Unit]
Description=Multi-Tenant Organization API
After=network.target

[Service]
Type=notify
User=appuser
WorkingDirectory=/home/appuser/multi-tenant-api
Environment="PATH=/home/appuser/multi-tenant-api/venv/bin"
ExecStart=/home/appuser/multi-tenant-api/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

7. **Enable and Start Service**
```bash
sudo systemctl enable multi-tenant-api
sudo systemctl start multi-tenant-api
sudo systemctl status multi-tenant-api
```

8. **Setup Nginx Reverse Proxy**
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/multi-tenant-api
```

```nginx
upstream api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

9. **Enable Nginx Configuration**
```bash
sudo ln -s /etc/nginx/sites-available/multi-tenant-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

10. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## Environment Configuration

### Production Environment Variables

```env
# Database
MONGODB_URL=mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority
MASTER_DB_NAME=master_db

# Security (MUST CHANGE)
SECRET_KEY=<generate-strong-random-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=Multi-Tenant Organization Service
DEBUG=False
```

### Generate Strong Secret Key
```python
import secrets
print(secrets.token_urlsafe(32))
```

## Security Best Practices

### 1. Secrets Management
- Use environment variables (NOT in code)
- Use secret management tools (HashiCorp Vault, AWS Secrets Manager)
- Never commit secrets to version control
- Rotate secrets regularly

### 2. Database Security
- Enable MongoDB authentication
- Use TLS/SSL connections
- Restrict network access to MongoDB
- Regular backups and testing

### 3. API Security
- Enable HTTPS/TLS
- Implement rate limiting
- Add request signing
- Use API keys for service-to-service
- Implement CORS properly

### 4. Application Security
- Keep dependencies updated
- Use security scanning tools
- Implement logging and monitoring
- Add request validation
- Sanitize inputs

### 5. Access Control
- Implement least privilege
- Use strong passwords
- Multi-factor authentication (future)
- Audit logging
- Regular access reviews

## Monitoring & Logging

### Application Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Health Monitoring
```bash
# Check API health
curl http://localhost:8000/health

# Monitor logs
tail -f /var/log/multi-tenant-api.log
```

### Performance Monitoring
- Monitor CPU and memory usage
- Track database query performance
- Monitor API response times
- Set up alerts for errors

### Tools to Consider
- Prometheus (metrics)
- Grafana (visualization)
- ELK Stack (logging)
- Sentry (error tracking)
- DataDog (APM)

## Backup Strategy

### MongoDB Backup
```bash
# Full backup
mongodump --uri "mongodb://localhost:27017" --out /backup/mongo_backup

# Restore
mongorestore --uri "mongodb://localhost:27017" /backup/mongo_backup

# Schedule backup (cron)
0 2 * * * mongodump --uri "mongodb://localhost:27017" --out /backup/mongo_$(date +\%Y\%m\%d)
```

### Application Backup
- Version control (Git)
- Infrastructure as Code (IaC)
- Configuration backups
- Regular testing of restores

## Scaling Considerations

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Upgrade database instance
- Monitor resource utilization

### Horizontal Scaling
```
Load Balancer (Nginx/HAProxy)
    ├─ API Instance 1
    ├─ API Instance 2
    ├─ API Instance 3
    └─ ...
         │
    MongoDB Cluster
```

### Caching
- Redis for session caching
- Database query result caching
- API response caching

## Database Optimization

### Sharding Strategy (Future)
```
master_db (single instance)
    ├─ organizations
    └─ admin_users

Tenant DBs (distributed):
    ├─ org_acme (shard 1)
    ├─ org_techcorp (shard 2)
    └─ ...
```

### Connection Pooling
- MongoDB default: 50 connections
- Adjust based on load
- Monitor pool utilization

## Troubleshooting

### Common Issues

**API Won't Start**
```bash
# Check logs
uvicorn app.main:app --reload

# Verify Python version
python --version

# Check dependencies
pip list
```

**MongoDB Connection Error**
```bash
# Verify MongoDB running
mongosh

# Check connection string
echo $MONGODB_URL

# Test connection
python -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017').admin.command('ping')"
```

**Port Already in Use**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :8000
kill -9 <PID>
```

## Deployment Checklist

- [ ] Set SECRET_KEY to secure random value
- [ ] Configure MONGODB_URL for production
- [ ] Set DEBUG=False
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS for production domains
- [ ] Set up monitoring and alerting
- [ ] Configure logging
- [ ] Set up backup strategy
- [ ] Test disaster recovery
- [ ] Load test the API
- [ ] Set up CI/CD pipeline
- [ ] Document runbooks
- [ ] Configure auto-scaling
- [ ] Set up DNS records
- [ ] Test all endpoints in production
- [ ] Monitor error rates
- [ ] Verify data isolation (multi-tenancy)

## Performance Tuning

### API Tuning
- Increase worker processes
- Adjust timeout values
- Enable compression
- Optimize database queries

### Database Tuning
- Create appropriate indexes
- Monitor slow queries
- Optimize connection pool
- Regular maintenance tasks

### Infrastructure Tuning
- CDN for static assets
- Database replication
- Read replicas for scaling
- Connection pooling

---

**Deployment Guide Version**: 1.0.0  
**Last Updated**: December 12, 2024
