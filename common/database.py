import os
import psycopg2

db_hostname = 'localhost'
db_username = os.environ['APP_DB_USERNAME']
db_password = os.environ['APP_DB_PASSWORD']
db_name = os.environ['APP_DB_NAME']

def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT category_id, amount FROM transactions" )

    for category, amount in cur.fetchall() :
        print(category, amount)

myConnection = psycopg2.connect( host=db_hostname, user=db_username, password=db_password, dbname=db_name )
doQuery( myConnection )
myConnection.close()