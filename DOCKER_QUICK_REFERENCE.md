# 🐳 RAG_APP Docker Quick Reference

## ⚡ Essential Commands

### Startup
```bash
cd RAG_APP
docker-compose up -d          # Start all services
docker-compose logs -f        # View live logs
docker-compose ps             # Check status
```

### Access Points
```
API Docs:       http://localhost:8000/docs
ReDoc:          http://localhost:8000/redoc
PostgreSQL:     localhost:5432
Redis:          localhost:6379
Ollama:         http://localhost:11434
```

### Shutdown
```bash
docker-compose stop           # Graceful stop
docker-compose down           # Stop and remove
docker-compose down -v        # Also remove volumes
```

---

## 🔧 Service Management

### View Logs
```bash
docker-compose logs -f rag_api      # API logs
docker-compose logs -f postgres     # Database logs
docker-compose logs -f redis        # Cache logs
docker-compose logs -f ollama       # LLM logs
```

### Restart Services
```bash
docker-compose restart              # Restart all
docker-compose restart rag_api      # Specific service
docker-compose restart --time 30 rag_api
```

### Rebuild
```bash
docker-compose build                # Rebuild all
docker-compose build --no-cache rag_api
docker-compose up -d --build        # Rebuild & start
```

---

## 💻 Container Access

### Execute Commands
```bash
# Python shell
docker-compose exec rag_api python

# Bash shell
docker-compose exec rag_api bash

# PostgreSQL client
docker-compose exec postgres psql -U postgres

# Redis CLI
docker-compose exec redis redis-cli

# Ollama CLI
docker-compose exec ollama ollama list
```

### Install Python Packages
```bash
docker-compose exec rag_api pip install <package>
```

### Run Python Script
```bash
docker-compose exec rag_api python /app/script.py
```

---

## 📊 Monitoring

### Check Resource Usage
```bash
docker stats                    # Real-time stats
docker stats --no-stream       # One-time snapshot
```

### Health Checks
```bash
docker-compose ps              # Show health status
docker inspect rag_api         # Detailed health info
```

### Port Verification
```bash
# Linux/Mac
lsof -i :8000                  # Check if port 8000 is in use
lsof -i :5432                  # Check port 5432

# Windows
netstat -ano | findstr :8000
```

---

## 🔒 Database Operations

### Connect to PostgreSQL
```bash
docker-compose exec postgres psql -U postgres -d Data_Analytics
```

### Common SQL Queries
```bash
# List tables
\dt

# Show user schema
\d user_details

# Show sales schema
\d sales

# Run query
SELECT COUNT(*) FROM sales;

# Backup database
docker-compose exec postgres pg_dump -U postgres Data_Analytics > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres Data_Analytics < backup.sql
```

### Redis Operations
```bash
docker-compose exec redis redis-cli
KEYS *                         # List all keys
GET <key>                      # Get key value
DEL <key>                      # Delete key
FLUSHDB                        # Clear all data
DBSIZE                         # Database size
```

---

## 🤖 Ollama Model Management

### Check Models
```bash
docker-compose exec ollama ollama list
```

### Pull Models
```bash
docker-compose exec ollama ollama pull phi3:mini
docker-compose exec ollama ollama pull mistral
docker-compose exec ollama ollama pull neural-chat
```

### Remove Models
```bash
docker-compose exec ollama ollama rm phi3:mini
```

### Run Model
```bash
docker-compose exec ollama ollama run phi3:mini "prompt here"
```

---

## 🧹 Cleanup Operations

### Remove Stopped Containers
```bash
docker container prune         # Remove unused containers
docker image prune             # Remove unused images
docker volume prune            # Remove unused volumes
```

### Full Cleanup
```bash
docker-compose down -v         # Stop and remove everything
docker system prune -a         # Remove all unused images/containers
```

### Clean Docker
```bash
docker-compose rm -f           # Force remove containers
docker volume rm rag_api_*     # Remove volumes
```

---

## 📈 Performance Tuning

### Database Optimization
```sql
-- Create indexes
CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_user_email ON user_details(email);
```

### Redis Optimization
```bash
docker-compose exec redis redis-cli
CONFIG GET maxmemory           # Check memory limit
CONFIG SET maxmemory 1gb       # Set memory limit
```

### API Worker Tuning
```bash
# Edit docker-compose.yml command line:
# --workers 4 (increase for more CPU cores)
# --loop uvloop (faster event loop)
```

---

## 🐛 Troubleshooting Checklist

- [ ] All containers running: `docker-compose ps`
- [ ] No port conflicts: `docker stats`
- [ ] API responsive: `curl http://localhost:8000/docs`
- [ ] Database connected: `docker-compose logs postgres`
- [ ] Redis working: `docker-compose exec redis redis-cli ping`
- [ ] Ollama models loaded: `curl http://localhost:11434/api/tags`

---

## 📈 Production Deployment

### With Production Config
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Enable SSL/TLS
1. Uncomment SSL section in nginx.conf
2. Add certificates to ./ssl directory
3. Restart: `docker-compose restart nginx`

### Scale Services
```bash
# Add to docker-compose.yml
deploy:
  replicas: 3
  
# Then deploy
docker-compose up -d --scale rag_api=3
```

---

## 🚨 Emergency Commands

### Force Stop Everything
```bash
docker-compose kill
docker-compose down
```

### Rescue Database
```bash
# Backup before cleanup
docker-compose exec postgres pg_dump -U postgres Data_Analytics > emergency_backup.sql

# Full reset
docker-compose down -v
docker-compose up -d postgres
# Restore if needed:
cat emergency_backup.sql | docker-compose exec -T postgres psql -U postgres Data_Analytics
```

### View System Logs
```bash
docker-compose logs --tail=100 rag_api
journalctl -u docker.service
```

---

## 🔗 Useful Links

- **FastAPI Docs:** http://localhost:8000/docs
- **PostgreSQL Docs:** https://www.postgresql.org/docs/
- **Redis Commands:** https://redis.io/commands
- **Ollama Models:** https://ollama.ai/library
- **Docker Docs:** https://docs.docker.com/

---

## 📞 Quick Support

**Issue:** Services not starting
```bash
docker-compose logs -f
# Check for port conflicts or resource limits
```

**Issue:** Database won't connect
```bash
docker-compose exec postgres pg_isready
docker-compose restart postgres
```

**Issue:** High memory usage
```bash
docker stats
# Reduce model size or increase Docker memory allocation
```

**Issue:** Slow API responses
```bash
docker-compose logs -f rag_api
# Check CPU usage: docker stats
```

---

**Last Updated:** February 2026  
**Version:** 1.0  
**Compatible With:** Docker 20.10+, Docker Compose 3.8+
