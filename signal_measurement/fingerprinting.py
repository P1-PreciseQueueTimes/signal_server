import os
import json
from misc_elements import FINGERPRINT_DB

def init_fingerprint_db():
    if not os.path.exists(FINGERPRINT_DB):
        with open(FINGERPRINT_DB, "w") as f:
            f.write("[]")
        print("Fingerprint database initialized.")

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
    with open(FINGERPRINT_DB,"r+") as f:
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
