from flask import render_template
from web_app import app
import arduino_usb_io
import time

arduino = arduino_usb_io.MyArduino()


@app.route('/')
@app.route('/index')
def index():
    c_temp, f_temp = arduino.get_temp()
    return render_template('index.html', title='RemoteCozy', c_temp=c_temp, f_temp=f_temp)


@app.route('/ON')
def turn_on():
    arduino.send(arduino.commands["Turn on"])
    c_temp, f_temp = arduino.get_temp()
    return render_template('index.html', title='RemoteCozy', c_temp=c_temp, f_temp=f_temp)


@app.route('/OFF')
def turn_off():
    arduino.send(arduino.commands["Turn off"])
    c_temp, f_temp = arduino.get_temp()
    return render_template('index.html', title='RemoteCozy', c_temp=c_temp, f_temp=f_temp)


@app.route('/30MIN')
def timer_30_min():
    arduino.send(arduino.commands["Turn on"])
    time.sleep(30*60)
    arduino.send(arduino.commands["Turn off"])
    c_temp, f_temp = arduino.get_temp()
    return render_template('index.html', title='RemoteCozy', c_temp=c_temp, f_temp=f_temp)

