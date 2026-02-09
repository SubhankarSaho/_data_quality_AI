from sqlalchemy import create_engine, text
from config import DB_URL

engine = create_engine(DB_URL)

def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS metrics_registry (
            metric_id TEXT PRIMARY KEY,
            metric_sql TEXT NOT NULL,
            status TEXT NOT NULL,
            first_seen DATE NOT NULL
        )
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS metric_history (
            metric_id TEXT NOT NULL,
            date DATE NOT NULL,
            value FLOAT NOT NULL
        )
        """))
