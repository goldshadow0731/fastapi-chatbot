# -*- coding: utf-8 -*-
from fastapi import FastAPI
# import uvicorn


# FastAPI
app = FastAPI()


@app.get("/")
def index():
    return "OK"


# if __name__ == "__main__":
#     uvicorn.run(app=app, port=80, log_level="info")
