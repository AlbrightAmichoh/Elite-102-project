import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'elite102_project', password = '1903920sadA@')
cursor = connection.cursor()

testQuery = ("SELECT * FROM user")

cursor.execute(testQuery)

for item in cursor:
    print(item)

cursor.close()
connection.close()