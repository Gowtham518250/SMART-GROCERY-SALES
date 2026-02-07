# ✅ RAG_APP Docker Deployment Checklist

## Pre-Deployment (Development)

### System Requirements
- [ ] Docker installed (20.10+)
- [ ] Docker Compose installed (2.0+)
- [ ] 8GB RAM available
- [ ] 20GB disk space free
- [ ] Ports 8000, 5432, 6379, 11434 available

### Project Setup
- [ ] Cloned/downloaded RAG_APP
- [ ] Navigated to RAG_APP directory
- [ ] Read DOCKER_SETUP.md
- [ ] Read DOCKER_QUICK_REFERENCE.md

### Configuration
- [ ] Copied `.env.example` to `.env`
- [ ] Updated database credentials in `.env`
- [ ] Updated SECRET_KEY in `.env` (use `openssl rand -hex 32`)
- [ ] Set OLLAMA_BASE_URL correctly
- [ ] Verified all required directories exist

---

## Initial Deployment

### Build & Start
- [ ] Run `docker-compose up -d`
- [ ] Verify images building: `docker-compose logs`
- [ ] Wait 2-3 minutes for services to stabilize
- [ ] Check status: `docker-compose ps`

### Verification
- [ ] All 4 containers running (`docker-compose ps`)
- [ ] API responsive: `curl http://localhost:8000/docs`
- [ ] PostgreSQL ready: `docker-compose logs postgres | grep "ready"`
- [ ] Redis connected: `docker-compose exec redis redis-cli ping`
- [ ] Ollama started: `docker-compose logs ollama | grep "listening"`

### Database Initialization
- [ ] Database tables created (auto-ran init-db.sql)
- [ ] User table accessible: `docker-compose exec postgres psql -U postgres -d Data_Analytics -c "SELECT COUNT(*) FROM user_details;"`
- [ ] Sales table accessible: `docker-compose exec postgres psql -U postgres -d Data_Analytics -c "SELECT COUNT(*) FROM sales;"`

### API Testing
- [ ] Access API docs: http://localhost:8000/docs
- [ ] Access ReDoc: http://localhost:8000/redoc
- [ ] Try sample endpoint (if available)

---

## Health Checks

### Service Health

#### PostgreSQL
```bash
✓ docker-compose exec postgres pg_isready
  Result: "accepting connections"
```

#### Redis
```bash
✓ docker-compose exec redis redis-cli ping
  Result: "PONG"
```

#### Ollama
```bash
✓ curl -s http://localhost:11434/api/tags | grep -q "phi3:mini"
  Result: model should be listed
```

#### RAG API
```bash
✓ curl -s http://localhost:8000/docs | grep -q "swagger"
  Result: page should contain "swagger"
```

---

## Post-Deployment Tasks

### Create Admin User
- [ ] Create first admin account via API
  ```bash
  curl -X POST http://localhost:8000/auth/register \
    -H "Content-Type: application/json" \
    -d '{"user_name":"admin","email":"admin@example.com","password":"SecurePass123"}'
  ```
- [ ] Test login: `curl -X POST http://localhost:8000/auth/login ...`

### Test Core Features
- [ ] Upload test document to /rag/upload
- [ ] Query document at /rag/query
- [ ] Check today insights at /today_insight/
- [ ] Test SQL analyst at /sql_analyst/analyze

### Backup Verification
- [ ] Backup database: 
  ```bash
  docker-compose exec postgres pg_dump -U postgres Data_Analytics > backup.sql
  ```
- [ ] Verify backup file created with size > 1KB

---

## Monitoring Setup

### Log Monitoring
- [ ] Enable log aggregation (optional)
- [ ] Configure log rotation in docker-compose.prod.yml
- [ ] Set up alerts for error logs

### Resource Monitoring
- [ ] Check initial resource usage: `docker stats`
- [ ] Set memory limits in docker-compose.yml if needed
- [ ] Monitor CPU usage over first week

### Performance Baseline
- [ ] Record API response times
- [ ] Note database query speeds
- [ ] Check model inference times

---

## Security Hardening (Production)

### Environment Security
- [ ] Change all default passwords
- [ ] Generate new SECRET_KEY (not default)
- [ ] Remove .env.example from production
- [ ] Never commit .env to version control
- [ ] Use environment variable secrets manager

