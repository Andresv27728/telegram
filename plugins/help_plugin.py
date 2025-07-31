"""
Help command plugin.
Handles the /help command with available commands information.
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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    try:
        if update.message:
            help_message = """
📋 *Comandos Disponibles:*

🏁 `/start` - Iniciar el bot y ver mensaje de bienvenida
❓ `/help` - Mostrar este mensaje de ayuda
🔊 `/echo [mensaje]` - Repetir tu mensaje

📝 *Tipos de Mensajes que Apoyo:*
• Mensajes de texto - Responderé a cualquier texto que envíes
• Comandos - Usa los comandos listados arriba

💡 *Consejos:*
• Solo escribe cualquier mensaje y te responderé
• Los comandos empiezan con una barra diagonal (/)
• Ejemplo: /echo ¡Hola mundo!
• ¡Siempre estoy aprendiendo y mejorando!

Si encuentras algún problema, por favor reinicia con /start
            """
            
            await update.message.reply_text(
                help_message,
                parse_mode=ParseMode.MARKDOWN
            )
            
            if update.effective_user:
                # Log statistics for web dashboard
                if status_tracker:
                    status_tracker.log_command(update.effective_user.id)
                
                # Decorated console output
                user = update.effective_user
                print(f"\n❓ Mensaje recibido: /help")
                print(f"👤 Usuario: {user.id}")
                print(f"🤖 Respuesta: Mensaje de ayuda enviado")
                print("═" * 50)
                
                logger.info(f"User {update.effective_user.id} requested help")
        
    except Exception as e:
        logger.error(f"Error in help_command: {e}")
        if update.message:
            await update.message.reply_text(
                "Lo siento, no pude cargar la información de ayuda. Por favor intenta de nuevo."
            )