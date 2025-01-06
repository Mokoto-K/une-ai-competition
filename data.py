# TODO - Implement a strategy class/module that selects the assets and timeframe
# automatically for the data module. ie if low risk is selected, choose less volitile
# assets and higher time frames like days and weeks to make decisions on. Better yet
# have the neural net decide if conditions are ripe for high risk or low risk and 
# adjust strategy accordingly, also auto control risk % amount.
# TODO - Switch from a csv to a proper db like sqlite or postgres

import requests as r
import csv
import os 
import datetime as dt
BASE_URL: str = "https://api.bybit.com"
OHLC_URL: str = BASE_URL + "/v5/market/kline"

ASSET_NAME: str = "BTCUSDT"
TIME_FRAME: str = "D"
CONTRACT_TYPE: str = "linear"
MAX_LIMIT: int = 1000

FILE_NAME: str = f"{ASSET_NAME}_{TIME_FRAME}_Data.csv"


def test_connection() -> int:
    """
    A test to check for internet connection prior to sending requests
    """

    try:
        r.get(OHLC_URL)
    except r.RequestException:
        print("Trouble retrieving your request, check if the exchange api is up\
        and running, check your internet connection and double check what you are\
        requesting")
        return 0
    
    return 1


def query_exchange(category: str, symbol: str, interval: str, limit: int) -> list: 
    """
    Requests exchange to retreieve current market records for given parameters 

    Params:
    category - The type of contract to query, (spot, linear, etc)
    symbol - Also known as ticker, the name of the asset you are looking
    interval - The timeframe you want to retrieve records for D(day), M(month)
    60(hourly), etc
    limit - The number of records to get, 1000 being the max

    Returns:
    market_data - A list of market records in reverse order such that the oldest
    records are first and the newest records are last.
    """
    
    parameters: dict = {"category": category, 
          "symbol": symbol,      
          "interval": interval,         
          "limit": limit 
          }

    response = r.get(OHLC_URL, params = parameters)
    market_data: list = [row for row in response.json()["result"]["list"]]

    market_data.reverse()
    return market_data


def create_DB() -> None:
    """
    Creates a database if one does not yet exist
    """

    with open(FILE_NAME, "w") as new_file:

        print("CREATING NEW DATABASE FILE")
        
        # Add the column names to the file 
        new_file.write("date,time,open,high,low,close,volume,utc\n")
    
    market_data: list = query_exchange(CONTRACT_TYPE, ASSET_NAME, TIME_FRAME, MAX_LIMIT)
    write_to_DB(market_data) 


def write_to_DB(market_data: list) -> None:
    """
    Writes passed in data to the database

    Params:
    market_data - A list containing market information to be written to the db
    """

    # Open our DB file and write the contents of the list to the file
    with open(FILE_NAME, "a", newline = "") as file:
        writer = csv.writer(file, delimiter = ",")     

        for line in range(len(market_data)):
            # slice out the UTC timestamp and divide it by 1000 as "fromdatestamp"
            # doesn't use the full utc stamp (they might want to change this)
            timestamp: float = int(market_data[line][0]) / 1000

            # Format the data and time for the line entry
            date: str = dt.datetime.fromtimestamp(timestamp).strftime("%a-%d-%b-%y")
            time: str = dt.datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")

            open_price: float = round(float(market_data[line][1]))
            high_price: float = round(float(market_data[line][2]))
            low_price: float = round(float(market_data[line][3]))
            close_price: float = round(float(market_data[line][4]))

            # For volume we are choosing to multiply by the open price as it's
            # measured via asset contracts sold and not USD, so we convert to USD
            volume: float = round(float(market_data[line][5])) * open_price

            writer.writerow([date, time, open_price, high_price, low_price, close_price, volume, timestamp])


    print(f"{len(market_data)} line(s) written to Database")


def update_DB():
    """
    Compares database timestamps to current market timestamps to determine how
    many records are missing from the database that need to be downloaded to 
    update it to the current market information
    """
    
    print("CHECKING IF DATABASE IS UP TO DATE")
    records_to_retrieve = 1 

    # Query the exchange to get the lastest data & extract just the unix timestamp
    lastest_ts = float(query_exchange(CONTRACT_TYPE, ASSET_NAME, TIME_FRAME, 1)[0][0].split(",")[0]) / 1000
    
    # Get the last three records from the db (3 to be safe)
    recent_utc_timestamps: list = get_records(3)

    if lastest_ts == recent_utc_timestamps[0]:
        # If the utc ts are the same, update only the latest record to current info
        delete_records(1)

    else:
        # Calculate the time difference between each entry 
        time_difference = recent_utc_timestamps[1] - recent_utc_timestamps[2]

        # Subtract current ts from last db entry ts and divide by the difference
        # between entries this will give us the number of entries missing
        records_to_retrieve = int((lastest_ts - recent_utc_timestamps[0]) / time_difference + 1)

        # This is the plus 1 from the above sum we are deleting. This is due to
        # not assuming we recorded the precise close for the current timeframe 
        # in the database and therefore will re-record it now we know its closed
        delete_records(1)

    market_data: list = query_exchange(CONTRACT_TYPE, ASSET_NAME, TIME_FRAME, records_to_retrieve)
    write_to_DB(market_data)


def get_records(records: int) -> list:
    """
    Queries the database for the last entry and retrieves it's date

    Returns:
    date - The date for the last line in the database
    """
    print(f"RETRIEVEING LAST RECORDS FROM CSV")

    date_list = []

    with open(FILE_NAME, "r") as file:
        all_lines = file.readlines()

        for i in range(1, records+1):
            # get all lines in the db, slice the requested lines out, split them
            # by "," take the last value, strip the newline, isolate the unix ts
            date_list.append(float(all_lines[-i:][0].split(",")[7].strip("\n")))

    return date_list


def delete_records(records: int):
    """
    Rewrites the database file with the last x amount of lines excluded

    Params:
    records - The number of lines to exclude
    """

    print(f"DELETING {records} RECORD(S) FROM DATABASE")

    with open(FILE_NAME, "r") as read_file:
        database = read_file.readlines()
        with open(FILE_NAME, "w") as fead_rile: # fead_rile... he chuckles to himself
            fead_rile.writelines(database[: -records])


def main():
    # TODO - Decide if user decides params or hardcoded for time being

    # If there is no trouble connecting to the exchange, run through the logic
    if test_connection:  
        if not os.path.exists(FILE_NAME):
            create_DB()

        update_DB()

if __name__ == "__main__":
    main()
