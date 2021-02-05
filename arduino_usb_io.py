import sys
import serial


class MyArduino:
    commands = {"Turn off": "0", "Turn on": "1", "Buzzer on": 2, "Buzzer off": 3}

    def __init__(self, port=None, timeout=0.5):
        if port is None:
            if sys.platform == 'win32':
                port = 'COM3'
            elif sys.platform == 'linux' or sys.platform == 'linux2':
                port = "/dev/ttyACM0"
            else:
                port = "/dev/ttyACM0"
        self.arduino = serial.Serial(port, 9600, timeout=timeout)

    def turn_on(self):
        self.send(self.commands["Buzzer on"])
        self.send(self.commands["Turn on"])

    def turn_off(self):
        self.send(self.commands["Buzzer off"])
        self.send(self.commands["Turn off"])

    def send(self, message):
        self.arduino.write("{}\n".format(message).encode())

    def get_temp(self):
        # TODO: dummy code for now.
        c_temp = 37.8
        f_temp = 105.8
        return c_temp, f_temp
