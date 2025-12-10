from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, predict
from app.database.base import Base
from app.database.session import engine

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PPD API", description="API untuk Penambangan Data")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(predict.router)

@app.get("/")
def root():
    return {"message": "Welcome to PPD API"}
