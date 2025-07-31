"""
Main entry point for the Telegram bot.
Handles bot initialization, handler registration, and startup.
"""
import logging
import asyncio
from telegram.ext import Application
from config import config
from plugin_loader import plugin_loader
from web_server import run_web_server, status_tracker

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to start the Telegram bot and web server."""
    
    # Start web server first (always, regardless of bot token)
    logger.info("Starting web dashboard on port 5000...")
    web_thread = run_web_server(port=5000)
    
    # Check if we have a valid bot token
    if not config.validate():
        missing_vars = config.get_missing_vars()
        logger.warning(f"Bot token not configured: {', '.join(missing_vars)}")
        logger.info("Web dashboard is running, but bot is disabled until token is provided.")
        # Just keep the web server running
        try:
            while True:
                await asyncio.sleep(10)  # Keep the process alive for web server
        except KeyboardInterrupt:
            logger.info("Application stopped by user")
        return
    
    logger.info("Starting Telegram bot...")
    
    try:
        # Create the Application
        application = Application.builder().token(config.BOT_TOKEN).build()
        
        # Load all plugins automatically
        plugin_loader.load_all_plugins(application)
        
        loaded_plugins = plugin_loader.get_loaded_plugins()
        logger.info(f"Successfully loaded {len(loaded_plugins)} plugins: {list(loaded_plugins.keys())}")
        
        # Mark bot as started for status tracking
        status_tracker.bot_started()
        
        # Determine if we should use webhook or polling
        if config.WEBHOOK_URL:
            logger.info(f"Starting bot with webhook: {config.WEBHOOK_URL}")
            # Start webhook
            async with application:
                await application.start()
                await application.updater.start_webhook(
                    listen="0.0.0.0",
                    port=config.PORT,
                    url_path="webhook",
                    webhook_url=f"{config.WEBHOOK_URL}/webhook"
                )
                await application.updater.idle()
        else:
            logger.info("Starting bot with polling...")
            # Start polling
            await application.run_polling(
                allowed_updates=["message", "callback_query"]
            )
            
    except Exception as e:
        status_tracker.bot_stopped()
        logger.error(f"Failed to start bot: {e}")
        logger.info("Web dashboard is still running at http://localhost:5000")
        # Keep web server running even if bot fails
        try:
            while True:
                await asyncio.sleep(10)
        except KeyboardInterrupt:
            logger.info("Application stopped by user")

def run_bot():
    """Run the bot using asyncio."""
    try:
        # Import and apply nest_asyncio to handle nested event loops
        import nest_asyncio
        nest_asyncio.apply()
        
        # Try to get existing loop, if none exists create one
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the main function
        loop.run_until_complete(main())
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed with error: {e}")
        raise

if __name__ == "__main__":
    # Print startup information
    # Colors for console output
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    
    print(f"\n{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║                    🤖 TELEGRAM BOT INICIANDO                 ║{RESET}")
    print(f"{BOLD}{CYAN}╚══════════════════════════════════════════════════════════════╝{RESET}\n")
    
    if not config.BOT_TOKEN:
        print(f"{RED}❌ ERROR: BOT_TOKEN environment variable is required!{RESET}")
        print(f"{YELLOW}Please set your Telegram bot token in the BOT_TOKEN environment variable.{RESET}")
        print(f"{YELLOW}You can get a bot token from @BotFather on Telegram.{RESET}")
        print(f"\n{BOLD}Example:{RESET}")
        print(f"{BLUE}export BOT_TOKEN='your_bot_token_here'{RESET}")
        print(f"{BLUE}python main.py{RESET}")
        exit(1)
    
    print(f"{GREEN}✅ Bot token configurado{RESET}")
    print(f"{BLUE}📊 Nivel de logging: {BOLD}{config.LOG_LEVEL}{RESET}")
    print(f"{MAGENTA}🌐 Dashboard web: {BOLD}http://localhost:5000{RESET}")
    
    if config.WEBHOOK_URL:
        print(f"{CYAN}🔗 Modo webhook: {BOLD}{config.WEBHOOK_URL}{RESET}")
        print(f"{CYAN}🔌 Puerto: {BOLD}{config.PORT}{RESET}")
    else:
        print(f"{YELLOW}🔄 Modo polling activo{RESET}")
    
    print(f"\n{BOLD}{GREEN}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  Bot listo para recibir mensajes - Presiona Ctrl+C para detener{RESET}")
    print(f"{BOLD}{GREEN}{'='*60}{RESET}\n")
    
    # Start the bot
    run_bot()