### Network Security
- [ ] Enable SSL/TLS in nginx.conf
- [ ] Configure firewall rules
- [ ] Restrict Redis to internal network only
- [ ] Use HTTPS for all API calls
- [ ] Enable CORS only for known origins

### Database Security
- [ ] Change PostgreSQL default password
- [ ] Create separate users for read/write
- [ ] Enable PostgreSQL encryption at rest
- [ ] Set up automated backups
- [ ] Configure connection limits

### Application Security
- [ ] Disable DEBUG mode in production
- [ ] Hide /docs and /redoc endpoints (optional)
- [ ] Enable rate limiting on all endpoints
- [ ] Implement API keys/OAuth2
- [ ] Set security headers in nginx

---

## Backup & Disaster Recovery

### Automated Backups
- [ ] Set up daily database backups
  ```bash
  # Add to crontab
  0 2 * * * docker-compose exec postgres pg_dump -U postgres Data_Analytics > /backups/db-$(date +%Y%m%d).sql
  ```
- [ ] Set up document storage backups
- [ ] Test restore procedure monthly

### Disaster Recovery Plan
- [ ] Document recovery steps
- [ ] Create recovery runbook
- [ ] Test full recovery (weekly)
- [ ] Store backups in multiple locations
- [ ] Keep 30-day backup retention

---

## Performance Optimization

### Database
- [ ] Create necessary indexes
  ```sql
  CREATE INDEX idx_sales_date ON sales(sale_date);
  CREATE INDEX idx_sales_shopkeeper ON sales(shopkeeper_id);
  ```
- [ ] Run VACUUM daily
- [ ] Monitor slow queries
- [ ] Increase shared_buffers if needed

### Caching
- [ ] Configure Redis eviction policy
- [ ] Set appropriate TTL values
- [ ] Monitor cache hit ratio
- [ ] Adjust max memory if needed

### API Performance
- [ ] Monitor response times
- [ ] Check worker utilization
- [ ] Adjust worker count if needed
- [ ] Enable query caching

### LLM Performance
- [ ] Monitor model inference time
- [ ] Consider model optimization
- [ ] Test batch operations
- [ ] Optimize prompt templates

---

## Maintenance Schedule

### Daily
- [ ] Check container health
- [ ] Monitor error logs
- [ ] Verify backups completed

### Weekly
- [ ] Run database VACUUM
- [ ] Test disaster recovery
- [ ] Review resource usage

### Monthly
- [ ] Update Docker images
- [ ] Security audit
- [ ] Performance review
- [ ] Backup verification

### Quarterly
- [ ] Update dependencies
- [ ] Security review
- [ ] Capacity planning
- [ ] Disaster recovery drill

---

## Troubleshooting Quick Links

| Issue | Command |
|-------|---------|
| Services not starting | `docker-compose logs -f` |
| Port conflicts | `docker-compose down` |
| Database not connecting | `docker-compose restart postgres` |
| High memory | `docker stats` |
| API slow | `docker-compose logs -f rag_api` |

---

## Final Verification

### Before Going Live

- [ ] All health checks passing
- [ ] Backups verified working
- [ ] Security check completed
- [ ] Performance baseline established
- [ ] Team trained on operations
- [ ] Runbooks prepared
- [ ] Monitoring configured
- [ ] Alerting configured
- [ ] Disaster recovery tested
- [ ] Load test completed (if applicable)

### Sign-Off

- [ ] Project Lead: _________________ Date: _______
- [ ] Ops/DevOps: _________________ Date: _______
- [ ] Security: _________________ Date: _______

---

## Contacts & References

| Role | Name | Contact |
|------|------|---------|
| Project Manager | | |
| DevOps Engineer | | |
| DBA | | |
| Security Officer | | |

**Documentation Location:** /RAG_APP/DOCKER_SETUP.md  
**Quick Reference:** /RAG_APP/DOCKER_QUICK_REFERENCE.md  
**Summary:** /RAG_APP/DOCKER_SUMMARY.md  

---

**Deployment Date:** _______________  
**Deployed By:** _______________  
**Environment:** [ ] Development  [ ] Staging  [ ] Production

---

**Status:** [ ] In Progress  [ ] Complete  [ ] Issues Found

**Notes:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

**Version:** 1.0  
**Last Updated:** February 2026
