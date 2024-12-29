from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from sqlalchemy import func
from app import models, schemas, crud

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

# SELECT ... WHERE с несколькими условиями.
# Получить все треки, соответствующие определённому настроению и продолжительности.
@router.get("/filter/", response_model=List[schemas.Track])
def filter_tracks(mood: str, min_duration: int, db: Session = Depends(get_db)):
    tracks = db.query(models.Track).filter(
        models.Track.mood == mood,
        models.Track.duration > min_duration
    ).all()
    return tracks

# UPDATE с нетривиальным условием.
# Увеличить play_count треков длительностью более 300 секунд на 10%.
@router.put("/increase_play_count/")
def increase_play_count(db: Session = Depends(get_db)):
    tracks = db.query(models.Track).filter(models.Track.duration > 300)
    for track in tracks:
        track.play_count = round(track.play_count * 1.1)
    db.commit()
    return {"message": "Play counts updated"}

# GROUP BY
# Получить количество треков по настроению (mood).
@router.get("/mood_summary/")
def get_tracks_by_mood(db: Session = Depends(get_db)):
    mood_summary = db.query(models.Track.mood, func.count(models.Track.track_id)).group_by(models.Track.mood).all()
    return {"data": mood_summary}

# JOIN
# Получить все треки с данными об альбоме и артисте.
@router.get("/join/", response_model=List[schemas.Track])
def get_tracks_with_album_artist(db: Session = Depends(get_db)):
    tracks = db.query(models.Track, models.Album, models.Artist).join(
        models.Album, models.Track.album_id == models.Album.album_id
    ).join(
        models.Artist, models.Track.artist_id == models.Artist.artist_id
    ).all()
    return [
        {
            "track": track[0],
            "album": track[1],
            "artist": track[2]
        }
        for track in tracks
    ]

# Сортировка
# Получить все треки, отсортированные по указанному полю.
@router.get("/sort/", response_model=List[schemas.Track])
def sort_tracks(sort_by: str = "play_count", db: Session = Depends(get_db)):
    valid_fields = ["play_count", "duration", "title", "mood"]  # Можно добавить другие поля для сортировки
    if sort_by not in valid_fields:
        return {"message": f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}"}

    tracks = db.query(models.Track).order_by(getattr(models.Track, sort_by)).all()
    return tracks