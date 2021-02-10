import sys
import arduino_usb_io
from collections import deque
import threading
from flask import Flask, render_template
import time


job_queue = deque([])
arduino = arduino_usb_io.MyArduino()
status = 'OFF'


def check_job_queue():
    global job_queue, status
    while True:
        cur_time = time.time()
        if job_queue and job_queue[0][0] < cur_time:
            if job_queue[0][1] is 'on':
                arduino.turn_on()
                status = 'ON'
            elif job_queue[0][1] is 'off':
                arduino.turn_off()
                status = 'OFF'
            job_queue.popleft()
        time.sleep(1)


app = Flask(__name__)
@app.route('/')
@app.route('/index')
def index():
    global status
    temp, humidity = arduino.get_temp()
    return render_template('index.html', title='RemoteCozy', status=status, t=temp, h=humidity)


@app.route('/ON')
def turn_on():
    global job_queue
    cur_time = time.time()
    job_queue.append([cur_time, 'on'])
    return render_template('status.html', title='ON')


@app.route('/OFF')
def turn_off():
    global job_queue
    cur_time = time.time()
    job_queue.append([cur_time, 'off'])
    return render_template('status.html', title='OFF')


@app.route('/15MIN')
def timer_15_min():
    global job_queue
    cur_time = time.time()
    job_queue.append([cur_time, 'on'])
    job_queue.append([cur_time+15*60, 'off'])
    return render_template('status.html', title='15 mins')


@app.route('/30MIN')
def timer_30_min():
    global job_queue
    cur_time = time.time()
    job_queue.append([cur_time, 'on'])
    job_queue.append([cur_time+30*60, 'off'])
    return render_template('status.html', title='30 mins')


if __name__ == '__main__':
    t = threading.Thread(target=check_job_queue, args=())
    t.daemon = True
    t.start()

    if sys.platform == 'win32':
        app.run()
    else:
        app.run(host='0.0.0.0')
