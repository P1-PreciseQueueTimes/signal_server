from flask import Flask, request
import time

app = Flask(__name__)

sent_time = 0

receivers = {}

test = [1,2,3,4,5]

sum(test)

@app.route("/")
def hello_world():
    return "It is up :)" 

@app.route("/get/calibration/diff_time/<host_name>",methods=["GET"])
def get_time(host_name): 

    difference_in_times = receivers[host_name]

    average_difference = sum(difference_in_times)/len(difference_in_times)

    return str(average_difference) 

@app.route("/post/testing/sender",methods=["POST"])
def post_sender(): 
    global sent_time
    request_data = request.get_json()

    request_number = request_data["request_number"]

    pie_time = request_data["internal_time"]
    sent_time = pie_time
    print()

    print("Sent signal\nReq num: {}\nTime: {}".format(request_number,pie_time))

    return ""

@app.route("/post/testing/receiver",methods=["POST"])
def post_receiver():
    global sent_time, receivers
    request_data = request.get_json()

    host_name = request_data["host_name"]

    pie_time = request_data["internal_time"]

    signal_strength= request_data["signal_strength"]

    diff_time_ns = pie_time - sent_time  

    diff_time_ms = diff_time_ns / 1000000.0

    if host_name in receivers.keys():
        receivers[host_name].append(diff_time_ns)
    else:
        receivers[host_name] = [diff_time_ns]

    print()
    print("Host Name: {}\nPie Time: {}\nDiff Time ms: {}\nSignal Strength db:{}\n".format(host_name,pie_time,diff_time_ms,signal_strength))

    return "" 


if __name__ == "__main__":
    app.run()
