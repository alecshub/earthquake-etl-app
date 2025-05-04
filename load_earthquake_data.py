import psycopg2
import geojson
from shapely.geometry import Point
from shapely.wkb import dumps
import datetime

# Add parameters here:
db_params = {
    "host": "", # "host"
    "database": "earthquakes", # "database"
    "user": "", # "user"
    "password": "", # "password"
    "port": "", # "port"
}

with open("earthquake_data.geojson", "r") as file:
    data = geojson.load(file)

with psycopg2.connect(**db_params) as conn:
    with conn.cursor() as curs:
        for feature in data["features"]:
            properties = feature["properties"]
            geometry = feature["geometry"]
            id = feature["id"]

            # Extract data from properties
            magnitude = properties["mag"]
            location = properties["place"]
            time = datetime.datetime.fromtimestamp(properties["time"]/1000.0)
            tsunami = properties["tsunami"]

            # Extract geometry data
            # Create a Shapely Point object
            point = Point(geometry["coordinates"])

            # convert Shapely Point object into Well-Known Binary (WKB) representation
            wkb_geometry = dumps(point, hex=True, srid=4326)

            # Extract id
            earthquake_id = id

            # Insert data into table
            curs.execute(
                """
                INSERT INTO earthquakes (earthquake_id, magnitude, location, time, tsunami, geometry)
                Values (%s, %s, %s, %s, %s, ST_GeomFromWKB(decode(%s, 'hex'), 4326))
                """,
                (earthquake_id, magnitude, location, time, tsunami, wkb_geometry)
            )

print("Data loaded into PostgreSQL successfully.")