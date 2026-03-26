"""
Movie Recommender — Backend HTTP Server
Pure stdlib http.server (no external web framework required).
Endpoints:
  GET /recommend?movie=<title>&n=<int>   → JSON list of recommendations
  GET /movies?q=<query>&limit=<int>      → JSON search results
  GET /trending?limit=<int>              → JSON trending movies
  GET /titles                            → JSON array of all titles
  OPTIONS *                              → CORS preflight

Run: python3 app.py
Default port: 8000  (set PORT env var to override)
"""

import json
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

# --------------------------------------------------------------------------- #
# Bootstrap: locate dataset, initialize model
# --------------------------------------------------------------------------- #
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BACKEND_DIR, "movie_dataset.csv")

# Lazy-load model (populated in main())
_recommender = None

def get_recommender():
    global _recommender
    if _recommender is None:
        from model import MovieRecommender
        if not os.path.exists(CSV_PATH):
            print(f"[ERROR] Dataset not found at {CSV_PATH}")
            print("  Please run:  python3 download_data.py")
            sys.exit(1)
        print("[Server] Loading model … (first run may take a few seconds)")
        _recommender = MovieRecommender(CSV_PATH)
        print("[Server] Model ready ✓")
    return _recommender


# --------------------------------------------------------------------------- #
# HTTP Handler
# --------------------------------------------------------------------------- #
CORS_HEADERS = {
    "Access-Control-Allow-Origin":  "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        # Cleaner logging
        print(f"  {self.address_string()} → {fmt % args}")

    # ----------------------------------------------------------------------- #
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        for k, v in CORS_HEADERS.items():
            self.send_header(k, v)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, message, status=400):
        self._send_json({"error": message}, status)

    # ----------------------------------------------------------------------- #
    def do_OPTIONS(self):
        self.send_response(204)
        for k, v in CORS_HEADERS.items():
            self.send_header(k, v)
        self.end_headers()

    # ----------------------------------------------------------------------- #
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path   = parsed.path.rstrip("/")
        params = urllib.parse.parse_qs(parsed.query)

        rec = get_recommender()

        # ------------------------------------------------------------------- #
        if path == "/recommend":
            movie = params.get("movie", [""])[0].strip()
            n     = int(params.get("n", ["10"])[0])
            if not movie:
                return self._send_error("Missing 'movie' parameter", 400)
            try:
                results = rec.recommend(movie, top_n=min(n, 20))
                self._send_json({"query": movie, "results": results})
            except KeyError as e:
                self._send_error(str(e), 404)
            except Exception as e:
                self._send_error(f"Internal error: {e}", 500)

        # ------------------------------------------------------------------- #
        elif path == "/movies":
            query = params.get("q", [""])[0].strip()
            limit = int(params.get("limit", ["10"])[0])
            results = rec.search(query, limit=min(limit, 30))
            self._send_json({"query": query, "results": results})

        # ------------------------------------------------------------------- #
        elif path == "/trending":
            limit = int(params.get("limit", ["20"])[0])
            results = rec.trending(limit=min(limit, 50))
            self._send_json({"results": results})

        # ------------------------------------------------------------------- #
        elif path == "/titles":
            self._send_json({"titles": rec.all_titles()})

        # ------------------------------------------------------------------- #
        elif path in ("", "/", "/health"):
            self._send_json({"status": "ok", "message": "Movie Recommender API"})

        # ------------------------------------------------------------------- #
        else:
            self._send_error("Not found", 404)


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Eagerly load model before accepting requests
    get_recommender()
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"\n🎬  Movie Recommender API  →  http://localhost:{port}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server] Shutting down.")
