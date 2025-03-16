from fastapi import FastAPI
from .routes.ner_stance_routes import router

 # Correct import

app = FastAPI()

# Include router
app.include_router(ner_stance_router, prefix="/ner-stance", tags=["NER & Stance Detection"])

@app.get("/")
def root():
    return {"message": "Real-Time Fact Checking API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
