import psycopg2

try:
    conn = psycopg2.connect("dbname='banter' user='banterapiuser' password='db_user_22'")
except Exception as e:
    print("Unable to connect to the database: "+str(e))