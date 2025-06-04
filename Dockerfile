# Use an official Python base image with Debian (slim variant)
FROM python:3.10-slim-buster

# ─── 1. Install system‐level dependencies ─────────────────────────────────────
# These are needed to build and run `dlib`, OpenCV, and Pillow.
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

# ─── 2. Set working directory ─────────────────────────────────────────────────
WORKDIR /app

# ─── 3. Copy requirements.txt and install Python dependencies ────────────────
# Using requirements.txt ensures only needed libs get installed.
COPY requirements.txt /app/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ─── 4. Copy entire application code into container ───────────────────────────
# Assumes the following structure at the project root:
# .
# ├── app/
# │   ├── main.py
# │   ├── models.py
# │   ├── database.py
# │   ├── auth.py
# │   ├── templates/
# │   └── static/
# ├── requirements.txt
# ├── current_user.txt
# └── ...
COPY . /app

# ─── 5. Expose port 8000 for Uvicorn ──────────────────────────────────────────
EXPOSE 8000

# ─── 6. Start the Uvicorn server ─────────────────────────────────────────────
# - host 0.0.0.0 makes it listen on all interfaces inside the container.
# - reload is optional: remove `--reload` for production.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
