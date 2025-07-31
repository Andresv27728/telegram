"""
Error handling plugin.
Handles errors that occur during bot operation.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
try:
    from web_server import status_tracker
except ImportError:
    status_tracker = None

logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors that occur during bot operation."""
    # Colors for console output
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    
    import datetime
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Decorated error logging
    print(f"\n⚠️ ERROR: {context.error}")
    if isinstance(update, Update) and update.effective_user:
        user = update.effective_user
        print(f"👤 Usuario: {user.id}")
    print("═" * 50)
    
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Log error for web dashboard
    if status_tracker:
        status_tracker.log_error()
    
    # If we have an update with a message, try to inform the user
    if isinstance(update, Update) and update.message:
        try:
            await update.message.reply_text(
                "¡Ups! Algo salió mal de mi lado. 🔧 Por favor intenta de nuevo en un momento."
            )
        except Exception as e:
            logger.error(f"Failed to send error message to user: {e}")