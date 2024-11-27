from flask import request
from misc_elements import SENT_TIME,RECEIVERS

def handleReceiver():
    global SENT_TIME, RECEIVERS 
    request_data = request.get_json()

    host_name = request_data["host_name"]

    pie_time = request_data["internal_time"]

    signal_strength= request_data["signal_strength"]

    diff_time_ns = pie_time - SENT_TIME 

    diff_time_ms = diff_time_ns / 1000000.0

    if host_name in RECEIVERS.keys():
        RECEIVERS[host_name].append(diff_time_ns)
    else:
        RECEIVERS[host_name] = [diff_time_ns]
    print()
    print("Host Name: {}\nPie Time: {}\nDiff Time ms: {}\nSignal Strength db:{}\n".format(host_name,pie_time,diff_time_ms,signal_strength))

    return "" 
