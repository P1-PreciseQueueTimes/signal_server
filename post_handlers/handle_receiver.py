import json
from time import time

from flask import request
from flask_socketio import emit

import misc_elements
import signal_measurement
from classes.receiver import Signal
import os


def handleReceiver():
    current_time = time()
    request_data = request.get_json()

    host_name = request_data["host_name"]
    signal_strength = int(request_data["signal_strength"])
    mac_adress = request_data["mac_adress"]

    new_signal = Signal(rssi=signal_strength,time_received=current_time,mac_adress=mac_adress)

    this_receiver = [receiver for receiver in misc_elements.RECEIVERS if receiver.host_name == host_name][0]

    this_receiver.ReceivedSignal(new_signal)

    this_receiver.UpdateSignals(countdown=30)

    distance = signal_measurement.calc_distance_reg(signal_strength)

    print("Host Name: {}\nMac adress: {}\nSignal Strength db:{}\nDistance: {}\n".format(
        host_name,mac_adress, signal_strength,  distance
    ))

    misc_elements.People_In_Area = 0

    people_outside_area = 0

    people_locations = [] 

    max_distance_from_center_cm = 850 + 1000


    for signal in this_receiver.signals:
        all_receivers_has_mac = True

        print([i.HasMac(signal.mac_adress) for i in misc_elements.RECEIVERS])

        for receiver in misc_elements.RECEIVERS:
            if not receiver.HasMac(signal.mac_adress):
                all_receivers_has_mac = False 
                break

        if all_receivers_has_mac:
            print(f"Calculating for mac: {signal.mac_adress}\n")

            distances = [signal_measurement.calc_distance_reg(receiver.GetRSSIMac(signal.mac_adress).rssi) for receiver in misc_elements.RECEIVERS] 
            locations = [receiver.cordinates for receiver in misc_elements.RECEIVERS]

            mac_cordinates = signal_measurement.lns(locations,distances)
            people_locations.append(mac_cordinates)

            [x_cord,y_cord] = mac_cordinates

            print(f"Mac: {signal.mac_adress}\nLocation: ({x_cord}, {y_cord})\n")

            center_x = misc_elements.CENTER[0]
            center_y = misc_elements.CENTER[1]

            distance_from_center = ((center_x - x_cord)**2 + (center_y - y_cord)**2)**0.5

            if distance_from_center < max_distance_from_center_cm:
                misc_elements.People_In_Area += 1
            else:
                people_outside_area += 1
    if not os.path.exists("test.csv"):
        with open("test.csv","w") as file:
            file.write("in_area, outside_area\n")
    if os.path.exists("test.csv"):
        with open("test.csv","a") as file:
            file.write(f"{misc_elements.People_In_Area}, people_outside_area\n")

    print(f"People in area: {misc_elements.People_In_Area}")

    print(f"People outside area: {people_outside_area}")


    out_obj = {"host_name": host_name, "distance": distance,"people":misc_elements.People_In_Area,"people_locations":people_locations}
    out_obj_str = json.dumps(out_obj)
    emit("reception", out_obj_str, broadcast=True, namespace="/")

    return ""
