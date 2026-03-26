"""
Movie Recommendation Model
Uses TF-IDF + Cosine Similarity for content-based filtering.
Dataset: https://github.com/rashida048/Some-NLP-Projects/blob/master/movie_dataset.csv
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
import re

# --------------------------------------------------------------------------- #
# 1. LOAD & PREPARE DATA
# --------------------------------------------------------------------------- #

def _clean_text(val):
    """Lowercase, strip, replace NaN with empty string."""
    if pd.isna(val) or val is None:
        return ""
    return str(val).lower().strip()



# Maps ISO 639-1 language codes to human-readable tags added to the soup so
# that language/industry becomes a similarity signal.
LANGUAGE_TAGS = {
    "hi": "hindi bollywood indian",
    "mr": "marathi maharashtra indian",
    "te": "telugu tollywood indian",
    "ta": "tamil kollywood indian",
    "kn": "kannada sandalwood indian",
    "ml": "malayalam mollywood indian",
    "bn": "bengali indian",
    "pa": "punjabi indian",
}


def _build_soup(row):
    """
    Combine relevant features into one 'soup' string per movie.
    Fields: genres, keywords, cast (top 3), director, language/industry tag
    """
    parts = []
    # genres  ----------------------------------------------------------------
    genres = _clean_text(row.get("genres", ""))
    genres = re.sub(r"['\"\[\]{}]", "", genres).replace(",", " ")
    parts.append(genres)

    # keywords  --------------------------------------------------------------
    keywords = _clean_text(row.get("keywords", ""))
    keywords = re.sub(r"['\"\[\]{}]", "", keywords).replace(",", " ")
    parts.append(keywords)

    # cast (first 3 actors) --------------------------------------------------
    cast = _clean_text(row.get("cast", ""))
    cast = re.sub(r"['\"\[\]{}]", "", cast)
    # keep only first 3 names
    cast_names = [c.strip().replace(" ", "") for c in cast.split(",")[:3]]
    parts.append(" ".join(cast_names))

    # director  --------------------------------------------------------------
    director = _clean_text(row.get("director", ""))
    director = director.replace(" ", "")
    parts.append(director * 3)  # weight director more

    # overview  --------------------------------------------------------------
    overview = _clean_text(row.get("overview", ""))
    parts.append(overview)

    # language / industry tag (weighted × 2 to cluster by industry) ----------
    lang = _clean_text(row.get("original_language", ""))
    lang_tag = LANGUAGE_TAGS.get(lang, "")
    if lang_tag:
        parts.append(lang_tag * 2)

    return " ".join(filter(None, parts))


class MovieRecommender:
    """
    Content-based movie recommender.
    Pre-computes TF-IDF matrix + cosine similarity on construction.
    """

    def __init__(self, csv_path: str):
        self.df = self._load_data(csv_path)
        self._build_model()

    # ----------------------------------------------------------------------- #
    def _load_data(self, csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path)

        # Normalize column names
        df.columns = [c.lower().strip() for c in df.columns]

        # Fill NaN in text columns
        text_cols = ["genres", "keywords", "cast", "director", "overview",
                     "title", "tagline"]
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].fillna("")

        # Ensure required columns exist
        if "title" not in df.columns:
            raise ValueError("Dataset must have a 'title' column")

        # Build soup
        df["soup"] = df.apply(_build_soup, axis=1)

        # Create lowercase title index for fast lookup
        df["title_lower"] = df["title"].str.lower().str.strip()

        # Popularity/vote score for trending (optional columns)
        if "vote_average" in df.columns and "vote_count" in df.columns:
            df["vote_average"] = pd.to_numeric(df["vote_average"], errors="coerce").fillna(0)
            df["vote_count"] = pd.to_numeric(df["vote_count"], errors="coerce").fillna(0)
            df["score"] = df["vote_average"] * np.log1p(df["vote_count"])
        else:
            df["score"] = 0

        return df.reset_index(drop=True)

    # ----------------------------------------------------------------------- #
    def _build_model(self):
        """Fit TF-IDF and compute full cosine similarity matrix."""
        tfidf = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=10_000
        )
        tfidf_matrix = tfidf.fit_transform(self.df["soup"])
        # Cosine similarity (dense for small datasets ~5k rows)
        self.sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        print(f"[Model] Built similarity matrix: {self.sim_matrix.shape}")

    # ----------------------------------------------------------------------- #
    def _movie_to_dict(self, row) -> dict:
        """Serialize a DataFrame row to a plain dict."""
        def safe(col, default=""):
            return str(row.get(col, default)) if not pd.isna(row.get(col, np.nan)) else default

        return {
            "title":             safe("title"),
            "overview":          safe("overview"),
            "genres":            safe("genres"),
            "director":          safe("director"),
            "cast":              safe("cast"),
            "release_date":      safe("release_date"),
            "vote_average":      safe("vote_average", "0"),
            "vote_count":        safe("vote_count", "0"),
            "poster_path":       safe("poster_path"),   # may be empty
            "id":                safe("id"),
            "original_language": safe("original_language"),
        }

    # ----------------------------------------------------------------------- #
    def recommend(self, title: str, top_n: int = 10) -> list[dict]:
        """
        Return top_n recommendations for a given movie title.
        Raises KeyError if title not found.
        """
        title_lower = title.lower().strip()
        matches = self.df[self.df["title_lower"] == title_lower]

        if matches.empty:
            # Try partial match
            partial = self.df[self.df["title_lower"].str.contains(
                re.escape(title_lower), na=False)]
            if partial.empty:
                raise KeyError(f"Movie '{title}' not found in dataset.")
            idx = partial.index[0]
        else:
            idx = matches.index[0]

        # Similarity scores for this movie
        sim_scores = list(enumerate(self.sim_matrix[idx]))
        # Sort by similarity descending, skip self (score == 1.0 at idx)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [s for s in sim_scores if s[0] != idx][:top_n]

        results = []
        for i, score in sim_scores:
            movie = self._movie_to_dict(self.df.iloc[i])
            movie["similarity"] = round(float(score), 4)
            results.append(movie)
        return results

    # ----------------------------------------------------------------------- #
    def search(self, query: str, limit: int = 10) -> list[dict]:
        """Search movies by partial title match."""
        q = query.lower().strip()
        if not q:
            return []
        mask = self.df["title_lower"].str.contains(re.escape(q), na=False)
        matches = self.df[mask].sort_values("score", ascending=False).head(limit)
        return [self._movie_to_dict(r) for _, r in matches.iterrows()]

    # ----------------------------------------------------------------------- #
    def trending(self, limit: int = 20) -> list[dict]:
        """Return top movies by weighted vote score."""
        top = self.df.sort_values("score", ascending=False).head(limit)
        return [self._movie_to_dict(r) for _, r in top.iterrows()]

    # ----------------------------------------------------------------------- #
    def all_titles(self) -> list[str]:
        return sorted(self.df["title"].dropna().unique().tolist())
