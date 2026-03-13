from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import config
import logging

class TelegramChannel:
    """Interface for Telegram bot communication."""
    
    def __init__(self, agent: Any):
        self.token = config.TELEGRAM_BOT_TOKEN
        self.agent = agent
        self.logger = logging.getLogger("nexus.channels.telegram")

    async def start(self):
        """Starts the Telegram bot poll."""
        if not self.token:
            self.logger.error("TELEGRAM_BOT_TOKEN not configured")
            return

        app = ApplicationBuilder().token(self.token).build()
        
        # Handlers
        app.add_handler(CommandHandler("start", self._handle_help))
        app.add_handler(CommandHandler("help", self._handle_help))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self._handle_message))
        
        self.logger.info("Telegram bot starting...")
        await app.run_polling()

    async def _handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("NEXUS Agent Framework. Send me a message to begin.")

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text
        # Process via agent
        response = await self.agent.process_message(user_text)
        await update.message.reply_text(response)
