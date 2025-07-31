# Sistema de Plugins para Bot de Telegram

Esta carpeta contiene todos los comandos del bot organizados como plugins independientes. Cada plugin maneja una funcionalidad específica.

## Plugins Existentes

### Comandos Básicos
- **start_plugin.py** - Comando `/start` con mensaje de bienvenida
- **help_plugin.py** - Comando `/help` con lista de comandos disponibles
- **echo_plugin.py** - Comando `/echo` que repite mensajes

### Funcionalidades del Sistema
- **message_plugin.py** - Maneja mensajes de texto normales
- **error_plugin.py** - Maneja errores del bot

## Cómo Agregar un Nuevo Plugin

Para crear un nuevo comando, sigue estos pasos:

### 1. Crear el archivo del plugin
Crea un archivo con el nombre `[nombre]_plugin.py` en esta carpeta.

Ejemplo: `saludo_plugin.py`

```python
"""
Saludo command plugin.
Handles the /saludo command that greets users.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def saludo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /saludo command."""
    try:
        if update.message and update.effective_user:
            user_name = update.effective_user.first_name or 'Amigo'
            response = f"¡Hola {user_name}! 👋 ¡Que tengas un gran día!"
            
            await update.message.reply_text(response)
            logger.info(f"User {update.effective_user.id} used saludo command")
        
    except Exception as e:
        logger.error(f"Error in saludo_command: {e}")
        if update.message:
            await update.message.reply_text(
                "Lo siento, no pude procesar el comando saludo."
            )
```

### 2. Registrar el plugin en el cargador
Edita `plugin_loader.py` y agrega tu comando en la función `_load_plugin`:

```python
elif module_name == "saludo_plugin" and hasattr(plugin_module, 'saludo_command'):
    application.add_handler(CommandHandler("saludo", plugin_module.saludo_command))
    logger.info("Registered /saludo command")
```

### 3. Actualizar la ayuda (opcional)
Si quieres que tu comando aparezca en `/help`, edita `help_plugin.py`:

```python
🌟 `/saludo` - Saludar amigablemente
```

### 4. Reiniciar el bot
El bot cargará automáticamente tu nuevo plugin al reiniciarse.

## Estructura de un Plugin

Cada plugin debe:

1. **Tener una función asíncrona** que maneje el comando
2. **Recibir `update` y `context`** como parámetros
3. **Manejar errores** con try/except
4. **Registrar actividad** con logging
5. **Validar que existen** `update.message` y `update.effective_user`

## Tipos de Handlers

### Comando Simple
```python
application.add_handler(CommandHandler("comando", funcion_comando))
```

### Comando con Argumentos
```python
# En plugin_loader.py - mismo registro
# En tu función del plugin:
def proceso_argumentos(update, context):
    args = context.args  # Lista con argumentos del comando
```

### Handler de Mensajes
```python
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, funcion_mensaje))
```

### Handler de Errores
```python
application.add_error_handler(funcion_error)
```

## Consejos

- **Nombres consistentes**: Usa `[nombre]_plugin.py` para archivos y `[nombre]_command` para funciones
- **Logging**: Siempre incluye logging para debugging
- **Manejo de errores**: Nunca dejes que un error rompa el bot
- **Validaciones**: Verifica que existan `update.message` y `update.effective_user`
- **Respuestas amigables**: Usa mensajes claros y útiles para el usuario

## Ejemplo Completo: Plugin de Tiempo

```python
"""
Tiempo command plugin.
Handles the /tiempo command that shows current time.
"""
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def tiempo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /tiempo command."""
    try:
        if update.message:
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")
            date_str = now.strftime("%d/%m/%Y")
            
            response = f"🕐 Hora actual: {time_str}\n📅 Fecha: {date_str}"
            
            await update.message.reply_text(response)
            
            if update.effective_user:
                logger.info(f"User {update.effective_user.id} requested time")
        
    except Exception as e:
        logger.error(f"Error in tiempo_command: {e}")
        if update.message:
            await update.message.reply_text(
                "Lo siento, no pude obtener la hora actual."
            )
```

¡El sistema de plugins hace que agregar nuevas funcionalidades sea súper fácil!