import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus

def get_engine():
    user = os.getenv("DB_USER")
    password = quote_plus(os.getenv("DB_PASSWORD"))
    host = os.getenv("DB_HOST")
    db = os.getenv("DB_NAME")

    engine = create_engine(
        f"mysql+mysqlconnector://{user}:{password}@{host}/{db}"
    )

    return engine
