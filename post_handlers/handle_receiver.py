from flask import request
from misc_elements import SENT_TIME,RECEIVERS

from flask_socketio import emit

import json

#Test Function
def rssi_to_distance(rssi, A = -40, n = 3):
    #Basic Path Loss Model
    return 10**((A - rssi) / (10 * n))


def handleReceiver():
    global SENT_TIME, RECEIVERS 
    request_data = request.get_json()

    host_name = request_data["host_name"]

    pie_time = request_data["internal_time"]

    signal_strength= request_data["signal_strength"]

    signal_strength = int(signal_strength)

    if host_name not in RECEIVERS.keys():
        RECEIVERS[host_name] = [signal_strength]
    else:
        RECEIVERS[host_name].append(signal_strength)

    diff_time_ns = pie_time - SENT_TIME 

    diff_time_ms = diff_time_ns / 1000000.0

    average_signal_strength = sum(RECEIVERS[host_name])/len(RECEIVERS[host_name])

    #Test again
    distance = rssi_to_distance(average_signal_strength)

    print()
    print("Host Name: {}\nPie Time: {}\nDiff Time ms: {}\nSignal Strength db:{}\nAverage Signal Strength:{}\nCalibrated Distance{}\n".format(host_name,pie_time,diff_time_ms,signal_strength,average_signal_strength,distance))

    out_obj = {"host_name":host_name,"distance":distance}

    out_obj_str = json.dumps(out_obj)

    emit("reception",out_obj_str,broadcast=True,namespace="/")

    return "" 
