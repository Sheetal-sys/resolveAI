from sqlalchemy import text

from app.database.db import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))
    print(result.fetchone())