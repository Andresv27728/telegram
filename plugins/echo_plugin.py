"""
Echo command plugin - Example of how to add new commands.
Handles the /echo command that repeats what the user says.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
try:
    from web_server import status_tracker
except ImportError:
    status_tracker = None

logger = logging.getLogger(__name__)

async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /echo command - repeats the user's message."""
    try:
        if update.message:
            # Get the text after the /echo command
            message_text = update.message.text
            if message_text and len(message_text.split()) > 1:
                # Remove "/echo " from the beginning
                echo_text = message_text[6:].strip()
                response = f"🔊 Repitiendo: {echo_text}"
            else:
                response = "🔊 Usa: /echo [tu mensaje aquí]\n\nEjemplo: /echo ¡Hola mundo!"
            
            if update.effective_user:
                # Log statistics for web dashboard
                if status_tracker:
                    status_tracker.log_command(update.effective_user.id)
                
                # Decorated console output
                user = update.effective_user
                print(f"\n🔊 Mensaje recibido: {message_text}")
                print(f"👤 Usuario: {user.id}")
                print(f"🤖 Respuesta: {response}")
                print("═" * 50)
                
                logger.info(f"User {update.effective_user.id} used echo command")
            
            await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error in echo_command: {e}")
        if update.message:
            await update.message.reply_text(
                "Lo siento, no pude procesar el comando echo. Intenta de nuevo."
            )