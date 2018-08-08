import pandas
import os

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

	def find_entry(self,key,val):
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
		item = item.loc[0]
		return { k:item[k] for k in self.keys}

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

	def obtenerPorCedula(self,cedula):
		return self.excelMngr.find_entry('Cedula',cedula)	

	def crearUsuario(self,usuario):
		return self.excelMngr.new_entry(usuario)



users = Usuarios()
'''users.crearUsuario({
	'nombre': 'jorge',
	'cedula': '1020202',
	'telefono': '310222929',
	})'''
print users.obtenerPorCedula(1020810530)
