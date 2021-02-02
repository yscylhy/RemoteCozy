from flask import Flask, render_template, Response
app = Flask(__name__)
import serial

ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Raspi'}
    return render_template('index.html', title='Home', user=user)

@app.route('/ON')
def turn_on():
    user = {'username': 'Raspi'}
    ser.write(b'1\n')
    return render_template('index.html', title='Home', user=user)


@app.route('/OFF')
def turn_off():
    user = {'username': 'Raspi'}
    ser.write(b'0\n')
    return render_template('index.html', title='Home', user=user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
