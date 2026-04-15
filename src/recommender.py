from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields converted."""
    import csv

    float_fields = {"energy", "valence", "danceability", "acousticness",
                    "instrumentalness", "loudness_db", "clarity"}
    int_fields = {"id", "tempo_bpm", "duration_seconds"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in float_fields:
                if field in row:
                    row[field] = float(row[field])
            for field in int_fields:
                if field in row:
                    row[field] = int(row[field])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a (score, reasons) tuple ranking how well a song fits the user's preferences."""
    points = 0.0
    reasons = []

    # Mood match — highest weight (3.0)
    if song.get("mood") == user_prefs.get("mood"):
        points += 3.0
        reasons.append(f"mood matches '{song['mood']}'")

    # Energy closeness — up to 2.0 points
    target_energy = user_prefs.get("energy", 0.5)
    energy_closeness = 1.0 - abs(song.get("energy", 0.5) - target_energy)
    energy_points = round(2.0 * energy_closeness, 2)
    points += energy_points
    reasons.append(f"energy {energy_points}/2.0")

    # Clarity / valence — up to 1.5 points
    clarity = song.get("clarity", song.get("valence", 0.0))
    clarity_points = round(1.5 * clarity, 2)
    points += clarity_points
    reasons.append(f"clarity {clarity_points}/1.5")

    # Genre match — 1.5 points
    if song.get("genre") == user_prefs.get("genre"):
        points += 1.5
        reasons.append(f"genre matches '{song['genre']}'")

    # Acoustic fit — small bonus (0.5)
    if song.get("acousticness", 0.0) > 0.5:
        points += 0.5
        reasons.append("acoustic feel")

    return round(points, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
