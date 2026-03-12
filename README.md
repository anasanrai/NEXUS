# NEXUS - Autonomous AI Operating System

A production-ready autonomous AI agent system for businesses. NEXUS automates everything from web research to deployments, email management, social media posting, and more.

**Status**: ✅ **PRODUCTION READY** - See [INDEX.md](INDEX.md) for complete documentation navigation.

## 🚀 Quick Links

- **[INDEX.md](INDEX.md)** - Documentation navigation guide (start here!)
- **[SUMMARY.md](SUMMARY.md)** - Executive summary (5 min read)
- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[SETUP.md](SETUP.md)** - Detailed configuration guide
- **[REVIEW.md](REVIEW.md)** - Technical validation report

## 🚀 Features

### Core Capabilities
- **Web Intelligence**: Search, research, and scrape web content
- **Browser Automation**: Navigate, click, fill forms, extract data
- **Code Management**: Write, debug, test, and deploy code via Git
- **Workflow Automation**: Create and manage n8n workflows
- **Deployment**: Manage Vercel, AWS, and other platforms
- **Content Creation**: Generate images, videos, and audio
- **Social Media**: Post to Twitter, LinkedIn, Instagram with scheduling
- **Email**: Send, receive, search, and manage emails
- **Payment Processing**: Handle Stripe payments and invoices
- **Communication**: Telegram bot for command interface
- **Memory**: Long-term semantic memory with Supabase + pgvector
- **Self-Expansion**: Install packages and tools on demand

### Intelligence
- **Smart Routing**: Auto-selects optimal AI model per task
- **Task Planning**: Decomposes complex tasks into subtasks
- **Error Handling**: Retry logic with exponential backoff
- **Cost Tracking**: Monitors API costs per task and model

## 🏗️ Architecture

```
nexus/
├── agent/           # Core agent logic (router, planner, executor)
├── tools/          # Tool registry and implementations
├── memory/         # Short-term (Redis) and long-term (Supabase)
├── channels/       # Communication interfaces (Telegram)
├── scheduler/      # Autonomous task scheduling
├── config.py       # Environment and configuration
└── main.py        # Entry point
```

## 📋 Tech Stack

- **Language**: Python 3.12
- **LLMs**: OpenRouter (minimax, GLM-5, Gemini 2.5-flash, Claude Sonnet)
- **Browser**: Playwright + browser-use
- **Memory**: Supabase + pgvector
- **Cache**: Redis
- **Messaging**: Telegram API
- **Scheduler**: APScheduler
- **Web Search**: Tavily API
- **Media**: Replicate, Kling, Fish Audio

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/nexus.git
cd nexus
```

### 2. Setup Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Setup Supabase
```sql
-- Create tables for memory and entities
CREATE TABLE memories (
  id BIGSERIAL PRIMARY KEY,
  content TEXT,
  metadata JSONB,
  embedding vector(32),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE clients (id BIGSERIAL PRIMARY KEY, name TEXT, email TEXT);
CREATE TABLE tasks (id BIGSERIAL PRIMARY KEY, title TEXT, status TEXT, description TEXT);
CREATE TABLE events (id BIGSERIAL PRIMARY KEY, title TEXT, start_time TIMESTAMP, end_time TIMESTAMP);
CREATE TABLE revenue (id BIGSERIAL PRIMARY KEY, amount FLOAT, source TEXT, description TEXT, date TIMESTAMP);
```

### 5. Start Redis (Optional)
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

## 🚀 Usage

### Start NEXUS
```bash
python main.py
```

### Via Telegram
```
Send any message to your NEXUS Telegram bot to execute tasks

Commands:
/start   - Initialize
/help    - Show help
/status  - Agent status
/tasks   - Pending tasks
/revenue - Revenue summary
```

### Via Python API
```python
from agent.core import nexus_core

result = await nexus_core.process_message(
    "Search for Python async tutorials",
    session_id="session_123"
)
```

## 📊 Examples

### Task Examples
- "Search for machine learning trends in 2024"
- "Create a blog post about AI and publish it to WordPress"
- "Post a LinkedIn article with an AI-generated image"
- "Deploy the latest code to Vercel and send me the URL"
- "Send an email summary of today's activity"
- "Execute the 'lead_generation' n8n workflow"

### Autonomous Scheduling
- 6 AM: Morning briefing with yesterday's metrics
- 9 AM: Hunt for Upwork freelance projects
- 11 AM: Post daily LinkedIn content
- 6 PM: Evening summary with costs and results

## 💰 Cost Optimization

NEXUS automatically selects the most cost-effective model:
- **Simple tasks**: Gemini 2.5-flash (cheapest)
- **Browser tasks**: GLM-5 (best vision)
- **Complex tasks**: minimax-m2.5 (best tool calling)
- **Fallback**: Claude Sonnet (most reliable)

Track costs with:
```bash
# In Telegram
/status  # Shows total API costs
```

## � Documentation

- **[SUMMARY.md](SUMMARY.md)** - Executive summary with quick overview
- **[REVIEW.md](REVIEW.md)** - Complete validation report and architecture verification
- **[SETUP.md](SETUP.md)** - Detailed installation and configuration guide
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start guide
- **[CHANGELOG.md](CHANGELOG.md)** - Complete change log of all modifications

## �🔒 Security

- ✅ API keys in .env (never committed)
- ✅ Approval required for payments
- ✅ All actions logged
- ✅ HTTPS for external APIs
- ✅ Token rotation recommended

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Logs
docker-compose logs -f nexus
```

## 📈 Monitoring

- **Telegram**: Real-time notifications
- **Logs**: `nexus.log` with all operations
- **Memory**: Redis + Supabase for context
- **Metrics**: Cost, execution time, success rate

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Add tests
4. Submit a PR

## 📄 License

MIT License - See LICENSE file

## 🔗 Links

- [OpenRouter API](https://openrouter.ai)
- [Supabase](https://supabase.com)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Tavily Search](https://tavily.com)

## 💬 Support

- GitHub Issues: Bug reports and feature requests
- Email: support@nexusai.com
- Telegram: @nexus_ai_bot

---

**NEXUS** - Your autonomous AI operating system for business success 🤖✨
