# 🎬 CineMatch — AI Movie Recommendation System

A production-ready, content-based movie recommendation engine powered by **Python**, **scikit-learn**, and a **Netflix-inspired UI**.

---

## ✨ Features

| Feature | Details |
|---|---|
| **ML Model** | TF-IDF vectorisation + cosine similarity |
| **Features used** | genres · keywords · cast · director · overview |
| **API** | Pure Python stdlib HTTP server (no extra framework needed) |
| **UI** | Dark cinematic theme, autocomplete search, movie cards, modal details |
| **Graceful degradation** | Falls back to demo data if backend is offline |
| **Docker** | Single `docker-compose up` to run everything |

---

## 🗂 Project Structure

```
movie-recommender/
├── backend/
│   ├── app.py              # HTTP API server (stdlib)
│   ├── model.py            # ML recommendation engine
│   ├── download_data.py    # Dataset downloader
│   └── requirements.txt
├── frontend/
│   └── index.html          # Single-file SPA (HTML + CSS + JS)
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Quick Start (Local)

### 1 · Install Python dependencies

```bash
pip install -r backend/requirements.txt
```

### 2 · Download the dataset

```bash
cd backend
python3 download_data.py
```

### 3 · Start the API server

```bash
python3 app.py
# → http://localhost:8000
```

### 4 · Open the frontend

```bash
# Option A: just open in browser
open frontend/index.html

# Option B: serve via Python
python3 -m http.server 3000 --directory frontend
# → http://localhost:3000
```

---

## 🐳 Docker (recommended)

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| Backend API | http://localhost:8000 |
| Frontend | http://localhost:3000 |

---

## 🔌 API Endpoints

### `GET /recommend?movie=<title>&n=<int>`
Returns top-N similar movies.

```json
{
  "query": "The Dark Knight",
  "results": [
    {
      "title": "Batman Begins",
      "overview": "...",
      "genres": "Action Adventure",
      "director": "Christopher Nolan",
      "cast": "Christian Bale, Michael Caine, ...",
      "vote_average": "8.2",
      "release_date": "2005-06-15",
      "similarity": 0.8432
    }
  ]
}
```

### `GET /movies?q=<query>&limit=<int>`
Search movies by partial title.

### `GET /trending?limit=<int>`
Top movies by weighted vote score.

### `GET /titles`
All movie titles (used for autocomplete).

### `GET /health`
Health check → `{"status": "ok"}`

---

## 🧠 How the Model Works

```
Dataset CSV
    │
    ▼
Combine features → "soup" string per movie
    │  genres + keywords + cast (top 3) + director×3 + overview
    │
    ▼
TF-IDF Vectorizer (10k features, bigrams, English stopwords)
    │
    ▼
Cosine Similarity Matrix (N × N)
    │
    ▼
For query movie → rank all others by similarity score → return top N
```

**Why TF-IDF + Cosine?**
- Fast to compute on CPU (dataset ~5k movies)
- No training data needed (unsupervised)
- Transparent & interpretable

---

## 🎨 UI Highlights

- **Playfair Display** serif for headings — cinematic, editorial
- **DM Sans** for body — modern, legible
- Gold accent palette (`#e8c97b`) on deep-space dark background
- CSS grain overlay for film-stock texture
- Animated floating orb backgrounds in hero
- Staggered card entrance animations
- Movie detail modal with backdrop image
- Autocomplete with keyboard navigation (↑↓ Enter Esc)
- Skeleton/spinner loading states
- Offline demo mode (works without backend)

---

## 🧪 Test Cases

| Input | Expected |
|---|---|
| `The Dark Knight` | Batman Begins, Inception, The Prestige, … |
| `Toy Story` | Finding Nemo, Monsters Inc., A Bug's Life, … |
| `xyzabc123` | 404 error → "Movie not found" toast |
| `` (empty) | Validation error before API call |

---

## ☁️ Deployment

### Backend → Render
1. Push `backend/` to GitHub
2. Create new **Web Service** on [render.com](https://render.com)
3. Build command: `pip install -r requirements.txt && python3 download_data.py`
4. Start command: `python3 app.py`
5. Set env var `PORT=10000`

### Frontend → Vercel / Netlify
1. Push `frontend/` to GitHub
2. Deploy as **Static Site** (no build step needed)
3. Update `const API = "https://your-render-url.onrender.com"` in `index.html`

---

## 📦 Dependencies

```
pandas>=2.0.0       # Data loading & manipulation
scikit-learn>=1.3.0 # TF-IDF, cosine similarity
numpy>=1.24.0       # Numerical ops
```

No web framework required — uses Python's built-in `http.server`.

---

## 📄 Dataset

[movie_dataset.csv](https://github.com/rashida048/Some-NLP-Projects/blob/master/movie_dataset.csv) — ~5000 movies with genres, keywords, cast, director, overview, vote stats.

---

## 📸 Screenshots

Open `frontend/index.html` in any modern browser after starting the backend.

---

*Built with ❤️ using Python · scikit-learn · HTML/CSS/JS*
