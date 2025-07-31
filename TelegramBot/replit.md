# Telegram Bot Replit Guide

## Overview

This is a Python-based Telegram bot application built using the `python-telegram-bot` library with Flask web integration. The bot provides plugin-based command handling, message processing, and a real-time web dashboard showing bot statistics and uptime. The application supports both polling and webhook modes with a modular plugin architecture for easy extensibility.

## User Preferences

Preferred communication style: Simple, everyday language.
Architecture preference: Plugin-based command system for easy extensibility.

## System Architecture

### Core Architecture Pattern
The application follows a **plugin-based modular architecture** with clear separation of concerns:

- **Configuration Layer**: Centralized environment variable management with multiple token sources
- **Plugin System**: Individual plugins for each command and functionality in `/plugins` directory
- **Plugin Loader**: Automatic discovery and registration of all plugins
- **Application Layer**: Bot initialization and plugin orchestration
- **Logging Layer**: Comprehensive logging throughout the application

### Technology Stack
- **Runtime**: Python 3.8+
- **Bot Framework**: python-telegram-bot library
- **Web Framework**: Flask for dashboard and API endpoints
- **System Monitoring**: psutil for system metrics
- **Configuration**: Environment variables with .env file support and token.txt
- **Logging**: Python's built-in logging module
- **Async Support**: nest-asyncio for concurrent bot and web server
- **Deployment**: Supports both polling and webhook modes

## Key Components

### Configuration Management (`config.py`)
- **Purpose**: Centralized configuration using environment variables
- **Key Features**: 
  - Validates required environment variables on startup
  - Supports both polling and webhook deployment modes
  - Configurable logging levels
- **Required Variables**: `BOT_TOKEN`
- **Optional Variables**: `WEBHOOK_URL`, `PORT`, `LOG_LEVEL`

### Plugin System (`plugins/` directory)
- **Purpose**: Modular command system where each plugin handles specific functionality
- **Architecture**: Individual plugin files with dedicated handlers
- **Plugin Loader**: Automatic discovery and registration system (`plugin_loader.py`)
- **Current Plugins**:
  - `start_plugin.py` - `/start` command with personalized welcome message
  - `help_plugin.py` - `/help` command with available commands list
  - `echo_plugin.py` - `/echo` command that repeats user messages
  - `message_plugin.py` - Text message handler for general interactions
  - `error_plugin.py` - Error handler for graceful failure handling
- **Token Management**: Multiple sources supported (token.txt file, .env file, environment variables)

### Main Application (`main.py`)
- **Purpose**: Bot initialization and startup orchestration
- **Responsibilities**:
  - Configuration validation before startup
  - Web server initialization on port 5000
  - Plugin loading and registration with the Telegram application
  - Mode selection (webhook vs polling)
  - Bot status tracking integration
  - Centralized error handling setup

### Web Dashboard System (`web_server.py`, `templates/dashboard.html`)
- **Purpose**: Real-time monitoring and statistics display
- **Features**:
  - Bot uptime tracking since last restart
  - Message and command statistics with user counting
  - System resource monitoring (CPU, memory, disk usage)
  - Error logging and tracking
  - Auto-refresh every 30 seconds
  - REST API endpoints for data access
- **Integration**: Plugins automatically log statistics to the tracker

## Data Flow

### Command Processing Flow
1. User sends command to Telegram
2. Telegram API forwards to bot application
3. Application routes to appropriate handler method
4. Handler processes command and generates response
5. Response sent back through Telegram API
6. All interactions logged for debugging

### Error Handling Flow
1. Exceptions caught at handler level
2. Errors logged with detailed information
3. User-friendly error messages sent to chat
4. Bot continues operation without crashing

## External Dependencies

### Telegram Bot API
- **Integration**: Direct integration via python-telegram-bot library
- **Authentication**: Bot token from @BotFather
- **Communication**: HTTPS requests to Telegram servers
- **Modes**: Supports both long-polling and webhook receiving

### Environment Configuration
- **Development**: .env file support for local development
- **Production**: Environment variables for deployment
- **Validation**: Startup checks ensure required configuration is present

## Deployment Strategy

### Dual Deployment Support
The application supports two deployment modes:

#### Polling Mode (Default)
- **Use Case**: Development and simple hosting environments
- **Method**: Bot actively polls Telegram servers for updates
- **Benefits**: Easier setup, works behind firewalls
- **Configuration**: No additional environment variables needed

#### Webhook Mode (Production)
- **Use Case**: Production deployments with public endpoints
- **Method**: Telegram pushes updates to bot's webhook URL
- **Benefits**: More efficient, real-time updates
- **Configuration**: Requires `WEBHOOK_URL` and `PORT` environment variables

### Configuration Requirements
- **Minimum**: `BOT_TOKEN` from Telegram's @BotFather
- **Optional**: `WEBHOOK_URL`, `PORT`, `LOG_LEVEL`
- **Validation**: Application validates configuration on startup and provides clear error messages for missing variables

### Error Resilience
- **Graceful Degradation**: Bot continues operating even when individual commands fail
- **Comprehensive Logging**: All operations logged for debugging and monitoring
- **User Communication**: Friendly error messages sent to users without exposing technical details