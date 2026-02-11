from db import init_db, engine
from metric_engine import (
    metric_id_from_sql,
    execute_metric,
    append_history,
    update_metric_status
)

# ------------------------------------------------
# 1. Initialize DB
# ------------------------------------------------
init_db()

# ------------------------------------------------
# 2. RESET HISTORY (BASELINE ONLY)
# ------------------------------------------------
with engine.begin() as conn:
    conn.exec_driver_sql("DELETE FROM metric_history")
    conn.exec_driver_sql("DELETE FROM metrics_registry")

print("🧹 Cleared old metric history")

# ------------------------------------------------
# 3. Load NORMAL insurance data (baseline period)
# ------------------------------------------------
sql_file = open("sample_data.sql").read()
statements = [s.strip() for s in sql_file.split(";") if s.strip()]

with engine.begin() as conn:
    for stmt in statements:
        conn.exec_driver_sql(stmt)

print("📊 Loaded baseline insurance data")

# ------------------------------------------------
# 4. Insurance metrics
# ------------------------------------------------
metric_files = [
    "metrics/daily_claim_amount.sql",
    "metrics/approval_rate.sql",
    "metrics/avg_processing_time.sql",
    "metrics/avg_claim_amount.sql"
]

# ------------------------------------------------
# 5. Build baseline (IMPORTANT PART)
# ------------------------------------------------
for metric_path in metric_files:
    metric_sql = open(metric_path).read()
    metric_id = metric_id_from_sql(metric_sql)

    df = execute_metric(metric_sql)

    # 🔑 BASELINE MODE → append ALL historical rows
    append_history(metric_id, df, mode="baseline")

    update_metric_status(metric_id)

    print(f"✅ Baseline built for {metric_path}")

print("\n🎉 Insurance baseline setup complete")
