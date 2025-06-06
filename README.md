# WhatsApp + ChatGPT Bot

## Requisitos
- Cuenta en Facebook Developer con WhatsApp Cloud API
- API Key de OpenAI
- Python 3.10+
- Flask

## Variables de entorno necesarias

```
VERIFY_TOKEN=siprinbot
WHATSAPP_TOKEN=tu_token_whatsapp_cloud
PHONE_NUMBER_ID=tu_id_numero
OPENAI_API_KEY=tu_api_key_openai
```

## Despliegue
Puedes usar servicios como [Render](https://render.com) o correr en local con `ngrok`.

## Audio
La función de texto a voz requiere subir el archivo generado a un hosting para compartir el link con WhatsApp. El ejemplo lo deja preparado.
