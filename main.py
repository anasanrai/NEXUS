import asyncio
import logging
from agent.core import NexusAgent
from channels.telegram import TelegramChannel
from scheduler.cron import CronScheduler
from config import settings

async def main():
    # Setup Logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger("nexus.main")
    logger.info("Initializing NEXUS Agent Framework...")

    # 1. Initialize Agent Core
    agent = NexusAgent()

    # 2. Initialize Scheduler
    scheduler = CronScheduler()
    # Example job: scheduler.add_job(agent.some_periodic_task, 'interval', minutes=60)
    scheduler.start()

    # 3. Initialize Channels
    telegram = TelegramChannel(agent)
    
    logger.info("NEXUS System Ready.")

    # Run Telegram bot (blocking)
    try:
        await telegram.start()
    except KeyboardInterrupt:
        logger.info("Shutting down NEXUS...")
    finally:
        scheduler.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
