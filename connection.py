import psycopg2

def connection_manager():
	connection = psycopg2.connect(
	    database="",
	    user="",
	    password="",
	    host="",
	    port='5432'
	)
	cursor=connection.cursor()
	return cursor
