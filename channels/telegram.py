"""
Telegram Bot Channel
Interface for receiving commands and sending updates via Telegram.
"""

import logging
import asyncio
from typing import Optional
from telegram import Update, ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from datetime import datetime

from config import config
from agent.core import nexus_core

logger = logging.getLogger(__name__)


class TelegramChannel:
    """Telegram bot interface."""
    
    def __init__(self):
        """Initialize Telegram bot."""
        self.token = config.telegram.bot_token
        self.chat_id = int(config.telegram.chat_id)
        self.app = None
    
    async def initialize(self):
        """Initialize bot application."""
        self.app = Application.builder().token(self.token).build()
        
        # Register handlers
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("tasks", self.cmd_tasks))
        self.app.add_handler(CommandHandler("revenue", self.cmd_revenue))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        
        logger.info("Telegram bot initialized")
    
    async def start(self):
        """Start bot."""
        try:
            await self.initialize()
            await self.app.initialize()
            await self.app.start()
            await self.app.updater.start_polling()
            logger.info("✓ Telegram bot started")
        except Exception as e:
            logger.error(f"Failed to start Telegram bot: {str(e)}")
            raise
    
    async def stop(self):
        """Stop bot."""
        try:
            if self.app:
                await self.app.stop()
                await self.app.shutdown()
            logger.info("Telegram bot stopped")
        except Exception as e:
            logger.error(f"Error stopping Telegram bot: {str(e)}")
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        try:
            message = "🤖 **NEXUS Online**\n\n"
            message += "Autonomous AI Operating System\n\n"
            message += "Commands:\n"
            message += "/help - Show help\n"
            message += "/status - Agent status\n"
            message += "/tasks - Pending tasks\n"
            message += "/revenue - Revenue summary\n"
            
            await update.message.reply_text(message, parse_mode="markdown")
        except Exception as e:
            logger.error(f"cmd_start failed: {str(e)}")
            await update.message.reply_text("Error: Could not send message")
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        try:
            help_text = """
*NEXUS Commands*

*Task Execution*
- Send any message to execute a task
- NEXUS will plan and execute automatically

*Information*
- /status - Get system status
- /tasks - View pending tasks
- /revenue - Revenue summary for last 30 days

*Management*
- /cancel - Cancel current task
- /logs - View recent logs

*Examples*
"Search for Python async best practices"
"Create a blog post about AI"
"Deploy to Vercel"
            """
            await update.message.reply_text(help_text, parse_mode="markdown")
        except Exception as e:
            logger.error(f"cmd_help failed: {str(e)}")
            await update.message.reply_text("Error: Could not send help")
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        try:
            status = await nexus_core.get_status()
            
            message = "🟢 **NEXUS Status**\n\n"
            message += f"Status: {status.get('status', 'unknown')}\n"
            message += f"Version: {status.get('version', 'N/A')}\n"
            message += f"Tools Available: {status.get('tools_available', 0)}\n"
            message += f"Session: {status.get('session_id', 'N/A')[:8]}...\n\n"
            
            cost = status.get('cost_summary', {})
            message += f"💰 Total Cost: ${cost.get('total', 0):.4f}\n"
            
            await update.message.reply_text(message, parse_mode="markdown")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def cmd_tasks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /tasks command."""
        try:
            from memory.entities import get_pending_tasks
            tasks = await get_pending_tasks()
            
            if not tasks:
                await update.message.reply_text("✅ No pending tasks")
                return
            
            message = f"📋 **Pending Tasks ({len(tasks)})**\n\n"
            for task in tasks[:5]:
                message += f"- {task.get('title', 'N/A')}\n"
            
            if len(tasks) > 5:
                message += f"\n... and {len(tasks) - 5} more"
            
            await update.message.reply_text(message, parse_mode="markdown")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def cmd_revenue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /revenue command."""
        try:
            from memory.entities import get_revenue_summary
            summary = await get_revenue_summary(days=30)
            
            message = "💵 **Revenue Summary (30 days)**\n\n"
            message += f"Total: ${summary.get('total', 0):.2f}\n"
            message += f"Transactions: {summary.get('count', 0)}\n\n"
            
            by_source = summary.get('by_source', {})
            if by_source:
                message += "**By Source:**\n"
                for source, amount in by_source.items():
                    message += f"- {source}: ${amount:.2f}\n"
            
            await update.message.reply_text(message, parse_mode="markdown")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages."""
        try:
            user_message = update.message.text
            
            # Show typing indicator
            await update.message.chat.send_action(ChatAction.TYPING)
            
            # Process with NEXUS
            result = await nexus_core.process_message(
                user_message,
                session_id=f"telegram_{update.effective_user.id}",
            )
            
            response = result.get("response", "No response generated")
            
            # Split long messages
            if len(response) > 4096:
                for i in range(0, len(response), 4096):
                    await update.message.reply_text(
                        response[i:i+4096],
                        parse_mode="markdown",
                    )
            else:
                await update.message.reply_text(response, parse_mode="markdown")
            
            # Log cost
            cost = result.get("cost", 0)
            if cost > 0:
                logger.info(f"Task cost: ${cost:.4f}")
        
        except Exception as e:
            logger.error(f"Handle message failed: {str(e)}")
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def send_notification(self, message: str, parse_mode: str = "markdown"):
        """Send notification to admin."""
        try:
            if self.app:
                await self.app.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode=parse_mode,
                )
        except Exception as e:
            logger.error(f"Send notification failed: {str(e)}")


# Global instance
telegram_channel = TelegramChannel()
