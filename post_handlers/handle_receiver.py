from time import time
from flask import request
from flask_socketio import emit
import json
from flask import request
from flask_socketio import emit

import misc_elements
import signal_measurement




def handleReceiver():
    request_data = request.get_json()

    host_name = request_data["host_name"]
    pie_time = request_data["internal_time"]
    signal_strength = int(request_data["signal_strength"])
    mac_adress = request_data["mac_adress"]


    if host_name not in misc_elements.RECEIVERS.keys():
        misc_elements.RECEIVERS[host_name] = [signal_strength]
    else:
        misc_elements.RECEIVERS[host_name].append(signal_strength)

    average_signal_strength = sum(misc_elements.RECEIVERS[host_name]) / len(misc_elements.RECEIVERS[host_name])

    distance = signal_measurement.calc_distance_reg(signal_strength)

    print("Host Name: {}\nMac adress: {}\nPie Time: {}\nSignal Strength db:{}\nAverage Signal Strength:{}\nDistance: {}\n".format(
        host_name,mac_adress, pie_time,signal_strength,  average_signal_strength,distance
    ))


    if len(misc_elements.RECEIVERS) == 3:  # When all sniffers report

        trilateration_location = signal_measurement.lns([signal_measurement.calc_distance_reg(misc_elements.RECEIVERS[i][-1]) for i in misc_elements.RECEIVERS.keys()])
        misc_elements.Tri_x_diff.append(misc_elements.Test_x - trilateration_location[0])

        misc_elements.Tri_y_diff.append(misc_elements.Test_y - trilateration_location[1])

        print(f"Trilateration cordinates: ({trilateration_location[0],trilateration_location[1]})\nAverage difference: ({sum(misc_elements.Tri_x_diff)/len(misc_elements.Tri_x_diff)},{sum(misc_elements.Tri_y_diff)/len(misc_elements.Tri_y_diff)})\n")

        if misc_elements.CALIBRATION_MODE:
            # Save fingerprint during calibration
            location = [misc_elements.Test_x,misc_elements.Test_y] 
            if not location:
                return "Error: 'location' is required during calibration.", 400
            signal_measurement.save_fingerprint(location, misc_elements.RECEIVERS)
            print(f"Calibration data saved for location: {location}")
            misc_elements.RECEIVERS = {}  # Reset for next calibration

        else:
            # Always use fingerprint matching for localization
            estimated_position = signal_measurement.match_fingerprint(misc_elements.RECEIVERS)
            if estimated_position:
                print(f"Estimated Position (Fingerprinting): {estimated_position}")
                emit("position_update", {"x": estimated_position[0], "y": estimated_position[1]}, broadcast=True,namespace="/")
            else:
                print("Error: No matching fingerprint found.")


    # Emit the filtered signal to the clients
    out_obj = {"host_name": host_name, "distance": distance}
    out_obj_str = json.dumps(out_obj)
    emit("reception", out_obj_str, broadcast=True, namespace="/")

    return ""
