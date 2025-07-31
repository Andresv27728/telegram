"""
Web server for Telegram bot status dashboard.
Shows bot uptime, statistics, and system information.
"""
import os
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify
import psutil
import asyncio
from threading import Thread

logger = logging.getLogger(__name__)

class BotStatusTracker:
    """Tracks bot statistics and status information."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.message_count = 0
        self.command_count = 0
        self.error_count = 0
        self.active_users = set()
        self.is_bot_running = False
    
    def bot_started(self):
        """Mark bot as started."""
        self.is_bot_running = True
        self.start_time = datetime.now()
        logger.info("Bot status tracker: Bot started")
    
    def bot_stopped(self):
        """Mark bot as stopped."""
        self.is_bot_running = False
        logger.info("Bot status tracker: Bot stopped")
    
    def log_message(self, user_id: int):
        """Log a message received."""
        self.message_count += 1
        self.active_users.add(user_id)
    
    def log_command(self, user_id: int):
        """Log a command received."""
        self.command_count += 1
        self.active_users.add(user_id)
    
    def log_error(self):
        """Log an error."""
        self.error_count += 1
    
    def get_uptime(self):
        """Get bot uptime as a formatted string."""
        if not self.is_bot_running:
            return "Bot no está ejecutándose"
        
        uptime = datetime.now() - self.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def get_stats(self):
        """Get all statistics as a dictionary."""
        return {
            'is_running': self.is_bot_running,
            'uptime': self.get_uptime(),
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'message_count': self.message_count,
            'command_count': self.command_count,
            'error_count': self.error_count,
            'active_users': len(self.active_users),
            'system': {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent
            }
        }

# Global status tracker
status_tracker = BotStatusTracker()

def create_web_app():
    """Create and configure Flask web application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    
    @app.route('/')
    def dashboard():
        """Main dashboard page."""
        stats = status_tracker.get_stats()
        return render_template('dashboard.html', stats=stats)
    
    @app.route('/api/stats')
    def api_stats():
        """API endpoint for bot statistics."""
        return jsonify(status_tracker.get_stats())
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'bot_running': status_tracker.is_bot_running,
            'timestamp': datetime.now().isoformat()
        })
    
    return app

def run_web_server(port=5000):
    """Run the web server in a separate thread."""
    app = create_web_app()
    
    def run_app():
        try:
            logger.info(f"Starting web server on port {port}")
            app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
        except Exception as e:
            logger.error(f"Web server error: {e}")
    
    # Run in a separate thread so it doesn't block the bot
    server_thread = Thread(target=run_app, daemon=True)
    server_thread.start()
    logger.info("Web server thread started")
    
    return server_thread

if __name__ == "__main__":
    # For testing the web server independently
    run_web_server()
    import time
    time.sleep(60)  # Keep alive for testing