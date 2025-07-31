"""
Message handling plugin.
Handles regular text messages from users.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
try:
    from web_server import status_tracker
except ImportError:
    status_tracker = None

logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages from users."""
    try:
        user = update.effective_user
        if user and update.message and update.message.text:
            message_text = update.message.text
            
            # Decorated console output with essential info
            print(f"\n💬 Mensaje recibido: {message_text}")
            print(f"👤 Usuario: {user.id}")
            
            # Log statistics for web dashboard
            if status_tracker:
                status_tracker.log_message(user.id)
            
            # Simple message processing logic
            response = _process_message(message_text, user.first_name or 'Amigo')
            
            print(f"🤖 Respuesta: {response}")
            print("═" * 50)
            
            # Also log to file for debugging
            logger.info(f"[{user.first_name or 'Desconocido'}@{user.username or 'unknown'}] {message_text} -> {response}")
            
            await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        if update.message:
            await update.message.reply_text(
                "Lo siento, no pude procesar tu mensaje. Por favor intenta de nuevo."
            )

def _process_message(message: str, user_name: str) -> str:
    """Process the user's message and generate an appropriate response."""
    message_lower = message.lower().strip()
    
    # Greeting responses
    if any(greeting in message_lower for greeting in ['hola', 'hi', 'hey', 'buenos días', 'buenas tardes', 'buenas noches', 'hello']):
        return f"¡Hola {user_name}! 👋 ¿Cómo puedo ayudarte hoy?"
    
    # Question responses
    elif message_lower.endswith('?'):
        return f"¡Esa es una pregunta interesante, {user_name}! 🤔 Todavía estoy aprendiendo, pero me encantaría ayudarte a explorar ese tema."
    
    # Gratitude responses
    elif any(thanks in message_lower for thanks in ['gracias', 'thank', 'thanks', 'appreciate']):
        return "¡De nada! 😊 Estoy feliz de ayudar en cualquier momento."
    
    # Goodbye responses
    elif any(bye in message_lower for bye in ['adiós', 'chau', 'nos vemos', 'bye', 'goodbye', 'see you', 'farewell']):
        return f"¡Adiós {user_name}! 👋 Siéntete libre de volver cuando quieras. ¡Que tengas un gran día!"
    
    # Help-related responses
    elif any(help_word in message_lower for help_word in ['ayuda', 'help', 'assist', 'support']):
        return "¡Estoy aquí para ayudar! 💪 Puedes usar /help para ver qué puedo hacer, ¡o sigue charlando conmigo!"
    
    # Positive responses
    elif any(positive in message_lower for positive in ['bueno', 'genial', 'excelente', 'increíble', 'good', 'great', 'awesome', 'excellent', 'amazing']):
        return f"¡Es maravilloso escuchar eso, {user_name}! 🎉 ¡Las vibras positivas son las mejores!"
    
    # Default response for other messages
    else:
        responses = [
            f"Gracias por compartir eso conmigo, {user_name}! 💭",
            f"Punto interesante, {user_name}! Cuéntame más al respecto.",
            f"Te escucho, {user_name}! 👂 ¿De qué más te gustaría hablar?",
            f"¡Qué genial, {user_name}! Disfruto nuestra conversación. 😊",
            f"Te estoy escuchando, {user_name}! Siéntete libre de compartir más pensamientos."
        ]
        # Simple hash-based selection for consistency
        response_index = hash(message) % len(responses)
        return responses[response_index]