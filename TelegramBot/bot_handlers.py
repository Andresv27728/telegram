"""
Telegram bot handlers for commands and messages.
Contains all the bot's functionality and response logic.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BotHandlers:
    """Class containing all bot command and message handlers."""
    
    @staticmethod
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /start command."""
        try:
            user = update.effective_user
            if user and update.message:
                welcome_message = f"""
🤖 *Welcome to the Bot, {user.first_name or 'Friend'}!*

I'm here to help you with various tasks. Here's what I can do:

• `/start` - Show this welcome message
• `/help` - Get help and see available commands
• Send me any text message and I'll respond!

Feel free to explore and interact with me. Type /help for more information.
                """
                
                await update.message.reply_text(
                    welcome_message,
                    parse_mode=ParseMode.MARKDOWN
                )
                
                logger.info(f"User {user.id} ({user.username or 'unknown'}) started the bot")
            
        except Exception as e:
            logger.error(f"Error in start_command: {e}")
            if update.message:
                await update.message.reply_text(
                    "Sorry, something went wrong. Please try again later."
                )
    
    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /help command."""
        try:
            if update.message:
                help_message = """
📋 *Available Commands:*

🏁 `/start` - Start the bot and see welcome message
❓ `/help` - Show this help message

📝 *Message Types I Support:*
• Text messages - I'll respond to any text you send
• Commands - Use the commands listed above

💡 *Tips:*
• Just type any message and I'll respond
• Commands start with a forward slash (/)
• I'm always learning and improving!

If you encounter any issues, please try restarting with /start
                """
                
                await update.message.reply_text(
                    help_message,
                    parse_mode=ParseMode.MARKDOWN
                )
                
                if update.effective_user:
                    logger.info(f"User {update.effective_user.id} requested help")
            
        except Exception as e:
            logger.error(f"Error in help_command: {e}")
            if update.message:
                await update.message.reply_text(
                    "Sorry, I couldn't load the help information. Please try again."
                )
    
    @staticmethod
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle regular text messages from users."""
        try:
            user = update.effective_user
            if user and update.message and update.message.text:
                message_text = update.message.text
                
                # Log the received message
                logger.info(f"Received message from {user.id} ({user.username or 'unknown'}): {message_text}")
                
                # Simple message processing logic
                response = BotHandlers._process_message(message_text, user.first_name or 'Friend')
                
                await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error in handle_message: {e}")
            if update.message:
                await update.message.reply_text(
                    "Sorry, I couldn't process your message. Please try again."
                )
    
    @staticmethod
    def _process_message(message: str, user_name: str) -> str:
        """Process the user's message and generate an appropriate response."""
        message_lower = message.lower().strip()
        
        # Greeting responses
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return f"Hello {user_name}! 👋 How can I help you today?"
        
        # Question responses
        elif message_lower.endswith('?'):
            return f"That's an interesting question, {user_name}! 🤔 I'm still learning, but I'd love to help you explore that topic."
        
        # Gratitude responses
        elif any(thanks in message_lower for thanks in ['thank', 'thanks', 'appreciate']):
            return "You're very welcome! 😊 I'm happy to help anytime."
        
        # Goodbye responses
        elif any(bye in message_lower for bye in ['bye', 'goodbye', 'see you', 'farewell']):
            return f"Goodbye {user_name}! 👋 Feel free to come back anytime. Have a great day!"
        
        # Help-related responses
        elif any(help_word in message_lower for help_word in ['help', 'assist', 'support']):
            return "I'm here to help! 💪 You can use /help to see what I can do, or just keep chatting with me!"
        
        # Positive responses
        elif any(positive in message_lower for positive in ['good', 'great', 'awesome', 'excellent', 'amazing']):
            return f"That's wonderful to hear, {user_name}! 🎉 Positive vibes are the best!"
        
        # Default response for other messages
        else:
            responses = [
                f"Thanks for sharing that with me, {user_name}! 💭",
                f"Interesting point, {user_name}! Tell me more about it.",
                f"I hear you, {user_name}! 👂 What else would you like to discuss?",
                f"That's cool, {user_name}! I enjoy our conversation. 😊",
                f"I'm listening, {user_name}! Feel free to share more thoughts."
            ]
            # Simple hash-based selection for consistency
            response_index = hash(message) % len(responses)
            return responses[response_index]
    
    @staticmethod
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors that occur during bot operation."""
        logger.error(f"Exception while handling an update: {context.error}")
        
        # If we have an update with a message, try to inform the user
        if isinstance(update, Update) and update.message:
            try:
                await update.message.reply_text(
                    "Oops! Something went wrong on my end. 🔧 Please try again in a moment."
                )
            except Exception as e:
                logger.error(f"Failed to send error message to user: {e}")
