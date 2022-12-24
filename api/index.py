# -*- coding: utf-8 -*-
import requests
import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


# Flask
app = Flask(__name__)

# OpenAI
api_key = os.getenv("OPENAI_API_KEY")

# Line Bot
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


@app.route("/")
def index():
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(event=MessageEvent, message=TextMessage)
def message_handler(event: MessageEvent):
    response = requests.post(
        url="https://api.openai.com/v1/completions",
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "model": "text-davinci-003",
            "prompt": event.message.text,
            "max_tokens": 256,
            "temperature": 0.5,
            "n": 1
        }
    )
    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=TextSendMessage(
            text=response.json()["choices"][0]["text"].lstrip("\n")
        )
    )
