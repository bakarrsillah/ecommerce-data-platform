import os
from sqlalchemy import create_engine

def get_engine():
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not set")

    # Force SSL for Render
    if "sslmode" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"

    return create_engine(DATABASE_URL)
