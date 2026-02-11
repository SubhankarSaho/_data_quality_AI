import pandas as pd
from db import init_db, engine
from metric_engine import (
    metric_id_from_sql,
    execute_metric,
    append_history,
)
from anomaly import detect_anomaly
from trust import calculate_trust_score
from decision_graph import root_cause_graph

# ------------------------------------------------
# 1. Initialize DB (NO RESETS HERE)
# ------------------------------------------------
init_db()

# ------------------------------------------------
# 2. Load NEW DAY insurance data (Day N+1)
# ------------------------------------------------
sql_file = open("sample_data.sql").read()
statements = [s.strip() for s in sql_file.split(";") if s.strip()]

with engine.begin() as conn:
    for stmt in statements:
        conn.exec_driver_sql(stmt)

print("📅 Loaded new insurance data")

# ------------------------------------------------
# 3. Insurance Metrics to Monitor
# ------------------------------------------------
metric_files = {
    "Daily Claim Amount": "metrics/daily_claim_amount.sql",
    "Claim Approval Rate": "metrics/approval_rate.sql",
    "Avg Processing Time": "metrics/avg_processing_time.sql",
    "Avg Claim Amount": "metrics/avg_claim_amount.sql"
}

# ------------------------------------------------
# 4. Run Monitoring for EACH metric
# ------------------------------------------------
for metric_name, metric_path in metric_files.items():

    print(f"\n📊 Monitoring Metric: {metric_name}")

    metric_sql = open(metric_path).read()
    metric_id = metric_id_from_sql(metric_sql)

    # Execute metric query
    df = execute_metric(metric_sql)

    # Append only latest day (monitor mode)
    append_history(metric_id, df, mode="monitor")

    # ------------------------------------------------
    # 5. Load historical values
    # ------------------------------------------------
    history_df = pd.read_sql(
        f"""
        SELECT date, value
        FROM metric_history
        WHERE metric_id = '{metric_id}'
        ORDER BY date
        """,
        engine
    )

    if len(history_df) < 4:
        print("⚠️ Not enough history yet, skipping anomaly detection")
        continue

    history_values = history_df["value"].iloc[:-1]
    current_value = history_df["value"].iloc[-1]

    # ------------------------------------------------
    # 6. Debug (keep during demos)
    # ------------------------------------------------
    print("---- DEBUG ----")
    print("History:", list(history_values))
    print("Current:", current_value)
    print("Mean:", history_values.mean())
    print("Std :", history_values.std())
    print("--------------")

    # ------------------------------------------------
    # 7. Detect anomaly
    # ------------------------------------------------
    is_anomaly, z = detect_anomaly(history_values, current_value)
    trust = calculate_trust_score(is_anomaly)

    print(f"Trust Score: {trust}")

    # ------------------------------------------------
    # 8. AI Explanation if anomaly
    # ------------------------------------------------
    if is_anomaly:
        result = root_cause_graph.invoke({
            "metric": metric_name,
            "value": current_value,
            "z_score": z,
            "pipeline_ok": True
        })
        print("🚨 ALERT")
        print(result["explanation"])
    else:
        print("✅ Metric within normal range")
