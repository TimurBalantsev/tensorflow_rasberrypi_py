import threading
from flask import Flask, render_template, request, redirect, url_for
from time import sleep
import datetime

import readings
import sms
import MatrixLEDgpiozero
import keypad
import lobePredictionsCV2

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

distance_threshhold = 0.1
distance_subject = "Something too close"
armee_subject = "Someone is armed"
is_connected = False
password = "1234"

def keyPadLoop():
    global is_connected
    print("please enter password")
    while not password == keypad.current_chain:
        keypad.checkLines()
        sleep(0.2)
    is_connected = True
    print("You are logged in please refresh the page")


t = threading.Thread(target=keyPadLoop)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route("/", methods=["GET", "POST"])
def page_principale():
    global password
    global is_connected
    global distance_subject
    global armee_subject
    global distance_threshhold
    if is_connected:
        if request.method == "POST":
            message = request.form["message"]
            print(message)
            x = threading.Thread(target=MatrixLEDgpiozero.displayMessage,args=(message,))
            x.start()
            
        prediction = lobePredictionsCV2.take_capture()
        if prediction.etiquette == "Armee":
            curr_time = datetime.datetime.now().strftime('%d %b %Y %H:%M:%S')
            content = f"detection de quelqun armee le {curr_time}"
            sms.send_email(armee_subject,content)
        curr_time = datetime.datetime.now().strftime('%d %b %Y %H:%M:%S')
        curr_distance = readings.get_distance()
        curr_temp = readings.get_temperature()
        curr_hum = readings.get_humidity()
        if curr_hum == None:
            curr_hum = -1
        if curr_temp == None:
            curr_temp = -1
        if curr_distance <= distance_threshhold:
            formated_dis = "{:.2f}".format(curr_distance)
            content = f"Sensor detected something {formated_dis}m away from it on {curr_time}"
            # s = threading.Thread(target=sms.send_email, args=(distance_subject, content,))
            # s.start()
            sms.send_email(distance_subject, content)
        
        return render_template(
            "page_principale.html",
            current_time=curr_time,
            temp="{:.1f} C".format(curr_temp),
            hum="{:.1f} %".format(curr_hum),
            distance="{:.2f} m".format(curr_distance),
            sms_reason=sms.dernier_sms.reason,
            sms_time=sms.dernier_sms.time,
            etiquette=prediction.etiquette,
            confidence="{:.2f}".format(prediction.confidence*100),
            img=prediction.file[1:]
            )
    else:
        if request.method == "POST":
            given_password = request.form["password"]
            if password == given_password:
                is_connected = True
                return redirect(url_for('page_principale'))
            

        if not t.is_alive():
            t.start()

        return render_template(
            "connexion.html"
        )

