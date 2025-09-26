from fastapi import APIRouter

router = APIRouter(prefix="/fantasy", tags=["fantasy"])

@router.get("/")
def get_fantasy():
    return {"msg": "fantasy endpoint"}
