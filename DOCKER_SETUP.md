# RAG_APP - Docker Setup Guide

Complete Docker containerization for RAG_APP with FastAPI, PostgreSQL, Redis, and Ollama LLM.

## 📋 Project Structure

```
RAG_APP/
├── app.py                      # FastAPI application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image for RAG_APP
├── docker-compose.yml          # Multi-container orchestration
├── .dockerignore               # Docker build exclusions
├── .env                        # Environment variables
├── authentication.py           # JWT & password auth
├── db.py                       # PostgreSQL connection
├── RAG.py                      # RAG document processing
├── sql_analyst.py              # SQL chat interface
├── chatbot.py                  # Chatbot routes
├── today_insight.py            # Daily AI insights
├── bill_generated.py           # Bill generation
├── RAG_Document_Store/         # Vector database storage
└── store/                      # File storage
```

## 🚀 Quick Start - Docker

### Prerequisites
- Docker Desktop (or Docker + Docker Compose)
- 4GB+ RAM available
- 10GB+ disk space (for models & databases)
- Environment variables file (`.env`)

### Step 1: Prepare Environment

Create a `.env` file in the RAG_APP directory:

```bash
# Database Configuration
DB_USER=postgres
DB_PASSWORD=Gowtham@2004
DB_NAME=Data_Analytics
DB_HOST=postgres

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Ollama Configuration
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=phi3:mini

# JWT & Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=False
```

### Step 2: Start All Services

```bash
# Navigate to RAG_APP directory
cd RAG_APP

# Start all containers (builds if needed)
docker-compose up -d

# Or with logs
docker-compose up
```

**What starts:**
- ✅ PostgreSQL database on `localhost:5432`
- ✅ Redis cache on `localhost:6379`
- ✅ Ollama LLM on `localhost:11434`
- ✅ RAG API on `localhost:8000`

### Step 3: Verify Services

```bash
# Check all containers
docker-compose ps

# View API docs
http://localhost:8000/docs
http://localhost:8000/redoc

# Check Ollama models
curl http://localhost:11434/api/tags

# Test Redis
docker-compose exec redis redis-cli ping
```

### Step 4: Load Initial Database

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d Data_Analytics

# Or run initialization script
docker-compose exec postgres psql -U postgres -d Data_Analytics -f /docker-entrypoint-initdb.d/init.sql
```

## 📦 Dependencies Breakdown

### Web Framework (1.1 MB)
- **fastapi** - Modern Python web framework
- **uvicorn** - ASGI server for FastAPI
- **python-multipart** - Form data handling

### Database (5.2 MB)
- **sqlalchemy** - Python ORM
- **psycopg2-binary** - PostgreSQL adapter
- **alembic** - Database migrations

### Authentication (1.5 MB)
- **python-jose** - JWT token handling
- **passlib** - Password utilities
- **bcrypt** - Cryptographic hashing

### AI/ML Stack (2.5 GB)
- **langchain** - LLM orchestration
- **langchain-community** - Community integrations
- **sentence-transformers** - Text embeddings
- **faiss-cpu** - Vector similarity search
- **torch** - PyTorch ML framework

### Document Processing
- **pypdf** - PDF parsing
- **pdf2image** - PDF to image conversion
- **pytesseract** - OCR support

### Caching & Performance
- **redis** - In-memory data store
- **requests** - HTTP library

### Environment Management
- **python-dotenv** - Load environment variables

## 🐳 Docker Images Used

| Service | Image | Size | Purpose |
|---------|-------|------|---------|
| RAG_API | python:3.10-slim | ~150 MB | Application server |
| PostgreSQL | postgres:15-alpine | ~80 MB | Database |
| Redis | redis:7-alpine | ~40 MB | Cache layer |
| Ollama | ollama/ollama | ~9.8 GB | LLM inference |

**Total Size: ~10.1 GB** (varies based on models loaded in Ollama)

## 🔧 Common Docker Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f rag_api
docker-compose logs -f postgres
docker-compose logs -f redis
docker-compose logs -f ollama
```

### Stop Services
```bash
# Stop without removing
docker-compose stop

# Stop and remove all containers/volumes
docker-compose down -v
```

