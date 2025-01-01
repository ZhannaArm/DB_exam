import requests

BASE_URL = "http://127.0.0.1:8000"

def get_artist_ids():
    response = requests.get(f"{BASE_URL}/artists")
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
    else:
        artists = response.json().get('data', [])
        print(f"Artists: {artists}")
        artist_ids = {artist['name']: artist['artist_id'] for artist in artists}
        print(f"Artist IDs: {artist_ids}")
        return artist_ids

def get_album_ids():
    response = requests.get(f"{BASE_URL}/albums")
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
    else:
        albums = response.json().get('data', [])
        album_ids = {album['title']: album['album_id'] for album in albums}
        print(f"Album IDs: {album_ids}")
        return album_ids

def create_artists():
    artists = [
        {"name": "Taylor Swift", "genre": "Pop", "country": "USA", "debut_year": 2006,
         "biography": "Famous American artist."},
        {"name": "Ed Sheeran", "genre": "Pop", "country": "UK", "debut_year": 2011,
         "biography": "Grammy-winning singer."},
        {"name": "Beyonce", "genre": "R&B", "country": "USA", "debut_year": 1997, "biography": "Queen Bey."}
    ]
    for artist in artists:
        response = requests.post(f"{BASE_URL}/artists/create", json=artist)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
        else:
            print(response.json())

def create_albums(artist_ids):
    albums = [
        {"title": "1989", "release_year": 2014, "record_label": "Big Machine", "genre": "Pop",
         "artist_id": artist_ids.get("Taylor Swift")},
        {"title": "Divide", "release_year": 2017, "record_label": "Asylum", "genre": "Pop",
         "artist_id": artist_ids.get("Ed Sheeran")},
        {"title": "Lemonade", "release_year": 2016, "record_label": "Columbia", "genre": "R&B",
         "artist_id": artist_ids.get("Beyonce")}
    ]
    for album in albums:
        response = requests.post(f"{BASE_URL}/albums/create", json=album)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
        else:
            print(response.json())

def create_tracks(artist_ids, album_ids):
    tracks = [
        {"title": "Blank Space", "duration": 231, "lyrics": "Got a long list of ex-lovers...", "play_count": 1000,
         "mood": "Energetic", "artist_id": artist_ids.get("Taylor Swift"), "album_id": album_ids.get("1989")},
        {"title": "Shape of You", "duration": 233, "lyrics": "I'm in love with the shape of you...", "play_count": 2000,
         "mood": "Happy", "artist_id": artist_ids.get("Ed Sheeran"), "album_id": album_ids.get("Divide")},
        {"title": "Formation", "duration": 240, "lyrics": "You know you that b****...", "play_count": 1500,
         "mood": "Confident", "artist_id": artist_ids.get("Beyonce"), "album_id": album_ids.get("Lemonade")}
    ]
    for track in tracks:
        response = requests.post(f"{BASE_URL}/tracks/create", json=track)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
        else:
            print(response.json())


if __name__ == "__main__":
    create_artists()

    artist_ids = get_artist_ids()
    create_albums(artist_ids)

    album_ids = get_album_ids()
    create_tracks(artist_ids, album_ids)
