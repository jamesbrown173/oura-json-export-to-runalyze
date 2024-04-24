import json
import pprint
import requests

########################################################################
# Import the data and define the json to be submitted in the put request
########################################################################

with open("./data/replace_this_with_your_data", "r") as file:
    # Retrieve data from the file
    contents = json.load(file)

    #Access the 'Sleep' key and get the most recent entry
    sleep_data = contents['sleep']
    most_recent_entry = sleep_data[-1]

    # Define the values that we want to extract and create a dictionary for the SLEEP data
    data_sleep = {
        "start_time": most_recent_entry["bedtime_start"],
        "duration": round(most_recent_entry["time_in_bed"] / 60),
        "rem_duration": round(most_recent_entry["rem_sleep_duration"] / 60),
        "light_sleep_duration": round(most_recent_entry["light_sleep_duration"] / 60),
        "deep_sleep_duration": round(most_recent_entry["deep_sleep_duration"] / 60),
        "awake_duration": round(most_recent_entry["awake_time"] / 60),
        "hr_average": round(most_recent_entry["average_heart_rate"]),
        "hr_lowest": round(most_recent_entry["lowest_heart_rate"]),
        "quality": round(most_recent_entry["score"] / 10),
    }
    # Define the values that we want to extract and create a dictionary for the HRV data
    # Here the HRV data uses the bedtime_end as its time, however it's a nightly average
    data_hrv = {
        "date_time": most_recent_entry["bedtime_end"],
        "measurement_type": "asleep",
        "hrv": 55,
    }

    # sample_data_sleep = {
    #   "start_time": "2024-04-30T22:52:33.000+07:00",
    #   "duration": 370,
    #   "rem_duration": 46,
    #   "light_sleep_duration": 211,
    #   "deep_sleep_duration": 118,
    #   "awake_duration": 50,
    #   "hr_average": 57,
    #   "hr_lowest": 47,
    #   "quality": 8
    # }


    # Print the JSON data for debugging
    # print("JSON Data HRV:", data_hrv)
    # print("JSON Data sleep:", data_sleep)


########################################################################
# Make the Put request
########################################################################

BASE_URL = "https://runalyze.com"

# URL for the PUT request
sleep_url = BASE_URL + "/api/v1/metrics/sleep"
hrv_url = BASE_URL + "/api/v1/metrics/hrv"


# Token for authentication
# Here you'll need to create a config.json file with your private token
# Load token from config file
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)
    token = config_data["token"]


# Headers containing the token
headers = {
    "token": token,
    "Content-Type": "application/json",
}

# Make the POST request for sleep
response_sleep = requests.post(sleep_url, json=data_sleep, headers=headers)
# Check if the request was successful
print("Sleep Response Status Code:", response_sleep.status_code)
print("Sleep Response Body:", response_sleep.text)

# Make the POST request for HRV
response_hrv = requests.post(hrv_url, json=data_hrv, headers=headers)
# Check if the request was successful
print("HRV Response Status Code:", response_hrv.status_code)
print("HRV Response Body:", response_hrv.text)

