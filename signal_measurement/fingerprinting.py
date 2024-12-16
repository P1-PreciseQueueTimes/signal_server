import os
import json
from misc_elements import FINGERPRINT_DB
from classes import Receiver 

def init_fingerprint_db():
    """
    Checks if fingerprint file exists. 
    Only creates file if it does not exist to avoid overriding existing data
    """
    if not os.path.exists(FINGERPRINT_DB):
        with open(FINGERPRINT_DB, "w") as f:
            f.write("[]")
        print("Fingerprint database initialized.")

def save_fingerprint(location,RECEIVERS:list[Receiver],mac_adress):
    """Save RSSI fingerprints for calibration."""
    out_str = ""
    #Opens database as read+write.
    with open(FINGERPRINT_DB,"w+") as f:
        file_json = json.load(f)
        location_exists = False 
        #Checks if location already exists in database. If so, append signal 
        for data_index in range(len(file_json)):
            if file_json[data_index]["location"][0] == location[0] and file_json[data_index]["location"][1] == location[1]:
                for receiver in RECEIVERS:
                    #IF host name of receivers already in location then append. If not create new key with value of rssi.
                    if  receiver.host_name in file_json[data_index]["rssi_values"].keys():
                        file_json[data_index]["rssi_values"][receiver.host_name].append(receiver.GetRSSIMac(mac_adress))
                    else:
                        file_json[data_index]["rssi_values"][receiver.host_name] = [receiver.GetRSSIMac(mac_adress)]
                location_exists = True

        #If the location does not exist in database, then create new data point with host name.
        if not location_exists:
            data_out = {
                "location": location,
                "rssi_values": {receiver.host_name: [receiver.GetRSSIMac(mac_adress)] for receiver in RECEIVERS} 
            }
            file_json.append(data_out)
        out_str = json.dumps(file_json)
        f.write(out_str)
    print(f"Fingerprint saved for location {location}.")

def match_fingerprint(RECEIVERS:list[Receiver],mac_adress):
    """Match live RSSI to fingerprints."""
    with open(FINGERPRINT_DB,"r+") as f:
        fingerprints = json.load(f)
        best_match = None
        min_error = float("inf")
        #Calculates the mean squared error for each locaton, and picks the location where the error is the smallst.
        for fingerprint in fingerprints:
            rssi_values = fingerprint["rssi_values"]
            sum_mean = sum([(abs(receiver.GetRSSIMac(mac_adress)) -  abs(sum(rssi_values[receiver.host_name]))/len(rssi_values[receiver.host_name]))**2 for receiver in RECEIVERS])
            error = sum_mean/len(RECEIVERS)
            if error < min_error:
                min_error = error
                best_match = fingerprint["location"]
        return best_match
