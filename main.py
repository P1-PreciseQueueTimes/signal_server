from get_handlers import handleIndex
from post_handlers import handleSender,handleReceiver,handleStartupSender,handleStartupReceiver

from flask import Flask
from flask_socketio import SocketIO

from websocket_handlers import handleConnection,handleManualScan,handleAutomaticScan

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


if __name__ == "__main__":
	socketio.run(APP)
