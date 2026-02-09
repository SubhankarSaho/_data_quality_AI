import hashlib
import pandas as pd
from datetime import date
from sqlalchemy import text
from db import engine
from config import LEARNING_DAYS

def metric_id_from_sql(sql: str) -> str:
    return hashlib.md5(sql.encode()).hexdigest()

def register_metric(metric_id: str, sql: str):
    with engine.begin() as conn:
        conn.execute(text("""
        INSERT OR IGNORE INTO metrics_registry
        (metric_id, metric_sql, status, first_seen)
        VALUES (:id, :sql, 'learning', :dt)
        """), {
            "id": metric_id,
            "sql": sql,
            "dt": date.today()
        })

def execute_metric(sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, engine)

def append_history(metric_id, df, mode="monitor"):
    """
    mode = 'baseline'  → append all rows (build variance)
    mode = 'monitor'   → append only latest row
    """

    if mode == "baseline":
        rows = df.copy()
    else:
        rows = df.sort_values("date").iloc[-1:].copy()

    rows["metric_id"] = metric_id

    rows[["metric_id", "date", "value"]].to_sql(
        "metric_history",
        engine,
        if_exists="append",
        index=False
    )




def update_metric_status(metric_id: str):
    count = pd.read_sql(
        f"""
        SELECT COUNT(*) AS c
        FROM metric_history
        WHERE metric_id = '{metric_id}'
        """,
        engine
    )["c"][0]

    if count >= LEARNING_DAYS:
        with engine.begin() as conn:
            conn.execute(text("""
            UPDATE metrics_registry
            SET status = 'active'
            WHERE metric_id = :id
            """), {"id": metric_id})
