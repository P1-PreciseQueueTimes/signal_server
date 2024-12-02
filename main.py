from get_handlers import handleIndex
from flask import Flask, request
from flask_socketio import SocketIO
from post_handlers.handle_receiver import init_fingerprint_db
from websocket_handlers import handleConnection,handleManualScan,handleAutomaticScan
from post_handlers import handleSender,handleReceiver,handleStartupSender,handleStartupReceiver

init_fingerprint_db()

will_list = ["asbjorn","william","martin","josephine","MUSHIN"]

will_req_num = 0

import os

template_path = os.getcwd() + "/templates"
APP = Flask(__name__,template_folder=template_path)

APP.add_url_rule("/","handleIndex",handleIndex,methods=["GET"])

APP.add_url_rule("/post/testing/sender","handleSender",handleSender,methods=["POST"])

APP.add_url_rule("/post/testing/receiver","handleReceiver",handleReceiver,methods=["POST"])

APP.add_url_rule("/post/testing/receiver/start","handleStartupReceiver",handleStartupReceiver,methods=["POST"])

APP.add_url_rule("/post/testing/sender/start","handleStartupSender",handleStartupSender,methods=["POST"])

@APP.route("/post/testing/receiver/calibrate", methods=["POST"])  
def ToggleCalibrate():
    global CALIBRATION_MODE
    request_data = request.get_json()
    mode = request_data.get("mode", "off").lower()
    if mode == "on":
        CALIBRATION_MODE = True
        print("Calibration mode activated.")
    elif mode == "off":
        CALIBRATION_MODE = False
        print("Calibration mode deactivated.")
    else:
        return "Invalid mode. Use 'on' or 'off'.", 400
    return f"Calibration mode set to {mode}."

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


if __name__ == "__main__":
	socketio.run(APP)
