# Trek
# V0LT
# Version 0.1
# Licensed under the GPLv3


# ----- Configuration -----

# Generate an API key in HealthBox with 'app' permissions and access to metric A1 (Steps), then input it here as a string. If this variable is left blank, Trek will ask you to enter your API key every time you run the program.
default_apikey = ""

# Enter the host address and port of your HealthBox instance here. For example, if you host HealthBox locally on the default port, enter `localhost:5050`. If this variable is left blank, Trek will ask you to enter your HealthBox server information every time you run the program.
default_server = "localhost:5050"



# This variable determines whether or not the URL will be printed when making the network request to HealthBox. This is extremely useful for debugging, but can be messy during normal usage.
url_debugging = False

# ----- End of Configuration -----



# Import required modules
import os
import time
import datetime 
from datetime import timezone
import traceback
import urllib.parse
import matplotlib.pyplot as plt # Required to display graphs of steps data
import json # Required to interpret data recieved from HealthBox

# Try to impory PyGTK, but don't terminate if it's not installed.
try:
    import pygtk # Used to improve the UI quality of matplotlib
except ImportError:
    pass

# Attempt to import the 'requests' module
try:
    import requests
except ModuleNotFoundError as error:
    if traceback.format_exception_only (ModuleNotFoundError, error) != ["ModuleNotFoundError: No module named 'requests'\n"]: # Make sure the error we're catching is the right one
        raise # If not, raise the error

 
# Define the function that will be used to clear the screen
def clear():
    if os.name == 'posix': # If the user is running MacOS or GNU/Linux
        _ = os.system('clear')
    else: # If the user is running Windows
        _ = os.system('cls')



# Define the function required to make network requests to HealthBox
class APICallError (Exception): pass # This will be used when returning errors.

def make_request (*, server, api_key, print_url = False):
    endpoint = "metrics/a1/past".split ('/') # Define the method and metric that this request will use on HealthBox.
    url = f"http://{server}/api/app/{'/'.join (endpoint)}?api_key={urllib.parse.quote (api_key)}" # Form the URL that will be used to communicate with HealthBox

    if print_url: print (f"Making a request to {url}") # Only print the URL if URL debugging is requested by the user.

    response = requests.get (url) # Send the network request.
    response_data = response.json () # Save the response of the network request to the response_data variable.
    if not response_data ["success"]: # If something goes wrong, return an error.
        raise APICallError (response_data ["error"])

    del response_data ["success"]
    del response_data ["error"]
    return response_data



# Ask the user for the starting date of the range of time they'd like to graph
print("Please enter the starting date you'd like to count steps from.")

while True: # Run forever until the user enters a valid day.
    day = int(input("Day: "))
    if (day >= 1 and day <= 31):
        break
    else:
        clear()
        print("Please enter a day that falls between 1 and 31.")

while True: # Run forever until the user enters a valid month.
    month = int(input("Month: "))
    if (month >= 1 and month <= 12):
        break
    else:
        clear()
        print("Please enter a month that falls between 1 and 12.")
       
while True: # Run forever until the user enters a valid year
    year = int(input("Year: "))
    if (year >= 1900):
        break
    else:
        clear()
        print("Please enter a year that falls past 1900.")



dt = datetime.date(year, month, day) # Combine the entered day, month, and year into a single variable.
start_timestamp = int(time.mktime(dt.timetuple())) # Convert the date to a Unix timestamp.



# Ask the user for the ending date of the range of time they'd like to graph
print("Please enter the ending date you'd like to count steps to.")

while True: # Run forever until the user enters a valid day.
    day = int(input("Day: "))
    if (day >= 1 and day <= 31):
        break
    else:
        clear()
        print("Please enter a day that falls between 1 and 31.")

while True: # Run forever until the user enters a valid month.
    month = int(input("Month: "))
    if (month >= 1 and month <= 12):
        break
    else:
        clear()
        print("Please enter a month that falls between 1 and 12.")
       
while True: # Run forever until the user enters a valid year
    year = int(input("Year: "))
    if (year >= 1900):
        break
    else:
        clear()
        print("Please enter a year that falls past 1900.")


dt = datetime.date(year, month, day) # Combine the entered day, month, and year into a single variable.
end_timestamp = int(time.mktime(dt.timetuple())) # Convert the date to a Unix timestamp.

if (start_timestamp >= end_timestamp):
    print("Error: The ending date you entered is earlier than the starting date!")
    exit()

day_difference = int((end_timestamp - start_timestamp)/86400) # Calculate how many days span between the starting date and ending date. 86400 is the number of seconds in a day.



# Ask the user for their HealthBox instance information, if they haven't pre-configured it in the configuration at the top of this script.
if (default_apikey == ""): # Check to see if the user has configured a preset API key in the configuration at the top of this script. If not, ask them to enter their API key.
    healthbox_apikey = input("HealthBox API key: ");
else: # If the user as configured an API key in the configuration at the top of this script, use that instead of asking them to enter one.
    healthbox_apikey = default_apikey

if (default_server == ""): # Check to see if the user has configured a preset HealthBox server address in the configuration at the top of this script. If not, ask them to enter the host and port for their HealthBox instance.
    healthbox_server = input("HealthBox instance server and port: ")
else: # If the user has configured a HealthBox server address in the configuration at the top of this script, use that instead of asking them to enter one.
    healthbox_server = default_server

# Form and send the network request that will be used to submit the information to HealthBox using the make_request function.
response = make_request (server = healthbox_server, api_key = healthbox_apikey, print_url = url_debugging)


response = str(response).replace("'", '"')
raw_data = json.loads(response)



# Parse the data recieved from HealthBox into only the "start_time" and "steps_count" values. These are the only variables we will use in our plot.
clean_data = []

for element in raw_data["past"]:
    clean_data.append([element["data"]["start_time"], element["data"]["steps_count"]])


# Break up the data into days, adding up all samples submitted for the same day.
daily_data = []

for value in range(0, day_difference): # Iterate through each day in the span of time between the starting date and ending date.
    total_daily_steps = 0 # Reset the daily steps counter each new day.
    for element in clean_data: # Iterate through the data and count up samples that start on the current day.
       if ((element[0] >= (value*86400)+start_timestamp) and (element[0] <= (value*86400)+start_timestamp+86399)):
            total_daily_steps = total_daily_steps + int(element[1])
    daily_data.append([[value], [total_daily_steps]])


# Break up data into x and y values so it can be graphed.
x_data = [] # Stores the day numbers
for element in daily_data:
    x_data.append(element[0])

y_data = [] # Stores the step counts per day
for element in daily_data:
    y_data.append(element[1])


# Graph data and display it on screen.
plt.xticks(range(1, day_difference)) # Force the x-axis to be displayed as whole numbers
plt.xlabel("Day") # Label the X axis
plt.ylabel("Steps") # Label the Y axis
plt.title("Daily Steps") # Label the graph
plt.plot(x_data, y_data) # Plot the data
plt.show() # Show the graph
