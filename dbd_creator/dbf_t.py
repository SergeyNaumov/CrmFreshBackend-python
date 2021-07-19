import dbf
table = dbf.Table('test.dbf', 'plan C(255); header c(255); code C(50)', codepage='cp866')
table.open(dbf.READ_WRITE)

table.append(('название плана', 'название товара', 'xx'))
table.append(('вторая строка', 'название товара', 'xx2'))
table.append(('третья строка', 'название товара', 'xx2'))

for record in table:
    print('r:',record)
table.close()
#table.open('test.dbf',mode=dbf.READ_WRITE)