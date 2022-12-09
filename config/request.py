from fastapi import APIRouter
from db import conn
from models import actor, listed_in, service, title, title_actor, title_listed_in, title_service
from sqlalchemy import text

request = APIRouter()

@request.get("/")
def read_root():
    sql_text = text("SELECT * FROM service")
    with conn:
        result = conn.execute(sql_text).fetchall()
        for row in result:
            print(row)



@request.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
