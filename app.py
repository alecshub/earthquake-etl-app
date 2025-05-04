import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from datetime import date
from datetime import datetime

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

# Our main data endpoint
@app.get("/api/data")
def get_data():

    url = os.getenv("DATABASE_URL")
    connection = psycopg2.connect(url)
    with connection:
        with connection.cursor() as cursor:

            # Build the SQL query to return all relevant data
            query = """
                SELECT
                    earthquake_id,
                    magnitude,
                    location, 
                    time,
                    geometry,
                    ST_X(geometry) AS lon,
                    ST_Y(geometry) AS lat
                FROM earthquakes
                WHERE 1=1
            """
            # List to store the parameters we retrieve from the url
            params = []

            # This is where we will pull the values from the URL.
            # Dates need to be converted to datetime.datetime objects to match your database format
            
            start_date = request.args.get("start_date")
            print(f'start date: {start_date}') # print for debugging purposes
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            # Combine date with time so that it matches the database
            start_date = datetime.combine(start_date, datetime.min.time())
            # Ensure the datetime is in the exact format required to filter our database
            start_date = start_date.strftime('%Y-%m-%d %H:%M:%S')

            end_date = request.args.get("end_date")
            print(f'end date: {end_date}') # print for debugging purposes
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            # Combine date with time so that it matches the database
            end_date = datetime.combine(end_date, datetime.max.time())
            # Ensure the datetime is in the exact format required to filter our database
            end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')

            # Add the date filter to your query
            query += " AND time >= %s AND time <= %s"

            params.append(start_date)
            params.append(end_date)

            # Magnitudes
            min_magnitude = request.args.get("min_magnitude")
            print(f'min_magnitude: {min_magnitude}')

            max_magnitude = request.args.get("max_magnitude")
            print(f'max_magnitude: {max_magnitude}')

            query += " AND magnitude >= %s AND magnitude <= %s"
            params.append(min_magnitude)
            params.append(max_magnitude)

            # Sorting
            sort_command = request.args.get("sort")
            if sort_command == "Ascending":
                query += " ORDER BY magnitude ASC"
            elif sort_command == "Descending":
                query += " ORDER BY magnitude DESC"

            # count
            count = request.args.get("count")
            if count != "All" and count != "None":
                earthquake_count = int(count)
                query += " LIMIT %s"
                params.append(earthquake_count)
            
            # Execute the query!
            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Running the query and fetchall() returns a list of tuples
            earthquakes = []
            for row in rows:
                earthquake_id = row[0]
                magnitude = row[1]
                location = row[2]
                time = row[3]
                geometry = row[4]
                lon = row[5]
                lat = row[6]

                earthquakes.append({
                    "earthquake_id": earthquake_id,
                    "magnitude": magnitude,
                    "location": location,
                    "time": time,
                    "geometry": geometry,
                    "lon": lon,
                    "lat": lat
                })

        connection.commit()
        return jsonify(earthquakes)