
from flask_socketio import emit
import misc_elements
import json


"""
Handles for making the sender send out probe requests.
"""

def handleManualScan(msg):
    """
    Handles the manual scan.
    """
    print(msg)

    json_data = json.loads(msg)

    misc_elements.Test_x = int(json_data["x"])

    misc_elements.Test_y = int(json_data["y"])

    print("made manual scan")

    emit("manual scan","lol",broadcast=True)

def handleAutomaticScan(msg):
    """
    Handles the automatic scan.
    """
    print(msg)

    json_data = json.loads(msg)

    misc_elements.Test_x = int(json_data["x"])

    misc_elements.Test_y = int(json_data["y"])

    print("made automatic scan")

    emit("automatic scan","lol",broadcast=True)
