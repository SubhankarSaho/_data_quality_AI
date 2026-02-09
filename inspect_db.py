import pandas as pd
from db import engine

print("\n--- metric_history ---")
print(pd.read_sql(
    "SELECT date, value FROM metric_history ORDER BY date",
    engine
))

print("\n--- metrics_registry ---")
print(pd.read_sql(
    "SELECT metric_id, status FROM metrics_registry",
    engine
))

print("\n--- orders ---")
print(pd.read_sql(
    "SELECT * FROM orders ORDER BY order_date",
    engine
))
