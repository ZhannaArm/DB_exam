from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/albums", tags=["albums"])

@router.post("/", response_model=schemas.Album)
def create_album(album: schemas.AlbumCreate, db: Session = Depends(get_db)):
    return crud.create_album(db, album)

@router.get("/{album_id}", response_model=schemas.Album)
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.get_album(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@router.put("/{album_id}", response_model=schemas.Album)
def update_album(album_id: int, album: schemas.AlbumUpdate, db: Session = Depends(get_db)):
    updated_album = crud.update_album(db, album_id, album)
    if not updated_album:
        raise HTTPException(status_code=404, detail="Album not found")
    return updated_album

@router.delete("/{album_id}")
def delete_album(album_id: int, db: Session = Depends(get_db)):
    success = crud.delete_album(db, album_id)
    if not success:
        raise HTTPException(status_code=404, detail="Album not found")
    return {"message": "Album deleted successfully"}
