import serial.tools.list_ports


ports = list(serial.tools.list_ports.comports())
for port in ports:
	print port
	print 'vid ' + str(port.vid)
	print 'pid ' + str(port.pid)
	print