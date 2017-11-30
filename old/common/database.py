import os
import psycopg2

db_hostname = 'localhost'
db_name = os.environ['BANTER_DB_NAME']
db_username = os.environ['BANTER_DB_USERNAME']
db_password = os.environ['BANTER_DB_PASSWORD']


def connect():
	return psycopg2.connect( host=db_hostname, user=db_username, password=db_password, dbname=db_name )

def disconnect(conn):
	conn.close()

def doQuery():
	conn = connect()
	cur = conn.cursor()

	cur.execute( "SELECT id, email FROM users" )

	for _id, email in cur.fetchall() :
		print(_id, email)

	disconnect(conn)


doQuery()

