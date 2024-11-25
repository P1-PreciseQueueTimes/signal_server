from flask import Flask, request,render_template
import time

app = Flask(__name__)

sent_time = 0

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/get/testing/time",methods=["GET"])
def get_time(): 

    return str(round(time.time()))

@app.route("/post/testing/receiver_start",methods=["POST"])
def post_receiver_start(): 
    global sent_time
    request_data = request.get_json()

    host_name = request_data["host_name"]

    connected = request_data["connected"]

    print("Stat connection\nHost name: {}\nConnected {}\n".format(host_name,connected))

    return ""

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
    global sent_time
    request_data = request.get_json()

    host_name = request_data["host_name"]

    pie_time = request_data["internal_time"]
    diff_time = (pie_time - sent_time) / 1000000
    print()
    print("Host Name: {}\nPie Time: {}\nDiff Time ms: {}\n".format(host_name,pie_time,diff_time))

    return "" 


if __name__ == "__main__":
    app.run()
