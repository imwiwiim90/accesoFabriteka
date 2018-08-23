import pandas
import os
from datetime import datetime, date
from dateutil import parser
import sys

sys.path.insert(0,'./app/modules')
import accesoFabriteka as fabritek

DEFAULT_SHEET_NAME = 'Sheet1'
class ExcelManager():
	def __init__(self,filename,keys,index=None):
		files = os.listdir('./')
		self.filename = filename
		if not self.filename in files:
			os.popen('touch ' + self.filename)
		self.keys = keys
		self.index = index

	def new_entry(self,item):
		try:
			data = pandas.read_excel(self.filename)
			data = data.append(item,ignore_index=True)
		except:
			data = pandas.DataFrame({k:[str(item[k])] for k in self.keys})

		writer = pandas.ExcelWriter(self.filename, engine=None)
		data.to_excel(writer, sheet_name=DEFAULT_SHEET_NAME)
		writer.save()

	def find(self,key,val,unique=False):
		data = pandas.read_excel(self.filename)
		if len(data) == 0:
			return None
		# set data as unindexed
		if self.index:
			new_data = {}
			for k in self.keys:
				new_data[k] = []
				for index in data.index.values:
					if k == self.index:
						new_data[k].append(index)
					else:
						new_data[k].append(data.loc[index][k])
			data = pandas.DataFrame({k: new_data[k] for k in self.keys})
		if type(val) is str:
			data[key] = data[key].astype('|S')

		item = data.loc[data[key] == val]
		if len(item) == 0:
			return
		if unique:
			item = item.iloc[0]
			return { k:item[k] for k in self.keys}
		else:
			return [{k:item.iloc[i][k] for k in self.keys} for i in range(len(item))]

	def save_entry(self,item,key):
		data = pandas.read_excel(self.filename)
		data = data.loc[data[key] == item[key]]
		if len(data) == 1:
			data = data.loc[0]
			writer = pandas.ExcelWriter(self.filename, engine=None)
			data.to_excel(writer, sheet_name=DEFAULT_SHEET_NAME)
			writer.save()
			return True


class Usuarios():
	def __init__(self):
		self.excelMngr= ExcelManager('usuarios.xlsx',['Cedula','Nombre','Telefono'],'Cedula')
		self.registroPuerta = RegistroPuerta()
		self.registroTarjeta = RegistroTarjeta()

	def obtenerPorCedula(self,cedula):
		return self.excelMngr.find_entry('Cedula',cedula)	

	def crearUsuario(self,usuario):
		return self.excelMngr.new_entry(usuario)

	# get the time spend inside while holding the card
	def getLogsFromLastEntrance(self,cedula):
		last_entrance = self.registroTarjeta.getLastEntrance(cedula)
		return self.registroPuerta.getFromDatetime(cedula,last_entrance['Fecha'] + ' ' + last_entrance['Hora'])


class RegistroTarjeta():
	def __init__(self):
		self.excelMngr = ExcelManager('RegistroTarjeta.xlsx',['Cedula','Fecha','Hora','Entrada/salida'])

	def getLastEntrance(self,cedula):
		lastRegister = self.excelMngr.find('Cedula',cedula)[-2:]
		if lastRegister[0]['Entrada/salida'] == 'Entrada':
			return lastRegister[0]
		else:
			return lastRegister[1]


class RegistroPuerta():
	def __init__(self):
		self.excelMngr = ExcelManager('RegistroPuerta.xlsx',['cedula','datetime'])

	def register(self,pin):
		[_type,name,phone,mail,cc] = fabritek.verificarPinAsignado(pin)
		self.excelMngr.new_entry({
			'cedula' : cc,
			'datetime' : str(datetime.now())
			})

	def getFromDatetime(self,cedula,datetime_str):
		d = parser.parse(datetime_str)
		items =  self.excelMngr.find('cedula',cedula)
		print datetime_str
		print items
		print [item for item in items if d <= parser.parse(item['datetime'])]
		return [item for item in items if d <= parser.parse(item['datetime'])]



