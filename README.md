# Telegram Bot

A Python Telegram bot with basic command handling and message processing capabilities.

## Features

- 🤖 Sistema de plugins modular (`/start`, `/help`, `/echo`)
- 💬 Procesamiento interactivo de mensajes de texto
- 🌐 Dashboard web con estadísticas en tiempo real
- 📊 Seguimiento de tiempo activo y métricas del bot
- 🔄 Soporte para modos polling y webhook
- 📝 Logging completo para debugging
- ⚠️ Manejo de errores para fallos de API
- 🔧 Configuración por variables de entorno

## Setup

### Prerequisites

- Python 3.8 or higher
- A Telegram bot token (get one from [@BotFather](https://t.me/BotFather))

### Installation

1. **Get a Bot Token**:
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Create a new bot with `/newbot`
   - Save the bot token you receive

2. **Add Your Bot Token**:
   
   **Opción más fácil** - Usando el archivo token.txt:
   ```bash
   # Edita el archivo token.txt y pega tu token ahí
   # Reemplaza AQUI_PONES_TU_TOKEN_DE_TELEGRAM con tu token real
   ```

   **Alternativas**:
   - Usando variable de entorno:
     ```bash
     export BOT_TOKEN="your_telegram_bot_token_here"
     ```
   - Usando archivo .env (copia desde .env.example):
     ```bash
     cp .env.example .env
     # Edita .env con tu token
     ```

3. **Ejecuta el Bot**:
   ```bash
   python main.py
   ```

## Dashboard Web

El bot incluye un dashboard web que muestra:

- ⏱️ **Tiempo activo** del bot desde el último reinicio
- 📊 **Estadísticas** de mensajes y comandos procesados
- 👥 **Usuarios únicos** que han interactuado con el bot
- ⚠️ **Conteo de errores** registrados
- 🖥️ **Métricas del sistema** (CPU, memoria, disco)

### Acceder al Dashboard

Una vez que ejecutes el bot, puedes acceder al dashboard en:
- **URL local**: http://localhost:5000
- **En Replit**: Se abrirá automáticamente en el puerto 5000

El dashboard se actualiza automáticamente cada 30 segundos y muestra información en tiempo real sobre el estado del bot.
   