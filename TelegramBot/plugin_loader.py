"""
Plugin loader system for Telegram bot.
Automatically loads and registers all plugins from the plugins directory.
"""
import os
import importlib
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logger = logging.getLogger(__name__)

class PluginLoader:
    """Loads and manages bot plugins."""
    
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = plugins_dir
        self.loaded_plugins = {}
    
    def load_all_plugins(self, application: Application) -> None:
        """Load and register all plugins from the plugins directory."""
        if not os.path.exists(self.plugins_dir):
            logger.warning(f"Plugins directory '{self.plugins_dir}' not found")
            return
        
        # Get all Python files in plugins directory
        plugin_files = [f for f in os.listdir(self.plugins_dir) 
                       if f.endswith('_plugin.py') and f != '__init__.py']
        
        logger.info(f"Found {len(plugin_files)} plugin files")
        
        for plugin_file in plugin_files:
            self._load_plugin(plugin_file, application)
    
    def _load_plugin(self, plugin_file: str, application: Application) -> None:
        """Load a single plugin file and register its handlers."""
        try:
            # Remove .py extension to get module name
            module_name = plugin_file[:-3]
            full_module_name = f"{self.plugins_dir}.{module_name}"
            
            # Import the plugin module
            plugin_module = importlib.import_module(full_module_name)
            
            logger.info(f"Loading plugin: {module_name}")
            
            # Register handlers based on plugin name
            if module_name == "start_plugin" and hasattr(plugin_module, 'start_command'):
                application.add_handler(CommandHandler("start", plugin_module.start_command))
                logger.info("Registered /start command")
            
            elif module_name == "help_plugin" and hasattr(plugin_module, 'help_command'):
                application.add_handler(CommandHandler("help", plugin_module.help_command))
                logger.info("Registered /help command")
            
            elif module_name == "echo_plugin" and hasattr(plugin_module, 'echo_command'):
                application.add_handler(CommandHandler("echo", plugin_module.echo_command))
                logger.info("Registered /echo command")
            
            elif module_name == "message_plugin" and hasattr(plugin_module, 'handle_message'):
                application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, plugin_module.handle_message))
                logger.info("Registered message handler")
            
            elif module_name == "error_plugin" and hasattr(plugin_module, 'error_handler'):
                application.add_error_handler(plugin_module.error_handler)
                logger.info("Registered error handler")
            
            self.loaded_plugins[module_name] = plugin_module
            logger.info(f"Successfully loaded plugin: {module_name}")
            
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_file}: {e}")
    
    def get_loaded_plugins(self) -> dict:
        """Get dictionary of loaded plugins."""
        return self.loaded_plugins.copy()
    
    def reload_plugin(self, plugin_name: str, application: Application) -> bool:
        """Reload a specific plugin (useful for development)."""
        try:
            if plugin_name in self.loaded_plugins:
                # Reload the module
                importlib.reload(self.loaded_plugins[plugin_name])
                logger.info(f"Reloaded plugin: {plugin_name}")
                return True
            else:
                logger.warning(f"Plugin {plugin_name} not found in loaded plugins")
                return False
        except Exception as e:
            logger.error(f"Failed to reload plugin {plugin_name}: {e}")
            return False

# Global plugin loader instance
plugin_loader = PluginLoader()