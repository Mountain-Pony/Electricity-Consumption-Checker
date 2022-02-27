from flask import Flask
from flask_cors import cross_origin
from dateutil import parser
import pandas as pd
import requests
import json
import os
import datetime

def get_url():
    """Gets the URL that will be used in the electricity consumption data query.

    Returns:
        string: URL for the API data query.
    """    
    api_url = ("https://helsinki-openapi.nuuka.cloud/api/v1.0/EnergyData/Daily/ListByProperty" 
    + "?Record=LocationName&SearchString=1000%20Hakaniemen%20kauppahalli&ReportingGroup="     
    + "Electricity&StartTime=2019-01-01&EndTime=2019-12-31")
    return api_url

def get_location(data):
    """Finds the location from the given JSON data.

    Args:
        data (json): The given JSON data.

    Returns:
        string: The name of the location.
    """
    location = data[0]["locationName"]
    location = location.lower()
    location = location.replace(" ", "-")
    return location

def create_filename(location, timestamp, extension):
    """Creates a filename using the given parameters.       

    Args:
        location (string): The location (the place whose electricity consumption is being checked).
        timestamp (string): Current timestamp (yyyy-mm-dd).
        extension (string): Extension of the file.

    Returns:
        string: Filename based on the given parameters.
    """    
    file_name = location + "-" + timestamp + "." + extension
    return file_name

def format_date(date):
    """Converts given date to string if its' type is something else.
       Separates yyyy-mm-dd from the start of the string.
       The given string must start with the date.
       For example: "2022-01-01 00:00:00" turns to "2022-01-01".

    Args:
        date (any): Given date

    Returns:
        string: yyyy-mm-dd
    """
    is_string = isinstance(date, str)
    if (is_string == False): date = str(date)
    date = date[0:10]
    return date

def arrange_monthly(data):
    """Arranges the given daily electricity consumption data to monthly format.
       Sums the consumption of each month and adds it to a results table.
       The results table comprises month, year, combined consumption for each month, and unit.

    Args:
        data (json): The given JSON data.

    Returns:
        list: Arranged data.
    """
    first_date = parser.parse(data[0]["timestamp"])
    first_month = first_date.month
    unit = data[0]["unit"]
    consumption = 0
    last_index = len(data) - 1
    results = []
    results.append("Month,Year,Consumption,Unit")

    for index, item in enumerate(data):
        date = parser.parse(item["timestamp"])
        month = date.month
        value = item["value"]

        if (first_month == month):
            consumption = consumption + value
        
        if (first_month != month):
            result = (number_to_month(first_month) + "," + str(date.year) 
            + "," + str(round(consumption, 2)) + "," + unit)
            results.append(result)
            consumption = value
            first_month = month

        if (index == last_index):
            result = (number_to_month(month) + "," + str(date.year) + "," 
            + str(round(consumption, 2)) + "," + unit)
            results.append(result)

    return results

def arrange_weekly(data):
    """Arranges the given daily electricity consumption data to weekly format.
       Sums the consumption of each week and adds it to a results table.
       Week starts on monday and ends on sunday.
       The results table comprises the date of the 1st day of week, 
       the number of days in the week, combined consumption for each week, and unit.

    Args:
        data (json): The given JSON data.

    Returns:
       list: Arranged data.
    """
    first_date = parser.parse(data[0]["timestamp"])
    first_day = first_date.weekday() # Monday = 0
    unit = data[0]["unit"]
    last_index = len(data) - 1
    consumption = 0
    count_days = 0
    if (first_day == 0): count_days = 1
    results = []
    results.append("1st day of week,Number of days in week,Consumption,Unit")

    for index, item in enumerate(data):
        date = parser.parse(item["timestamp"])
        day = date.weekday()        
        value = item["value"]

        if (day != 0):
            consumption = consumption + value
            count_days = count_days + 1

        if ((day == 0) and (count_days > 1)):
            result = (format_date(first_date) + "," + str(count_days) 
            + "," + str(round(consumption, 2)) + "," + unit)
            results.append(result)
            consumption = value
            count_days = 1
            first_date = date
        
        if (index == last_index):
            result = (format_date(date) + "," + str(count_days) 
            + "," + str(round(consumption, 2)) + "," + unit)
            results.append(result)

    return results

def number_to_month(number):
    """Converts the given numeric month to written format.

    Args:
        number (integer): The given numeric month.

    Returns:
        string: The name of the month.
    """
    months = ["January", "February", "March", "April", 
               "May", "June", "July", "August", 
               "September", "October", "November", "December"]
    return months[number - 1]
    
electricityApp = Flask(__name__)
# electricityApp.config['CORS_HEADERS'] = 'Content-Type'
@electricityApp.route("/", methods = ["GET"])
@cross_origin(origin="localhost:5000")
def main():
    """This is the main function. Runs when user clicks 'Get data' button on client side.

    Returns:
        json: Requested data.
    """
    api_url = get_url()    
    response = requests.get(api_url)
    json_data = json.loads(response.content)    
    
    location = get_location(json_data)
    timestamp = datetime.datetime.now()
    timestamp = format_date(timestamp)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    file_name = create_filename(location, timestamp, "csv")
    df = pd.DataFrame(json_data)
    df.to_csv(file_name, encoding="utf-8")

    monthly_data = arrange_monthly(json_data)
    monthly_json = json.dumps(monthly_data)
    return monthly_json
    
if __name__ == "__main__":
    electricityApp.run(host="127.0.0.1", port=5000)
