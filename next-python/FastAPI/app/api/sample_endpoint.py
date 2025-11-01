from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/sample")
def get_sample():
    """Sample GET endpoint"""
    return {"message": "This is a sample endpoint"}

@router.post("/sample")
def create_sample(data: dict):
    """Sample POST endpoint"""
    if not data:
        raise HTTPException(status_code=400, detail="Invalid data")
    return {"message": "Data received", "data": data}