# Module de lecture/ecriture du port série
from serial import *
import os, platform

if platform.system() == "Darwin":
    serial_port = "/dev/tty.usbmodem1421"
else:
    # Port série ttyACM0
    serial_port="/dev/ttyACM0"

# Vitesse de baud : 9600
# Timeout en lecture : 1 sec
# Timeout en écriture : 1 sec
with Serial(port=serial_port, baudrate=9600, timeout=1, writeTimeout=1) as port_serie:
    if port_serie.isOpen():
        while True:
            ligne = port_serie.readline()
            print ligne

