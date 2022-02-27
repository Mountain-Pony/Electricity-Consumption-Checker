# Electricity-Consumption-Checker
Data provided by [Nuuka Open API](https://helsinki-openapi.nuuka.cloud/swagger/index.html).<br />

Electricity Consumption Checker is a tool for inspecting the electricity consumption
of a given property.<br />
For now, the tool supports only Nuuka Open API and the only available property
is Hakaniemi Market Hall in Helsinki.<br />
Also, the [URL](https://helsinki-openapi.nuuka.cloud/api/v1.0/EnergyData/Daily/ListByProperty?Record=LocationName&SearchString=1000%20Hakaniemen%20kauppahalli&ReportingGroup=Electricity&StartTime=2019-01-01&EndTime=2019-12-31) for the query is hard coded for now.<br />

## Quick guide
Install Python requirements:<br />
```
pip install -r requirements.txt
```
Run electricity.py (it runs on 127.0.0.1:5000).<br />
Open index.html and click the 'Get data' button.<br />

## Description of functionality
Clicking the 'Get data' button sends a request to the server.<br />
After receiving the request, the server performs a data query to the API using 
the hard coded URL. After a successful query, the server processes the received 
JSON data in the following way.<br />
It parses the data and converts it into CSV format. This CSV data will be saved
on the server as a CSV file. The file is named based on the location and the date 
range of the query.<br />
It arranges the parsed JSON data into a monthly format and sends it to the client 
in JSON format. (There is also a function for arranging the data into weekly format, 
but it is not in use at the moment).
Client-side JavaScript will then process the received data and print it to the UI 
in such a way that it is easy to read.<br />
At least when running index.html on localhost, the app ran into CORS issues. 
This was solved with the Flask extension Flask-CORS by allowing CORS on a 
specific route, which is localhost:5000 in the case of this app.<br />

## Files
| File                                  | Description                       |
| ------------------------------------- | --------------------------------- |
| index.html                            | UI                                |
| resources/js/electricityFront.js      | Client side code                  |
| resources/css/style.css               | Style                             |
| \*.json                               | JS config / metadata information  |
| electricity.py                        | Server side code                  |
| tests_electricity.py                  | Tests for electricity.py          |
| requirements.txt                      | Python requirements               |
| tehtavat.pdf                          | Answers for the preassignment     |
| readme.md                             | Readme                            |
