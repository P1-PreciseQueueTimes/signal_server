from get_handlers import handleIndex
from flask import Flask, json,request
from flask_socketio import SocketIO
from signal_measurement import init_fingerprint_db
from websocket_handlers import handleConnection,handleManualScan,handleAutomaticScan
from post_handlers import handleSender,handleReceiver,handleStartupSender,handleStartupReceiver
import misc_elements


init_fingerprint_db()

will_list = ["asbjorn","william","martin","josephine","MUSHIN"]

will_req_num = 0

import os


static_path = os.getcwd() + "/static"
static_url = ""

template_path = os.getcwd() + "/templates"

APP = Flask(__name__,template_folder=template_path,static_folder=static_path,static_url_path=static_url)

APP.add_url_rule("/","handleIndex",handleIndex,methods=["GET"])

APP.add_url_rule("/post/testing/sender","handleSender",handleSender,methods=["POST"])

APP.add_url_rule("/post/testing/receiver","handleReceiver",handleReceiver,methods=["POST"])

APP.add_url_rule("/post/testing/receiver/start","handleStartupReceiver",handleStartupReceiver,methods=["POST"])

APP.add_url_rule("/post/testing/sender/start","handleStartupSender",handleStartupSender,methods=["POST"])

@APP.route("/get/testing/get_rides", methods=["GET"])  
def GetRides():
    out_obj = {"chosen_ride":misc_elements.chosen_ride,"rides":[ride.name for ride in misc_elements.rides]}
    return json.dumps(out_obj) 

@APP.route("/post/testing/ride", methods=["POST"])  
def PostRide():
    request_data = request.get_json()
    chosen_ride = request_data["value"]
    print(chosen_ride)
    misc_elements.chosen_ride = chosen_ride
    return ""

@APP.route("/post/testing/reset_receivers", methods=["GET"])  
def ResetReceivers():
    misc_elements.RECEIVERS = {}
    print("Reset receivers")
    return ""

@APP.route("/post/testing/calibrate", methods=["GET"])  
def ToggleCalibrate():
    misc_elements.CALIBRATION_MODE = not misc_elements.CALIBRATION_MODE
    print(f"Set calibrate to {misc_elements.CALIBRATION_MODE}")
    return json.dumps({"mode":misc_elements.CALIBRATION_MODE}) 

@APP.route("/get/testing/esp32",methods=["GET"])
def handle_esp32_test():
    chosen_ride = None 

    for ride in misc_elements.rides:
        if ride.name == misc_elements.chosen_ride:
            chosen_ride = ride

    if not chosen_ride:
        return "0"


    queue_time = chosen_ride.calculate_queue_time(misc_elements.People_In_Area)

    return f"{queue_time}"

socketio = SocketIO(APP)
	

socketio.on_event("connect",handleConnection)

socketio.on_event("make manual scan",handleManualScan)

socketio.on_event("make automatic scan",handleAutomaticScan)


if __name__ == "__main__":
	socketio.run(APP)
