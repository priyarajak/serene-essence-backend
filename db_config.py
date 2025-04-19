import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pomi@12345",
            database="serene_essence"
        )
        return conn
    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        raise
