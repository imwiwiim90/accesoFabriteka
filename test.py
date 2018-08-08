import pandas


pin = '9315886B'
phone = '3120992022'
name = 'Jose'

item = pandas.DataFrame({
	'name': [name],
	'phone': [phone],
	'pin': [pin],
	})
#item = item.append({'name':name,'phone':phone,'pin':phone},ignore_index=True)

item = pandas.read_excel('tests.xlsx')
#item = item.append({'name':name,'phone':phone,'pin':phone},ignore_index=True)
#writer = pandas.ExcelWriter('test.xlsx', engine=None)
#item.to_excel(writer, sheet_name = 'Sheet1')
#writer.save()

print item.loc[item['name'] == 'Jose'].loc[0]
print len(item)