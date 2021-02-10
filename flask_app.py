import sys
import arduino_usb_io
import heapq
import threading
from flask import Flask, render_template
import time


job_queue = []
arduino = arduino_usb_io.MyArduino()
status = 'OFF'


def check_job_queue():
    global job_queue, status
    read_dht11_interval = 60
    pre_read_time = time.time()
    arduino.update_dht11()

    while True:
        cur_time = time.time()
        if job_queue and job_queue[0][0] < cur_time:
            if job_queue[0][1] is 'on':
                arduino.turn_on()
                status = 'ON'
                while job_queue and job_queue[0][1] is 'on':
                    heapq.heappop(job_queue)
            elif job_queue[0][1] is 'off':
                arduino.turn_off()
                status = 'OFF'
                while job_queue and job_queue[0][1] is 'off':
                    heapq.heappop(job_queue)
        if pre_read_time - time.time() > read_dht11_interval:
            arduino.update_dht11()
            pre_read_time += read_dht11_interval
        time.sleep(1)


app = Flask(__name__)
@app.route('/')
@app.route('/index')
def index():
    global status
    arduino.update_dht11()
    f = arduino.fahrenheit
    c = arduino.celsius
    h = arduino.humidity
    return render_template('index.html', title='RemoteCozy', status=status, f=f, c=c, h=h)


@app.route('/ON')
def turn_on():
    global job_queue
    cur_time = time.time()
    heapq.heappush(job_queue, [cur_time, 'on'])
    return render_template('status.html', title='ON')


@app.route('/OFF')
def turn_off():
    global job_queue
    cur_time = time.time()
    heapq.heappush(job_queue, [cur_time, 'off'])
    return render_template('status.html', title='OFF')


@app.route('/15MIN')
def timer_15_min():
    global job_queue
    cur_time = time.time()
    heapq.heappush(job_queue, [cur_time, 'on'])
    heapq.heappush(job_queue, [cur_time+15*60, 'off'])
    return render_template('status.html', title='15 mins')


@app.route('/30MIN')
def timer_30_min():
    global job_queue
    cur_time = time.time()
    heapq.heappush(job_queue, [cur_time, 'on'])
    heapq.heappush(job_queue, [cur_time+30*60, 'off'])
    return render_template('status.html', title='30 mins')


@app.route('/REFRESH')
def refresh():
    arduino.update_dht11()
    return render_template('status.html', title='Refreshing')


if __name__ == '__main__':
    t = threading.Thread(target=check_job_queue, args=())
    t.daemon = True
    t.start()

    if sys.platform == 'win32':
        app.run()
    else:
        app.run(host='0.0.0.0')
