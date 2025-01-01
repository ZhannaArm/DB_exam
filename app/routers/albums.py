from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from sqlalchemy import func
from app import models, schemas, crud

router = APIRouter(prefix="/albums", tags=["albums"])

@router.post("/create", response_model=schemas.Album)
def create_album(album: schemas.AlbumCreate, db: Session = Depends(get_db)):
    return crud.create_album(db, album)

@router.get("/{album_id}", response_model=schemas.Album)
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.get_album(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return schemas.Album.model_validate(album)

@router.put("/{album_id}", response_model=schemas.Album)
def update_album(album_id: int, album: schemas.AlbumUpdate, db: Session = Depends(get_db)):
    updated_album = crud.update_album(db, album_id, album)
    if not updated_album:
        raise HTTPException(status_code=404, detail="Album not found")
    return schemas.Album.model_validate(updated_album)

@router.delete("/{album_id}")
def delete_album(album_id: int, db: Session = Depends(get_db)):
    success = crud.delete_album(db, album_id)
    if not success:
        raise HTTPException(status_code=404, detail="Album not found")
    return {"message": "Album deleted successfully"}

# Пагинация для получения всех альбомов
@router.get("/", response_model=schemas.PaginatedResponse[schemas.Album])
def get_albums(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(models.Album)
    total_count = query.count()
    albums = query.offset(skip).limit(limit).all()

    album_data = [schemas.Album.model_validate(album) for album in albums]

    return schemas.PaginatedResponse(
        data=album_data,
        total_count=total_count,
        skip=skip,
        limit=limit
    )

# SELECT ... WHERE с несколькими условиями.
# Получить альбомы, которые соответствуют определенному жанру и были выпущены после заданного года.
@router.get("/filter/", response_model=List[schemas.Album])
def filter_albums(genre: str, min_year: int, db: Session = Depends(get_db)):
    albums = db.query(models.Album).filter(
        models.Album.genre == genre,
        models.Album.release_year > min_year
    ).all()
    return albums

# UPDATE с нетривиальным условием.
# Обновить лейбл записи для альбомов, выпущенных после 2010 года.
@router.put("/update_record_label/")
def update_record_label(new_label: str, year: int, db: Session = Depends(get_db)):
    albums = db.query(models.Album).filter(models.Album.release_year > year).all()
    for album in albums:
        album.record_label = new_label
    db.commit()
    return {"message": "Record labels updated"}

# GROUP BY
# Получить количество альбомов по жанрам.
@router.get("/genre_summary/")
def get_albums_by_genre(db: Session = Depends(get_db)):
    genre_summary = db.query(models.Album.genre, func.count(models.Album.album_id)).group_by(models.Album.genre).all()
    return {"data": genre_summary}

# JOIN
# Получить список альбомов с их исполнителями.
@router.get("/artists/", response_model=List[schemas.Album])
def get_albums_with_artists(db: Session = Depends(get_db)):
    albums = db.query(models.Album, models.Artist).join(models.Artist).all()
    return albums

# Сортировка
# Сортировать альбомы по году выпуска.
@router.get("/sorted/", response_model=List[schemas.Album])
def get_sorted_albums(order: str = "asc", db: Session = Depends(get_db)):
    if order == "asc":
        albums = db.query(models.Album).order_by(models.Album.release_year.asc()).all()
    else:
        albums = db.query(models.Album).order_by(models.Album.release_year.desc()).all()
    return albums
