from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.post("/", response_model=schemas.Track)
def create_track(track: schemas.TrackCreate, db: Session = Depends(get_db)):
    return crud.create_track(db, track)

@router.get("/{track_id}", response_model=schemas.Track)
def get_track(track_id: int, db: Session = Depends(get_db)):
    track = crud.get_track(db, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track

@router.put("/{track_id}", response_model=schemas.Track)
def update_track(track_id: int, track: schemas.TrackUpdate, db: Session = Depends(get_db)):
    updated_track = crud.update_track(db, track_id, track)
    if not updated_track:
        raise HTTPException(status_code=404, detail="Track not found")
    return updated_track

@router.delete("/{track_id}")
def delete_track(track_id: int, db: Session = Depends(get_db)):
    success = crud.delete_track(db, track_id)
    if not success:
        raise HTTPException(status_code=404, detail="Track not found")
    return {"message": "Track deleted successfully"}
