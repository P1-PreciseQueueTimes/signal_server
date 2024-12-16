import get_handlers
from flask import Flask 
from flask_socketio import SocketIO
from signal_measurement import init_fingerprint_db
import post_handlers
import websocket_handlers
import os

if __name__ == "__main__":

    init_fingerprint_db()

    static_path = os.getcwd() + "/static"
    static_url = ""

    template_path = os.getcwd() + "/templates"

    APP = Flask(__name__,template_folder=template_path,static_folder=static_path,static_url_path=static_url)

    socketio = SocketIO(APP)
    #Setup flask app/http server.

    #Setup different routes for get requests.
    APP.add_url_rule("/","handleIndex",get_handlers.handleIndex,methods=["GET"])
    APP.add_url_rule("/get/testing/get_rides","handleRides",get_handlers.handleRides,methods=["GET"])
    APP.add_url_rule("/get/testing/reset_receivers","handleReset",get_handlers.handleReset,methods=["GET"])
    APP.add_url_rule("/get/testing/esp32","handleESP32",get_handlers.handleESP32,methods=["GET"])
    APP.add_url_rule("/get/testing/calibrate","handleCalibrate",get_handlers.handleCalibrate,methods=["GET"])

    #Setup different routes for post requests.
    APP.add_url_rule("/post/testing/sender","handleSender",post_handlers.handleSender,methods=["POST"])
    APP.add_url_rule("/post/testing/receiver","handleReceiver",post_handlers.handleReceiver,methods=["POST"])
    APP.add_url_rule("/post/testing/receiver/start","handleStartupReceiver",post_handlers.handleStartupReceiver,methods=["POST"])
    APP.add_url_rule("/post/testing/sender/start","handleStartupSender",post_handlers.handleStartupSender,methods=["POST"])
    APP.add_url_rule("/post/testing/ride","handleRide",post_handlers.handleRide,methods=["POST"])

	
    #Setup different event names for websocket.
    socketio.on_event("connect",websocket_handlers.handleConnection)
    socketio.on_event("make manual scan",websocket_handlers.handleManualScan)
    socketio.on_event("make automatic scan",websocket_handlers.handleAutomaticScan)


    socketio.run(APP)
