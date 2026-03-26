# ── Backend ──────────────────────────────────────────────────
FROM python:3.11-slim AS backend

WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Download dataset at build time
RUN python3 download_data.py

EXPOSE 8000
CMD ["python3", "app.py"]
