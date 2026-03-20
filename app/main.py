from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from app.routers import upload

load_dotenv()

app = FastAPI(title="AI Evaluator")

app.include_router(upload.router, prefix="/api", tags=["Upload"])

@app.get("/")
def root():
    return {"message": "AI Evaluator is running"}