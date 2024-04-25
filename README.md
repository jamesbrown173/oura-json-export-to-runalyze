# Oura JSON to Runalyze Free

Download your Oura Ring JSON data and quickly upload Sleep and HRV values to Runalyze.

Oura Ring is a popular health tracking ring, however if you're not a paid member you're unable to access the API making intergrating data into other services cumbersome as it requires manual entry. https://cloud.ouraring.com/

Runalyze is a popular training log with functionality to analyze your sleep and HRV data (and it's free!). https://runalyze.com/

This script allows you to drag and drop the JSON data, which can be exported for free from the Oura Ring member page, and it'll automatically process the data and add the Sleep and HRV data to your Runalyze account.

# Prerequisites

- An oura ring
- Runalyze acount and private token.
- Python

# How to use:

1. Download the whole folder and open main.py.
2. You need to add your Runaylze private token to config.json. You can obtain a private token at https://runalyze.com/settings/personal-api.
3. Head over to your Oura Ring account https://cloud.ouraring.com/.
4. In the top right, go to My Account then Export Data.
5. Export download the sleep.json data. For ease of access you can bookmark this link https://cloud.ouraring.com/account/export/sleep/json.
6. Once the file has downloaded run the main.py and drag and drop the json downloaded into the window.
7. Go to your Sleep and HRV windows to check the data has been added.




