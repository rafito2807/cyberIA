from flask import Flask, request, jsonify
from chatgpt import get_chatgpt_response
from utils import text_to_speech
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "cyberia")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Error", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get("entry"):
        for entry in data["entry"]:
            for change in entry["changes"]:
                value = change["value"]
                messages = value.get("messages")
                if messages:
                    for message in messages:
                        phone_number_id = value["metadata"]["phone_number_id"]
                        from_number = message["from"]
                        user_text = message["text"]["body"]

                        # Obtener respuesta del modelo
                        reply_text = get_chatgpt_response(user_text)
                        send_whatsapp_message(from_number, reply_text)

                        # Opcional: enviar como audio
                        audio_url = text_to_speech(reply_text)
                        if audio_url:
                            send_whatsapp_audio(from_number, audio_url)
    return "OK", 200

def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=payload)

def send_whatsapp_audio(to, audio_url):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "audio",
        "audio": {"link": audio_url}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)# Forzado para redeploy en Render


