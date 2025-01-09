# DB_exam
# Music API Project

This project is a Music API built using FastAPI, SQLAlchemy, and Alembic for handling database migrations. It allows managing artists, albums, and tracks with features like CRUD operations, metadata storage, and relationships between entities. The frontend is built with HTML, CSS, and JavaScript.

## Project Structure

```
project/
├── alembic/           # Database migrations
├── app/
│   ├── models.py    # SQLAlchemy models
│   ├── routers/    # FastAPI routes
│   ├── crud.py      # CRUD operations
│   └── database.py      # Database initialization
└── frontend/       # HTML, CSS, JS files
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL or compatible database

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ZhannaArm/DB_exam.git
   cd music-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Update the database URL in `alembic.ini` and `app/db.py`.
   - Run migrations:
     ```bash
     alembic upgrade head
     ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Access the API docs:
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

## Usage

### Endpoints

#### Artists
- **GET** `/artists`: List all artists.
- **POST** `/artists/create`: Add a new artist.

#### Albums
- **GET** `/albums`: List all albums.
- **POST** `/albums/create`: Add a new album.

#### Tracks
- **GET** `/tracks`: List all tracks.
- **POST** `/tracks/create`: Add a new track.

### Example Script

The `scripts.py` file provides examples for interacting with the API:

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Create an artist
response = requests.post(f"{BASE_URL}/artists/create", json={
    "name": "Taylor Swift",
    "genre": "Pop",
    "country": "USA",
    "debut_year": 2006,
    "biography": "Famous American artist."
})
print(response.json())
```
