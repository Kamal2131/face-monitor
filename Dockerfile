# ─── 1. Use base image with prebuilt dlib wheel support ───────────────────────
FROM python:3.10-bullseye

# ─── 2. Install system dependencies for OpenCV, dlib, and general build tools ─
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libatlas-base-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    libboost-system-dev \
    libboost-serialization-dev \
    libboost-filesystem-dev \
    libjpeg-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# ─── 3. Set working directory ─────────────────────────────────────────────────
WORKDIR /app

# ─── 4. Copy and install Python dependencies ──────────────────────────────────
COPY requirements.txt /app/

# Force pip to use binary wheels (avoid compiling from source)
RUN pip install --upgrade pip \
    && pip install --only-binary :all: dlib \
    && pip install --no-cache-dir -r requirements.txt

# ─── 5. Copy application code ─────────────────────────────────────────────────
COPY . /app

# ─── 6. Expose port for Uvicorn ───────────────────────────────────────────────
EXPOSE 8000

# ─── 7. Run FastAPI app using Uvicorn ─────────────────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
