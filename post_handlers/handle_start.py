
from flask import request

def handleStartupReceiver():
    """
    Handles whenever the receiver starts.
    """
    request_data = request.get_json()

    host_name = request_data["host_name"]

    print("{} is now listening".format(host_name))

    return "" 

def handleStartupSender():
    """
    Handles whenever the sender starts.
    """
    request_data = request.get_json()

    host_name = request_data["host_name"]

    print("{} is now sending".format(host_name))

    return "" 
