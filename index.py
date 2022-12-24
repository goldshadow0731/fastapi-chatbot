# -*- coding: utf-8 -*-
import requests
import os

from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import uvicorn


# FastAPI
app = FastAPI()

# OpenAI
api_key = os.getenv("OPENAI_API_KEY")

# Line Bot
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


@app.get("/")
def index():
    return "OK"


@app.post("/webhook")
async def webhook(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
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


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0")
