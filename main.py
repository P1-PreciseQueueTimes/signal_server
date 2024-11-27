from get_handlers import handleIndex
from post_handlers import handleSender,handleReceiver,handleStartupSender,handleStartupReceiver

from flask import Flask
from flask_socketio import SocketIO

from websocket_handlers import handleConnection,handleManualScan,handleAutomaticScan

from Trilateration import CalculateDistance, Trilateration

will_list = ["asbjorn","william","martin","josephine","MUSHIN"]

will_req_num = 0

import os

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


@APP.route("/post/trilateration", methods=["POST"])
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
    points = []
    for sniffer in sniffers:
        distance = CalculateDistance(sniffer['rssi'], tx_power)
        points.append({'x': sniffer['x'], 'y': sniffer['y'], 'distance': distance})

    # Perform trilateration
    if len(points) < 3:
        return {"error": "At least three sniffers are required"}, 400

    try:
        x, y = Trilateration(points)
        return {"x": x, "y": y}
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
	socketio.run(APP)
