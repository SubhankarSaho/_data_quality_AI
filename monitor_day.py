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
# 2. Load NEW DAY data (this is Day N+1)
# ------------------------------------------------
sql_file = open("sample_data.sql").read()
statements = [s.strip() for s in sql_file.split(";") if s.strip()]

with engine.begin() as conn:
    for stmt in statements:
        conn.exec_driver_sql(stmt)

print("📅 Loaded new day data")

# ------------------------------------------------
# 3. Execute metric (ONE data point only)
# ------------------------------------------------
metric_sql = open("metrics.sql").read()
metric_id = metric_id_from_sql(metric_sql)

df = execute_metric(metric_sql)

# 🔑 MONITOR MODE → append ONLY latest date
append_history(metric_id, df, mode="monitor")

# ------------------------------------------------
# 4. Load history (exclude current point)
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

history_values = history_df["value"].iloc[:-1]
current_value = history_df["value"].iloc[-1]

# ------------------------------------------------
# 5. HARD DEBUG (leave this while learning)
# ------------------------------------------------
print("---- DEBUG START ----")
print("HISTORY VALUES:", list(history_values))
print("CURRENT VALUE:", current_value)
print("HISTORY MEAN:", history_values.mean())
print("HISTORY STD:", history_values.std())
print("HISTORY LENGTH:", len(history_values))
print("---- DEBUG END ----")

# ------------------------------------------------
# 6. Detect anomaly
# ------------------------------------------------
is_anomaly, z = detect_anomaly(history_values, current_value)
trust = calculate_trust_score(is_anomaly)

print(f"Trust Score: {trust}")

# ------------------------------------------------
# 7. Explain if anomaly
# ------------------------------------------------
if is_anomaly:
    result = root_cause_graph.invoke({
        "metric": metric_id,
        "value": current_value,
        "z_score": z,
        "pipeline_ok": True
    })
    print("\n🚨 ALERT")
    print(result["explanation"])
else:
    print("✅ Metric within normal range")
