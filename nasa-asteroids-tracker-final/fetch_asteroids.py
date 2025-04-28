import requests
import mysql.connector
from datetime import datetime

API_KEY = "dOelWH9Yka5GvLUWMWMdYxP7RK73daql3bNSoVVT"
Url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-08&api_key={API_KEY}"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sairam@123",
    database="astro"
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS asteroids (
        id BIGINT PRIMARY KEY,
        name VARCHAR(255),
        absolute_magnitude_h FLOAT,
        estimated_diameter_min_km FLOAT,
        estimated_diameter_max_km FLOAT,
        is_potentially_hazardous_asteroid BOOLEAN
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS close_approach (
        id INT AUTO_INCREMENT PRIMARY KEY,
        neo_reference_id BIGINT,
        close_approach_date DATE,
        relative_velocity_kmph FLOAT,
        astronomical FLOAT,
        miss_distance_km FLOAT,
        miss_distance_lunar FLOAT,
        orbiting_body VARCHAR(100),
        FOREIGN KEY (neo_reference_id) REFERENCES asteroids(id)
    )
""")

conn.commit()
print("✅ Tables created (if not exist).")

asteroids_data = []
target = 10000

while len(asteroids_data) < target:
    response = requests.get(Url)
    response_data = response.json()
    details = response_data['near_earth_objects']
    for data, info in details.items():
        for i in info:
            estimated_diameter_min_km = i['estimated_diameter']['kilometers'].get('estimated_diameter_min', None)
            estimated_diameter_max_km = i['estimated_diameter']['kilometers'].get('estimated_diameter_max', None)
            close_approach_date = i['close_approach_data'][0].get('close_approach_date', None)
            relative_velocity_kmph = float(i['close_approach_data'][0]["relative_velocity"]["kilometers_per_hour"])
            astronomical = float(i['close_approach_data'][0]["miss_distance"]["astronomical"])
            miss_distance_km = float(i['close_approach_data'][0]["miss_distance"]["kilometers"])
            miss_distance_lunar = float(i['close_approach_data'][0]["miss_distance"]["lunar"])
            orbiting_body = i['close_approach_data'][0]["orbiting_body"]

            asteroids_data.append(dict(
                id=int(i['id']),
                neo_reference_id=int(i['neo_reference_id']),
                name=i['name'],
                absolute_magnitude_h=i['absolute_magnitude_h'],
                estimated_diameter_min_km=estimated_diameter_min_km,
                estimated_diameter_max_km=estimated_diameter_max_km,
                is_potentially_hazardous_asteroid=i.get('is_potentially_hazardous_asteroid'),
                close_approach_date=datetime.strptime(close_approach_date, '%Y-%m-%d').date(),
                relative_velocity_kmph=relative_velocity_kmph,
                astronomical=astronomical,
                miss_distance_km=miss_distance_km,
                miss_distance_lunar=miss_distance_lunar,
                orbiting_body=orbiting_body
            ))

            if len(asteroids_data) >= target:
                break
        if len(asteroids_data) >= target:
            break
    Url = response_data['links']['next']

print(f"✅ Fetched {len(asteroids_data)} asteroids from API.")

for asteroid in asteroids_data:
    cursor.execute("""
        INSERT IGNORE INTO asteroids (id, name, absolute_magnitude_h,
            estimated_diameter_min_km, estimated_diameter_max_km, is_potentially_hazardous_asteroid)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        asteroid['id'],
        asteroid['name'],
        asteroid['absolute_magnitude_h'],
        asteroid['estimated_diameter_min_km'],
        asteroid['estimated_diameter_max_km'],
        asteroid['is_potentially_hazardous_asteroid']
    ))

    cursor.execute("""
        INSERT INTO close_approach (neo_reference_id, close_approach_date, relative_velocity_kmph,
            astronomical, miss_distance_km, miss_distance_lunar, orbiting_body)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        asteroid['neo_reference_id'],
        asteroid['close_approach_date'],
        asteroid['relative_velocity_kmph'],
        asteroid['astronomical'],
        asteroid['miss_distance_km'],
        asteroid['miss_distance_lunar'],
        asteroid['orbiting_body']
    ))

conn.commit()
cursor.close()
conn.close()

print("✅ All data inserted successfully into MySQL!")
