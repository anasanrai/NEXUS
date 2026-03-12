# NEXUS Production Deployment Checklist

## Pre-Deployment Validation ✅

### Environment Setup
- [ ] Python 3.12+ installed (`python3 --version`)
- [ ] pip package manager available (`pip --version`)
- [ ] Git installed for repository access (`git --version`)
- [ ] Docker installed (for containerized deployment) - OPTIONAL

### Repository Structure
- [ ] All 50 files present and accounted for
- [ ] No missing directories (agent, tools, memory, etc.)
- [ ] All Python files have proper imports
- [ ] Configuration files present (.env.example, config.py)

### Code Validation
```bash
# Run these validation checks
python3 -m py_compile main.py agent/core.py agent/router.py \
  tools/registry.py scheduler/cron.py channels/telegram.py \
  memory/entities.py

# Result should show no errors/warnings
```

- [ ] All Python files compile without syntax errors
- [ ] No import errors when running validation
- [ ] All async/await patterns correct
- [ ] Error handling in place throughout

## Configuration Setup 🔧

### Environment Variables
- [ ] Create `.env` file from `.env.example`
  ```bash
  cp .env.example .env
  ```
- [ ] Add OpenRouter API key: `OPENROUTER_API_KEY`
- [ ] Add Tavily API key: `TAVILY_API_KEY`
- [ ] Add Supabase credentials: `SUPABASE_URL`, `SUPABASE_KEY`
- [ ] Add Redis connection: `REDIS_URL`
- [ ] Add Telegram bot token: `TELEGRAM_BOT_TOKEN`
- [ ] Add Telegram chat ID: `TELEGRAM_CHAT_ID`
- [ ] Set environment: `APP_ENVIRONMENT=production` or `development`

### Optional Services
- [ ] Configure Stripe key for payment processing (if using payments)
- [ ] Configure GitHub token for Git operations (if using Git tools)
- [ ] Configure WordPress credentials (if posting blogs)
- [ ] Configure social media API keys (Twitter, LinkedIn, Instagram)

## Dependencies Installation 📦

### Python Requirements
```bash
pip install -r requirements.txt
```

Verify installed packages:
- [ ] aiohttp >= 3.9
- [ ] python-telegram-bot >= 20.0
- [ ] playwright >= 1.40
- [ ] redis >= 5.0
- [ ] supabase >= 2.0
- [ ] apscheduler >= 3.10
- [ ] fastapi >= 0.100
- [ ] uvicorn >= 0.23
- [ ] httpx >= 0.25

### Optional Browser Installation
```bash
playwright install
```
- [ ] Chromium installed
- [ ] Firefox installed
- [ ] WebKit installed

## Database Setup 🗄️

### Supabase Configuration
- [ ] Create Supabase project
- [ ] Create tables by running SQL in SETUP.md:
  - [ ] `clients` table
  - [ ] `tasks` table
  - [ ] `revenue` table
  - [ ] `events` table
- [ ] Enable pgvector extension
- [ ] Create database user/role
- [ ] Test database connection

### Redis Setup
- [ ] Redis server running (local or cloud)
- [ ] Redis port accessible (default: 6379)
- [ ] Test connection: `redis-cli ping`
- [ ] Memory sufficient (2GB recommended)

## Service Integration Testing 🧪

### Run Validation Script
```bash
python3 validate_system.py
```

Expected output:
- [ ] Python version shown
- [ ] Config imports successfully
- [ ] All agent components importable
- [ ] Memory systems available
- [ ] Tool registry accessible
- [ ] Telegram channel available
- [ ] Scheduler available
- [ ] All async functions detected

### Test Each Service
```bash
# Test configuration
python3 -c "from config import config, validate_config; \
  validate_config(config) and print('✓ Config OK')"
```
- [ ] Configuration validates without errors

```bash
# Test agent components
python3 -c "from agent.core import nexus_core; \
  print(f'✓ Core OK: status={nexus_core.get_status}')"
```
- [ ] Agent core loads successfully

```bash
# Test tools registry
python3 -c "from tools.registry import initialize_tool_registry; \
  import asyncio; \
  registry = asyncio.run(initialize_tool_registry()); \
  print(f'✓ {len(registry.list_tools())} tools registered')"
```
- [ ] 31 tools register successfully

## Telegram Setup 📱

### Bot Configuration
- [ ] Created bot with @BotFather
- [ ] Bot token added to `.env`
- [ ] Chat ID obtained and added to `.env`
- [ ] Bot invited to desired chat/group
- [ ] Admin privileges granted if needed

### Test Bot Commands
- [ ] `/start` - Shows welcome message
- [ ] `/help` - Shows available commands
- [ ] `/status` - Shows agent status
- [ ] `/tasks` - Shows pending tasks
- [ ] `/revenue` - Shows revenue summary

## Deployment Options 🚀

### Option A: Local Python
```bash
python3 main.py
```

