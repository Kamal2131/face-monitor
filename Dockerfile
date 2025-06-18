# ─── 1. Use a lightweight official Python image ───────────────────────────────
FROM python:3.10-slim-buster

# ─── 2. Install only essential system packages ────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# ─── 3. Set working directory ─────────────────────────────────────────────────
WORKDIR /app

# ─── 4. Install Python dependencies ───────────────────────────────────────────
COPY requirements.txt /app/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ─── 5. Copy application source code ──────────────────────────────────────────
COPY . /app

# ─── 6. Expose the app port ───────────────────────────────────────────────────
EXPOSE 8000

# ─── 7. Start the FastAPI app ─────────────────────────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
