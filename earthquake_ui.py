import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
import json
import plotly.figure_factory as ff

st.set_page_config(layout="wide")
st.title('Earthquake Data App')

# Initialize dataframe
df = pd.DataFrame()
df["magnitude"] = ""


# --- Sidebar Content ---

# Date Filter in sidebar
min_value=datetime.date(2025, 2, 12) # static dataset start date
max_value=datetime.date(2025, 3, 14) # static dataset end date

dates = st.sidebar.date_input(
    "Select date or range:",
    value=(min_value,max_value),
    min_value=min_value,
    max_value=max_value,
    format="MM.DD.YYYY"
    )


# Magnitude slider in sidebar
magnitudes = st.sidebar.slider(
    'Select an earthquake magnitude range',
    0.0, 10.0, (2.0, 8.0))


# Sort Asc vs Desc radio button
sort_radio = st.sidebar.radio(
    "Sort earthquakes by magnitude",
    ["Descending", "Ascending"]
)

options = ["All", "10", "50", "100"]
count_selection = st.sidebar.pills("Number of earthquakes to show", options, selection_mode="single")

# Make HTTP request on button press
if st.sidebar.button("Apply", type="primary"):
  # Need to reformat from datetime to string before sending to api
  start_date = dates[0].strftime("%Y-%m-%d")
  end_date = dates[1].strftime("%Y-%m-%d")
  min_magnitude = magnitudes[0]
  max_magnitude = magnitudes[1]
  # url contains all parameters to be passed to api
  url = f'http://127.0.0.1:5000/api/data?start_date={start_date}&end_date={end_date}&min_magnitude={min_magnitude}&max_magnitude={max_magnitude}&sort={sort_radio}&count={count_selection}'
  response = requests.get(url)
  # st.write(response.text)
  data = json.loads(response.text)  # Parse the JSON string
  df = pd.DataFrame(data)  # Create DataFrame from the parsed JSON


# --- Main page content ---

# Create a layout with two columns
col1, col2 = st.columns(2)

# Add BANs here:
total_earthquakes = len(df)
with col1:
  st.metric(label="**Total Earthquakes Shown**", value=total_earthquakes)

if not df.empty:
  max_magnitude = df['magnitude'].max()
  with col2:
    st.metric(label="**Highest Magnitude Shown**", value=max_magnitude)
else:
   with col2:
    st.metric(label="**Highest Magnitude Shown**", value=0)

# Magnitude Probability Density Chart
col1, col2, col3 = st.columns([1, 3, 1])

if not df.empty:
  group_labels = 'Magnitudes'
  mag_list = df['magnitude'].tolist()
  fig = ff.create_distplot([mag_list], [group_labels])
  fig.update_layout(title="Magnitude Probability Density")
  fig.update_layout(xaxis_title="Magnitude")
  fig.update_layout(yaxis_title="Probability Density")
  col2.plotly_chart(fig)


# Map
map_data = df.copy()
# Scale the magnitude so that it has a more significant spread when used as the point radius size
map_data['magnitude'] = map_data['magnitude'] ** 4 * 300

map_container = st.container()
with map_container:
    st.map(data=map_data, latitude='lat', longitude='lon', size='magnitude', zoom=1)

# Table
st.dataframe(df)