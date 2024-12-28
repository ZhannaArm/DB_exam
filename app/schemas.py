from pydantic import BaseModel
from typing import List, Optional

class ArtistBase(BaseModel):
    name: str
    genre: str
    country: Optional[str] = None
    debut_year: Optional[int] = None
    biography: Optional[str] = None

class AlbumBase(BaseModel):
    title: str
    release_year: Optional[int] = None
    record_label: Optional[str] = None
    genre: Optional[str] = None

class TrackBase(BaseModel):
    title: str
    duration: int
    lyrics: Optional[str] = None
    play_count: Optional[int] = 0
    mood: Optional[str] = None

# ----- Artist Schemas -----
class ArtistCreate(ArtistBase):
    pass

class ArtistUpdate(ArtistBase):
    pass

class Artist(ArtistBase):
    artist_id: int

    class Config:
        orm_mode = True

# ----- Album Schemas -----
class AlbumCreate(AlbumBase):
    artist_id: int

class AlbumUpdate(AlbumBase):
    pass

class Album(AlbumBase):
    album_id: int
    artist_id: int

    class Config:
        orm_mode = True

# ----- Track Schemas -----
class TrackCreate(TrackBase):
    artist_id: int
    album_id: int

class TrackUpdate(TrackBase):
    pass

class Track(TrackBase):
    track_id: int
    artist_id: int
    album_id: int

    class Config:
        orm_mode = True