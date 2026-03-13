from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Callable, Any
import logging

class CronScheduler:
    """Manages periodic tasks and scheduled jobs."""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.logger = logging.getLogger("nexus.scheduler")

    def add_job(self, func: Callable, trigger: str, **kwargs):
        """
        Schedules a new job.
        trigger: 'interval', 'cron', or 'date'
        """
        self.scheduler.add_job(func, trigger, **kwargs)
        self.logger.info(f"Scheduled job: {func.__name__} with {trigger} trigger")

    def start(self):
        """Starts the scheduler."""
        self.scheduler.start()
        self.logger.info("Scheduler started.")

    def stop(self):
        """Stops the scheduler."""
        self.scheduler.shutdown()
        self.logger.info("Scheduler stopped.")
