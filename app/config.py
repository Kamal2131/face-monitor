# app/config.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI()

# Mount static files (e.g., CSS, JS, uploads)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Template engine using Jinja2
templates = Jinja2Templates(directory="app/templates")

# Optional: Add CORS middleware (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only. Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
