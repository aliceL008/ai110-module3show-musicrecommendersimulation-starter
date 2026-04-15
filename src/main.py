"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, DEFAULT_WEIGHTS, ENERGY_FIRST_WEIGHTS, GENRE_DOMINANCE_WEIGHTS


PROFILES = {
    "High-Energy Pop":   {"genre": "pop",  "mood": "happy",  "energy": 0.9},
    "Chill Lofi":        {"genre": "lofi", "mood": "chill",  "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense","energy": 0.92},
}


EXPERIMENTS = {
    "Default":          DEFAULT_WEIGHTS,
    "Energy-First":     ENERGY_FIRST_WEIGHTS,
    "Genre-Dominance":  GENRE_DOMINANCE_WEIGHTS,
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_label, user_prefs in PROFILES.items():
        print("\n" + "#" * 50)
        print(f"  Profile: {profile_label}")
        print("#" * 50)
        for exp_label, weights in EXPERIMENTS.items():
            recommendations = recommend_songs(user_prefs, songs, k=3, weights=weights)
            print(f"\n  [{exp_label}]")
            for i, (song, score, explanation) in enumerate(recommendations, start=1):
                print(f"  #{i}  {song['title']} by {song['artist']}  (score: {score:.2f})")
                print(f"       {explanation}")


if __name__ == "__main__":
    main()
