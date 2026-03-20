from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Evaluator")

@app.get("/")
def root():
    return {"message": "AI Evaluator is running"}