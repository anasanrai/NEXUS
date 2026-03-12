"""
NEXUS Main Entry Point
Starts the agent, Telegram bot, scheduler, and web server.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("nexus.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("🤖 NEXUS Autonomous AI Operating System")
    logger.info("=" * 60)
    
    telegram_channel = None
    nexus_scheduler = None
    
    try:
        from config import config, validate_config
        
        # Validate configuration
        if not validate_config(config):
            logger.error("Missing required configuration variables!")
            logger.error("Please configure .env file with required API keys")
            logger.error("See .env.example for required variables")
            sys.exit(1)
        
        logger.info(f"Environment: {config.app.environment}")
        logger.info(f"Debug: {config.app.debug}")
        
        # Import core components
        from agent.core import nexus_core
        from channels.telegram import TelegramChannel
        from scheduler.cron import NEXUSScheduler
        
        # Initialize NEXUS core
        logger.info("Initializing NEXUS core...")
        try:
            await nexus_core.register_tools()
            logger.info(f"✓ Tools registered: {len(nexus_core.short_term_memory.redis.keys('*') if nexus_core.short_term_memory.redis else [])} memory entries")
        except Exception as e:
            logger.warning(f"Tool registration warning: {str(e)}")
        
        # Start Telegram bot
        if config.telegram.bot_token:
            logger.info("Starting Telegram bot...")
            try:
                telegram_channel = TelegramChannel()
                await telegram_channel.start()
                logger.info("✓ Telegram bot running")
            except Exception as e:
                logger.error(f"Failed to start Telegram bot: {str(e)}")
                telegram_channel = None
        else:
            logger.warning("Telegram bot token not configured, skipping")
        
        # Start scheduler
        logger.info("Starting task scheduler...")
        try:
            nexus_scheduler = NEXUSScheduler()
            await nexus_scheduler.start()
            logger.info("✓ Scheduler running (6 jobs)")
        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}")
            nexus_scheduler = None
        
        # Optional: Start FastAPI server for dashboard
        if config.app.environment == "production":
            logger.info("Starting FastAPI server for dashboard...")
            try:
                from fastapi import FastAPI
                from fastapi.responses import JSONResponse
                import uvicorn
                
                app = FastAPI(title="NEXUS")
                
                @app.get("/api/status")
                async def api_status():
                    """Get NEXUS status."""
                    status = await nexus_core.get_status()
                    return JSONResponse(status)
                
                @app.post("/api/agent/execute")
                async def api_execute(task: dict):
                    """Execute task."""
                    result = await nexus_core.process_message(
                        task.get("message", ""),
                        user_context=task.get("context"),
                    )
                    return JSONResponse(result)
                
                # Run in background thread
                import threading
                def run_server():
                    config_dict = uvicorn.Config(app, host="0.0.0.0", port=8000)
                    server = uvicorn.Server(config_dict)
                    asyncio.run(server.serve())
                
                server_thread = threading.Thread(target=run_server, daemon=True)
                server_thread.start()
                logger.info("✓ FastAPI server running on port 8000")
            except Exception as e:
                logger.warning(f"Dashboard server failed to start: {str(e)}")
        
        logger.info("")
        logger.info("🚀 NEXUS is running!")
        logger.info("=" * 60)
        logger.info("Awaiting tasks via Telegram bot...")
        logger.info("Commands: /help, /status, /tasks, /revenue")
        logger.info("=" * 60)
        logger.info("")
        
        # Keep running
        while True:
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("Shutdown signal received (Ctrl+C)")
    except Exception as e:
        logger.exception(f"Fatal error: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("Shutting down NEXUS...")
        try:
            if telegram_channel:
                await telegram_channel.stop()
                logger.info("Telegram bot stopped")
            if nexus_scheduler:
                await nexus_scheduler.stop()
                logger.info("Scheduler stopped")
        except Exception as e:
            logger.error(f"Shutdown error: {str(e)}")
        
        logger.info("🛑 NEXUS offline")
        logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
