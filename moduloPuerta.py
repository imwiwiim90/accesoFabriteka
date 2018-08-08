import serial.tools.list_ports
import time
import os
import pandas

'''

ports = list(serial.tools.list_ports.comports())
for p in ports:
	print (p)

print(ports)
if ports==[]:
	print("El puerto serial esta jodido")
else:
	print("si hay puerto")


ser=serial.Serial('/dev/tty.wchusbserial1420', 115200, timeout=0)



while 1:
	info=ser.readline()
	if(info!=b''):
		print(info)

'''
# 6790
# 29987
#
import threading
import re


class ModuloPuerta(threading.Thread):
	VID = 6790
	PID = 29987
	def __init__(self):
		threading.Thread.__init__(self)
		self.serial = None
		self.port = None
		self.connected = False

	def run(self):
		self.createConnection()
		for i in range(10):
			if self.checkConnection():
				text = self.readPin()
				print text
				if text:
					permited = self.checkUser(text)
					print permited
					self.communicate(permited)
			else:
				print "not connected"
				self.createConnection()
			time.sleep(1)

	def createConnection(self):
		ports = list(serial.tools.list_ports.comports())

		for port in ports:
			if (port.vid == self.VID and port.pid == self.PID):
				ser = serial.Serial(port.device, 115200, timeout=0)
				self.serial = ser
				self.connected = True
				return True
		return False

	def checkConnection(self):
		if self.connected == False:
			return False
		x =	os.popen("ls /dev/ | grep " + self.serial.name.replace('/dev/','')).readlines()
		if len(x) == 0:
			return False
		return True

	def checkUser(self,pin):
		files=os.listdir('./')
		if 'usuarios.xlsx' in files:
			df = pandas.read_excel('usuarios.xlsx')
			try:
				# 9315886B
				print pin
				df.loc[pin]
				return True
			except:
				return False
		return False

	def communicate(self,valid):
		char = (b'v' if valid else b'i')
		self.serial.write(char)


	def readPin(self):
		info = self.serial.readline()
		if (re.match(r'modulo2:\s(\d|\s)+',info)):
			return ''.join(re.findall(r'\s(\w\w)+',info))
		return None


# abrir usuarios
#

# v -> valido
# i -> invalido
m = ModuloPuerta()

m.start()
m.join()
