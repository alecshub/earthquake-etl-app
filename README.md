# earthquake-etl-app
An example ETL pipeline that:
1. extracts earthquake data from the USGS (United States Geological Survey),
2. stores the data in a PostgreSQL database,
3. serves the data to a Streamlit frontend via flask backend API, allowing users to filter, visualize, and download data.

## Local Setup Instructions

To run this project on your local machine, please follow these steps:
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/alecshub/earthquake-etl-app.git
    cd earthquake-etl-app
    ```

2.  **Set up the Environment:**

    **Using Conda (Recommended):**
    ```bash
    conda env create -f environment.yml
    conda activate earthquake_env
    ```

3.  **Configure PostgreSQL:**
    * Ensure you have a PostgreSQL database named `earthquake_db` created.
    * **Create a `.env` file** in the root of your project directory with the following content, replacing the values if your PostgreSQL setup is different:
        ```
        DATABASE_URL=postgresql://user:password@host:port/earthquake_db
        ```

4.  **Fetch Data:**
    Run fetch_earthquake_data.ipynb to fetch the dataset from USGS. This will download a .geojson file that should be kept in the same repository as the other project files.
    
5.  **Load Initial Data:**
    Open the load_earthquake_data.py file and update the following parameters to match those specified in step 4.
      ```
      "host": "", # "host"
      "database": "earthquakes", # "database"
      "user": "", # "user"
      "password": "", # "password"
      "port": "", # "port"
      ```
    Run load_earthquake_data.py populate your local PostgreSQL database.

6.  **Run the Flask Backend:**
    Run the Flask development server:
    ```bash
    flask run
    ```
    The backend API should now be running at the port specified in step 4.

7.  **Run the Streamlit Frontend:**
    Open the file earthquake_ui.py and change the dates that determine the bounds of the date slider to the max and min date of your downloaded dataset.
      ```
      min_value=datetime.date(2025, 2, 12) # static dataset start date
      max_value=datetime.date(2025, 3, 14) # static dataset end date
      ```
    
    Open a new terminal window, navigate to the root of your project directory, and run the Streamlit application:
    ```bash
    streamlit run earthquake_ui.py
    ```
    The Streamlit app should open automatically in your web browser.

8.  **Apply filters on app:**
    Filter the earthquake data using the left-hand nav. When you click the 'Apply' button, the Streamlit app will send an http request to the flask API and data will populate within the app.

## Potential Future Enhancements
Future improvements for this project include migrating the database to a cloud-hosted service instead of local PostgreSQL, setting up daily data updates using Airflow, and containerizing the application with Docker. These enhancements would allow for easier deployment and public accessibility, removing the need for users to handle code or local setups.
