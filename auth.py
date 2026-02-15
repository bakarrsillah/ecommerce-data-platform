import hashlib
from sqlalchemy import text
from db import get_engine

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    engine = get_engine()
    hashed = hash_password(password)

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT user_id, username, role 
                FROM users 
                WHERE username = :username 
                AND password_hash = :password
            """),
            {"username": username, "password": hashed}
        ).fetchone()

    return result
