from typing import List, Optional

from app.lib.con_mdb import mdb_conn
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/mongodb", tags=["MongoDB"])

class Item(BaseModel):
    name: str
    description: Optional[str] = None

@router.get("/items")
async def list_items():
    # Example query
    items = mdb_conn.execute_query("items")
    return {"items": items}

@router.post("/items")
async def create_item(item: Item):
    mdb_conn.client.insert_one("items", item.dict())
    return {"message": "Item created", "item": item}
