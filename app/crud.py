from sqlalchemy.orm import Session
from app import models, schemas

def create_artist(db: Session, artist: schemas.ArtistCreate):
    db_artist = models.Artist(**artist.model_dump())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def get_artists(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Artist).offset(skip).limit(limit).all()

def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).filter(models.Artist.artist_id == artist_id).first()

def update_artist(db: Session, artist_id: int, artist: schemas.ArtistUpdate):
    db_artist = db.query(models.Artist).filter(models.Artist.artist_id == artist_id).first()
    if not db_artist:
        return None
    for key, value in artist.model_dump(exclude_unset=True).items():
        setattr(db_artist, key, value)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def delete_artist(db: Session, artist_id: int):
    db_artist = db.query(models.Artist).filter(models.Artist.artist_id == artist_id).first()
    if not db_artist:
        return None
    db.delete(db_artist)
    db.commit()
    return db_artist

def create_album(db: Session, album: schemas.AlbumCreate):
    db_album = models.Album(**album.model_dump())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

def get_albums(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Album).offset(skip).limit(limit).all()

def get_album(db: Session, album_id: int):
    return db.query(models.Album).filter(models.Album.album_id == album_id).first()

def update_album(db: Session, album_id: int, album: schemas.AlbumUpdate):
    db_album = db.query(models.Album).filter(models.Album.album_id == album_id).first()
    if not db_album:
        return None
    for key, value in album.model_dump(exclude_unset=True).items():
        setattr(db_album, key, value)
    db.commit()
    db.refresh(db_album)
    return db_album

def delete_album(db: Session, album_id: int):
    db_album = db.query(models.Album).filter(models.Album.album_id == album_id).first()
    if not db_album:
        return None
    db.delete(db_album)
    db.commit()
    return db_album

def create_track(db: Session, track: schemas.TrackCreate):
    db_track = models.Track(**track.model_dump())
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track

def get_tracks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Track).offset(skip).limit(limit).all()

def get_track(db: Session, track_id: int):
    return db.query(models.Track).filter(models.Track.track_id == track_id).first()

def update_track(db: Session, track_id: int, track: schemas.TrackUpdate):
    db_track = db.query(models.Track).filter(models.Track.track_id == track_id).first()
    if not db_track:
        return None
    for key, value in track.model_dump(exclude_unset=True).items():
        setattr(db_track, key, value)
    db.commit()
    db.refresh(db_track)
    return db_track

def delete_track(db: Session, track_id: int):
    db_track = db.query(models.Track).filter(models.Track.track_id == track_id).first()
    if not db_track:
        return None
    db.delete(db_track)
    db.commit()
    return db_track

def get_tracks_by_mood_and_duration(db: Session, mood: str, min_duration: int, max_duration: int):
    return db.query(models.Track).filter(
        models.Track.mood == mood,
        models.Track.duration >= min_duration,
        models.Track.duration <= max_duration
    ).all()