Expected startup sequence:
- [ ] ✓ Configuration validated
- [ ] ✓ Tools registered (31 available)
- [ ] ✓ Telegram bot started
- [ ] ✓ Scheduler started (6 jobs)
- [ ] 🚀 NEXUS is running!

### Option B: Docker
```bash
docker-compose up -d
```

Verify:
- [ ] Container is running: `docker ps`
- [ ] Logs show startup sequence: `docker-compose logs -f nexus`
- [ ] Can access health endpoint: `curl localhost:8000/api/status`

### Option C: Production Server
- [ ] Set `APP_ENVIRONMENT=production` in `.env`
- [ ] Secure all API keys and secrets
- [ ] Enable HTTPS/SSL certificates
- [ ] Setup CI/CD pipeline
- [ ] Configure monitoring & alerts
- [ ] Setup log aggregation

## Monitoring & Maintenance 📊

### Log Files
- [ ] Check `nexus.log` for any warnings/errors
- [ ] Monitor log file size (consider rotation)
- [ ] Key log messages:
  - [ ] Agent startup complete
  - [ ] Tools registered
  - [ ] Service initialization
  - [ ] Task execution results

### Performance Monitoring
```bash
# Monitor resource usage
top  # CPU & memory
iostat  # Disk I/O
netstat  # Network connections
```

- [ ] CPU usage reasonable (< 80%)
- [ ] Memory usage stable (< 500MB)
- [ ] No memory leaks over time
- [ ] Database connections stable

### Health Checks
- [ ] Telegram responses working
- [ ] Tool execution completing
- [ ] Scheduler jobs running at correct times
- [ ] No hanging operations

## First Run Checklist ✅

1. **Startup Test**
   ```bash
   python3 main.py
   ```
   - [ ] Server starts without errors
   - [ ] Prints production ready message
   - [ ] Listens for Telegram commands

2. **First Command**
   - [ ] Open Telegram
   - [ ] Send `/start` to bot
   - [ ] Receive welcome message

3. **Status Check**
   - [ ] Send `/status` to bot
   - [ ] Receive agent status information
   - [ ] Shows tools are registered

4. **Test Task**
   - [ ] Send a simple message to bot
   - [ ] Agent processes the request
   - [ ] Response received successfully

5. **Monitor Logs**
   - [ ] Check `nexus.log` for operation details
   - [ ] No critical errors shown
   - [ ] API costs tracked correctly

## Troubleshooting 🔧

### Common Issues

**Issue: "ModuleNotFoundError"**
```bash
# Solution: Install requirements
pip install -r requirements.txt --upgrade
```

**Issue: "Could not connect to Telegram"**
- [ ] Verify bot token in .env
- [ ] Check internet connection
- [ ] Confirm bot is created with @BotFather

**Issue: "Redis connection failed"**
- [ ] Verify Redis is running: `redis-cli ping`
- [ ] Check REDIS_URL in .env
- [ ] Ensure port is accessible

**Issue: "Supabase connection failed"**
- [ ] Verify SUPABASE_URL and key in .env
- [ ] Check database tables exist
- [ ] Confirm network connectivity to Supabase

**Issue: "API costs high"**
- [ ] Check query patterns
- [ ] Review cached vs fresh requests
- [ ] Consider response caching

## Scaling Considerations 📈

For production deployment:
- [ ] Setup auto-scaling rules
- [ ] Configure load balancing
- [ ] Use connection pooling
- [ ] Implement rate limiting
- [ ] Setup monitoring alerts
- [ ] Create backup & recovery plan
- [ ] Plan disaster recovery

## Documentation Review 📚

Before going live, review:
- [ ] README.md - Feature overview
- [ ] SETUP.md - Installation details
- [ ] QUICKSTART.md - Getting started
- [ ] REVIEW.md - Technical validation
- [ ] CHANGELOG.md - All modifications
- [ ] SUMMARY.md - Executive summary

## Launch Decision ✅

- [ ] All validation checks passed
- [ ] Configuration complete
- [ ] Database initialized
- [ ] All services tested
- [ ] Logs monitoring operational
- [ ] Scaling plan in place
- [ ] Backup plan documented
- [ ] Team trained and ready

**Status:** Ready for Production Deployment! 🚀

---

## Post-Deployment Tasks

After going live:

### Week 1
- [ ] Monitor system performance
- [ ] Track API costs
- [ ] Collect feedback
- [ ] Fix any issues

### Week 2-4
- [ ] Analyze execution patterns
- [ ] Optimize long-running tasks
- [ ] Fine-tune timeouts
- [ ] Review error logs

### Monthly
- [ ] Review cost reports
- [ ] Update tool mappings
- [ ] Clean old logs
- [ ] Check security patches

---

**Deployment Checklist Version:** 1.0
**Last Updated:** 2024
**Status:** READY FOR PRODUCTION ✅
