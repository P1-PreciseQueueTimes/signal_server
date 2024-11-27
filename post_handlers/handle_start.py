
from flask import request

def handleStartupReceiver():
    request_data = request.get_json()

    host_name = request_data["host_name"]

    print("{} is now listening".format(host_name))

    return "" 

def handleStartupSender():
    request_data = request.get_json()

    host_name = request_data["host_name"]

    print("{} is now sending".format(host_name))

    return "" 
