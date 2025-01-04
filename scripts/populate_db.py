import random
import requests
from faker import Faker

BASE_URL = "http://127.0.0.1:8000"
faker = Faker()

def create_artists(n=100):
    for _ in range(n):
        artist = {
            "name": faker.name(),
            "genre": random.choice(["Pop", "Rock", "Hip-Hop", "Jazz", "Classical"]),
            "country": faker.country(),
            "debut_year": random.randint(1950, 2023),
            "biography": faker.text(max_nb_chars=200),
        }
        response = requests.post(f"{BASE_URL}/artists/create", json=artist)
        if response.status_code != 200:
            print(f"Error creating artist: {response.text}")
        else:
            print(f"Created artist: {response.json()}")

def create_albums(artist_ids, n=200):
    for _ in range(n):
        album = {
            "title": faker.word().capitalize(),
            "release_year": random.randint(1970, 2023),
            "record_label": faker.company(),
            "genre": random.choice(["Pop", "Rock", "Hip-Hop", "Jazz", "Classical"]),
            "artist_id": random.choice(artist_ids),
        }
        response = requests.post(f"{BASE_URL}/albums/create", json=album)
        if response.status_code != 200:
            print(f"Error creating album: {response.text}")
        else:
            print(f"Created album: {response.json()}")

def create_tracks(artist_ids, album_ids, n=500):
    for _ in range(n):
        track = {
            "title": faker.sentence(nb_words=3).replace(".", ""),
            "duration": random.randint(120, 360),
            "lyrics": faker.text(max_nb_chars=500),
            "play_count": random.randint(0, 1000000),
            "mood": random.choice(["Happy", "Sad", "Energetic", "Calm"]),
            "artist_id": random.choice(artist_ids),
            "album_id": random.choice(album_ids) if random.random() > 0.2 else None,
        }
        response = requests.post(f"{BASE_URL}/tracks/create", json=track)
        if response.status_code != 200:
            print(f"Error creating track: {response.text}")
        else:
            print(f"Created track: {response.json()}")

def get_artist_ids():
    response = requests.get(f"{BASE_URL}/artists")
    if response.status_code != 200:
        print(f"Error fetching artists: {response.text}")
        return []
    artists = response.json().get("data", [])
    return [artist["artist_id"] for artist in artists]

def get_album_ids():
    response = requests.get(f"{BASE_URL}/albums")
    if response.status_code != 200:
        print(f"Error fetching albums: {response.text}")
        return []
    albums = response.json().get("data", [])
    return [album["album_id"] for album in albums]

if __name__ == "__main__":
    print("Creating artists...")
    create_artists(100)

    print("Fetching artist IDs...")
    artist_ids = get_artist_ids()

    print("Creating albums...")
    create_albums(artist_ids, 200)

    print("Fetching album IDs...")
    album_ids = get_album_ids()

    print("Creating tracks...")
    create_tracks(artist_ids, album_ids, 500)

    print("Database population complete!")
