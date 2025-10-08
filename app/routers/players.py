from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud
from app.schemas import player

router = APIRouter(prefix="/players", tags=["players"])

@router.get("/", response_model=list[player.Player])
def list_players(db: Session = Depends(get_db)):
    return crud.get_players(db)

@router.post("/", response_model=player.Player)
def add_player(player_in: player.PlayerCreate, db: Session = Depends(get_db)):
    return crud.create_player(db, player_in)
