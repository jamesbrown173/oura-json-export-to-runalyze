


import json
import requests
import tkinter as tk
from tkinter import filedialog

########################################################################
# The UI
########################################################################

# Open the file and retrieve the values
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open("./data/my_data.json", "r") as file:
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
                "hrv": round(most_recent_entry["average_hrv"]),
            }

            # Print the JSON data for debugging
            print("JSON Data HRV:", data_hrv)
            print("JSON Data sleep:", data_sleep)

            BASE_URL = "https://runalyze.com"

            # URL for the PUT request
            sleep_url = BASE_URL + "/api/v1/metrics/sleep"
            hrv_url = BASE_URL + "/api/v1/metrics/hrv"

            # Token for authentication
            # Here you'll need to create a config.json file with your private token
            # Load token from config file
            token = get_token()


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


def get_token():
    try:
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
            return config_data["token"]
    except FileNotFoundError:
        token_window = tk.Toplevel(root)
        token_window.title("Enter Token")

        token_label = tk.Label(token_window, text="Enter your private token:")
        token_label.pack()

        token_entry = tk.Entry(token_window)
        token_entry.pack()

        def save_token():
            token = token_entry.get()
            with open("config.json", "w") as config_file:
                json.dump({"token": token}, config_file)
            token_window.destroy()

        submit_button = tk.Button(token_window, text="Submit", command=save_token)
        submit_button.pack()

        token_window.wait_window(token_window)

        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
            return config_data["token"]


root = tk.Tk()
root.title("JSON File Reader")


label = tk.Label(root, text="Click here to select your JSON file")
label.pack()

root.bind("<Button-1>", lambda e: open_file())  # Bind left-click to open file dialog

root.mainloop()






