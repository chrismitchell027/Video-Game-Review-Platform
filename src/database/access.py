import psycopg2

DATABASE = "project"
USER = "postgres"
PASSWORD = "PASSWORD GOES HERE"
HOST = "localhost"
PORT = "5432"

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def get_db_cursor():
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            return conn, cursor
        except psycopg2.Error as e:
            print(f"Error creating cursor: {e}")
            conn.close()
            return None, None
    else:
        return None, None