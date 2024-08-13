from typing import Union
import auth
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {
        "API is alive"
    }

