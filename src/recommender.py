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
    """Reads songs from CSV, returns list of dicts with id, title, artist, and audio features."""
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            })
    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict, all_songs: List[Dict] = None) -> Tuple[float, List[str]]:
    """Scores song against user preferences; weights features by entropy (consistency across dataset)."""
    score = 0.0
    reasons = []

    # Calculate entropy-based weights from all songs
    weights = _get_feature_weights(all_songs) if all_songs else {
        'genre': 1.0, 'mood': 1.0, 'energy': 1.0, 'tempo_bpm': 1.0,
        'valence': 1.0, 'danceability': 1.0, 'acousticness': 1.0,
    }

    # Categorical features
    if 'genre' in user_prefs and user_prefs['genre'] == song['genre']:
        score += weights['genre']
        reasons.append(f"Genre '{song['genre']}' matches (weight: {weights['genre']:.1f})")

    if 'mood' in user_prefs and user_prefs['mood'] == song['mood']:
        score += weights['mood']
        reasons.append(f"Mood '{song['mood']}' matches (weight: {weights['mood']:.1f})")

    # Numeric features
    for feat in ['energy', 'tempo_bpm', 'valence', 'danceability', 'acousticness']:
        if feat in user_prefs:
            user_val = user_prefs[feat]
            song_val = song[feat]

            # Normalize distance
            if feat == 'tempo_bpm':
                distance = abs(user_val - song_val) / 200
            else:
                distance = abs(user_val - song_val)

            # Distance-based score (closer = higher)
            match_score = max(0, (1 - distance) * weights[feat])
            if match_score > 0.05:
                score += match_score
                reasons.append(f"{feat}: {song_val:.2f} vs {user_val:.2f} (weight: {weights[feat]:.1f})")

    return (score, reasons)


def _get_feature_weights(songs: List[Dict]) -> Dict[str, float]:
    """Calculate entropy-based weights. High consistency = high weight."""
    consistencies = {}

    # Categorical: consistency = % of songs with most common value
    genre_count = Counter([s['genre'] for s in songs])
    consistencies['genre'] = genre_count.most_common(1)[0][1] / len(songs)

    mood_count = Counter([s['mood'] for s in songs])
    consistencies['mood'] = mood_count.most_common(1)[0][1] / len(songs)

    # Numeric: consistency = 1 - normalized range spread
    for feat in ['energy', 'tempo_bpm', 'valence', 'danceability', 'acousticness']:
        values = [s[feat] for s in songs]
        min_val, max_val = min(values), max(values)
        range_spread = max_val - min_val if max_val != min_val else 0.001
        if feat == 'tempo_bpm':
            norm_spread = range_spread / 200
        else:
            norm_spread = range_spread
        consistencies[feat] = 1.0 - min(norm_spread, 1.0)

    # Assign weights 7→1 based on consistency ranking
    sorted_feats = sorted(consistencies.items(), key=lambda x: x[1], reverse=True)
    weights = {feat: float(7 - idx) for idx, (feat, _) in enumerate(sorted_feats)}

    return weights

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores all songs, ranks by score, returns top k with explanations."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, songs)
        explanation = "; ".join(reasons) if reasons else "No matching preferences"
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
