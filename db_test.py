import mysql.connector
from mysql.connector import Error

try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="potk123!",
        database="POTK_DB"
    )

    if db_connection.is_connected():
        db_info = db_connection.get_server_info()
        print("Uspešno povezano na MySQL strežnik. Različica strežnika:", db_info)

        cursor = db_connection.cursor()
        cursor.execute("SELECT DATABASE();")
        current_database = cursor.fetchone()
        print("Trenutno aktivna baza podatkov je:", current_database)

except Error as e:
    print("Napaka pri povezovanju na MySQL strežnik:", e)

finally:
    if 'db_connection' in locals() and db_connection.is_connected():
        cursor.close()
        db_connection.close()
        print("Povezava na MySQL strežnik je zaprta.")

