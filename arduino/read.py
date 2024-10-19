import serial
import time
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)  # Use 'COMx' on Windows, '/dev/ttyACM0' on Linux

time.sleep(5)
while True:
    if arduino.in_waiting:
        packet = arduino.readline()
        serialText = packet.decode('utf-8').rstrip()
        print(serialText)