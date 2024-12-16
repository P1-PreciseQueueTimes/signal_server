
from flask import request

def handleSender(): 
    """
    Handles whenever the sender sends out a signal.
    """
    global sent_time
    request_data = request.get_json()

    request_number = request_data["request_number"]

    pie_time = request_data["internal_time"]
    sent_time = pie_time
    print()

    print("Sent signal\nReq num: {}\nTime: {}".format(request_number,pie_time))

    return ""
