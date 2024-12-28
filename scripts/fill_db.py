import requests

BASE_URL = "http://127.0.0.1:8000"

def create_artists():
    artists = [
        {"name": "Taylor Swift", "genre": "Pop", "country": "USA", "debut_year": 2006, "biography": "Famous American artist."},
        {"name": "Ed Sheeran", "genre": "Pop", "country": "UK", "debut_year": 2011, "biography": "Grammy-winning singer."},
        {"name": "Beyonce", "genre": "R&B", "country": "USA", "debut_year": 1997, "biography": "Queen Bey."}
    ]
    for artist in artists:
        response = requests.post(f"{BASE_URL}/artists/", json=artist)
        print(response.json())

def create_albums():
    albums = [
        {"title": "1989", "release_year": 2014, "record_label": "Big Machine", "genre": "Pop", "artist_id": 1},
        {"title": "Divide", "release_year": 2017, "record_label": "Asylum", "genre": "Pop", "artist_id": 2},
        {"title": "Lemonade", "release_year": 2016, "record_label": "Columbia", "genre": "R&B", "artist_id": 3}
    ]
    for album in albums:
        response = requests.post(f"{BASE_URL}/albums/", json=album)
        print(response.json())

def create_tracks():
    tracks = [
        {"title": "Blank Space", "duration": 231, "lyrics": "Got a long list of ex-lovers...", "play_count": 1000, "mood": "Energetic", "artist_id": 1, "album_id": 1},
        {"title": "Shape of You", "duration": 233, "lyrics": "I'm in love with the shape of you...", "play_count": 2000, "mood": "Happy", "artist_id": 2, "album_id": 2},
        {"title": "Formation", "duration": 240, "lyrics": "You know you that b****...", "play_count": 1500, "mood": "Confident", "artist_id": 3, "album_id": 3}
    ]
    for track in tracks:
        response = requests.post(f"{BASE_URL}/tracks/", json=track)
        print(response.json())

if __name__ == "__main__":
    create_artists()
    create_albums()
    create_tracks()
