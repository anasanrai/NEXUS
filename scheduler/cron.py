"""
NEXUS Scheduler
Autonomous scheduled tasks and cron jobs.
"""

import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta

from agent.core import nexus_core
from memory.entities import get_revenue_summary, get_pending_tasks
from channels.telegram import telegram_channel

logger = logging.getLogger(__name__)


class NEXUSScheduler:
    """Autonomous task scheduler."""
    
    def __init__(self):
        """Initialize scheduler."""
        self.scheduler = AsyncIOScheduler()
    
    async def initialize(self):
        """Initialize and register jobs."""
        # Morning briefing - 6 AM
        self.scheduler.add_job(
            self._morning_briefing,
            CronTrigger(hour=6, minute=0),
            id="morning_briefing",
        )
        
        # Heartbeat - every 30 minutes
        self.scheduler.add_job(
            self._heartbeat,
            CronTrigger(minute="*/30"),
            id="heartbeat",
        )
        
        # Hunt Upwork jobs - 9 AM
        self.scheduler.add_job(
            self._hunt_upwork_jobs,
            CronTrigger(hour=9, minute=0),
            id="upwork_hunt",
        )
        
        # Post LinkedIn content - 11 AM
        self.scheduler.add_job(
            self._post_linkedin,
            CronTrigger(hour=11, minute=0),
            id="linkedin_post",
        )
        
        # Check pending tasks - every hour
        self.scheduler.add_job(
            self._check_pending_tasks,
            CronTrigger(minute=0),
            id="check_tasks",
        )
        
        # Evening summary - 6 PM
        self.scheduler.add_job(
            self._evening_summary,
            CronTrigger(hour=18, minute=0),
            id="evening_summary",
        )
        
        logger.info("Scheduler initialized with 6 jobs")
    
    async def start(self):
        """Start scheduler."""
        try:
            await self.initialize()
            self.scheduler.start()
            logger.info("✓ Scheduler started (6 jobs)")
        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}")
            raise
    
    async def stop(self):
        """Stop scheduler."""
        try:
            if self.scheduler and self.scheduler.running:
                self.scheduler.shutdown()
            logger.info("Scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {str(e)}")
    
    async def _morning_briefing(self):
        """Morning briefing task."""
        logger.info("Executing morning briefing")
        
        try:
            # Get revenue with timeout
            revenue = await asyncio.wait_for(
                get_revenue_summary(days=1),
                timeout=30.0
            )
            
            # Get pending tasks with timeout
            tasks = await asyncio.wait_for(
                get_pending_tasks(),
                timeout=30.0
            )
            
            message = "🌅 **Morning Briefing**\n\n"
            message += f"Yesterday's Revenue: ${revenue.get('total', 0):.2f}\n"
            message += f"Pending Tasks: {len(tasks)}\n"
            message += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            await asyncio.wait_for(
                telegram_channel.send_notification(message),
                timeout=10.0
            )
            logger.info("✓ Morning briefing sent")
        except asyncio.TimeoutError:
            logger.error("Morning briefing timed out")
        except Exception as e:
            logger.error(f"Morning briefing failed: {str(e)}")
    
    async def _heartbeat(self):
        """Periodic heartbeat check."""
        logger.debug("Heartbeat check")
        
        try:
            status = await asyncio.wait_for(
                nexus_core.get_status(),
                timeout=15.0
            )
            # Just log status for monitoring
            logger.debug(f"Heartbeat OK: {status.get('status')} - Tools: {status.get('tools_available')}")
        except asyncio.TimeoutError:
            logger.warning("Heartbeat timeout")
        except Exception as e:
            logger.warning(f"Heartbeat check failed: {str(e)}")
    
    async def _hunt_upwork_jobs(self):
        """Hunt for Upwork jobs."""
        logger.info("🔍 Hunting Upwork jobs")
        
        try:
            task = "Search for Python and AI projects on Upwork with budget > $500"
            result = await asyncio.wait_for(
                nexus_core.process_message(task),
                timeout=120.0
            )
            logger.info(f"✓ Upwork hunt completed: {len(result.get('response', ''))} chars")
        except asyncio.TimeoutError:
            logger.warning("Upwork hunt timed out (120s)")
        except Exception as e:
            logger.error(f"Upwork hunt failed: {str(e)}")
    
    async def _post_linkedin(self):
        """Post LinkedIn content."""
        logger.info("📱 Posting to LinkedIn")
        
        try:
            task = "Generate and post an interesting article about AI trends to LinkedIn"
            result = await asyncio.wait_for(
                nexus_core.process_message(task),
                timeout=120.0
            )
            logger.info("✓ LinkedIn post sent")
        except asyncio.TimeoutError:
            logger.warning("LinkedIn post timed out (120s)")
        except Exception as e:
            logger.error(f"LinkedIn post failed: {str(e)}")
    
    async def _check_pending_tasks(self):
        """Check and execute pending tasks."""
        logger.info("📋 Checking pending tasks")
        
        try:
            tasks = await asyncio.wait_for(
                get_pending_tasks(),
                timeout=30.0
            )
            if tasks:
                logger.info(f"Found {len(tasks)} pending tasks")
                # Execute first task with timeout
                task = tasks[0]
                await asyncio.wait_for(
                    nexus_core.process_message(f"Execute: {task.get('description', '')}"),
                    timeout=120.0
                )
                logger.info("✓ Pending task executed")
        except asyncio.TimeoutError:
            logger.warning("Check pending tasks timed out")
        except Exception as e:
            logger.error(f"Check tasks failed: {str(e)}")
    
    async def _evening_summary(self):
        """Evening summary."""
        logger.info("🌆 Generating evening summary")
        
        try:
            # Get daily metrics with timeouts
            revenue = await asyncio.wait_for(
                get_revenue_summary(days=1),
                timeout=30.0
            )
            tasks = await asyncio.wait_for(
                get_pending_tasks(),
                timeout=30.0
            )
            status = await asyncio.wait_for(
                nexus_core.get_status(),
                timeout=15.0
            )
            
            message = "🌆 **Evening Summary**\n\n"
            message += f"Today's Revenue: ${revenue.get('total', 0):.2f}\n"
            message += f"API Costs: ${status.get('cost_summary', {}).get('total', 0):.4f}\n"
            message += f"Pending Tasks: {len(tasks)}\n"
            message += f"Success Rate: {status.get('execution_summary', {}).get('success_rate', 0)*100:.0f}%\n"
            
            await asyncio.wait_for(
                telegram_channel.send_notification(message),
                timeout=10.0
            )
            logger.info("✓ Evening summary sent")
        except asyncio.TimeoutError:
            logger.warning("Evening summary timed out")
        except Exception as e:
            logger.error(f"Evening summary failed: {str(e)}")


# Global instance
nexus_scheduler = NEXUSScheduler()
