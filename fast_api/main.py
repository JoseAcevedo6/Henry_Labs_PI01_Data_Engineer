from fastapi import FastAPI
from connect import connect_execute, query1, query2, query3, query4

app = FastAPI()

@app.get("/")
def read_root():
    respuesta = connect_execute(query4('Amazon', 2020))
    return respuesta
