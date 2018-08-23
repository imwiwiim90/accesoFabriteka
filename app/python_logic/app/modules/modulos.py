import serial.tools.list_ports
import time
import os
import pandas 
import accesoFabriteka as fabritek 
from Datos import RegistroPuerta

# 6790
# 29987
#
import threading
import re

lock = threading.Lock()
connections = []

class Modulo(threading.Thread):

	VID = 1027
	PID = 24577


	def __init__(self):
		threading.Thread.__init__(self)
		self.serial = None
		self.port = None
		self.connected = False
		self.test_port = None
		self.test = False
		self.name = ''
		self.device = ''

	def run(self):
		self.createConnection()
		while True:
			if self.checkConnection():
				pin = ''
				try:
					pin = self.readPin()
				except:
					self.connected = False
				if pin:
					self.pin(pin)
			else:
				print "not connected " + self.name 
				self.createConnection()
			time.sleep(1)

	def createConnection(self):
		ports = list(serial.tools.list_ports.comports())
		if self.test:
			ser = serial.Serial(self.test_port, 9600, timeout=5)
			self.serial = ser
			self.connected = True
		for port in ports:
			#if (port.vid == self.VID and port.pid == self.PID):
			lock.acquire()
			if (port.vid != None and port.pid != None and not port.device in connections):
				print self.name + ' connecting ' + str(port.vid)
				ser = serial.Serial(port.device, 9600, timeout=1)
				self.serial = ser
				name = self.readName()
				if self.name == name:
					self.connected = True
					connections.append(port.device)
					lock.release()
					return True
			lock.release()
		return False
	def disconnect(self):
		self.connected = False
		connections.remove(self.device)
		self.device = ''

	def checkConnection(self):
		if self.test:
			return True
		if self.connected == False:
			return False
		x =	os.popen("ls /dev/ | grep " + self.serial.name.replace('/dev/','')).readlines()
		if len(x) == 0:
			self.disconnect()
			return False
		return True

	def write(self,string):
		self.serial.write(string + '\n')

	def readName(self):
		self.write('n')
		info = ''
		try:
			info = self.serial.readline()
		except:
			return None
		while len(info) > 0 and (info[-1] == '\n' or info[-1] == '\r') :
			info = info[:-1]
		if re.match(r'name:\w+', info):
			return info[5:]
		return None

	def readPin(self):
		info = self.serial.readline()
		while len(info) > 0 and(info[-1] == '\n' or info[-1] == '\r'):
			info = info[:-1]
		if (re.match(r'Card UID:\s(\w|\s)+',info)):
			return ''.join(info[10:].split(' '))
		return None


class ModuloPuerta(Modulo):
	def __init__(self):
		Modulo.__init__(self)
		self.name = 'puerta'
		self.test_port = '/dev/ptyp3'

	def checkUser(self,pin):
		return fabritek.verificarPin(pin)

	def communicate(self,valid):
		char = (b'v' if valid else b'i')
		self.write(char)

	def registerEntrance(self,pin):
		registroPuerta = RegistroPuerta()
		registroPuerta.register(pin)

	def pin(self,pin):
		permited = self.checkUser(pin)
		print 'entrada: ' + str(permited)
		self.communicate(permited)
		if permited:
			self.registerEntrance(pin)

class ModuloEntrada(Modulo):
	def __init__(self):
		Modulo.__init__(self)
		self.name = 'entrada'
		self.test_port = '/dev/ptyp2'
		self.last_pin = None

	def pin(self,pin):
		print pin
		self.write('v')
		self.last_pin = pin

	def get(self):
		pin = self.last_pin
		self.last_pin = None
		return pin

	def clear(self):
		self.last_pin = None

# abrir usuarios
#

# v -> valido
# i -> invalido


'''
m = ModuloPuerta()
m.test = True

m.start()
m.join()
'''
