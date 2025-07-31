"""
Start command plugin.
Handles the /start command with welcome message.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
try:
    from web_server import status_tracker
except ImportError:
    status_tracker = None

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    try:
        user = update.effective_user
        if user and update.message:
            welcome_message = f"""
🤖 *¡Bienvenido al Bot, {user.first_name or 'Amigo'}!*

Estoy aquí para ayudarte con varias tareas. Esto es lo que puedo hacer:

• `/start` - Mostrar este mensaje de bienvenida
• `/help` - Obtener ayuda y ver comandos disponibles
• ¡Envíame cualquier mensaje de texto y te responderé!

Siéntete libre de explorar e interactuar conmigo. Escribe /help para más información.
            """
            
            await update.message.reply_text(
                welcome_message,
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Log statistics for web dashboard
            if status_tracker:
                status_tracker.log_command(user.id)
            
            # Decorated console output
            print(f"\n🚀 Mensaje recibido: /start")
            print(f"👤 Usuario: {user.id}")
            print(f"🤖 Respuesta: Mensaje de bienvenida enviado")
            print("═" * 50)
            
            logger.info(f"User {user.id} ({user.username or 'unknown'}) started the bot")
        
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        if update.message:
            await update.message.reply_text(
                "Lo siento, algo salió mal. Por favor intenta de nuevo más tarde."
            )