# -*- coding: utf-8 -*-
import os

import openai


# OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatResponse():
    @staticmethod
    def get_response(text: str):
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=text,
            max_tokens=512,
            temperature=0.5,
        )
        return response["choices"][0]["text"].replace('\n', '')
