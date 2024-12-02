import json
import os
import numpy as np
from flask import request
from flask_socketio import emit
from scipy.optimize import minimize
from misc_elements import SENT_TIME, RECEIVERS

def init_fingerprint_db():
    if not os.path.exists(FINGERPRINT_DB):
        with open(FINGERPRINT_DB, "w") as f:
            f.write("[]")
        print("Fingerprint database initialized.")
        
# File to store RSSI fingerprints
FINGERPRINT_DB = "fingerprint_db.json"
MODE = "fingerprint"  # Switch between "fingerprint" and "trilateration"

def RSSI_to_distance(rssi, A=-40, n=3):
    return 10 ** ((A - rssi) / (10 * n))

def Calculate_position(RECEIVERS):
    locations = np.array([
        [0, 0],  # P1
        [6, 0],  # P2
        [3, 7]   # P3
    ])
    distances = []
    for key in RECEIVERS:
        avg_signal = sum(RECEIVERS[key]) / len(RECEIVERS[key])
        distances.append(RSSI_to_distance(avg_signal))
    initial_guess = np.mean(locations, axis=0)

    def Mean_Square_Error(x, locations, distances):
        mse = 0.0
        for loc, dist in zip(locations, distances):
            mse += (np.linalg.norm(np.array(x) - np.array(loc)) - dist) ** 2
        return mse / len(distances)

    result = minimize(Mean_Square_Error, initial_guess, args=(locations, distances), method='L-BFGS-B')
    return result.x

def save_fingerprint(location, RECEIVERS):
    """Save RSSI fingerprints for calibration."""
    with open(FINGERPRINT_DB, "a") as f:
        data = {
            "location": location,
            "rssi_values": {k: sum(v) / len(v) for k, v in RECEIVERS.items()}
        }
        f.write(json.dumps(data) + "\n")
    print(f"Fingerprint saved for location {location}.")

def match_fingerprint(RECEIVERS):
    """Match live RSSI to fingerprints."""
    with open(FINGERPRINT_DB, "r") as f:
        fingerprints = [json.loads(line) for line in f]
    best_match = None
    min_error = float("inf")
    for fingerprint in fingerprints:
        rssi_values = fingerprint["rssi_values"]
        error = np.linalg.norm([
            sum(RECEIVERS[k]) / len(RECEIVERS[k]) - rssi_values.get(k, 0) for k in RECEIVERS
        ])
        if error < min_error:
            min_error = error
            best_match = fingerprint["location"]
    return best_match

CALIBRATION_MODE = False  # Global flag for calibration mode

def handleReceiver():
    global SENT_TIME, RECEIVERS, CALIBRATION_MODE
    request_data = request.get_json()

    host_name = request_data["host_name"]
    pie_time = request_data["internal_time"]
    signal_strength = int(request_data["signal_strength"])

    if host_name not in RECEIVERS.keys():
        RECEIVERS[host_name] = [signal_strength]
    else:
        RECEIVERS[host_name].append(signal_strength)

    if len(RECEIVERS) == 3:  # When all sniffers report
        if CALIBRATION_MODE:
            # Save fingerprint during calibration
            location = request_data.get("location")  # Known location in calibration mode
            if not location:
                return "Error: 'location' is required during calibration.", 400
            save_fingerprint(location, RECEIVERS)
            print(f"Calibration data saved for location: {location}")
            RECEIVERS = {}  # Reset for next calibration
        else:
            # Always use fingerprint matching for localization
            estimated_position = match_fingerprint(RECEIVERS)
            if estimated_position:
                print(f"Estimated Position (Fingerprinting): {estimated_position}")
                emit("position_update", {"x": estimated_position[0], "y": estimated_position[1]}, broadcast=True)
            else:
                print("Error: No matching fingerprint found.")
            RECEIVERS = {}  # Reset for next calculation

    return ""


