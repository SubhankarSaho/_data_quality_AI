# build_baseline.py

from db import init_db, engine
from metric_engine import (
    metric_id_from_sql,
    register_metric,
    execute_metric,
    append_history,
    update_metric_status
)

# 1. Init DB
init_db()

# 2. HARD RESET (BASELINE ONLY)
with engine.begin() as conn:
    conn.exec_driver_sql("DELETE FROM metric_history")
    conn.exec_driver_sql("DELETE FROM metrics_registry")
    conn.exec_driver_sql("DELETE FROM orders")

print("🧹 Database reset complete")

# 3. Load NORMAL baseline data
sql_file = open("sample_data.sql").read()
statements = [s.strip() for s in sql_file.split(";") if s.strip()]

with engine.begin() as conn:
    for stmt in statements:
        conn.exec_driver_sql(stmt)

# 4. Register metric
metric_sql = open("metrics.sql").read()
metric_id = metric_id_from_sql(metric_sql)
register_metric(metric_id, metric_sql)

# 5. Build baseline
# for _ in range(7):
#     df = execute_metric(metric_sql)
#     append_history(metric_id, df)

df = execute_metric(metric_sql)
append_history(metric_id, df, mode="baseline")
update_metric_status(metric_id)


# 6. Activate metric
update_metric_status(metric_id)

print("✅ Baseline built successfully")
