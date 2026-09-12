import sqlite3
Connection=sqlite3.connect("Naresh_it_employee.db")
cursor=Connection.cursor()

data=cursor.execute('''Select * from Naresh_it_employee''')
for row in data:
    print(row)

Connection.commit()
Connection.close()