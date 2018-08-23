import serial.tools.list_ports
import time

ports = list(serial.tools.list_ports.comports())
for port in ports:
	print port.device

ser = serial.Serial('/dev/ptyp3', 115200, timeout=5)
while True:
	print 'loop'
	print ser.readline()
	time.sleep(1)