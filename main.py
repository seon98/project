"""Thin launcher for running the FastAPI app.
Run:
    uv run uvicorn app.main:app --reload
"""
from app.main import app  # noqa: F401
