"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, UserProfile
import os
import glob


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Find all user profile CSVs
    user_files = sorted(glob.glob("data/user_*.csv"))

    if not user_files:
        print("No user profile files found in data/")
        return

    print("\nAvailable user profiles:")
    for i, filepath in enumerate(user_files, 1):
        filename = os.path.basename(filepath)
        print(f"{i}. {filename}")

    while True:
        try:
            choice = int(input("\nSelect a user profile (enter number): "))
            if 1 <= choice <= len(user_files):
                csv_path = user_files[choice - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(user_files)}")
        except ValueError:
            print("Invalid input. Enter a number.")

    print(f"\n{'='*60}")
    print(f"Loading profile: {os.path.basename(csv_path)}")
    print(f"{'='*60}\n")

    user = UserProfile(history_csv_path=csv_path)
    print(f"Preferences:")
    print(f"  Genre: {user.favorite_genre}")
    print(f"  Mood: {user.favorite_mood}")
    print(f"  Energy: {user.favorite_energy:.2f}")
    print(f"  Tempo: {user.favorite_tempo:.1f} BPM")
    print(f"  Valence: {user.favorite_valence:.2f}")
    print(f"  Danceability: {user.favorite_danceability:.2f}")
    print(f"  Acousticness: {user.favorite_acousticness:.2f}")
    print(f"\nFeature weights: {user.feature_weights}\n")

    user_prefs = {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.favorite_energy,
        "tempo_bpm": user.favorite_tempo,
        "valence": user.favorite_valence,
        "danceability": user.favorite_danceability,
        "acousticness": user.favorite_acousticness,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("Top 5 recommendations:\n")
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"{i}. {song['title']} by {song['artist']} - Score: {score:.2f}")
        if explanation:
            reasons = explanation.split("; ")
            print("   Reasons:")
            for reason in reasons:
                print(f"     • {reason}")
        else:
            print("   (No matching preferences)")
        print()


if __name__ == "__main__":
    main()
