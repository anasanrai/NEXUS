"""
NEXUS Setup Instructions
"""

# Quick Start Guide

## Prerequisites
- Python 3.12+
- Redis (for short-term memory)
- Supabase account
- API keys for: OpenRouter, Telegram, Gemini, GitHub, Tavily

## Step-by-Step Setup

### 1. Environment Setup
```bash
cd /path/to/nexus
cp .env.example .env
# Edit .env with your actual API keys
```

### 2. Python Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Database Setup

#### Supabase Tables
Create these tables in your Supabase project:

**memories** (for long-term memory)
```sql
create table memories (
  id bigserial primary key,
  content text,
  metadata jsonb,
  embedding vector(32),
  created_at timestamp default now()
);
create index on memories using ivfflat (embedding vector_cosine_ops);
```

**clients** (for client management)
```sql
create table clients (
  id bigserial primary key,
  name text,
  email text unique,
  phone text,
  company text,
  created_at timestamp default now()
);
```

**tasks** (for task management)
```sql
create table tasks (
  id bigserial primary key,
  title text,
  description text,
  status text default 'pending',
  priority int default 1,
  created_at timestamp default now(),
  due_date timestamp
);
```

**events** (for calendar)
```sql
create table events (
  id bigserial primary key,
  title text,
  description text,
  start_time timestamp,
  end_time timestamp,
  attendees text[],
  created_at timestamp default now()
);
```

**revenue** (for tracking)
```sql
create table revenue (
  id bigserial primary key,
  amount float,
  source text,
  description text,
  date timestamp default now()
);
```

### 4. Redis Setup
```bash
# Option 1: Using Docker
docker run -d -p 6379:6379 redis:7-alpine

# Option 2: Using Homebrew (macOS)
brew install redis
redis-server
```

### 5. Telegram Bot Setup
1. Go to @BotFather on Telegram
2. Create a new bot: /newbot
3. Copy the token to .env as TELEGRAM_BOT_TOKEN
4. Get your user ID: @userinfobot
5. Copy to .env as TELEGRAM_CHAT_ID

### 6. API Keys
- **OpenRouter**: Get from openrouter.ai
- **Gemini**: Get from Google AI Studio
- **Tavily**: Get from tavily.com
- **Anthropic**: Get from console.anthropic.com
- **GitHub**: Personal access token from github.com/settings/tokens
- **Vercel**: Token from vercel.com/account/tokens
- **Supabase**: Project API keys from supabase dashboard

## Testing

### Test Agent
```python
python -c "
import asyncio
from agent.core import nexus_core

result = asyncio.run(nexus_core.process_message('Hello NEXUS'))
print(result)
"
```

### Test Tools
```bash
# Test web search
python -c "
import asyncio
from tools.search import web_search

result = asyncio.run(web_search('Python async tutorials'))
print(result)
"
```

## Running NEXUS

### Development
```bash
python main.py
```

### Production with Docker
```bash
docker-compose up -d
docker-compose logs -f nexus
```

## Monitoring

### Telegram Commands
```
/start   - Initialize NEXUS
/help    - Show help
/status  - System status
/tasks   - Pending tasks
/revenue - Revenue summary
```

### Log Files
```bash
tail -f nexus.log
```

### Redis
```bash
redis-cli
> KEYS session:*
> LRANGE session:session_123:messages 0 -1
```

## Troubleshooting

### Can't connect to Redis
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG
```

### Supabase connection error
- Verify SUPABASE_URL and SUPABASE_KEY in .env
- Check network connectivity
- Verify tables exist in Supabase

### Telegram bot not responding
- Verify TELEGRAM_BOT_TOKEN is correct
- Check Telegram API status
- Ensure chat_id is numeric

### API key errors
- Check all API keys in .env
- Verify keys have correct permissions
- Ensure keys are not expired

## Performance Tuning

### Redis Optimization
```bash
# Increase max clients
redis-cli CONFIG SET maxclients 10000

# Monitor performance
redis-cli MONITOR
```

### Model Selection
For faster responses, use smaller models:
- Simple tasks: Gemini 2.5-flash
- Research: GLM-5
- Complex: minimax-m2.5

## Security Checklist

- [ ] .env file is in .gitignore
- [ ] API keys are revoked if exposed
- [ ] Run on HTTPS only
- [ ] Use strong Redis password
- [ ] Enable Supabase RLS policies
- [ ] Telegram bot token is secure

## Next Steps

1. Configure your first scheduled task
2. Add custom tools
3. Set up monitoring/alerts
4. Deploy to production
5. Integrate with your business systems

---

For detailed documentation, see README.md
