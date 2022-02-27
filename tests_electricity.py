from electricity import arrange_monthly, get_location, create_filename, format_date
import datetime

test_data = ( 
    {"timestamp":"2019-01-14T00:00:00", "locationName":"suomenlinna fortress", "value":1.1, "unit":"kWh"}, 
    {"timestamp":"2019-01-15T00:00:00", "locationName":"suomenlinna fortress", "value":1.21, "unit":"kWh"}, 
    {"timestamp":"2019-01-16T00:00:00", "locationName":"suomenlinna fortress", "value":1.05, "unit":"kWh"}, 
    {"timestamp":"2019-02-01T00:00:00", "locationName":"suomenlinna fortress", "value":2.01, "unit":"kWh"},
    {"timestamp":"2019-03-02T00:00:00", "locationName":"suomenlinna fortress", "value":3.00, "unit":"kWh"},
    {"timestamp":"2019-04-12T00:00:00", "locationName":"suomenlinna fortress", "value":4.67, "unit":"kWh"},
    {"timestamp":"2019-04-30T00:00:00", "locationName":"suomenlinna fortress", "value":4.00, "unit":"kWh"},
    {"timestamp":"2019-05-15T00:00:00", "locationName":"suomenlinna fortress", "value":5.1, "unit":"kWh"},
    {"timestamp":"2019-05-16T00:00:00", "locationName":"suomenlinna fortress", "value":500.02, "unit":"kWh"},
    {"timestamp":"2019-05-20T00:00:00", "locationName":"suomenlinna fortress", "value":5000.05, "unit":"kWh"},
    {"timestamp":"2019-06-15T00:00:00", "locationName":"suomenlinna fortress", "value":6.00, "unit":"kWh"},
    {"timestamp":"2019-06-25T00:00:00", "locationName":"suomenlinna fortress", "value":1.00, "unit":"kWh"},
    {"timestamp":"2019-07-10T00:00:00", "locationName":"suomenlinna fortress", "value":2.00, "unit":"kWh"},
    {"timestamp":"2019-07-12T00:00:00", "locationName":"suomenlinna fortress", "value":2.00, "unit":"kWh"},
    {"timestamp":"2019-08-01T00:00:00", "locationName":"suomenlinna fortress", "value":9.00, "unit":"kWh"} )

test_data_2 = (
    {"timestamp":"2019-07-12T00:00:00", "locationName":"market square", "value":2, "unit":"kWh"},
    {"timestamp":"2019-08-01T00:00:00", "locationName":"market square", "value":9, "unit":"kWh"}
)

def test_arrange_monthly():
    """Tests for arrange_monthly function."""
    test_data_monthly = arrange_monthly(test_data)
    assert test_data_monthly[1] == "January,2019,3.36,kWh"
    assert test_data_monthly[2] == "February,2019,2.01,kWh"
    assert test_data_monthly[3] == "March,2019,3.0,kWh"
    assert test_data_monthly[4] == "April,2019,8.67,kWh"
    assert test_data_monthly[5] == "May,2019,5505.17,kWh"
    assert test_data_monthly[6] == "June,2019,7.0,kWh"
    assert test_data_monthly[7] == "July,2019,4.0,kWh"
    assert test_data_monthly[8] == "August,2019,9.0,kWh"

def test_get_location():
    """Tests for get_location function."""
    location = get_location(test_data)
    assert location == "suomenlinna-fortress"
    location = get_location(test_data_2)
    assert location == "market-square"

def test_create_filename():
    """Tests for create_filename and format_date functions"""
    location = get_location(test_data)
    timestamp = datetime.datetime.now()
    timestamp = format_date(timestamp)
    file_name = create_filename(location, timestamp, "csv")
    assert file_name == ("suomenlinna-fortress" + "-" + timestamp + "-" + ".csv")

    location = get_location(test_data_2)
    timestamp = datetime.datetime(2019, 10, 17)
    timestamp = format_date(timestamp)
    file_name = create_filename(location, timestamp, "txt")
    assert file_name == ("market-square" + "-" + "2019-10-17" + "-" + ".txt")

if __name__ == "__main__":
    test_arrange_monthly()
    test_get_location()
    #test_create_filename()
    print("Everything passed")
    shutdown = input("Press Enter to shut down tests")
