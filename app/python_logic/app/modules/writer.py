import serial.tools.list_ports

device = '/dev/ttyp2'
s = serial.Serial(device, 9600, timeout=1)
prefix = 'Card UID: '
while True:
	print  s.readline()
	inp = raw_input(prefix)
	s.write(prefix + inp + '\n')	