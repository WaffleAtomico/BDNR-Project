from typing import List, Optional

from app.lib.con_mdb import mdb_conn
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/mongodb", tags=["MongoDB"])

class Pin(BaseModel):
    pin_id: str
    title: str
    description: str
    url: str
    tags: List[str]
    author_id: str
    created_at: datetime


@router.post("/pins")
async def create_pin(pin: Pin):
    mdb_conn.client.insert_one("pins", pin.model_dump())
    return {"message": "Pin creado"}

@router.get("/items")
async def list_items():
    # Example query
    items = mdb_conn.execute_query("items")
    return {"items": items}

@router.post("/items")
async def create_item(item: Item):
    mdb_conn.client.insert_one("items", item.dict())
    return {"message": "Item created", "item": item}
