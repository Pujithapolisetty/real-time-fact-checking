from fastapi import APIRouter
from pydantic import BaseModel

# Define router
router = APIRouter()

# Request and Response Modelsfrom fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class NERStanceRequest(BaseModel):
    text: str

class NERResponse(BaseModel):
    entities: list

class StanceResponse(BaseModel):
    stance: str

@router.get("/")
def test_route():
    return {"message": "NER & Stance Detection is working!"}

@router.post("/ner", response_model=NERResponse)
async def get_ner(data: NERStanceRequest):
    return {"entities": [{"word": "Apple", "type": "ORG"}]}  # Mock response

@router.post("/stance", response_model=StanceResponse)
async def get_stance(data: NERStanceRequest):
    return {"stance": "Support"}  # Mock response
