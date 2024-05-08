# import streamlit as st
# import pandas as pd
# import pickle
# import json
# from datetime import datetime
# from sklearn.preprocessing import StandardScaler
#
# # Load the saved columns' names
# with open('columns_used.json', 'r') as json_file:
#     columns_used = json.load(json_file)
#
# # Streamlit app
# st.title('Expense Prediction App')
#
# # User input for year and month
# year_month = st.text_input("Enter the year and month (e.g., 2024-05):")
# try:
#     input_date = datetime.strptime(year_month, '%Y-%m')
# except ValueError:
#     st.error("Please enter the year and month in the format YYYY-MM.")
#     st.stop()
#
# # Process the input year and month
# input_year = input_date.year
# input_month = input_date.month
#
# # Calculate time difference based on the input year and month
# current_date = datetime.now()
# input_datetime = datetime(input_year, input_month, 1)
# time_diff = (current_date - input_datetime).days
#
# # Load the trained model
# with open('final_model.pkl', 'rb') as file:
#     trained_model = pickle.load(file)
#
# # Load the fitted scaler
# with open('fitted_scaler.pkl', 'rb') as scaler_file:
#     fitted_scaler = pickle.load(scaler_file)
#
# # Prepare input data
# input_data = {'year': input_year, 'month': input_month, 'time_diff': time_diff}
# for category in columns_used[7:]:  # Start from index 7 for category columns
#     input_data[category] = 1
#
# # Convert input data to DataFrame and ensure all necessary columns are present
# input_df = pd.DataFrame([input_data])
# input_df['amount'] = 0  # Adding a placeholder 'amount' column
#
# # Ensure the necessary datetime features are present
# input_df['hours'] = input_datetime.hour
# input_df['weekday'] = input_datetime.weekday() + 1
# input_df['day_of_year'] = input_datetime.timetuple().tm_yday
# input_df['time_seconds'] = (input_datetime - input_datetime.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
#
# # Reorder columns to match the order used during training
# # Check if all columns are available, add missing ones with default values if necessary
# for col in columns_used:
#     if col not in input_df.columns:
#         input_df[col] = 0  # Assuming default missing values are zeros
#
# input_df = input_df[columns_used]
#
# # Scale the input features
# scaled_input = fitted_scaler.transform(input_df)
#
# # Make predictions
# predictions = trained_model.predict(scaled_input)
#
# # Display predictions
# st.write("Predicted Expenses for", year_month)
# for category, prediction in zip(columns_used[7:], predictions):  # Adjust index as necessary to match categorical data
#     st.write(f'{category}: ${prediction:.2f}')
import streamlit as st
import pandas as pd
import pickle
import json
from datetime import datetime
from sklearn.preprocessing import StandardScaler

# Load the saved columns' names
with open('columns_used.json', 'r') as json_file:
    columns_used = json.load(json_file)

# Streamlit app
st.title('Expense Prediction App')

# User input for year and month
year_month = st.text_input("Enter the year and month (e.g., 2024-05):")
try:
    input_date = datetime.strptime(year_month, '%Y-%m')
except ValueError:
    st.error("Please enter the year and month in the format YYYY-MM.")
    st.stop()

# Process the input year and month
input_year = input_date.year
input_month = input_date.month

# Calculate time difference based on the input year and month
current_date = datetime.now()
input_datetime = datetime(input_year, input_month, 1)
time_diff = (current_date - input_datetime).days

# Load the trained model
with open('final_model.pkl', 'rb') as file:
    trained_model = pickle.load(file)

# Load the fitted scaler
with open('fitted_scaler.pkl', 'rb') as scaler_file:
    fitted_scaler = pickle.load(scaler_file)

# Prepare input data
input_data = {'year': input_year, 'month': input_month, 'time_diff': time_diff}
for category in columns_used[7:]:  # Start from index 7 for category columns
    input_data[category] = 1

# Convert input data to DataFrame and ensure all necessary columns are present
input_df = pd.DataFrame([input_data])
input_df['amount'] = 0  # Adding a placeholder 'amount' column

# Ensure the necessary datetime features are present
input_df['hours'] = input_datetime.hour
input_df['weekday'] = input_datetime.weekday() + 1
input_df['day_of_year'] = input_datetime.timetuple().tm_yday
input_df['time_seconds'] = (input_datetime - input_datetime.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

# Reorder columns to match the order used during training
input_df = input_df[columns_used]

# Scale the input features
scaled_input = fitted_scaler.transform(input_df)

# Make predictions
predictions = trained_model.predict(scaled_input)

# Debug: Print predictions to check the output structure
st.write("Debug - Raw predictions:", predictions)

# Display predictions
st.write("Predicted Expenses for", year_month)
for category, prediction in zip(columns_used[7:], predictions):  # Adjust index as necessary to match categorical data
    st.write(f'{category}: ${prediction:.2f}')
