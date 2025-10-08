from sqlalchemy.orm import Session
from app.db import models
from app.schemas import player, match, fantasy, user

# Example: Player CRUD
def get_players(db: Session):
    return db.query(models.Player).all()

def create_player(db: Session, player_in: player.PlayerCreate):
    db_player = models.Player(**player_in.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

# Add similar functions for Match, FantasyPoints, User
