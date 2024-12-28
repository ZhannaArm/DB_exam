from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/artists", tags=["artists"])

@router.post("/", response_model=schemas.Artist)
def create_artist(artist: schemas.ArtistCreate, db: Session = Depends(get_db)):
    return crud.create_artist(db, artist)

@router.get("/{artist_id}", response_model=schemas.Artist)
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = crud.get_artist(db, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@router.put("/{artist_id}", response_model=schemas.Artist)
def update_artist(artist_id: int, artist: schemas.ArtistUpdate, db: Session = Depends(get_db)):
    updated_artist = crud.update_artist(db, artist_id, artist)
    if not updated_artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return updated_artist

@router.delete("/{artist_id}")
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    success = crud.delete_artist(db, artist_id)
    if not success:
        raise HTTPException(status_code=404, detail="Artist not found")
    return {"message": "Artist deleted successfully"}
