
from flask import request

def handleSender(): 
    global sent_time
    request_data = request.get_json()

    request_number = request_data["request_number"]

    pie_time = request_data["internal_time"]
    sent_time = pie_time
    print()

    print("Sent signal\nReq num: {}\nTime: {}".format(request_number,pie_time))

    return ""
