from fastapi import FastAPI
from app.database import engine, Base
from app.routers import artists, albums, tracks
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(tracks.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Music API!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

