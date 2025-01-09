from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from sqlalchemy import func
from app import models, schemas, crud

router = APIRouter(prefix="/artists", tags=["artists"])

@router.post("/create", response_model=schemas.Artist)
def create_artist(artist: schemas.ArtistCreate, db: Session = Depends(get_db)):
    return crud.create_artist(db, artist)

@router.get("/{artist_id}", response_model=schemas.Artist)
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = crud.get_artist(db, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return schemas.Artist.model_validate(artist)

@router.put("/{artist_id}", response_model=schemas.Artist)
def update_artist(artist_id: int, artist: schemas.ArtistUpdate, db: Session = Depends(get_db)):
    updated_artist = crud.update_artist(db, artist_id, artist)
    if not updated_artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return schemas.Artist.model_validate(updated_artist)

@router.delete("/{artist_id}")
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    success = crud.delete_artist(db, artist_id)
    if not success:
        raise HTTPException(status_code=404, detail="Artist not found")
    return {"message": "Artist deleted successfully"}

# Пагинация для получения всех артистов
@router.get("/", response_model=schemas.PaginatedResponse[schemas.Artist])
def get_artists(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(models.Artist)
    total_count = query.count()
    artists = query.offset(skip).limit(limit).all()

    artist_data = [schemas.Artist.model_validate(artist) for artist in artists]

    return schemas.PaginatedResponse(
        data=artist_data,
        total_count=total_count,
        skip=skip,
        limit=limit
    )

# SELECT ... WHERE с несколькими условиями.
# Получить всех артистов, которые соответствуют определенному жанру и дебютировали после заданного года.
@router.get("/filter/", response_model=List[schemas.Artist])
def filter_artists(genre: str, debut_year: int, db: Session = Depends(get_db)):
    artists = db.query(models.Artist).filter(
        models.Artist.genre == genre,
        models.Artist.debut_year > debut_year
    ).all()
    return artists

# UPDATE с нетривиальным условием.
# Обновить страну артистов, которые выпустили альбомы после 2010 года.
@router.put("/update_country/")
def update_artist_country(new_country: str, year: int, db: Session = Depends(get_db)):
    artists = db.query(models.Artist).join(models.Album).filter(models.Album.release_year > year).all()
    for artist in artists:
        artist.country = new_country
    db.commit()
    return {"message": "Artist countries updated"}

# GROUP BY
# Получить количество артистов по жанрам.
@router.get("/genre_summary/")
def get_artists_by_genre(db: Session = Depends(get_db)):
    genre_summary = db.query(models.Artist.genre, func.count(models.Artist.artist_id)).group_by(models.Artist.genre).all()
    return {"data": genre_summary}

# JOIN
# Получить всех артистов с их альбомами.
@router.get("/join/", response_model=List[schemas.Artist])
def get_artists_with_albums(db: Session = Depends(get_db)):
    artists = db.query(models.Artist, models.Album).join(
        models.Album, models.Artist.artist_id == models.Album.artist_id
    ).all()
    return [
        {
            "artist": artist[0],
            "albums": [album for album in artists if album[0] == artist[0]]
        }
        for artist in artists
    ]

# Сортировка
# Получить всех артистов, отсортированных по году дебюта или имени.
@router.get("/sort/", response_model=List[schemas.Artist])
def sort_artists(sort_by: str = "debut_year", db: Session = Depends(get_db)):
    valid_fields = ["name", "debut_year", "genre"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    artists = db.query(models.Artist).order_by(getattr(models.Artist, sort_by)).all()
    return artists