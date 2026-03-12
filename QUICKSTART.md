# QUICKSTART Guide for NEXUS

## 🚀 5-Minute Quick Start

### 1. Clone & Setup
```bash
cd /path/to/NEXUS
cp .env.example .env
```

### 2. Add Your API Keys
Edit `.env` with:
- OPENROUTER_API_KEY (from openrouter.ai)
- TELEGRAM_BOT_TOKEN (from @BotFather)
- TELEGRAM_CHAT_ID (your user ID)
- SUPABASE_URL & SUPABASE_KEY
- Other optional keys

### 3. Install & Run
```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Start NEXUS
python main.py
```

### 4. Test with Telegram
Send a message to your NEXUS bot on Telegram!

```
/start          - Initialize
/status         - Check status
/help           - Show commands
```

Or just send any task:
```
"Search for Python tutorials"
"Create a blog post about AI"
```

---

## 📊 Optional: Dashboard Setup

### Install & Run Dashboard
```bash
cd dashboard
npm install
npm run dev
```

Open http://localhost:3000


## 🔄 With Docker (Recommended for Production)

```bash
# Build and run everything
docker-compose up -d

# Check logs
docker-compose logs -f nexus

# Stop
docker-compose down
```

---

## 💡 Example Tasks

```
# Web Research
"Search for latest AI trends and summarize"

# Content Creation
"Write a blog post about machine learning and post it to WordPress"

# Automation
"Check my inbox and send me a summary email"

# Coding
"Create a Python function to calculate fibonacci and push to GitHub"

# Social Media
"Generate an AI image and post it to LinkedIn"

# Analytics
"Get my revenue summary for last 30 days"
```

---

## 🆘 Troubleshooting

### Check Status
```bash
# Via Telegram
/status

# Via logs
tail -f nexus.log
```

### Redis Not Running
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

### API Key Issues
- Verify keys in .env
- Check key permissions
- Test with: `python -c "from config import config; print(config.llm.openrouter_api_key[:10])..."`

---

## 📈 Upgrade to Production

1. Configure Supabase
2. Deploy with Docker
3. Set up monitoring
4. Configure auto-scaling
5. Add custom workflows

See SETUP.md for detailed guide.

---

**Start using NEXUS now!** 🤖✨
