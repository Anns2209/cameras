import pandas as pd
import mysql.connector

# Povezava do MySQL baze
db_connection = mysql.connector.connect(
    host="localhost",       # Zamenjaj z naslovom strežnika, če ni lokalni
    user="root",
    password="potk123!",
    database="POTK_DB"
)

# Seznam datotek, ki jih želiš naložiti
csv_files = ["./data.raw/temp1.csv", "./data.raw/temp2.csv"]

# Ustvarjanje kurzorja za izvajanje SQL ukazov
cursor = db_connection.cursor()

# SQL za ustvarjanje tabele
create_table_query = """
CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_name VARCHAR(255),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    air_temperature DECIMAL(5,2)
)
"""

# Ustvari tabelo
cursor.execute(create_table_query)

# Priprava SQL za vstavljanje podatkov
insert_query = """
INSERT INTO weather_data (source_name, latitude, longitude, air_temperature) 
VALUES (%s, %s, %s, %s)
"""

# Procesiranje vsake datoteke
for file in csv_files:
    # Branje podatkov iz CSV datoteke
    data = pd.read_csv(file)
    
    # Procesiranje in vstavljanje podatkov v tabelo
    for index, row in data.iterrows():
        source_name = row['SourceName']
        latitude = float(row['Latitude']) if pd.notna(row['Latitude']) else None
        longitude = float(row['Longitude']) if pd.notna(row['Longitude']) else None
        air_temperature = float(row['AirTemperature']) if pd.notna(row['AirTemperature']) else None
        
        # Vstavi vrstico
        cursor.execute(insert_query, (source_name, latitude, longitude, air_temperature))

# Potrdi spremembe
db_connection.commit()

# Zapri povezavo
cursor.close()
db_connection.close()

print("Podatki so uspešno vstavljeni v tabelo weather_data.")