### Rebuild Images
```bash
# Rebuild RAG_API after code changes
docker-compose build rag_api

# Force rebuild without cache
docker-compose build --no-cache rag_api

# Rebuild and restart
docker-compose up -d --build
```

### Access Container Shell
```bash
# RAG API
docker-compose exec rag_api bash

# PostgreSQL
docker-compose exec postgres psql -U postgres -d Data_Analytics

# Redis
docker-compose exec redis redis-cli

# Ollama
docker-compose exec ollama bash
```

## 📊 Performance Optimization

### Database Indexing
```sql
-- Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d Data_Analytics

-- Create indexes for faster queries
CREATE INDEX idx_sales_shopkeeper_id ON sales(shopkeeper_id);
CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_user_email ON user_details(email);
```

### Redis Optimization
```bash
# Monitor Redis performance
docker-compose exec redis redis-cli
> INFO stats
> DBSIZE
```

### Ollama Model Management
```bash
# Check loaded models
curl http://localhost:11434/api/tags

# Pull additional models
docker-compose exec ollama ollama pull mistral
docker-compose exec ollama ollama pull neural-chat

# Remove unused models
docker-compose exec ollama ollama rm phi3:mini
```

## 🔒 Security Best Practices

### Production Deployment

1. **Update `.env` with secure values:**
```bash
# Generate strong secret key
openssl rand -hex 32
```

2. **Use environment-specific compose files:**
```bash
# Development
docker-compose -f docker-compose.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

3. **Enable PostgreSQL authentication:**
```dockerfile
# In Dockerfile
RUN apt-get install -y postgresql-client
```

4. **Restrict network access:**
```yaml
# In docker-compose.yml
services:
  rag_api:
    networks:
      - rag_network
    # Don't expose Redis/Ollama to host
```

## 📝 Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | postgres | PostgreSQL hostname |
| `DB_USER` | postgres | Database user |
| `DB_PASSWORD` | Gowtham@2004 | Database password |
| `DB_NAME` | Data_Analytics | Database name |
| `REDIS_HOST` | redis | Redis hostname |
| `OLLAMA_BASE_URL` | http://ollama:11434 | Ollama API endpoint |
| `SECRET_KEY` | - | JWT secret (required for prod) |
| `DEBUG` | False | Debug mode |

## 🆘 Troubleshooting

### Services Won't Start
```bash
# Check for port conflicts
sudo lsof -i :8000
sudo lsof -i :5432

# Free up ports and restart
docker-compose down
docker-compose up -d
```

### Ollama Model Not Loading
```bash
# Check Ollama service status
docker-compose logs ollama

# Pull model manually
docker-compose exec ollama ollama pull phi3:mini

# Verify
curl http://localhost:11434/api/tags
```

### PostgreSQL Connection Issues
```bash
# Verify database exists
docker-compose exec postgres psql -U postgres -l

# Check connection
docker-compose exec rag_api python -c "from RAG_APP.db import engine; print(engine)"
```

### High Memory Usage
```bash
# Check Docker resource usage
docker stats

# Reduce model size in Ollama
docker-compose exec ollama ollama rm mistral
docker-compose exec ollama ollama pull phi3:mini
```

## 📚 API Endpoints

Once running, access:

- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health (if implemented)

### Key Routes
```
POST   /auth/register          # User registration
POST   /auth/login             # User login
GET    /auth/sales             # Get user sales
POST   /rag/upload             # Upload documents
POST   /rag/query              # Query documents
POST   /sql_analyst/analyze    # SQL analysis
POST   /today_insight/         # Get daily insights
POST   /bill/generate          # Generate bills
POST   /chat                   # Chatbot interface
```

## 🎯 Next Steps

1. **Initialize database schema** → Run migrations
2. **Upload documents** → RAG endpoint
3. **Start using** → Access /docs
4. **Monitor performance** → Check logs and stats
5. **Scale up** → Use Kubernetes for production

## 📞 Support

For issues, check:
1. Docker logs: `docker-compose logs -f`
2. Health endpoints: `/docs` or `/health`
3. Database: `docker-compose exec postgres psql ...`
4. Ollama: `curl http://localhost:11434/api/tags`

---

**Last Updated:** February 2026  
**Docker Version:** 24.0+  
**Python Version:** 3.10+
