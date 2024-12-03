from flask import request
from misc_elements import SENT_TIME, RECEIVERS
import numpy as np
from flask_socketio import emit
import json
import os
import numpy as np
from flask import request
from flask_socketio import emit
from scipy.optimize import minimize
from misc_elements import SENT_TIME 

import misc_elements

def init_fingerprint_db():
    if not os.path.exists(FINGERPRINT_DB):
        with open(FINGERPRINT_DB, "w") as f:
            f.write("[]")
        print("Fingerprint database initialized.")

        
# File to store RSSI fingerprints
FINGERPRINT_DB = "fingerprint_db.json"
MODE = "fingerprint"  # Switch between "fingerprint" and "trilateration"

init_fingerprint_db()

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
    out_str = ""
    with open(FINGERPRINT_DB,"r+") as f:
        file_json = json.load(f)

        location_exists = False 
        for data_index in range(len(file_json)):
            if file_json[data_index]["location"][0] == location[0] and file_json[data_index]["location"][1] == location[1]:
                for k,v in RECEIVERS.items():
                    file_json[data_index]["rssi_values"][k].append(v[-1])
                location_exists = True
        if not location_exists:
            data_out = {
                "location": location,
                "rssi_values": {k: [v[-1]] for k, v in RECEIVERS.items()}
            }
            file_json.append(data_out)
        out_str = json.dumps(file_json)
    with open(FINGERPRINT_DB,"w") as f:
        f.write(out_str)
    print(f"Fingerprint saved for location {location}.")

def match_fingerprint(RECEIVERS):
    """Match live RSSI to fingerprints."""
    with open(FINGERPRINT_DB ,"r+") as f:
        fingerprints = json.load(f)
        best_match = None
        min_error = float("inf")
        for fingerprint in fingerprints:
            rssi_values = fingerprint["rssi_values"]
            sum_mean = sum([(abs(RECEIVERS[k][-1]) -  abs(sum(rssi_values[k]))/len(rssi_values[k]))**2 for k in RECEIVERS.keys()])
            error = sum_mean/len(RECEIVERS.keys())
            if error < min_error:
                min_error = error
                best_match = fingerprint["location"]
        return best_match

# Initialize Kalman Filter parameters
F = np.array([[1]])  # State transition model
B = np.array([[0]])  # No control input in this case
H = np.array([[1]])  # Observation model
Q = np.array([[1]])  # Process noise covariance (tune as needed)
R = np.array([[10]]) # Measurement noise covariance (tune as needed)
x0 = np.array([[0]]) # Initial state estimate
P0 = np.array([[1]]) # Initial covariance estimate

# Store Kalman filters for each host
KALMAN_FILTERS = {}

def kalman_predict_update(kf, signal_strength):
    """Perform predict and update for Kalman Filter."""
    # Predict step
    kf['x'] = np.dot(kf['F'], kf['x'])
    kf['P'] = np.dot(np.dot(kf['F'], kf['P']), kf['F'].T) + kf['Q']
    # Update step
    S = np.dot(np.dot(kf['H'], kf['P']), kf['H'].T) + kf['R']
    K = np.dot(np.dot(kf['P'], kf['H'].T), np.linalg.inv(S))
    y = signal_strength - np.dot(kf['H'], kf['x'])
    kf['x'] = kf['x'] + np.dot(K, y)
    I = np.eye(kf['P'].shape[0])
    kf['P'] = np.dot(np.dot(I - np.dot(K, kf['H']), kf['P']),
                     (I - np.dot(K, kf['H'])).T) + np.dot(np.dot(K, kf['R']), K.T)
    return kf['x'][0][0]  # Return updated signal strength

def handleReceiver():
    global SENT_TIME 
    global SENT_TIME, RECEIVERS, KALMAN_FILTERS
    request_data = request.get_json()

    host_name = request_data["host_name"]
    pie_time = request_data["internal_time"]
    signal_strength = int(request_data["signal_strength"])

    signal_strength = int(request_data["signal_strength"])

    if host_name not in misc_elements.RECEIVERS.keys():
        misc_elements.RECEIVERS[host_name] = [signal_strength]

    if len(misc_elements.RECEIVERS) == 3:  # When all sniffers report
        if misc_elements.CALIBRATION_MODE:
            # Save fingerprint during calibration
            location = [misc_elements.Test_x,misc_elements.Test_y] 
            if not location:
                return "Error: 'location' is required during calibration.", 400
            save_fingerprint(location, misc_elements.RECEIVERS)
            print(f"Calibration data saved for location: {location}")
            misc_elements.RECEIVERS = {}  # Reset for next calibration
        else:
            # Always use fingerprint matching for localization
            estimated_position = match_fingerprint(misc_elements.RECEIVERS)
            if estimated_position:
                print(f"Estimated Position (Fingerprinting): {estimated_position}")
                emit("position_update", {"x": estimated_position[0], "y": estimated_position[1]}, broadcast=True,namespace="/")
            else:
                print("Error: No matching fingerprint found.")
            misc_elements.RECEIVERS = {}  # Reset for next calculation

    return ""

    # Initialize Kalman filter for the host if not already present
    if host_name not in KALMAN_FILTERS:
        KALMAN_FILTERS[host_name] = {
            "F": F, "B": B, "H": H, "Q": Q, "R": R, "x": x0.copy(), "P": P0.copy()
        }

    # Apply Kalman filter
    filtered_signal = kalman_predict_update(KALMAN_FILTERS[host_name], signal_strength)

    # Store filtered signal strength
    if host_name not in RECEIVERS.keys():
        RECEIVERS[host_name] = [filtered_signal]
    else:
        RECEIVERS[host_name].append(filtered_signal)

    # Calculate time difference
    diff_time_ns = pie_time - SENT_TIME
    diff_time_ms = diff_time_ns / 1000000.0

    # Compute average signal strength
    average_signal_strength = sum(RECEIVERS[host_name]) / len(RECEIVERS[host_name])

    # Print diagnostic information
    print()
    print("Host Name: {}\nPie Time: {}\nDiff Time ms: {}\nSignal Strength db:{}\nAverage Signal Strength:{}\n".format(
        host_name, pie_time, diff_time_ms, filtered_signal, average_signal_strength
    ))

    # Emit the filtered signal to the clients
    out_obj = {"host_name": host_name, "distance": filtered_signal}
    out_obj_str = json.dumps(out_obj)
    emit("reception", out_obj_str, broadcast=True, namespace="/")

    return ""
