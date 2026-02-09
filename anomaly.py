# import numpy as np
# from config import Z_THRESHOLD

# def detect_anomaly(history_values, current_value):
#     if len(history_values) < 3:
#         return False, 0.0

#     mean = history_values.mean()
#     std = history_values.std()

#     if std == 0:
#         return False, 0.0

#     z_score = (current_value - mean) / std
#     return abs(z_score) > Z_THRESHOLD, z_score


from config import Z_THRESHOLD

def detect_anomaly(history_values, current_value):
    mean = history_values.mean()
    std = history_values.std()

    print("ANOMALY DEBUG → mean:", mean, "std:", std)

    if std == 0 or len(history_values) < 3:
        print("ANOMALY DEBUG → Returning False (std==0 or too few points)")
        return False, 0

    z = (current_value - mean) / std
    print("ANOMALY DEBUG → z-score:", z, "threshold:", Z_THRESHOLD)

    return abs(z) > Z_THRESHOLD, z
