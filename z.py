import sqlite3
con=sqlite3.connect('login.db')
cursor=con.cursor()
a="gaurav"
b='gaureav@gmail.com'
c="gaurav"
cursor.execute(f'Insert into login Values("{a}","{b}","{c}");')
con.commit()
cursor.execute('select * from login;')
result=cursor.fetchall()
print(result)
con.close()
