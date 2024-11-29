from get_handlers import handleIndex
from post_handlers import handleSender,handleReceiver,handleStartupSender,handleStartupReceiver

from flask import Flask
from flask_socketio import SocketIO

from websocket_handlers import handleConnection,handleManualScan,handleAutomaticScan

will_list = ["asbjorn","william","martin","josephine","MUSHIN"]

will_req_num = 0

import os
import numpy as np
import trilateration2 as trl

template_path = os.getcwd() + "/templates"
APP = Flask(__name__,template_folder=template_path)

APP.add_url_rule("/","handleIndex",handleIndex,methods=["GET"])

APP.add_url_rule("/post/testing/sender","handleSender",handleSender,methods=["POST"])

APP.add_url_rule("/post/testing/receiver","handleReceiver",handleReceiver,methods=["POST"])

APP.add_url_rule("/post/testing/receiver","handleReceiver",handleReceiver,methods=["POST"])

APP.add_url_rule("/post/testing/receiver/start","handleStartupReceiver",handleStartupReceiver,methods=["POST"])

APP.add_url_rule("/post/testing/sender/start","handleStartupSender",handleStartupSender,methods=["POST"])

@APP.route("/get/testing/esp32",methods=["GET"])
def handle_esp32_test():
    global will_req_num,will_list
    will_req_num += 1
    will_req_num = will_req_num % len(will_list)

    return will_list[will_req_num] 

socketio = SocketIO(APP)
	

socketio.on_event("connect",handleConnection)

socketio.on_event("make manual scan",handleManualScan)

socketio.on_event("make automatic scan",handleAutomaticScan)

def handle_trilateration():
    import json
    from flask import request
    
    # Parse incoming data (assume it's JSON with RSSI and transmitter details)
    data = request.get_json()
    if not data or 'sniffers' not in data or 'tx_power' not in data:
        return {"error": "Invalid input"}, 400

    tx_power = data['tx_power']
    sniffers = data['sniffers']  # Each sniffer should have x, y, rssi

    # Calculate distances for each sniffer
    A = np.empty(len(sniffers), 3) # Define matrix with sniffer values in each row
    for sniffer in range(len(sniffers)):
        distance = trl.CalculateDistance(sniffer['rssi'], tx_power)
        A[sniffer, :] = [sniffers[sniffer]["x"], sniffers[sniffer]["y"], distance]

    # Perform trilateration
    if len(A) < 3:
        return {"error": "At least three sniffers are required"}, 400

    try:
        x, y = trl.LSM_solve(A)
        return {"x": x, "y": y}
    except Exception as e:
        return {"error": str(e)}, 500
    
S = np.random.rand(3,2)
trl.trilaterate(S)


if __name__ == "__main__":
	socketio.run(APP)
