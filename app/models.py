from sqlalchemy import Column, Integer, String, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    genre = Column(String, nullable=False)
    country = Column(String(50))
    debut_year = Column(Integer)
    biography = Column(Text)
    website = Column(String(200), nullable=True)

    albums = relationship("Album", back_populates="artist")

    __table_args__ = (
        Index('idx_artist_country', 'country'),
    )

class Album(Base):
    __tablename__ = "albums"

    album_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    release_year = Column(Integer, nullable=True)
    record_label = Column(String(100))
    genre = Column(String(50))
    language = Column(String(50), nullable=True)

    artist_id = Column(Integer, ForeignKey("artists.artist_id"), nullable=False)
    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_album_language', 'language'),
    )

class Track(Base):
    __tablename__ = "tracks"

    track_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    duration = Column(Integer, nullable=False)
    lyrics = Column(Text)
    play_count = Column(Integer, default=0)
    mood = Column(String(50))
    track_metadata = Column(JSONB, nullable=True)

    artist_id = Column(Integer, ForeignKey("artists.artist_id"), nullable=False)
    album_id = Column(Integer, ForeignKey("albums.album_id"), nullable=False)
    artist = relationship("Artist")
    album = relationship("Album", back_populates="tracks")

    __table_args__ = (
        Index('ix_track_metadata_trgm', 'track_metadata', postgresql_using='gin'),
    )
