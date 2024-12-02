from flask import request
from misc_elements import SENT_TIME, RECEIVERS
import numpy as np
from flask_socketio import emit
import json

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
    global SENT_TIME, RECEIVERS, KALMAN_FILTERS
    request_data = request.get_json()

    host_name = request_data["host_name"]
    pie_time = request_data["internal_time"]
    signal_strength = int(request_data["signal_strength"])

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
