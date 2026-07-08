from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import csv
from collections import Counter

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
    Represents a user's taste preferences computed from listening history.
    Required by tests/test_recommender.py
    """
    history_csv_path: str
    favorite_genre: str = None
    favorite_mood: str = None
    favorite_energy: float = None
    favorite_tempo: float = None
    favorite_valence: float = None
    favorite_danceability: float = None
    favorite_acousticness: float = None
    feature_weights: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        self._compute_preferences()

    def _compute_preferences(self):
        """Load history CSV and compute feature preferences and weights."""
        songs = []
        with open(self.history_csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                songs.append({
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                })

        if not songs:
            return

        # Categorical features: most common value
        genres = [s['genre'] for s in songs]
        moods = [s['mood'] for s in songs]
        self.favorite_genre = Counter(genres).most_common(1)[0][0]
        self.favorite_mood = Counter(moods).most_common(1)[0][0]

        # Numeric features: average value (or could use median/range)
        self.favorite_energy = sum(s['energy'] for s in songs) / len(songs)
        self.favorite_tempo = sum(s['tempo_bpm'] for s in songs) / len(songs)
        self.favorite_valence = sum(s['valence'] for s in songs) / len(songs)
        self.favorite_danceability = sum(s['danceability'] for s in songs) / len(songs)
        self.favorite_acousticness = sum(s['acousticness'] for s in songs) / len(songs)

        # Rank features by consistency and assign weights
        self._compute_feature_weights(songs)

    def _compute_feature_weights(self, songs: List[Dict]):
        """Rank features by consistency and assign weights (7 = most consistent, 1 = least)."""
        consistencies = {}

        # Categorical consistency: % of songs matching most common value
        genre_count = Counter([s['genre'] for s in songs])
        consistencies['genre'] = genre_count.most_common(1)[0][1] / len(songs)

        mood_count = Counter([s['mood'] for s in songs])
        consistencies['mood'] = mood_count.most_common(1)[0][1] / len(songs)

        # Numeric consistency: inverse of range spread (narrow = high consistency)
        numeric_features = ['energy', 'tempo_bpm', 'valence', 'danceability', 'acousticness']
        for feat in numeric_features:
            values = [s[feat] for s in songs]
            min_val, max_val = min(values), max(values)
            range_spread = max_val - min_val if max_val != min_val else 0.001
            # Normalize to 0-1 (small spread = high consistency)
            consistencies[feat] = 1.0 - min(range_spread, 1.0)

        # Sort by consistency (descending) and assign weights 7→1
        sorted_features = sorted(consistencies.items(), key=lambda x: x[1], reverse=True)
        self.feature_weights = {feat: (7 - idx) for idx, (feat, _) in enumerate(sorted_features)}

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
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    return []

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
