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
    arduino.turn_on()
    c_temp, f_temp = arduino.get_temp()
    return render_template('index.html', title='RemoteCozy', c_temp=c_temp, f_temp=f_temp)


@app.route('/OFF')
def turn_off():
    arduino.turn_off()
    c_temp, f_temp = arduino.get_temp()
    return render_template('index.html', title='RemoteCozy', c_temp=c_temp, f_temp=f_temp)


@app.route('/15MIN')
def timer_15_min():
    arduino.turn_on()
    time.sleep(15*60)
    arduino.turn_off()
    c_temp, f_temp = arduino.get_temp()
    return render_template('index.html', title='RemoteCozy', c_temp=c_temp, f_temp=f_temp)


@app.route('/30MIN')
def timer_30_min():
    arduino.turn_on()
    time.sleep(30*60)
    arduino.turn_off()
    c_temp, f_temp = arduino.get_temp()
    return render_template('index.html', title='RemoteCozy', c_temp=c_temp, f_temp=f_temp)

