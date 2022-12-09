from fastapi import FastAPI
from request import request

app = FastAPI()

app.include_router(request)