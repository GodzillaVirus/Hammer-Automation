import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import settings
from browser_manager import browser_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.app = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🔨 *Hammer Automation Bot*\n\n"
            "Available commands:\n"
            "/status - Check API status\n"
            "/sessions - List active sessions\n"
            "/help - Show help message\n\n"
            "Send any message to execute custom commands.",
            parse_mode='Markdown'
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        active_sessions = len(browser_manager.sessions)
        await update.message.reply_text(
            f"✅ *API Status: Online*\n\n"
            f"Active Sessions: {active_sessions}\n"
            f"Browser: Playwright + Stealth\n"
            f"Features: Cloudflare Bypass, CAPTCHA Solving",
            parse_mode='Markdown'
        )
    
    async def sessions_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not browser_manager.sessions:
            await update.message.reply_text("No active sessions")
            return
        
        message = "*Active Sessions:*\n\n"
        for session_id, session in browser_manager.sessions.items():
            age = asyncio.get_event_loop().time() - session.created_at
            message += f"• `{session_id[:8]}...` ({int(age)}s ago)\n"
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "*Hammer Automation Help*\n\n"
            "This bot controls the Hammer Automation API.\n\n"
            "*Features:*\n"
            "• Cloudflare Turnstile bypass\n"
            "• hCaptcha & reCAPTCHA solving\n"
            "• Anti-detection browser\n"
            "• Rate limit bypass\n"
            "• Session management\n\n"
            "*Commands:*\n"
            "/start - Start the bot\n"
            "/status - Check API status\n"
            "/sessions - List active sessions\n"
            "/help - Show this help",
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Command not recognized. Use /help for available commands."
        )
    
    async def initialize(self):
        self.app = Application.builder().token(settings.telegram_bot_token).build()
        
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("sessions", self.sessions_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        
        logger.info("Telegram bot started successfully")
    
    async def shutdown(self):
        if self.app:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
        
        logger.info("Telegram bot shut down successfully")

telegram_bot = TelegramBot()
