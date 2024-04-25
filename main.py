import sys
import json
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent



class DragDropWidget(QWidget):

    # Creates the window
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Oura JSON to Runalyze")
        self.setGeometry(300, 300, 600, 400)  # Increased window size to accommodate response labels

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Drag and drop your JSON file here", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.btn_select_file = QPushButton("Select File")
        self.btn_select_file.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select_file)

        # Labels to display response codes and bodies
        self.sleep_response_label = QLabel("Sleep Response: ", self)
        layout.addWidget(self.sleep_response_label)

        self.hrv_response_label = QLabel("HRV Response: ", self)
        layout.addWidget(self.hrv_response_label)

        self.setAcceptDrops(True)

    # Adds functionality to allow for dropping of the file onto the window
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith('.json'):
                self.open_file(file_path)

    # Alternatively the file can be selected from a dropdown menu
    def select_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("JSON files (*.json)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.open_file(file_paths[0])


    def open_file(self, file_path):
        with open(file_path, "r") as file:
            contents = json.load(file)

            sleep_data = contents['sleep']
            most_recent_entry = sleep_data[-1]

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

            data_hrv = {
                "date_time": most_recent_entry["bedtime_end"],
                "measurement_type": "asleep",
                "hrv": round(most_recent_entry["average_hrv"]),
            }

            # Print the request body here for debugging
            # print("JSON Data HRV:", data_hrv)
            # print("JSON Data sleep:", data_sleep)

            BASE_URL = "https://runalyze.com"
            sleep_url = BASE_URL + "/api/v1/metrics/sleep"
            hrv_url = BASE_URL + "/api/v1/metrics/hrv"

            token = self.get_token()

            headers = {
                "token": token,
                "Content-Type": "application/json",
            }

            response_sleep = requests.post(sleep_url, json=data_sleep, headers=headers)
            self.sleep_response_label.setText(f"Sleep Response: {response_sleep.status_code} - {response_sleep.text}")


            response_hrv = requests.post(hrv_url, json=data_hrv, headers=headers)
            self.hrv_response_label.setText(f"HRV Response: {response_hrv.status_code} - {response_hrv.text}")


    def get_token(self):
        with open("config.json", "r") as config_file:
                config_data = json.load(config_file)
                return config_data["token"]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DragDropWidget()
    widget.show()
    sys.exit(app.exec_())






