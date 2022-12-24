# -*- coding: utf-8 -*-
from fastapi import FastAPI


# FastAPI
app = FastAPI()


@app.get("/")
def index():
    return "OK"
