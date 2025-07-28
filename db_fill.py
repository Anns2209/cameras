import pandas as pd
import mysql.connector

# Povezava do MySQL baze
db_connection = mysql.connector.connect(
    host="localhost",       # Zamenjaj z naslovom strežnika, če ni lokalni
    user="root",
    password="potk123!",
    database="POTK_DB"
)

# Branje podatkov iz CSV datoteke
data = pd.read_csv("./data.raw/kamere.csv", encoding="utf-8")

# Ustvarjanje kurzorja za izvajanje SQL ukazov
cursor = db_connection.cursor()

# SQL za ustvarjanje tabele
create_table_query = """
CREATE TABLE IF NOT EXISTS kamere (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    image_link VARCHAR(255)
)
"""

# Ustvari tabelo
cursor.execute(create_table_query)

# Priprava SQL za vstavljanje podatkov
insert_query = """
INSERT INTO kamere (title, latitude, longitude, image_link) 
VALUES (%s, %s, %s, %s)
"""

# Procesiranje in vstavljanje podatkov v tabelo
for index, row in data.iterrows():
    title = row['Title (SLO)']
    coordinates = row['Coordinates'].strip("[]").split(", ")
    longitude = float(coordinates[0])
    latitude = float(coordinates[1])
    image_link = row['Image Link']
    
    # Vstavi vrstico
    cursor.execute(insert_query, (title, latitude, longitude, image_link))

# Potrdi spremembe
db_connection.commit()

# Zapri povezavo
cursor.close()
db_connection.close()

print("Podatki so uspešno vstavljeni v tabelo kamere.")
