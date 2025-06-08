# tesla-tracker

Un script en Python que monitorea la ubicación de tu vehículo Tesla y envía una alerta por Telegram si se encuentra fuera de una zona geográfica permitida.

## 📦 Requisitos

- Python 3.7 o superior
- Paquetes:

```bash
pip3 install teslapy telepot geopy
```

### ⚙️ Configuración

Crea un archivo config.py en el mismo directorio con el siguiente contenido:

```bash
TESLA_EMAIL = 'tu_correo@ejemplo.com'
TOKEN = 'tu_token_de_telegram'
CHAT_ID = 'tu_chat_id_de_telegram'
ZONA_PERMITIDA = (LATITUD, LONGITUD)  # Por ejemplo: (19.4326, -99.1332)
RADIO_MAX_KM = 2.0  # Radio máximo permitido en kilómetros
```

### 🗂 Archivos

    tesla-traker.py: Script principal para obtener la ubicación del vehículo y enviar alerta.

    tesla_tracker_scheduler.py: Ejecuta tesla-traker.py cada 15 minutos de forma continua.

    token.json: Se genera automáticamente tras la autenticación del usuario Tesla. No lo compartas.

### ▶️ Uso
#### 1. Ejecutar manualmente

```bash
python3 tesla-traker.py
```

Esto:

    Carga un token existente o te guía a través del proceso de autenticación.

    Consulta la ubicación del vehículo.

    Envía una alerta por Telegram si el auto está fuera de la zona segura.

#### 2. Ejecutar automáticamente cada 15 minutos

Usa el programador:

```bash
python3 tesla_tracker_scheduler.py
```

Este script ejecutará tesla-traker.py cada 15 minutos en un bucle infinito.

    📌 Ideal para servidores o Raspberry Pi siempre encendidos.

### 🔐 Autenticación

La primera vez que ejecutes el script, te pedirá iniciar sesión en tu cuenta Tesla y completar la autenticación 2FA. La URL que te proporcione debe abrirse en un navegador para completar el proceso. Copia y pega la URL final en la terminal cuando se te solicite.

Después de autenticado, se guarda un token.json y no será necesario repetir este paso, a menos que el token expire o se elimine.
📤 Telegram

El mensaje de alerta incluye:

    Kilometraje total del vehículo.

    Distancia desde la zona permitida.

    Un enlace para abrir la ubicación actual en Google Maps.

### 🧪 Pruebas

Puedes mover artificialmente las coordenadas en config.ZONA_PERMITIDA para verificar el comportamiento del sistema al detectar una salida de zona.
