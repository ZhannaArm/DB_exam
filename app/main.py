from fastapi import FastAPI
from app.database import engine, Base
from app.routers import artists, albums

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(artists.router)
app.include_router(albums.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Music API!"}
