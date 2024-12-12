import signal_measurement
import misc_elements
import json


def calculate_pie_average(rssi_values,pie):
    return sum(rssi_values[pie])/len(rssi_values[pie])

with open("udud.json","r+") as f:
    fingerprints = json.load(f)

    diff_list_x = []
    diff_list_y = []

    for fingerprints in fingerprints:
        rssi_values = fingerprints["rssi_values"]
        location = fingerprints["location"]

        average_values = [calculate_pie_average(rssi_values,"pie3"), calculate_pie_average(rssi_values,"pie4"),calculate_pie_average(rssi_values,"pie2") ]

        average_distances = [signal_measurement.calc_distance_reg(average_rssi) for average_rssi in average_values]

        trilateration_location = signal_measurement.lns(average_distances)

        diff_x = abs(location[0] - trilateration_location[0])
        diff_y = abs(location[1] - trilateration_location[1])

        diff_list_x.append(diff_x)
        diff_list_y.append(diff_y)

        print(f"Location: ({location[0]}, {location[1]})\nTrilateration: ({trilateration_location[0]}, {trilateration_location[1]})\nDiff: ({diff_x}, {diff_y})\n")

    average_diff_y = sum(diff_list_y)/len(diff_list_y)

    average_diff_x = sum(diff_list_x)/len(diff_list_x)

    print(f"Average diff: ({average_diff_x}, {average_diff_y})")




