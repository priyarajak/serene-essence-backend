import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="maglev.proxy.rlwy.net",
            user="root",
            password="HwYXYmgfoHCKfuIurQLUkyakgFTeFyqB", 
            database="railway",
            port=12984
        )
        return conn
    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        raise
