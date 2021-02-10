import sys
import serial
import time


class MyArduino:
    commands = {"Turn off": "0", "Turn on": "1", "Buzzer on": 2, "Buzzer off": 3,
                "DHT11": 4}

    def __init__(self, port=None, timeout=0.5):
        if port is None:
            if sys.platform == 'win32':
                port = 'COM3'
            elif sys.platform == 'linux' or sys.platform == 'linux2':
                port = "/dev/ttyACM0"
            else:
                port = "/dev/ttyACM0"
        self.ser = serial.Serial(port, 9600, timeout=timeout)
        self.fahrenheit = 32
        self.celsius = 0
        self.humidity = 0

    def turn_on(self):
        self.send(self.commands["Buzzer on"])
        self.send(self.commands["Turn on"])

    def turn_off(self):
        self.send(self.commands["Buzzer off"])
        self.send(self.commands["Turn off"])

    def send(self, message):
        self.ser.write("{}\n".format(message).encode())

    def update_dht11(self):
        self.ser.read(self.ser.inWaiting())
        self.send(self.commands["DHT11"])
        time.sleep(0.1)
        msg = self.ser.read(self.ser.inWaiting())
        msg = msg.decode("utf-8")
        try:
            self.humidity = float(msg.split("#")[1])
            self.celsius = float(msg.split("#")[2])
        except:
            pass

        self.fahrenheit = f"{(self.celsius*9/5) + 32:.1f}"
