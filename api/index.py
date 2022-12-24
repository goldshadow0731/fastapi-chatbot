# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai

from configs import SETTINGS


# FastAPI
app = FastAPI()

# OpenAI
openai.api_key = SETTINGS.OPENAI_API_KEY

# Line Bot
line_bot_api = LineBotApi(SETTINGS.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(SETTINGS.LINE_CHANNEL_SECRET)


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


@handler.add(MessageEvent, message=(TextMessage))
def handling_message(event):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=event.message.text,
        max_tokens=256,
        temperature=0.5,
    )
    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=TextSendMessage(
            text=response["choices"][0]["text"].replace('\n', ''))
    )
