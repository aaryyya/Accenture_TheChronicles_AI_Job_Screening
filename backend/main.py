# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.upload_routes import router as upload_router
from routes import calendar_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify "http://localhost:5173"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calendar_route.router, prefix="/calendar", tags=["calendar"])
app.include_router(upload_router, prefix="", tags=["upload"])

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}
