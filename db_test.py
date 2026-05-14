import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="k26121110s@",   # ← Your actual password
        database="marketing_db",
        use_pure=True              # ← Fixes connector errors
    )
    
    cursor = conn.cursor()
    print("Database Connected Successfully")

except mysql.connector.Error as e:
    print("Connection failed:", e)