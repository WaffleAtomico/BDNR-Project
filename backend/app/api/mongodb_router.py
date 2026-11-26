from app.lib.config import settings
from app.lib.con_mdb import mdb_conn
from app.models.mongodb_models import Board, Comment, Pin
from fastapi import APIRouter

router = APIRouter(prefix="/mongodb", tags=["MongoDB"])

# Nombre de la base de datos (variable MONGO_DB del .env).
db = mdb_conn.execute_query(settings.MONGO_DB)


@router.post("/pins")
async def create_pin(pin: Pin):
    db["pins"].insert_one(pin.model_dump())
    return {"message": "Pin creado"}


@router.post("/boards")
async def create_board(board: Board):
    db["boards"].insert_one(board.model_dump())
    return {"message": "Board creado"}


@router.post("/comments")
async def create_comment(comment: Comment):
    db["comments"].insert_one(comment.model_dump())
    return {"message": "Comentario creado"}