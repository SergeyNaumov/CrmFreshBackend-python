import dbf
table = dbf.Table('temptable', 'name C(30); age N(3,0); birth D')

print('db definition created with field names:', table.field_names)