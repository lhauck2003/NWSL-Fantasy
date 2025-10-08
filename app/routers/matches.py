from fastapi import APIRouter

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/")
def list_matches():
    return {"msg": "matches endpoint"}
