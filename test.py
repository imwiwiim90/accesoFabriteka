import pandas


pin = '9315886B'
phone = '3120992022'
name = 'Jose'

item = pandas.DataFrame({
	pin: [name,name]
	})
item = item.T
writer = pandas.ExcelWriter('test.xlsx', engine=None)
item.to_excel(writer, sheet_name = 'Sheet1')
writer.save()

item = pandas.read_excel('usuarios.xlsx')
print item.loc[pin]