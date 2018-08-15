import MySQLdb

db = MySQLdb.connect("localhost","root","manuvava","PP")
cursor = db.cursor()

cursor.execute("SELECT * FROM History ORDER BY ID DESC LIMIT 1")
row = str(cursor.fetchone())
if "1s0:00 PM" in row:
	print "YES"
else:
	print "NO"

