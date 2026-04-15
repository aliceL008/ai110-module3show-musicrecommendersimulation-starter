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


DEFAULT_WEIGHTS = {
    "mood":    3.0,
    "energy":  2.0,
    "clarity": 1.5,
    "genre":   1.5,
    "acoustic": 0.5,
}

ENERGY_FIRST_WEIGHTS = {
    "mood":    2.0,
    "energy":  3.0,
    "clarity": 1.5,
    "genre":   1.5,
    "acoustic": 0.5,
}

GENRE_DOMINANCE_WEIGHTS = {
    "mood":    1.5,
    "energy":  2.0,
    "clarity": 1.5,
    "genre":   3.0,
    "acoustic": 0.5,
}


def score_song(user_prefs: Dict, song: Dict, weights: Dict = None) -> Tuple[float, List[str]]:
    """Return a (score, reasons) tuple ranking how well a song fits the user's preferences."""
    w = weights if weights is not None else DEFAULT_WEIGHTS
    points = 0.0
    reasons = []

    # Mood match
    if song.get("mood") == user_prefs.get("mood"):
        points += w["mood"]
        reasons.append(f"mood matches '{song['mood']}'")

    # Energy closeness — scaled to weight max
    target_energy = user_prefs.get("energy", 0.5)
    energy_closeness = 1.0 - abs(song.get("energy", 0.5) - target_energy)
    energy_points = round(w["energy"] * energy_closeness, 2)
    points += energy_points
    reasons.append(f"energy {energy_points}/{w['energy']}")

    # Clarity / valence — scaled to weight max
    clarity = song.get("clarity", song.get("valence", 0.0))
    clarity_points = round(w["clarity"] * clarity, 2)
    points += clarity_points
    reasons.append(f"clarity {clarity_points}/{w['clarity']}")

    # Genre match
    if song.get("genre") == user_prefs.get("genre"):
        points += w["genre"]
        reasons.append(f"genre matches '{song['genre']}'")

    # Acoustic fit
    if song.get("acousticness", 0.0) > 0.5:
        points += w["acoustic"]
        reasons.append("acoustic feel")

    return round(points, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Dict = None) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights=weights)
        scored.append((song, score, "; ".join(reasons)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
