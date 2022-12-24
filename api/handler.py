# -*- coding: utf-8 -*-
from linebot.models import MessageEvent, TextSendMessage

from .chatgpt import ChatResponse


def message_handler(event: MessageEvent):
    return TextSendMessage(
        text=ChatResponse.get_response(event.message.text)
    )
