
from get_handlers import handleIndex,handleCalibration
from post_handlers import handleSender,handleReceiver

from flask import Flask
from flask_socketio import SocketIO

import os

template_path = os.getcwd() + "/templates"
APP = Flask(__name__,template_folder=template_path)

APP.add_url_rule("/","handleIndex",handleIndex,methods=["GET"])

APP.add_url_rule("/post/testing/sender","handleSender",handleSender,methods=["POST"])

APP.add_url_rule("/post/testing/receiver","handleReceiver",handleReceiver,methods=["POST"])

APP.add_url_rule("/get/calibration/diff_time/<host_name>","handleCalibration",handleCalibration,methods=["GET"])


socketio = SocketIO(APP)

def handleConnection(data):
	print("Hello World")
	

socketio.on_event("connect",handleConnection)

if __name__ == "__main__":
	socketio.run(APP)
