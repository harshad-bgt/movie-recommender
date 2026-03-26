"""
Download movie_dataset.csv from GitHub.
Run once before starting the backend: python3 download_data.py
"""
import urllib.request
import os

URL = (
    "https://raw.githubusercontent.com/"
    "rashida048/Some-NLP-Projects/master/movie_dataset.csv"
)
DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "movie_dataset.csv")

def download():
    if os.path.exists(DEST):
        print(f"[OK] Dataset already exists at {DEST}")
        return
    print(f"Downloading dataset …")
    urllib.request.urlretrieve(URL, DEST)
    size = os.path.getsize(DEST)
    print(f"[OK] Saved to {DEST}  ({size:,} bytes)")

if __name__ == "__main__":
    download()
